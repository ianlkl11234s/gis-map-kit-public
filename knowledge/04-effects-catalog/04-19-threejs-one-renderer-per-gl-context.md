---
id: 04-19
title: 一個 GL context 只放一個 Three.js renderer：第二個特效圖層會讓兩個都不畫
topic: 04-effects-catalog
kind: pitfall
scope: public
evidence: Observed
stacks: [mapbox-gl, maplibre, three.js]
tags: [three.js, custom layer, WebGLRenderer, GL context, state cache, resetState, dispose, hot reload]
---

## 原則
一個地圖 GL context 只放一個 `THREE.WebGLRenderer`：多個特效放進同一個 Scene，並在每次 render 前後呼叫 `renderer.resetState()`。

## 症狀
- 新增第二個 Three.js 特效圖層做對照後，兩個都不畫，或其中一個壞掉。
- hot reload 之後也會發生；資料筆數正確、沒有錯誤，畫面全無。

## 原因
每個 `THREE.WebGLRenderer` 都快取自己以為的 GL 狀態（目前的 program、VBO、blend、uniform）。兩個 renderer 包同一個地圖 GL context 時，一個改了狀態，另一個仍以為是自己上次留下的，shader、buffer 對不上就什麼都不畫。忘了 `removeLayer` 舊的就 `addLayer` 新的，也是同一種情況。

## 解法
1. 多個特效放進同一個 custom layer 的同一個 Scene，用 group、InstancedMesh 或 uniform 分開；要 A／B 對照時，改用原生圖層疊多次做，避開第二個 renderer。
2. 用地圖的 canvas 與 context 建 renderer（`context: gl`）、`autoClear = false`；每次 render 前後呼叫 `renderer.resetState()`，讓 Three.js 不信任自己的快取，並把狀態交還給地圖。
3. `onRemove` 裡 dispose 幾何、材質、renderer；重新掛載前先確定舊圖層已 `removeLayer`。

## 怎麼偵測
- 通用：只有開某兩個特效圖層時其中一個消失。
- 搜尋：同一個專案有兩處以上 `new THREE\.WebGLRenderer\(` 在不同 custom layer 內，且都傳入地圖的 `context`（three.js、mapbox-gl、maplibre）。
- 搜尋：custom layer 的 `render` 裡沒有 `resetState\(\)`（three.js）。

## 出處
- three.js `WebGLRenderer.resetState()` 文件。
- 相關卡：[04-17](04-17-effect-prototyping-workflow.md)（原型接線清單）、[04-18](04-18-threejs-custom-layer-matrix-and-one-renderer.md)（投影矩陣）、[07-10](../07-performance/07-10-memory-leaks-listeners-contexts.md)（切底圖或重建圖層後 WebGLRenderer 洩漏的 dispose 檢查）。
- 實例：[mini-taiwan-pulse bloom-experiments README](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/bloom-experiments/README.md)（新增第二個 Scene 對照後畫面全無）。
