---
id: 04-13
title: Three.js custom layer 預設不貼 globe：縮遠後光點、弧線飄在平面旁邊
topic: 04-effects-catalog
kind: pitfall
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, three.js]
tags: [globe, custom layer, ECEF, 球面, depthTest, 背面剔除, transition, CustomLayerInterface]
---

## 原則
要縮到 globe 視角的 custom layer，必須自己把頂點轉到球面（Mapbox 用 ECEF 與過渡係數混合，MapLibre 用官方 projection 參數）；只在平面 mercator 檢視使用時，不要付這個成本。

## 症狀
縮小到地球視角時，原生點線面都貼在球面上，但自訂的光點、弧線、軌跡仍畫在一張平面上，漂在地球旁邊或穿過球體；地球背面的物件仍可見。

## 原因
Mapbox GL JS 官方文件明講 globe 不支援 `CustomLayerInterface`；custom layer 只拿到 mercator matrix。MapLibre 官方則支援（有專屬的 projection 參數）。

## 解法
Mapbox 路線：
1. 預先計算每個頂點的 ECEF 座標（靜態幾何不要每幀重算 trig）。
2. 用 Mapbox 在 render 時另給的 globe→mercator 矩陣與過渡係數（zoom 約 5→6 由 0 漸變到 1），把 ECEF 位置轉進同一空間後與 mercator 位置 `mix`，再乘 mercator matrix。
3. `depthTest:false`：底圖已寫入實心球的深度，近遠平面問題會讓幾何消失；改用背面剔除（在 ECEF 空間判斷與相機的夾角）自行處理遮擋。
4. 弧線／線段頂點之間不會自動貼球，必須細分（見 [04-05](04-05-od-great-circle-arcs.md)）。
5. 每種 blending 設明確 `renderOrder`（見 [04-10](04-10-glow-bloom-points.md)）。
6. 只有一般 mercator 檢視（不會縮到 globe）時，不要做這些，這是長期維護成本。

MapLibre 路線：用官方 custom layer 的 projection data 參數，不需要自己算 ECEF。

## 怎麼偵測
- 通用：把 zoom 縮到 < 5，自訂物件不貼球、轉到背面仍在。
- 搜尋：`CustomLayerInterface` 且 render 內無 `globe|ecef|transition|projectionData`（mapbox-gl、maplibre）。

## 出處
- Mapbox GL JS globe guide（「Globe does not yet support CustomLayerInterface」）；MapLibre custom layer on globe 官方範例。
- 相關卡：[04-05](04-05-od-great-circle-arcs.md)、[04-10](04-10-glow-bloom-points.md)、[04-18](04-18-threejs-custom-layer-matrix-and-one-renderer.md)（custom layer 的矩陣取法與一個 context 一個 renderer）。
- 實例：[mini-taiwan-pulse QuakeRippleScene.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/QuakeRippleScene.ts)（zoom < 6 為 globe、背面收圈）。

