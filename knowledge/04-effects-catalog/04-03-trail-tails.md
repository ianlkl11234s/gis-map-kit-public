---
id: 04-03
title: 軌跡尾巴：四種做法與各自的成本
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, deck.gl, three.js]
tags: [trail, 彗尾, TripsLayer, line-gradient, 光軌, 批次, draw call, 歷史軌跡]
---

## 原則
依同時存在的尾巴數量選做法：單條用原生漸層線，數萬條用 deck.gl `TripsLayer`，數千條在 Three.js 合成單一 line strip；尾巴的時間窗一律用資料時間算。

## 症狀
想讓移動物件後面拖一條會淡出的尾巴，但物件一多就卡、尾巴在亮色主題看不見、尾端跟下一條軌跡連在一起。

## 原因
尾巴的本質是「最近 N 分鐘的路徑、越舊越透明」。每種實作把這個成本放在不同地方（CPU 歷史、GPU uniform、每條線一個 draw call）。

## 解法
先依規模挑做法：

| 做法 | 適合 | 代價 |
|---|---|---|
| 原生 `line-gradient`／`line-trim-offset` | 單條或少數線、全線同步漸層 | 每條線時間不同就做不到；需 `lineMetrics:true` |
| deck.gl `TripsLayer` | 數萬條、時間軸拖曳零延遲 | `currentTime` 是 uniform，**data 引用必須穩定**，否則每次重建 GPU buffer；不貼 Mapbox globe |
| Three.js 每物件一條 line，自訂 shader（尾 alpha 0→頭 1） | 數十到數百個 | 每條一個 draw call |
| Three.js 批次光軌：全部合成一條 line strip，每條佔固定 slot，slot 間以 opacity=0 的 guard 頂點隔開，per-vertex alpha | 數千條同時在空中 | slot 上限與逐出策略要設計（最接近抵達者先踢；用 min-heap，不要線性掃描） |
| 位置歷史環形緩衝 + `LineSegments` | 列車、船（尾巴短） | 歷史長度 × 物件數 的 CPU 記憶體 |

細節：
- 尾巴時間窗以「資料時間」算（不是掛鐘），才能跟著播放速度。
- 切段：相鄰點間隔超過門檻就斷，否則斷訊前後會畫成假直線（見 [04-02](04-02-moving-objects-interpolation.md)、[04-16](04-16-dont-fake-dynamics.md)）。
- 亮暗主題：暗色用 Additive、亮色必須換 Normal blending 並換成深飽和色，否則亮底上看不見（見 [04-10](04-10-glow-bloom-points.md) 疊序）。
- 靜態歷史軌跡（不動）做成不帶 repaint loop 的 batched geometry，style／參數變更時才要求一次重繪。

## 怎麼偵測
- 通用：尾巴數量一多就掉幀；亮色底圖尾巴消失；暫停後仍持續 100% GPU；deck.gl 圖層每次 React render 都重建 buffer。
- 搜尋：`new TripsLayer` 的 `data` 是在 render 內 `.filter\(|.map\(` 出來的新陣列（deck.gl）；`new THREE.Line` 出現在 for 迴圈內（three.js）。

## 出處
- deck.gl `TripsLayer` 文件。相關卡：[04-02](04-02-moving-objects-interpolation.md)、[04-10](04-10-glow-bloom-points.md)、[04-15](04-15-animation-repaint-budget.md)。
- 實例：[mini-taiwan-pulse LightTrail.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/LightTrail.ts)、[RailScene.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/RailScene.ts)。

