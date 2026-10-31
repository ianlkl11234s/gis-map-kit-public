---
id: 04-00
title: 動態／視覺效果總表：想表達的語意 → 效果 → 卡片 → 難度
topic: 04-effects-catalog
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [效果清單, 語意, 選擇表, 動畫, 難度, 索引]
---

## 原則
先講清楚「想讓使用者看懂什麼」，再從下表挑效果；答不出「拿掉這個動畫會少看懂什麼」就不要做。任何動態效果動手前先讀 [04-01](04-01-native-vs-custom-layer-decision.md)（選技術）、[04-15](04-15-animation-repaint-budget.md)（重繪預算）、[04-16](04-16-dont-fake-dynamics.md)（不假造資料）。靜態的表現形式（點、線、面、熱區、網格、標籤）見 [04-20](04-20-static-forms-catalog.md)。

難度：1=原生 paint／filter 幾行；2=一個 Three.js／deck.gl 元件；3=自寫 shader、GPU buffer、globe 貼球或需要編排。

## 對照表

| 想表達的語意 | 效果 | 技術重點 | 卡片 | 難度 |
|---|---|---|---|---|
| 這個東西在移動（車、船、飛機） | 光球沿路徑／時刻表滑行 | 時間插值、不外推、切段、進度投回線 | [04-02](04-02-moving-objects-interpolation.md) | 2 |
| 它剛才走過哪裡 | 軌跡尾巴（彗尾） | line-gradient／TripsLayer／批次 line strip | [04-03](04-03-trail-tails.md) | 2–3 |
| 風、水流的方向與強度 | 流場粒子 | raster-particle 或 CPU advection + instanced 線 | [04-04](04-04-flow-particle-field.md) | 3 |
| A 與 B 之間有流量（OD） | 大圓光弧 | slerp 細分、弧高編碼流量 | [04-05](04-05-od-great-circle-arcs.md) | 2–3 |
| 事件剛發生、向外擴散 | 漣漪／脈衝圈 | 避免每幀 setPaintProperty；instanced 四邊形 | [04-06](04-06-ripple-and-wavefront.md) | 2 |
| 事件後影響如何傳遞（有傳遞規則） | 事件回放、波前編排 | scoped clock、視覺＝時鐘純函數 | [04-07](04-07-event-replay-scoped-clock.md) | 3 |
| 數值隨時間變（面量圖、點、影像） | filter／feature-state／GPU fade／影像序列 | 不重 setData | [04-08](04-08-time-driven-change.md) | 1–3 |
| 這類點很重要／正在運作／要注意 | 光柱、旋轉光束、閃爍、選取圈 | InstancedMesh、有語意才加 | [04-09](04-09-emphasis-pulse-beam.md) | 1–2 |
| 這裡密集、像夜景燈火 | 偽 bloom 光暈 | Points + 三段 halo + 加性混合 | [04-10](04-10-glow-bloom-points.md) | 2–3 |
| 這個數值很大／水位多高 | 高度編碼量體 | fill-extrusion 或 InstancedMesh + lerp | [04-11](04-11-3d-volumes-data-encoding.md) | 1–2 |
| 帶使用者去看某處／講故事 | 鏡頭 flyTo、環繞、電影運鏡、跟隨 | 單一鏡頭來源、弧長取樣、減少動態 | [04-12](04-12-camera-motion.md) | 1–3 |
| 縮到整顆地球也要對 | custom layer 貼 globe | ECEF + 過渡係數 + 背面剔除 | [04-13](04-13-custom-layer-on-globe.md) | 3 |
| 氣氛：天氣、日夜、颱風雲、空域 | 程序化 shader | 標明純視覺、可關閉 | [04-14](04-14-atmosphere-weather-daynight.md) | 2–3 |
| 動畫太吃效能 | 重繪預算、量測 | 靜態不 repaint、全域排程、先量測 | [04-15](04-15-animation-repaint-budget.md) | 2 |
| 資料不夠，還要做動畫嗎 | 不假造動態規則 | Change／Flow／Propagation／Scenario | [04-16](04-16-dont-fake-dynamics.md) | — |
| 新效果怎麼試 | 案例庫與 sandbox | 零 build 單檔 HTML | [04-17](04-17-effect-prototyping-workflow.md) | 1 |

## 選技術速查（細節見 [04-01](04-01-native-vs-custom-layer-decision.md)）
- 整層一起變 → 原生 `setFilter`／`setPaintProperty`／`feature-state`。
- 上萬物件各自動 → GPU：Three.js custom layer、deck.gl、raw WebGL2。
- 要加性混合、粒子物理、instanced 動畫 → custom layer（接受不貼 globe、不自動 dispose 的代價）。
- 單位物體只有數十個且靜態 → 不用 3D。

## 怎麼偵測
- 通用：有動畫卻回答不出「拿掉會少看懂什麼」；暫停時仍在重繪；缺測被畫成 0。
- 搜尋：見各卡。

## 出處
- 各效果的依據與實例見對應卡片。

