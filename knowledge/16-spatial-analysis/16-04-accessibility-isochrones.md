---
id: 16-04
title: 可達性與等時圈：路網距離不是直線距離；等時圈用 concave＋全域 dissolve＋環差分級，缺口狀態不能填 0
topic: 16-spatial-analysis
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [可達性, 等時圈, isochrone, 服務範圍, 路網距離, 直線距離, OSRM, Valhalla, osmnx, PBF, concave hull, dissolve, 環差, 服務沙漠, coverage]
---

## 原則
可達性用路網距離，不用直線 buffer；等時圈對全部站一次 dissolve、用環差分級；缺口狀態（未連通、缺座標、未計算）分開表示，不填 0；外部路徑服務要先取得同意。

## 症狀
- 用 5 公里 buffer 回答「到最近醫院多遠」，但河對岸沒有橋，實際要繞 20 分鐘。
- 等時圈是鋸齒三角形，或碎成上萬片小多邊形，檔案十幾 MB。
- 分區跑完再合併，區界上顏色接不起來、同一片地方疊了好幾層。
- 沒算到的地方被畫成「服務沙漠」。

## 原因
- 山、河、高速公路、單行道讓實際行程遠大於直線（概念見 [00-05](../00-system-thinking/00-05-eight-relationship-types-and-spatial-vs-system-proximity.md)）。
- 等時圈是模型輸出，形狀隨交通方式、門檻、路網版本與演算法改變；沒算到不等於沒有服務。
- 分區各自 dissolve，同一片地區在不同分區算出不同的重疊數，合併後色塊接不上。

## 解法
1. **先選問題類型**：
   - 沿路最近的服務多遠 → 路網染色（多起點最短路徑，每段標距離與分級）。
   - 每個站的服務範圍 → 等時圈多邊形。
   - 沙漠在哪、跨服務比較 → 網格或 H3，每格算到最近服務的距離。
2. **路網來源**：小量查詢用 OSRM、Valhalla 等路徑服務（公開示範伺服器有使用限制，外部服務要先取得同意）；大量計算用本機 OSM PBF，先用 `osmium tags-filter` 只留需要的道路等級並估算記憶體，不對公開 Overpass 鏡像打全國範圍查詢。
3. **等時圈多邊形畫法**（建議預設）：可達節點 → concave hull（比例 0.5；convex 會鋸齒、0.3 太碎）→ buffer 約 15% 平滑 → simplify 約 10% → 所有站的多邊形切碎 → **依重疊站數 dissolve**，每個重疊數一個 feature。
4. **分區跑時只輸出各站原始多邊形**，頂層依站去重後**對全部站一次**算重疊數與 dissolve，不要每區各自 dissolve 再拼。
5. **分級用環差**：5、10、15 分的圈互相扣掉成不重疊的環，一個 fill 圖層就能上色，不用半透明圈層層疊加（[14-04](../14-scale-density/14-04-overlap-order-and-opacity.md)）。
6. **門檻時間查官方標準**（例如消防到場時間），不要隨意定。
7. **狀態分開表示**，不要填成 0 或最遠一級：有路徑＝距離或時間＋單位＋分級；超過門檻＝「超過 X 分」；找不到路網節點＝「未連通」；目標缺座標＝「缺座標」（不用中心點代替）；路網或來源失敗＝「無資料」＋原因；沒算的格子＝「未計算」，不是沙漠。
8. **多重身分的設施要進每個類別**：`CASE WHEN` 只進第一個符合的類別；「其他」類用正向白名單，不用 `NOT IN`。
9. **大面積覆蓋面直接做 PMTiles**（[06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)）。
10. 回答與圖例寫明交通方式、時間或距離門檻、資料日期，以及「這是路網估算，不含壅塞」。

## 怎麼偵測
- 通用：可達性圖是同心圓；等時圈邊界是直線多邊形；區界色塊斷掉；沒資料的區域和「很遠」同色。
- 搜尋：「可達|服務範圍|幾分鐘」的計算只用 `ST_Buffer|ST_DWithin|turf\.buffer|turf\.circle`；`convex_hull|ConvexHull` 用於等時圈；分區迴圈裡就呼叫 `unary_union|dissolve`（適用 stack：any）。
- 資料：等時圈 feature 數上萬，或同一重疊數有多個 feature。

## 出處
- OSRM、Valhalla、osmnx、osmium 官方文件；OSM 授權（ODbL）。
- 相關卡：[00-05](../00-system-thinking/00-05-eight-relationship-types-and-spatial-vs-system-proximity.md)、[06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)、[14-04](../14-scale-density/14-04-overlap-order-and-opacity.md)。
- 實例：[mini-taiwan-pulse 可達性分析 skill](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/skills/accessibility-analysis/SKILL.md)。

