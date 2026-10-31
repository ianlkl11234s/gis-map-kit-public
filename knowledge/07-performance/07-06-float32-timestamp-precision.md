---
id: 07-06
title: 絕對時間戳不要存 Float32：1.7e9 秒的精度只有 128 秒，動畫會一格一格跳
topic: 07-performance
kind: pitfall
scope: public
evidence: Observed
stacks: [mapbox-gl, maplibre, deck.gl, three.js]
tags: [float32, 精度, timestamp, unix, ulp, 相對時間, shader uniform, 階梯, 播放]
---

## 原則
時間戳存相對值（`t − base`），不要把 unix 絕對秒放進 `Float32Array` 或 shader uniform；絕對時間保留在 Float64 或 Uint32。

## 症狀
- 高倍速播放時軌跡的「已走過／未走過」邊界每隔一段時間才跳一格，而不是平滑前進。
- 時間比較在 shader 裡結果階梯狀；換成較小數字就正常。

## 原因
Float32 只有約 24 位元有效位數。unix 秒約 1.77e9，相鄰可表示的值相差 128 秒（ulp＝128），誤差約 ±64 秒。把絕對秒存進 `Float32Array` 或當 uniform 傳給 shader，再做比較，解析度只有 128 秒。

## 解法
1. 時間戳存**相對值**：`t − base`（base＝視窗起點或當日零點）。一天內最多 86,400，Float32 的 ulp 約 0.0078 秒。
2. shader 的 `uTime` 同樣用 `now − base`，base 作為另一個 uniform 或在 CPU 端先減。
3. 需要絕對時間的欄位（原始 timestamp）保留在 `Float64Array`／`Uint32Array`，不要走 float32。
4. 經緯度同理：Float32 約 2.4 m 的位移，在高 zoom 可見；降精度前先在高 zoom 驗證。
5. 加一個單元測試：在播放速度 60× 以上，檢查時間比較是否單調且連續。

## 怎麼偵測
- 通用：播放時邊界階梯式跳動，跳動週期固定（約 2 秒 @60×）。
- 搜尋：`new Float32Array\(.*(time|timestamp|ts)`；`uniform float uTime` 且傳入 `Date\.now\(\)\s*/\s*1000`（適用 stack：three.js、WebGL）。

## 出處
- IEEE 754 單精度；MDN Float32Array。

