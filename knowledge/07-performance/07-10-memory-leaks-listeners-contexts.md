---
id: 07-10
title: 記憶體洩漏：切底圖或重建圖層後，listener、WebGLRenderer、場景實例越留越多
topic: 07-performance
kind: pitfall
scope: public
evidence: Evaluated
stacks: [mapbox-gl, maplibre, deck.gl, three.js]
tags: [記憶體洩漏, dispose, listener, webglcontextlost, WebGLRenderer, 切底圖, style.load, cleanup, TypedArray]
---

## 原則
每個註冊的 listener、計時器與 GPU 資源都要有對應的釋放，並放進同一個 cleanup；重建圖層前先 dispose 舊的，並用「重複同一操作 N 次」量測斜率確認沒有洩漏。

## 症狀
- 反覆切換底圖或圖層後，頁面記憶體線性成長，最終變慢或 WebGL context lost。
- 殘留物件「閃一下又消失」（舊 closure 仍在運作）。
- 量記憶體的 JS heap 指標看不出問題。

## 原因
- 每次 `style.load` 重建 custom layer，卻沒有 `dispose` 舊的 renderer、場景、geometry、texture；每次多留一個場景實例、多個 renderer 與其 `webglcontextlost` listener。
- 在 `if (!ready) { map.on('style.load', ...) }` 這類分支內註冊的 listener 沒有進 cleanup。
- 計時器、throttle 的 trailing 呼叫在元件卸載後仍 fire 舊 closure。
- 量測指標的盲點（TypedArray 不在 JS heap）見 [07-01](07-01-performance-budget-and-measurement.md)。

## 解法
1. 所有 `map.on`、`addEventListener`、`setInterval`、`requestAnimationFrame` 都要有對應的 `off`／`clear`／`cancel`，放進同一個 cleanup。與 callback 相關的 deps 用 ref 保持穩定，減少重綁。
2. custom layer 的 `onRemove` 要 `dispose` geometry、material、texture、renderer（`renderer.dispose()`；必要時 `forceContextLoss()`）。
3. 同一個 GL context 只掛一個 three.js renderer 實例，重用而非重建。
4. 換底圖後重建的圖層，用 factory 加「若已存在則 reuse」判斷。
5. effect 內的 ref 旗標（如 `disposedRef`）在 effect 開頭重設，避免 StrictMode 雙掛載誤判。
6. **量測**：重複動作 N 次（換底圖 ×10），記錄 renderer 與 GPU 行程記憶體、實例計數（場景、renderer、listener）。斜率不為零＝洩漏；用 `backingStorageSize` 與行程 footprint（見 [07-01](07-01-performance-budget-and-measurement.md)）。

## 怎麼偵測
- 通用：重複同一操作後記憶體只升不降；`getEventListeners` 數量成長；WebGL context 警告。
- 搜尋：`map\.on\(` 沒有對應 `map\.off\(`；`new THREE\.WebGLRenderer` 位於每次 style.load 都會執行的函式；`onRemove` 缺少 `dispose`（適用 stack：mapbox-gl、three.js）。

## 出處
- three.js "How to dispose of objects"。
- 相關卡：[07-01](07-01-performance-budget-and-measurement.md)。

