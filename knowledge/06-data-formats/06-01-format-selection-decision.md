---
id: 06-01
title: 資料格式怎麼選：先問「會不會變、量大不大、要不要查詢」，再對照格式
topic: 06-data-formats
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [GeoJSON, TopoJSON, MVT, PMTiles, FlatGeobuf, GeoParquet, COG, Arrow, 選型, 格式]
---

## 原則
選格式前先回答三問：資料會不會變、量大不大（用 DevTools 實測；檔案大小門檻只當起點，見 [06-05](06-05-shrink-geometry-precision-simplify-columns.md)）、要不要依條件查詢；再對照下表，不要因為格式新就選它。

## 症狀
- 首屏卡在下載一個幾十 MB 的 GeoJSON。
- 為了一份月更的靜態資料架了一整套資料庫與圖磚服務。
- 選了很新的格式，結果前端函式庫根本不能直接讀。

## 原因
格式是「傳輸與讀取方式」，不是越新越好。選錯的代價出現在三處：首屏下載量、更新方式（換檔或換服務）、能不能在前端直接用。

## 解法
決策主幹只有三問，依序回答：
1. **會不會變？** 不會或很少 → 靜態檔；會 → 要有更新機制（換檔名、指標檔，或後端服務）。
2. **量大不大？** 以 DevTools 量到的首屏下載量與拖曳 FPS 判斷；檔案大小的起點門檻在 [06-05](06-05-shrink-geometry-precision-simplify-columns.md)，點數門檻在 [14-02](../14-scale-density/14-02-point-count-thresholds.md)，都以實測為準。小量 GeoJSON 通常最省事。
3. **要不要依條件查詢？** 只顯示 → 預烘焙；要依時間或屬性篩選 → 後端動態出圖磚或 RPC。

| 格式 | 適合 | 前端能否直接用 | 注意 |
|---|---|---|---|
| GeoJSON | 小到中量、學習與原型 | 是（所有 stack） | 整檔下載、前端切磚；頂點多時 pan 卡 |
| TopoJSON | 共享邊界的行政區面 | 需自行轉回 GeoJSON | 省空間但多一道轉換；與 PMTiles 相比通常不值得 |
| MVT（動態） | 會變、要依屬性或時間篩選的大面資料 | 是（向量圖磚 source） | 需要資料庫與出磚服務 |
| PMTiles | 靜態或半靜態、量大、只需顯示 | 需 pmtiles protocol 外掛 | 要 HTTP Range 與 CORS；見 [06-02](06-02-geojson-to-pmtiles-tippecanoe.md)、[06-03](06-03-gzip-breaks-range-requests.md) |
| FlatGeobuf | 需要空間索引、按 bbox 串流讀取的向量 | 需專用 reader | 一般建議，未實測 |
| GeoParquet | 分析倉庫、批次處理、欄位多 | 瀏覽器端少用；多在後端或 DuckDB | 屬分析端格式，不是顯示格式 |
| COG／GeoTIFF | 連續場、衛星影像、地形 | 需 reader 或轉成影像磚 | 一般建議；實例改走 PNG 圖磚或批次 RPC |
| Arrow／二進位欄式 | 大量時序或軌跡、要零拷貝 | 需自寫解碼 | 解析成本趨近記憶體複製；實作成本高 |
| 連續場烘成 PNG | 風、流、溫度等格點場 | 是（影像讀回） | 見 [06-09](06-09-bake-vector-field-to-png.md) |

補充原則：
- 統計值（縣市、村里）只傳數值表，共用一份邊界；不要每個指標各帶一份幾何。
- 資料「只給現在」又要比較時，自己存快照（見 [01-10](../01-taiwan-apis/01-10-realtime-api-has-no-history.md)），格式是次要問題。
- 先量再轉格式：很多「疑似很慢」的來源實測並不慢（見 [07-01](../07-performance/07-01-performance-budget-and-measurement.md)）。

## 怎麼偵測
- 通用：首屏 Network 面板有單一超過數十 MB 的 .geojson／.json；拖曳地圖時 Main thread 長任務；同一份行政區邊界被多個檔案重複帶。
- 搜尋：`addSource\(.*type:\s*['"]geojson['"]` 後面接大檔 URL；`\.geojson['"]` 的檔案大小（`find . -size +2M -name "*.geojson"`）（適用 stack：mapbox-gl、maplibre、leaflet、openlayers）。

## 出處
- 官方：PMTiles 規格與 protocol 外掛文件。FlatGeobuf、GeoParquet、COG、Arrow 為一般建議（General），非自己的實作經驗。
- 實例：[資料來源契約（動態走 RPC、統計走快照、靜態走 CDN 資產）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/development-rules.md)。

