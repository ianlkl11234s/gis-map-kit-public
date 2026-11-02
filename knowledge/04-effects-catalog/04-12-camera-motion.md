---
id: 04-12
title: 鏡頭動態：flyTo、環繞、電影運鏡、跟隨——同一時間只能有一個鏡頭來源
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, three.js]
tags: [鏡頭, flyTo, easeTo, orbit, 運鏡, keyframe, 跟隨, tour, reduced-motion, 錄影]
---

## 原則
同一時間只讓一個動畫控制鏡頭：要一起動的 padding 與 center 放在同一個 `flyTo`／`easeTo`；所有運鏡都要尊重 `prefers-reduced-motion`。

## 症狀
- `easeTo({padding})` 之後立刻 `flyTo`，padding 過渡半路被取消。
- 運鏡速度忽快忽慢、轉角急拐、鏡頭穿進山裡。
- 跟隨移動物件時鏡頭抖動或使用者無法微調。

## 原因
Mapbox／MapLibre 同一時間只有一個鏡頭動畫，後發會取消前者；自製運鏡若不控制速度剖面與旋轉阻尼就會有急變。

## 解法
- **兩件事要一起動就放在同一個動畫**（padding + center 同一個 `flyTo`／`easeTo`）。
- 全站預設 flyTo（`curve` 約 1.25）；尊重 `prefers-reduced-motion`（duration 0）。
- 環繞（orbit）：以固定角速度（約 0.2～8°/s、可正反向）改 bearing；用 RAF 計時而非數幀。
- 電影序列：keyframe（still／orbit hold + easing ease-in-out／linear／ease-out）、可循環、可存 JSON。錄影輸出用 Canvas 錄影，需把 UI 隱藏。
- 自訂 3D 引擎的運鏡：樣條（Catmull-Rom）按**弧長**取樣才會等速；用梯形速度剖面（加速—巡航—減速）；旋轉走阻尼 gimbal，不直接 set；路線規劃時先預載地形圖磚並做離地間隙保證。三種模式：點到點、繞山頂、等高線環。
- 跟隨：每幀把物件的位移量（delta）同時加到 target 與 camera position（delta-carry），保留使用者的相對視角；物件消失（回傳 null）就自動解除。駕駛艙視角疊在跟隨之上，不另開新的鏡頭來源。
- Agent／敘事：鏡頭動作與圖層切換順序是敘事的一部分（先飛、再開圖層、再畫結果）。

## 怎麼偵測
- 通用：padding 動畫半途停住；錄影時鏡頭抖；使用者開了減少動態仍然飛行。
- 搜尋：緊鄰兩行 `easeTo\(.*padding` 與 `flyTo\(`；沒有 `prefers-reduced-motion`/`matchMedia` 的 `flyTo` 封裝（mapbox-gl、maplibre）。

## 出處
- Mapbox／MapLibre `flyTo`、`easeTo` 文件；MDN `prefers-reduced-motion`。
- 實例：[mini-taiwan-pulse researchMotion.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/research/researchMotion.ts)（prefersReducedMotion）、[cameraPresets.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/cameraPresets.ts)。

