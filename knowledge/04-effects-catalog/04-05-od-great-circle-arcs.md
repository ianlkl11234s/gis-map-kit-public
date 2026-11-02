---
id: 04-05
title: OD 光弧與大圓弧：弧線要細分，不然在球面上是穿過地心的弦
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, deck.gl, three.js]
tags: [OD, arc, 大圓, slerp, 換日線, globe, 光弧, 流向]
---

## 原則
OD 弧線用球面線性插值（slerp）沿大圓細分，每條 24～64 段；只有起訖資料時只畫弧與流量，不畫物體沿弧移動。

## 症狀
- 地球視角下，兩機場間的弧線是一條穿過地球內部的直線。
- 跨換日線的弧線突然橫跨整張地圖。
- 把 OD 表畫成「物體沿直線移動」的動畫，看起來像真的軌跡。

## 原因
頂點被投影到球面，但頂點之間的線段不會。弧線若只有 2 個取樣點就是弦。經度直接做線性插值（lerp）在換日線與高緯度都是錯的。

## 解法
1. 用 slerp（在 3D 單位向量空間內）沿大圓取樣，每條弧 24～64 段；低於約 8 段在球面視角會看到穿地。
2. 換日線：不要比對原始經度差；用 3D 向量或 atan2 分支處理。
3. 弧高（拋物線抬升）與線寬可編碼流量；顏色編碼方向或類別。OD 表（只有起訖、沒有中間軌跡）只畫弧與流量，不做「物體沿弧移動」的假軌跡（見 [04-16](04-16-dont-fake-dynamics.md)）。
4. 動態：用 uniform 驅動「沿弧生長」或「亮點沿弧跑」，所有弧合成一個 `LineSegments`（一個 draw call），前提是已處理好 globe 貼球（見 [04-13](04-13-custom-layer-on-globe.md)）。
5. 平面小範圍、弧數少（< 數百）：原生 `line`（Mapbox 可加 `line-trim-offset`）或 deck.gl `ArcLayer` 即可，不需要 custom layer。

## 怎麼偵測
- 通用：縮到 globe 視角，弧線穿過球；跨太平洋的弧走錯邊。
- 搜尋：弧線取樣段數常數 < 8（`segments\s*[:=]\s*[2-7]\b`）；對經度做 `lerp\(.*lng|lon`（three.js、deck.gl、any）。

## 出處
- 球面線性插值（slerp）與大圓取樣為一般圖學與地理計算做法。相關卡：[04-13](04-13-custom-layer-on-globe.md)、[04-16](04-16-dont-fake-dynamics.md)。
- 實例：[mini-taiwan-pulse three-showcase.html](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/public/three-showcase.html) 的 arc、flowline 元件。

