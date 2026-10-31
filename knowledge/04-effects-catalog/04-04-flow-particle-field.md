---
id: 04-04
title: 風場／海流粒子：先查原生 raster-particle，不行再 CPU advection + instanced 線
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, three.js]
tags: [粒子, 風場, 海流, nullschool, advection, 向量場, raster-particle, 流線]
---

## 原則
流場粒子先用 Mapbox 原生 `raster-particle`；資料格式或引擎不符時，改用「預烘向量場 PNG + CPU advection + instanced 線」，粒子數量依 zoom 量化調整。

## 症狀
想做 nullschool 式的流動細線，但資料不是 Mapbox 的 raster-array，或需要在 MapLibre／globe 上跑。

## 原因
流場視覺需要數萬條每幀都動的線段；用 GeoJSON 每幀更新不可行。

## 解法
1. 先試 Mapbox 原生 `raster-particle`（v3.3 起；v3.4 修 globe 閃爍）。條件不符才自己做：資料非 raster-array（上傳處理流程重）、近即時更新、粒子要自有物理、用 MapLibre。
2. 自己做的配方：
   - 向量場預烘成 PNG（R→u、G→v、alpha 區分海陸），瀏覽器解碼成 `Uint8ClampedArray`，**在 CPU 上雙線性取樣**。
   - 每個粒子保留短歷史（尾跡點數）；CPU Euler 步進 `x += u*dt/metersPerDegLon`；出界／壽命到就重生。
   - 歷史點的 mercator 座標只在「新頭點」算一次，其餘靠陣列位移複製（靜態量快取，相機相關的 trig 才每幀跑）。
   - 繪製：instanced 四邊形展開成固定像素寬的線（或單一 `LineSegments`）。
   - 速度正規化上色（色帶 0→1）；海流用 alpha mask 侵蝕 1 px 避免畫到陸地。
   - **zoom 自適應密度**：拉遠自動加粒子（基準 zoom 以下每少一級多加 70% 基準量、封頂 6 倍），數量量化到固定倍數（如 4,000），避免連續縮放每幀重配置陣列。
   - 視覺速度與真實時間脫鉤（「每 1 真實秒推進 N 流體秒」），要在圖例註明。
3. 時間維度：場本身是 snapshot；播放時間軸只切換下一張場，粒子不重生。

## 怎麼偵測
- 通用：低 zoom 粒子稀疏、高 zoom 擁擠；海流線畫上陸地；改 zoom 時卡一下（陣列重配置）。
- 搜尋：`particleCount` 隨 `getZoom\(\)` 連續變化且沒有 quantize／`Math.round\(.*/ *\d+\)`（any）。

## 出處
- Mapbox style spec：raster-particle layer。
- 實例：[mini-taiwan-pulse climateParticleLineLayer.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/climateParticleLineLayer.ts)（自適應密度常數與量化）。

