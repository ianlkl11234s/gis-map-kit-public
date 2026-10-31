---
id: 15-04
title: 入門工具鏈：QGIS 看、ogr2ogr 轉、mapshaper 簡化、tippecanoe 切圖磚、turf 在前端算
topic: 15-getting-started
kind: catalog
scope: public
evidence: General
stacks: [any]
tags: [工具鏈, QGIS, ogr2ogr, GDAL, mapshaper, tippecanoe, PMTiles, MVT, turf, geopandas, geojson.io, 入門]
---

## 原則
重的事（轉座標、轉格式、簡化、切圖磚）在進網頁之前用命令列或腳本做，且每一步可重跑；前端只負責畫與互動。

## 症狀
- 拿到一份 SHP／KML／CSV，不知道先用什麼工具打開、怎麼變成網頁能用的格式。
- 在瀏覽器裡寫了幾百行程式做「轉座標、合併、簡化」，其實一行指令就能做完。

## 原因
地圖資料的處理多半在「進網頁之前」完成。每個工具各有專長，選錯工具不是做不到，而是事倍功半。

## 解法
一條常見的路：**看（QGIS）→ 轉格式與座標（ogr2ogr）→ 縮小（mapshaper）→ 大檔切圖磚（tippecanoe）→ 前端畫與互動（MapLibre＋turf）**。

| 工具 | 一句話何時用 | 例子 | 延伸 |
|---|---|---|---|
| QGIS | 拿到任何新資料先打開看：座標系、欄位、幾何對不對 | 拖 SHP 進去看屬性表與 CRS | [15-01](15-01-crs-basics-identify-and-convert.md) |
| geojson.io | 小檔快速檢視、手畫幾個點或面 | 貼上 GeoJSON 看位置 | [15-02](15-02-geojson-structure-and-bad-files.md) |
| ogr2ogr（GDAL） | 轉格式、轉座標、挑欄位、用 SQL 篩選 | `ogr2ogr -t_srs EPSG:4326 out.geojson in.shp` | [15-01](15-01-crs-basics-identify-and-convert.md) |
| geopandas | 要寫成可重跑的 Python 腳本、做 join 與彙總 | `gpd.read_file(...).to_crs(4326)` | [06-05](../06-data-formats/06-05-shrink-geometry-precision-simplify-columns.md) |
| mapshaper | 面與線太大要簡化，保留相鄰邊界不裂開 | `mapshaper in.geojson -simplify 10% -o out.geojson` | [06-05](../06-data-formats/06-05-shrink-geometry-precision-simplify-columns.md) |
| tippecanoe | 檔案超過數 MB 或點數上萬，切成向量圖磚（MVT／PMTiles） | `tippecanoe -o out.pmtiles -zg in.geojson` | [06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md) |
| pmtiles CLI | 檢查 PMTiles 的內容與 metadata，或抽出一塊圖磚 | `pmtiles show out.pmtiles` | [10-03](../10-ops/10-03-pmtiles-range-cdn-cors.md) |
| turf | 在前端算距離、面積、緩衝區、點在面內 | `turf.booleanPointInPolygon(pt, poly)` | [11-08](../11-extras/11-08-measure-draw-and-compare-maps.md) |
| PostGIS | 資料大到要放資料庫、要做空間 join 或給 API 查詢 | `ST_DWithin`、`ST_Contains` | [07-07](../07-performance/07-07-backend-preaggregate-and-data-path-triage.md) |

原則：
1. **重的事在預處理做**，前端只負責畫與互動；turf 適合少量即時計算，不適合在瀏覽器處理數十萬筆。
2. **每一步都可重跑**：指令或腳本存進 repo，不要只在 QGIS 裡手動點完就丟。
3. 格式怎麼選見 [06-01](../06-data-formats/06-01-format-selection-decision.md)；檔案縮小的順序見 [06-05](../06-data-formats/06-05-shrink-geometry-precision-simplify-columns.md)。

## 怎麼偵測
- 通用：前端程式裡有大量座標轉換、簡化或合併邏輯；資料夾裡只有處理後的檔案，沒有產生它的指令。
- 搜尋：前端 `import proj4|@turf/turf` 用於整份資料逐點處理（例如在 `features.map` 裡呼叫 `proj4(` 或 `turf.simplify(`）（適用 stack：any）。

## 出處
- 官方文件：QGIS、GDAL ogr2ogr、mapshaper、tippecanoe（felt/tippecanoe）、PMTiles、turf.js、PostGIS；參數細節以官方文件為準。
- 相關卡：[15-01](15-01-crs-basics-identify-and-convert.md)、[15-02](15-02-geojson-structure-and-bad-files.md)、[06-01](../06-data-formats/06-01-format-selection-decision.md)、[06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)、[06-05](../06-data-formats/06-05-shrink-geometry-precision-simplify-columns.md)。

