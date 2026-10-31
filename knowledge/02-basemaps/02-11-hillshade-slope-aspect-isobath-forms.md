---
id: 02-11
title: 山體陰影、坡度坡向、等深線要選哪種形態：預烤影像、即時 raster、還是分級向量
topic: 02-basemaps
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [hillshade, 山體陰影, 坡度, 坡向, slope, aspect, 等深線, isobath, GEBCO, 深度分帶, DEM, polygonize, PMTiles, feature-state, 地形]
---

## 原則
先決定使用者要不要點選查值、要不要換配色，再選地形衍生資料的形態：只當襯底用預烤影像，要點選與分級說明才用分級向量（PMTiles）。

## 症狀
- 想讓使用者點地圖查「這裡坡度幾級」，但坡度圖是一張 PNG，點下去什麼都拿不到。
- 等深線拉近到 z13 細得幾乎看不見；深度分帶的填色蓋到了陸地。
- 坡度圖和坡向圖疊在一起比對，「平地」的範圍對不起來。
- 地形圖層佔掉大量儲存，或每次換配色都要重新烘焙。

## 原因
地形衍生資料有三種常見形態，能做的事不同：

| 形態 | 能點選查值 | 換配色 | 成本 |
|---|---|---|---|
| 預烤影像（PNG／raster 圖磚，colormap 已烤進去） | 不能 | 要重烤 | 最便宜，前端只控透明度 |
| 值編碼 raster（像素存物理值，前端上色） | 只能靠取樣，不是 feature | 可在前端換（見 [05-11](../05-color/05-11-raster-value-encoding-color-mix-pixel-sampling.md)） | 要處理值編碼與 nodata |
| 分級向量（polygonize 成面，或抽等值線） | 可以，有屬性 | 可在前端換 | 要篩除小碎面；面數多、檔案大 |

另外兩個常見坑：
- 線寬固定時，拉近後相對於畫面變得極細；線圖層需要隨 zoom 放大。
- 不同衍生層用不同門檻定義「平地」（例如坡向用 slope < 5°，坡度分級第一級用 < 5%，約 2.86°），兩者相容但不相等。

## 解法
1. **只當底圖襯托**（山體陰影、色別標高）：用預烤影像或外部現成圖磚，前端只給透明度。夠用就停。
2. **要點選、要分級說明**（坡度、坡向）：DEM → 重算坡度坡向 → 分級 → 篩除小碎面（GDAL `sieve`）→ polygonize → tippecanoe 打成 PMTiles；前端依分級欄位用 `match` 或 `feature-state` 上色，同一份分級對照表給圖例與 popup 用。
3. **分級沿用領域既有門檻**，例如建管的坡度分級、八方位加平地，不自創切點；把每級的值域寫進資料契約。
4. **等深線＝線＋分帶兩種 feature 放同一支 PMTiles**，用 `kind` 屬性分流成 line 與 fill 兩個 sub-layer。分帶面要做成環差（自帶 hole、陸地挖空），並用幾個內陸點檢查沒有誤塗。
5. **線寬隨 zoom 內插**（例如 z5 0.4 → z15 2.2），不要寫固定寬度。
6. **深度與高程的分級邊界只在一處定義**，色階、圖例、popup 共用；上游若調整邊界，下游要同步改。
7. **標示定義差異**：兩個衍生層門檻不同時，在圖例或說明寫出來，提醒使用者不要直接疊圖比對。
8. 要「精確數值查詢」時，向量分級做不到，需要另接值編碼 raster 或後端的區域統計。

## 怎麼偵測
- 通用：點擊地形圖層沒有 popup；拉近後等深線消失；分帶填色出現在內陸。
- 搜尋：`hillshade|slope|aspect` 的 source 是單一 `image` 或 `.png`，而產品要點選查值（mapbox-gl、maplibre）。
- 搜尋：`"line-width"\s*:\s*\d` 寫固定數字的等值線圖層（mapbox-gl、maplibre）。
- 搜尋：等深線 PMTiles 的兩個 sub-layer 沒有 `["==", ["get", "kind"], …]` 這類 filter，或色階陣列長度與分級數不同（any）。

## 出處
- GDAL `gdaldem`（hillshade、slope、aspect）、`gdal_sieve`、`gdal_polygonize`、`gdal_contour` 文件；tippecanoe 文件。
- GEBCO Grid（public domain，需標示來源）。
- 相關卡：[02-10](02-10-dem-terrain-rgb-encoding-and-bathymetry.md)（DEM 編碼與 3D 地形）、[05-11](../05-color/05-11-raster-value-encoding-color-mix-pixel-sampling.md)（值編碼 raster 上色）、[06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)（GeoJSON 轉 PMTiles）。
- 實例：[坡度坡向向量化流程](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/terrain-vector/README.md)、[等深線與分帶](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/isobath/changelog.md)。
