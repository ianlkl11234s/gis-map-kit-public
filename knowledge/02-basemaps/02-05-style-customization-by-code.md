---
id: 02-05
title: 底圖客製化：用程式覆寫官方 style（paint／layout、beforeId、地名、語言、字型、地形）
topic: 02-basemaps
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre]
tags: [style, setPaintProperty, setLayoutProperty, beforeId, 地名, language, setLanguage, localIdeographFontFamily, terrain, globe, Standard, lightPreset, Mapbox Studio]
---

## 原則
客製底圖優先用執行期 API 覆寫官方 style（paint／layout、`beforeId`），不要先進 Studio 重做；覆寫都要能還原，並在 `style.load` 重套。

## 症狀
想讓底圖變暗、隱藏地名、切換語言卻不想重寫 style；資料層蓋住地名；換底圖後地形異常。

## 原因
官方 style 是一份 JSON，每一層都可在執行期用 API 覆寫。

## 解法
1. 看結構：`map.getStyle().layers.map(l => [l.id, l.type, l.source])`。
2. 整套壓暗：逐圖層 `setPaintProperty`，只處理底圖來源與 background，水域依圖層 id 辨識；底圖改版後 id 可能變。
3. 地名開關：只對有 `text-field` 的 symbol 圖層 `setLayoutProperty visibility`，記下 id 以便還原。
4. 地名語言：用 `language` 選項／`setLanguage`（只重載 source）。
5. CJK 字型：`localIdeographFontFamily` 用系統字，免向伺服器要 glyph。
6. 用 `beforeId` 把面圖層插在第一個 symbol 圖層之前，地名才不會被蓋住。
7. 地形：DEM 只在 pitch > 0 時才掛以節省效能；換底圖會清掉 terrain，在 `style.load` 重判斷（見 [02-06](02-06-setstyle-wipes-custom-layers.md)）。
8. 不要對隱藏圖層呼叫 `setPaintProperty`（地圖會持續重繪）。
9. Mapbox Standard style 改用 config（`setConfigProperty('basemap','lightPreset', ...)`，另有 `slot`）。
10. 道路、河流、行政界的個別開關：本卡未驗證，以官方文件確認。
11. 投影：預設 mercator，但官方說 v12 style 預設含 globe，需對各底圖呼叫 `map.getProjection()` 確認。
12. Mapbox Studio 樣式仍走 Mapbox 計費。

## 怎麼偵測
- 通用：資料層蓋住地名；暫停時 CPU 持續跑；中文地名變方框。
- 搜尋：`setPaintProperty`（在迴圈內呼叫於隱藏圖層）、`addLayer\(` 沒有 `beforeId`、`setStyle\(`（見 [02-06](02-06-setstyle-wipes-custom-layers.md)）（適用 stack：mapbox-gl, maplibre）。

## 出處
- 官方：docs.mapbox.com/mapbox-gl-js/guides/styles/、docs.mapbox.com/map-styles/standard/api/、docs.mapbox.com/mapbox-gl-js/guides/projections/。
- 相關卡：[02-06](02-06-setstyle-wipes-custom-layers.md)、[02-10](02-10-dem-terrain-rgb-encoding-and-bathymetry.md)（DEM 編碼與 3D 地形誇張）。
- 實例：[底圖暗色化、地名開關、terrain 的實作](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/MapView.tsx)（[commit 6afa7165](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/6afa7165b77818b8ecf032b2db26eb10d8fa9583)）、[地名語言](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/basemapLanguage.ts)（[commit 42904342](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/42904342cf00a8f82c8774d7698aba57ac1dd8bc)）、[隱藏圖層呼叫 setPaintProperty 的坑](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/pitfalls/2026-09-30-hidden-layer-paint-transition.md)。

