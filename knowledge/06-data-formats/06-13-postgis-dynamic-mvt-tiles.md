---
id: 06-13
title: PostGIS 動態出向量圖磚（ST_AsMVT）：何時用、zoom 下限、SRID 對齊與欄位白名單
topic: 06-data-formats
kind: decision
scope: public
evidence: Candidate
stacks: [any]
tags: [MVT, ST_AsMVT, ST_AsMVTGeom, ST_TileEnvelope, PostGIS, 動態圖磚, PMTiles, RPC, SRID, 3857, zoom 下限, 出磚服務, 向量圖磚]
---

## 原則
資料會變或要依條件查才用動態 MVT，靜態只顯示用 PMTiles；寫出磚函式時，`&&` 篩選兩邊要同一座標系，`ST_AsMVTGeom` 的幾何與 bounds 要都在 3857，函式內設 zoom 下限並只 select 需要的欄位，寫完用已知有資料的磚實測。

## 症狀
- 資料每天更新、又要依時間或屬性篩選，每次更新都得重切 PMTiles、重新部署。
- 自己寫了出磚函式，低 zoom 一張磚要掃整張表，資料庫被拖慢；公開端點被拿來打 z0 磚。
- 出磚函式在本機測試沒問題，一接上真資料就報 SRID 不一致，或回傳空磚。

## 原因
- 預烤的 PMTiles 適合「靜態、量大、只顯示」；資料會變、要依條件查、欄位常增時，每次更新都要重切，不划算。
- 動態出磚在請求時才查詢與編碼。低 zoom 的一張磚涵蓋很大範圍，若沒有下限或預先聚合，就等於對全表做 `ST_AsMVT`。
- `ST_TileEnvelope(z, x, y)` 預設回傳 EPSG:3857（Web Mercator，約 ±20037508 公尺）的範圍。資料若存 EPSG:4326，`geom && bbox` 是拿兩個不同座標系的框比較：PostGIS 對混合 SRID 的運算通常直接報 `Operation on mixed SRID geometries`；沒報錯也毫無意義。
- `ST_AsMVTGeom` 不會替你轉座標：官方文件寫明輸入幾何「必須已在目標地圖的座標系（需要時用 `ST_Transform`）」。把 4326 幾何直接交給它，經緯度會被當成公尺，所有圖形擠在原點附近，結果就是空磚。

## 解法
1. **路線選擇**：
   | 資料特性 | 路線 |
   |---|---|
   | 會變（即時、週期更新）、要依時間或屬性篩選、欄位常增 | PostGIS 動態 MVT |
   | 靜態或半靜態、量大、只顯示不查詢 | PMTiles 預烤（[06-02](06-02-geojson-to-pmtiles-tippecanoe.md)） |
   兩條可並存，依資料特性各自選。
2. **函式骨架**：`bbox := ST_TileEnvelope(z, x, y)` → 篩選（要能用 GiST 索引）→ `ST_AsMVTGeom(<3857 幾何>, bbox, 4096, 256, true)` → `ST_AsMVT(tile, '<layer>', 4096, 'mvtgeom')`。layer 名稱就是前端的 `source-layer`。
3. **SRID 對齊**：`&&` 兩邊、`ST_AsMVTGeom` 的幾何與 bounds，都要在同一座標系。兩種正確寫法：
   - **資料存 4326**（PostGIS 官方範例的寫法）：篩選時把磚框轉回 4326，索引仍用得到；編碼時才把幾何轉 3857。
     ```sql
     SELECT ST_AsMVT(t, 'layer', 4096, 'mvtgeom') FROM (
       SELECT id, name,
              ST_AsMVTGeom(ST_Transform(geom, 3857), ST_TileEnvelope(z, x, y), 4096, 256, true) AS mvtgeom
       FROM my_table
       WHERE geom && ST_Transform(ST_TileEnvelope(z, x, y, margin => 256.0 / 4096), 4326)
     ) t;
     ```
   - **另存一欄 3857 幾何**（例如 generated column `geom_3857`）並對它建 GiST 索引：`WHERE geom_3857 && ST_TileEnvelope(z, x, y)`，`ST_AsMVTGeom(geom_3857, …)`，省掉每次請求的 `ST_Transform`，適合讀多寫少的大表。
   - 不要寫成 `ST_Transform(geom, 3857) && bbox`：對欄位做轉換，一般的 `geom` GiST 索引就用不到了。
   - 寫完用一張已知有資料的磚實測（回傳 bytea 長度大於 0），不要只看函式能建立。
4. **zoom 下限與上限**：低於某個 zoom 直接回空磚（或改走預先聚合的表）；在函式內處理，不靠前端自律。公開 RPC 也要做時間範圍與筆數上限（[07-08](../07-performance/07-08-public-rpc-timeout-clamp-rowcap.md)）。
5. **欄位白名單與版本**：只 select 前端需要的欄位，不用 `SELECT *`，避免把內部欄位或個資編進磚；要支援資料版本或時間篩選時，把版本當參數傳入，並納入 HTTP 快取 key。
6. **前端接法**：MapLibre／Mapbox 的 vector source 需要 `tiles: [url]` 樣板；資料庫 RPC 通常不是 `/{z}/{x}/{y}` 網址，需一層出磚服務或代理轉成函式呼叫，或用 Martin、pg_tileserv。

## 怎麼偵測
- 通用：靜態大圖層卻用動態出磚；每天變的資料卻每天重切 PMTiles 並重部署；低 zoom 磚很慢。
- 搜尋：`ST_TileEnvelope\(` 所在函式裡沒有任何 `ST_Transform`，而被查的資料表幾何宣告為 `GEOMETRY(..., 4326)`（PostGIS）。
- 實測：對已知有資料的 z/x/y 呼叫出磚函式，報 mixed SRID 錯誤或回傳長度 0，就是 SRID 沒對齊（PostGIS）。
- 搜尋：出磚函式開頭沒有 `z < \d+` 這類下限判斷（PostGIS）。
- 搜尋：出磚子查詢用 `SELECT \*`（PostGIS）。

## 出處
- PostGIS 文件：`ST_TileEnvelope`（預設 bounds 為 SRID 3857）、`ST_AsMVTGeom`（幾何須先在目標座標系；官方範例 `ST_Transform(geom, 3857)` 編碼、`ST_Transform(ST_TileEnvelope(...), 4326)` 篩選）、`ST_AsMVT`。
- Martin、pg_tileserv 文件（現成的 PostGIS 出磚服務）。
- 相關卡：[06-01](06-01-format-selection-decision.md)（格式選型）、[06-02](06-02-geojson-to-pmtiles-tippecanoe.md)（PMTiles）、[07-07](../07-performance/07-07-backend-preaggregate-and-data-path-triage.md)（後端預先聚合）、[07-08](../07-performance/07-08-public-rpc-timeout-clamp-rowcap.md)（公開 RPC 上限）、[07-14](../07-performance/07-14-open-data-pii-column-exclusion.md)（排除個資欄位）。

