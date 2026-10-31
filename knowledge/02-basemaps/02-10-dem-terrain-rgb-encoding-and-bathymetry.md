---
id: 02-10
title: DEM 轉 terrain-RGB 圖磚：解碼哨兵值、缺磚處理、陸海合成與垂直誇張
topic: 02-basemaps
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [DEM, terrain-RGB, terrarium, raster-dem, 高程編碼, 海底地形, GEBCO, bathymetry, exaggeration, 垂直誇張, 烘焙, nodata, 缺磚]
---

## 原則
自烘 terrain-RGB 時，編碼公式、nodata 哨兵、缺磚策略與誇張倍率都要在一處定義、前後端共用；nodata 用精確哨兵判斷，不用深度門檻。

## 症狀
- 自烘高程圖磚後，海岸或離島出現黑坑、黑三角，或水下全被壓成同一個淺色。
- 加進海底地形後，淺海被當成 nodata 挖掉，或整個場景下沉。
- 3D 地形的山看起來是平的；調大誇張倍率後，貼地的點、線、模型浮空或鑽進山裡。
- 圖磚量暴增，多是沒有新資訊的海面升採樣磚。

## 原因
- terrain-RGB 是把高程塞進 PNG 的 RGB 三個通道。常見兩種編碼：Mapbox（`h = -10000 + (R*65536 + G*256 + B) * 0.1`）與 Terrarium（`h = R*256 + G + B/256 - 32768`）。編碼跟 source 宣告的 `encoding` 不一致，整片高程就錯。
- 編碼器常把 nodata 寫成 RGB(0,0,0)（Terrarium 解成 −32768 m）。用「低於某深度就當 nodata」的門檻擋，加入真實水深後會誤殺合法負值。
- 陸地 DEM（例如 20 m）與海底資料（例如 GEBCO、約 450 m）解析度差一個數量級；高 zoom 烘海面磚只是升採樣。
- 色階或著色若假設高程 ≥ 0，負值會被夾到最淺色，或在 `pow(負數, k)` 變 NaN 而成黑碎片。
- 以載入中心附近平均高程當基準面的引擎，中心落在海上時，負水深會拉低基準，整個場景下沉。
- 垂直誇張若烘進幾何，改倍率要重建網格，貼地物件也要用同一倍率重算高度。

## 解法
1. **編碼與宣告一致**：烘焙腳本、文件、前端解碼（或 `raster-dem` 的 `encoding`）用同一個公式；文件記下 zoom 範圍與缺磚的值。
2. **nodata 用精確哨兵判斷，不用深度門檻**：明確檢查 RGB(0,0,0)（或選定的哨兵值），只擋編碼洞。
3. **缺磚策略要寫明**：純海域可以不產磚、前端視為 0 m；或取上一層父磚的對應象限做雙線性升採樣。父磚請求要快取。
4. **陸海合成用 mosaic，不用平均**：陸地 DEM 在上、海底資料在下，只在陸地 nodata 處露出。海岸硬接縫先接受，太糟再做沿岸羽化。
5. **zoom 依來源解析度截止**：海底資料約 450 m 時，約 z10–12 到頂；更高 zoom 只烘陸地磚。
6. **色階分兩段**：海平面釘在固定位置（例如 0.35），海、陸各一段；別把最低值線性拉到 −4000 m。
7. **基準面只用陸地像素算**。
8. **誇張倍率**：
   - Mapbox／MapLibre：`map.setTerrain({ source, exaggeration })` 是 runtime 參數，原生圖層會貼地；自訂 3D 物件要用同一倍率算高度。
   - 自寫引擎：倍率做成 shader uniform、切換時插值，不烘進幾何；已烘進幾何的就在放開滑桿後才重建，貼地圖層讀同一倍率。
   - 真實比例常看起來太平，誇張是必要手段，但要在介面標示倍率。
9. 20 m DEM 近看會有階梯狀山坡，用細節法線或紋理遮掩，不要硬升採樣。

## 怎麼偵測
- 通用：沿海岸與離島平移，看有沒有黑坑或黑三角；開海底地形後檢查淺海是否透明見底；切換載入地點看場景高度有沒有變。
- 搜尋：`R\s*\*\s*256\s*\+\s*G` 或 `-\s*32768`，附近有 `v\s*<\s*-\d+` 這類深度門檻（適用自寫解碼，three.js／any）。
- 搜尋：`"encoding"\s*:\s*"(terrarium|mapbox)"` 與烘焙腳本用的公式是否一致（mapbox-gl、maplibre）。
- 搜尋：`Math\.max\(0,.*minH` 或 `pow\(` 作用在可能為負的正規化高程上（three.js 頂點著色）。
- 搜尋：`exaggeration` 只出現在 terrain 設定，沒有出現在自訂 3D 圖層的高度計算（mapbox-gl、maplibre、three.js）。

## 出處
- Mapbox Terrain-RGB 編碼說明；Terrarium 格式（Mapzen／AWS Terrain Tiles 文件）；MapLibre／Mapbox style spec `raster-dem` 的 `encoding` 與 `setTerrain` 的 `exaggeration`。
- GEBCO Grid 官方說明（public domain，需標示來源）。

