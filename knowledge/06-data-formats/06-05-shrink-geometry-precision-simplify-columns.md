---
id: 06-05
title: 檔案變小的順序：先刪欄位與多餘精度，再簡化，最後才換格式——簡化要留意拓撲與折返
topic: 06-data-formats
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [座標精度, 簡化, simplify, Douglas-Peucker, 拓撲, 欄位瘦身, gzip, topojson, 檔案大小, geography, 測地距離, ST_Segmentize]
---

## 原則
縮小檔案依序做：刪可推導欄位 → 截座標精度 → 傳輸壓縮 → 保拓撲簡化 → 才換格式，每步量一次大小；簡化後要量距離，必須先 `ST_Segmentize` 並用同一種距離驗收。

## 症狀
- 靜態 JSON／GeoJSON 太大，首屏下載慢。
- 簡化後邊界鋸齒、相鄰面之間出現縫隙或重疊。
- 簡化後的路線在折返處走位，逐車比對出現系統性偏移。
- 簡化後的界線拿去算 geography 距離，比全解析度差了數百公尺。

## 原因
- 檔案大小多半來自「可推導的欄位」與「過多的座標小數位」，不是頂點數本身。
- 逐一簡化每個面不保拓撲，相鄰面的共用邊會各自移動。
- Douglas-Peucker 這類演算法對折返幾何有系統性偏移，調 tolerance 不是萬靈丹。

## 解法
由便宜到昂貴依序做，每步量一次大小：
1. **刪可推導的欄位**（例如累計里程，前端可由座標算出）。
2. **座標精度**：依需求截位；一般地圖 5–6 位小數（約 1 m 與 0.1 m 量級）足夠，7 位以上多為雜訊。
3. **gzip／brotli 傳輸壓縮**（PMTiles 除外，見 [06-03](06-03-gzip-breaks-range-requests.md)）。
4. **統計類**：只傳數值表，共用一份邊界。
5. **簡化**：用保拓撲的工具（共享邊一起簡化，如 TopoJSON 流程或 mapshaper），簡化後疊圖檢查縫隙。
6. **折返幾何**要用「雙幾何跑同一顆引擎逐項比對」驗證，不要只看視覺。
7. 仍不夠才換格式（見 [06-01](06-01-format-selection-decision.md)、[06-02](06-02-geojson-to-pmtiles-tippecanoe.md)）。經驗門檻：面與線圖層的單檔控制在約 1–2 MB 內再放上網頁，超過就先簡化、再轉 PMTiles；小型網站的起點數字，大型站依載入時間調整。
8. 簡化是有損操作：保留原檔，並在文件記下 tolerance 與日期。
9. **簡化後若要量距離，量測座標系要和演算法一致**：Douglas-Peucker 在經緯度平面上保證偏離 ≤ tolerance，但簡化會把許多短段合成長弦；用 `::geography`（測地線）量距離時，長弦的平面直線和大圓線會分家，誤差可達數百公尺，調緊 tolerance 也救不了。做法是簡化後再切短：`ST_Segmentize(ST_SimplifyPreserveTopology(geom, tol), max_len)`，讓每段短到兩種直線幾乎重合；驗收用同一種距離（geography）量最差頂點，不要用平面度數乘 111 km 換算。`ST_HausdorffDistance`（離散版只比頂點）會低估簡化誤差，不適合當驗收。

## 怎麼偵測
- 通用：簡化後的界線量到的距離與全解析度差數百公尺，且換更小的 tolerance 誤差不變。
- 搜尋：`ST_Simplify` 與 `::geography`／`ST_Distance\(.*geography` 出現在同一條 SQL 或同一資料流程，且沒有 `ST_Segmentize`（PostGIS）。
- 通用：JSON 內有可由其他欄位算出的累計值；座標有 10 位以上小數；同一份邊界重複出現在多個檔。
- 搜尋：`\d+\.\d{8,}`（座標小數位過長，適用任何 GeoJSON）；欄位名 `cumDist|cum_|accum`（適用 any）。

## 出處
- 官方：TopoJSON、mapshaper 文件（保拓撲簡化）。
- 相關卡：[06-01](06-01-format-selection-decision.md)、[06-02](06-02-geojson-to-pmtiles-tippecanoe.md)、[06-03](06-03-gzip-breaks-range-requests.md)。
- 實例：[mini-taiwan-pulse 效能盤點（公車路線 JSON 刪累計里程，gzip 後 53→31 MB）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/audit/perf-audit-2026-09-30.md)；[簡化後平面距離與 geography 距離不一致的事故（平面偏離 1.9 m、geography 405.4 m；segmentize 後 19.9 m）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/pitfalls/2026-08-20-simplify-planar-vs-geography-distance.md)。

