---
id: 04-01
title: 動態效果先選技術：原生 paint 動畫、Three.js custom layer、deck.gl、raw WebGL 怎麼挑
topic: 04-effects-catalog
kind: decision
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, deck.gl, three.js]
tags: [custom layer, 選型, setPaintProperty, deck.gl, TripsLayer, raster-particle, line-trim-offset, 效能]
---

## 原則
做動態效果前先判斷「誰在動、動幾個」，能用原生 paint／filter／feature-state 就不要寫 shader；只有上萬個物件各自獨立動，或需要加性混合時，才升級到 custom layer 或 deck.gl。

## 症狀
想做一個動畫就直接寫 shader，結果不是在 globe 上不貼球、就是每幀 `setData` 卡頓，或為了原生本來就能做的事養了兩百行 GLSL。

## 原因
地圖上的「動」有三種成本結構，混在一起選會選錯：
1. 整層一起變（改 paint、改 filter、換 source）：原生就夠，成本是「每次變更一次」。
2. 少量物件每幀變：每幀改 paint 或 `setData` 勉強可行，但 source 會被標成 reload（`map.loaded()` 一直是 false、`idle` 不觸發）。
3. 成千上萬個物件各自獨立動：只有 GPU 側（custom layer、deck.gl）撐得住。

## 解法
依序問，遇到「夠了」就停：

| 想要的效果 | 先試 | 什麼時候才升級 |
|---|---|---|
| 顏色／大小／透明度隨時間變、累積顯示 | 原生 `setFilter`、`setPaintProperty`、`feature-state` | 逐 feature 每幀改（> 數千點） |
| 路線漸層、逐步長出的線 | 原生 `line-gradient`（需 `lineMetrics:true`）、`line-trim-offset`（Mapbox 限定） | 需要彗尾淡出且每條線時間不同 |
| 風／海流粒子 | Mapbox 原生 `raster-particle`（資料要是 raster-array 格式） | 資料不是該格式、即時更新、MapLibre、粒子要自己的物理 |
| 3D 模型擺在點上 | 原生 `model` layer（Mapbox 限定；MapLibre 用 custom layer） | 要程序化幾何或 instancing 動畫 |
| 柱、稜柱 | 原生 `fill-extrusion` | 柱高要每幀平滑、要發光 |
| 點的光暈、真正的加性混合 | Three.js／raw WebGL custom layer | 原生做不到 additive blending |
| 數萬到數十萬條軌跡、時間用 uniform 驅動 | deck.gl `TripsLayer`（data 引用穩定，只更新 `currentTime`） | 需要貼 Mapbox globe 或與其他 custom layer 共用 GL context |
| 大量粒子、不想背 Three.js | raw WebGL2 custom layer | — |

custom layer 的代價（要自己補）：沒有 `source`、沒有 `layout.visibility`、沒有 `minzoom/maxzoom`、不會自動貼 globe、不會自動 dispose、重繪要自己 `triggerRepaint`。

## 怎麼偵測
- 通用：動畫期間 `map.loaded()` 一直是 false；每幀都在改整份 GeoJSON；低 zoom 的 globe 上自訂物件漂在平面旁邊；暗色主題好看、亮色主題疊序錯。
- 搜尋：`setInterval|requestAnimationFrame` 同檔又有 `setData\(|setPaintProperty\(`（mapbox-gl、maplibre）；`CustomLayerInterface` 且只畫 < 200 個靜態點（可能過度設計）。
- 相關卡：[04-15](04-15-animation-repaint-budget.md)（重繪預算）、[04-13](04-13-custom-layer-on-globe.md)（globe 貼球）。

## 出處
- Mapbox／MapLibre style spec 與 changelog（`raster-particle` v3.3.0 起、`model` layer GA v3.17）。
- 相關卡：[04-18](04-18-threejs-custom-layer-matrix-and-one-renderer.md)（Three.js 投影矩陣與單一 renderer）。
- 實例：[mini-taiwan-pulse QuakeRippleScene.ts 檔頭](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/QuakeRippleScene.ts)（舊做法每幀改 circle-radius 造成 map.loaded() 恆為 false）。

