---
id: 07-04
title: 更新粒度：每幀別 setData；位置寫 typed array，樣式只更有變的 key，物件組不變就不重建
topic: 07-performance
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, deck.gl, three.js]
tags: [setData, typed array, buffer, InstancedMesh, per-instance attribute, dispose, 重建, diff, 閃爍, fast path]
---

## 原則
每幀只改變動的那一小部分：位置直接寫進 typed array，樣式只更新有變的 key，物件組沒變就不 dispose 重建；`setData` 只留給資料真正換集合的時候。

## 症狀
- 播放時每幀 CPU 很高，`setData` 佔大宗。
- 時間軸每跳一格，3D 物件閃一下。
- 每次樣式變更都整批重設。

## 原因
- `source.setData` 會重新序列化、切磚並標記整個 source reload，每次約數毫秒，不能每幀呼叫。
- 物件組沒變卻 dispose 再重建 mesh，會造成 GPU buffer 重建與閃爍。
- 把整個 paint 物件重設，引擎要整批重算。

## 解法
1. **每幀更新位置**：直接寫進 typed array（`Float32Array`）再標記 `needsUpdate`／部分上傳，成本約百分之一毫秒等級；`setData` 留給資料真正換集合的時候。
2. **fast path**：物件組（站點、車輛集合）不變時，只更新 matrix／color／per-instance attribute，不 dispose／recreate。
3. **per-instance attribute**：每個實例要有獨立相位、顏色、大小時，用 instanced attribute 加 shader（`onBeforeCompile` 擴充內建材質），單一 draw call。
4. **樣式 diff**：只對有變的 key 呼叫 `setPaintProperty`；隱藏圖層不寫（見 [07-03](07-03-hidden-layer-paint-keeps-map-busy.md)）。
5. **部分上傳**：只標記有變的範圍（`addUpdateRange`），不要整條 buffer 重傳。
6. **事件節流**：時間軸訂閱分粒度（每幀、10 Hz、1 Hz），重運算拆到低頻；用 ref 讀最新狀態，避免 callback 因 deps 改變而反覆重綁。改完用計時（[07-01](07-01-performance-budget-and-measurement.md)）比較前後，並用錄影確認沒有閃爍。

## 怎麼偵測
- 通用：Performance 面板每幀有 `setData`／`bufferData`；回放時閃爍。
- 搜尋：`requestAnimationFrame.*setData|setData\(.*\)\s*;?\s*//.*frame`；`dispose\(\)` 與 `new (InstancedMesh|Mesh)\(` 出現在每次更新的函式內（適用 stack：mapbox-gl、three.js）。

## 出處
- three.js `BufferAttribute.addUpdateRange`、InstancedMesh 文件。
- 相關卡：[07-01](07-01-performance-budget-and-measurement.md)、[07-03](07-03-hidden-layer-paint-keeps-map-busy.md)。

