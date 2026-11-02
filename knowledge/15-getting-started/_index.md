# 15-getting-started 入門：座標系統、GeoJSON、本機 server、工具鏈

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [15-00](15-00-getting-started-index.md) | 入門總表：拿到資料到第一張網頁地圖，遇到什麼先看哪張 | 入門依資料流程走：先認座標系，再確認 GeoJSON 結構，接著用本機 server 開頁面，需要轉檔時挑工具，最後套最… | catalog | General | any | 入門, 總表, 座標系統, GeoJSON, 本機 server, 工具鏈, 最小骨架 |
| [15-01](15-01-crs-basics-identify-and-convert.md) | 座標系統入門：先認出資料是 WGS84 還是 TWD97，網頁地圖一律用經緯度，轉換在預處理做 | 第一次拿到政府資料，不知道 X、Y 欄位是經緯度還是公尺，放上地圖什麼都看不到。 | pattern | General | any | 座標系統, 投影, CRS, WGS84, EPSG:4326, TWD97, EPSG:3826, Web Mercator, EPSG:3857, ogr2ogr, proj4, 面積失真, 入門 |
| [15-02](15-02-geojson-structure-and-bad-files.md) | GeoJSON 結構：FeatureCollection、geometry、properties，座標順序一律 [經度, 緯度] | 自己手寫或從 CSV 轉出來的 GeoJSON，丟進地圖後點跑到南極或印度洋。 | pattern | General | any | GeoJSON, FeatureCollection, Feature, geometry, properties, lng lat, 座標順序, RFC 7946, 壞檔, 驗證, 入門 |
| [15-03](15-03-local-server-file-protocol-cors.md) | 雙擊打開 HTML 地圖卻讀不到資料：file:// 不能 fetch，要開本機 HTTP server | 雙擊打開 index.html，底圖出得來，自己的 GeoJSON 卻沒畫。 | pitfall | General | any | file://, 本機 server, python3 -m http.server, npx serve, CORS, 同源政策, fetch, Range, PMTiles, 入門 |
| [15-04](15-04-toolchain-when-to-use.md) | 入門工具鏈：QGIS 看、ogr2ogr 轉、mapshaper 簡化、tippecanoe 切圖磚、turf 在前端算 | 拿到一份 SHP／KML／CSV，不知道先用什麼工具打開、怎麼變成網頁能用的格式。 | catalog | General | any | 工具鏈, QGIS, ogr2ogr, GDAL, mapshaper, tippecanoe, PMTiles, MVT, turf, geopandas, geojson.io, 入門 |
| [15-05](15-05-first-web-map-skeleton.md) | 第一張網頁地圖的最小骨架：MapLibre＋免 key 底圖（OpenFreeMap）＋一個 GeoJSON 圖層、圖例、popup | 第一次做網頁地圖，不知道最少要寫哪些東西，網路上的範例不是要 token 就是一大包框架。 | pattern | General | maplibre | MapLibre, OpenFreeMap, 最小範例, 骨架, GeoJSON, addSource, addLayer, popup, 圖例, 免 key, 入門, 範本 |
