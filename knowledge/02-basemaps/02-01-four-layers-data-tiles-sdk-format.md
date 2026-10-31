---
id: 02-01
title: 「地圖」是四層：地理資料、底圖服務、渲染 SDK、格式與儲存，不要混成一張廠商比較表
topic: 02-basemaps
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [底圖, OSM, Mapbox, MapLibre, Leaflet, deck.gl, PMTiles, Style JSON, 向量圖磚, 分層]
---

## 原則
選型時把「地理資料、底圖服務、渲染 SDK、格式與儲存」當成四個獨立的層分別決定，不要放在同一張廠商比較表裡；先定 SDK 與計費／授權限制，再選底圖與格式。

## 症狀
選型討論變成「Mapbox 還是 OSM 還是 Leaflet」，雞同鴨講；換了圖磚來源卻發現帳單沒變；換 SDK 後 style 或圖層沒法用。

## 原因
這些名詞屬於不同層，回答的問題不同：

| 層 | 例子 | 回答的問題 |
|---|---|---|
| 1 地理資料 | OpenStreetMap、政府開放資料 | 內容從哪來？授權？ |
| 2 底圖圖磚／樣式服務 | Mapbox Styles、CARTO、MapTiler、Protomaps 自託管、OSM 公用圖磚 | 誰把資料切成圖磚、樣式誰定、誰計費？ |
| 3 前端渲染 SDK | Mapbox GL JS、MapLibre GL JS、Leaflet、deck.gl、Three.js | 瀏覽器怎麼畫？能不能客製？ |
| 4 樣式、格式與儲存 | Style JSON、MVT、raster tiles、GeoJSON、PMTiles、COG、物件儲存 | 資料長什麼樣、放哪？ |

SDK 不同，能吃的 style／圖磚／計費方式也不同（例如某些 SDK 以「地圖物件初始化一次」計費，與圖磚來源無關，見 [02-04](02-04-mapbox-billing-token-license.md)）。

## 解法
1. 選型時先決定第 3 層（SDK）與計費／授權限制，再選第 2 層底圖，最後決定第 4 層資料格式。
2. 各 SDK 的特性：
   - Mapbox GL JS v3：高度客製、3D、自訂圖層；需 token；v2 起授權為 Mapbox TOS，非開源。
   - MapLibre GL JS：開源（BSD-3），分支自 2020-12 授權變更前的 Mapbox GL JS；同一套 Style Spec；不需 token；PMTiles 以官方 `addProtocol` 支援。
   - Leaflet：最輕量，以 raster 圖磚＋向量疊圖為主，適合少量點。
   - deck.gl：大量點、軌跡，通常搭配 MapLibre 或 Mapbox。
   - Three.js：自訂 3D，需自行處理投影、時間與 picking。
3. 資料格式選擇：小檔 GeoJSON；大量靜態用 PMTiles；會變且要查詢用動態向量圖磚；詳見資料格式主題的卡片。
4. 授權與單價以官方頁面為準；deck.gl、Three.js 的授權條款本卡未驗證，採用前自行確認。

## 怎麼偵測
- 通用：文件或提案把 SDK、底圖、資料授權放在同一欄位比較。
- 搜尋：`mapbox://styles|basemaps\.cartocdn|tile\.openstreetmap|protomaps`（適用 stack：mapbox-gl, maplibre, leaflet）。

## 出處
- 官方：github.com/mapbox/mapbox-gl-js（LICENSE）、github.com/maplibre/maplibre-gl-js、leafletjs.com、docs.protomaps.com/pmtiles。

