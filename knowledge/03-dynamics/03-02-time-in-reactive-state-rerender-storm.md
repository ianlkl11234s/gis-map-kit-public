---
id: 03-02
title: 播放中的時間放進框架響應式狀態：每幀整個 App 重繪，圖層越多越卡
topic: 03-dynamics
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [React, Vue, Svelte, useState, 響應式, re-render, currentTime, deps, external store, 時間軸, 60fps]
---

## 原則
播放中的時間放在框架外的 external store，不放進 `useState`／`ref`；誰需要時間就自己訂閱，圖層 hook 的參數不收 `currentTime`。

## 症狀
- 時間軸回放時，單開一個動態圖層還順，同時開三、四層就掉幀。
- DevTools 顯示整個根元件每秒重算約 60 次；CPU 花在「JS 重算」而不是「GPU 繪圖」。

## 原因
`currentTime` 放在框架的響應式狀態（React `useState`、Vue `ref`、Svelte store 的 `$`）裡，播放時 RAF 每幀寫一次，所有讀它的元件和 effect 每幀重新評估。成本約為圖層數 × 60 Hz；每個圖層 hook 若把 `currentTime` 放進 effect 依賴陣列，等於每幀重新註冊一次。

## 解法
1. **時間放在框架外**：模組級 external store，提供 `getTime()`（純讀）、`setTime(t)`（只有播放控制器可寫）、`subscribe(cb)`。
2. **誰要時間就自己訂閱**，不要由父層用 props 一路傳：
   - 動畫迴圈（RAF／custom layer render）：直接 `getTime()` 同步讀。
   - 篩選、查表：節流訂閱（見 [03-03](03-03-subscription-granularity-and-throttle.md)）。
   - 跨日載入：只在日期變化時訂閱。
   - 顯示時間的文字：用框架的外部訂閱介面（React `useSyncExternalStore`；Vue `shallowRef` 搭配 `onMounted` 訂閱、`onUnmounted` 取消；Svelte 自訂 `readable` store）。
3. 圖層 hook／composable 的參數不收 `currentTime`；需要時間就在內部訂閱。
4. 播放控制器在 RAF 裡直接 `store.setTime()`，不走框架狀態；同值寫入直接略過，不通知。

```ts
// 框架無關的最小骨架
let t = Date.now() / 1000;
const subs = new Set<(t: number) => void>();
export const timeStore = {
  getTime: () => t,
  setTime(next: number) { if (next === t) return; t = next; subs.forEach((cb) => cb(t)); },
  subscribe(cb: (t: number) => void) { subs.add(cb); return () => subs.delete(cb); },
};
```

```tsx
// React：effect 依賴裡沒有 currentTime
useEffect(() => {
  const apply = (t: number) => map.setFilter(id, ["<=", ["get", "ts"], t]);
  apply(timeStore.getTime());
  return timeStore.subscribe(apply); // 高頻請改用節流訂閱，見 03-03
}, [id]);
```

## 怎麼偵測
- 通用：播放時 React Profiler／Vue Devtools 顯示根元件每秒重算數十次；暫停後立刻恢復順暢。
- 搜尋：
  - React：`useEffect\(.*\[[^\]]*(currentTime|time|now)[^\]]*\]`、`useMemo\(.*\[[^\]]*currentTime`、hook 簽名 `function use\w+\([^)]*currentTime`、`setCurrentTime\(` 出現在 `requestAnimationFrame` 回呼內。
  - Vue：`watch\(\s*(currentTime|time)`、`computed\(.*currentTime`、RAF 回呼內 `currentTime\.value\s*=`。
  - 純 JS：沒有框架問題，但要看 RAF 裡有沒有 `map.setData|innerHTML` 每幀重建。
- 驗收：全部圖層關閉並暫停 5 秒，render 次數應為 0；播放時根元件的 render 次數不應隨播放增加。

## 出處
- React 官方文件的 external store 與 `useSyncExternalStore`；Vue 官方文件的 `shallowRef`／外部狀態整合。
- 相關卡：[03-03](03-03-subscription-granularity-and-throttle.md)、[03-09](03-09-store-write-during-render.md)（render 階段寫入 store 的警告）。
- 實例：[mini-taiwan-pulse 時間 store](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/state/timeStore.ts)、[時間軸架構文件](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/TIMELINE_ARCHITECTURE.md)（「為什麼不放 React state」：每幀更新讓整顆 App 約 60 Hz 重繪，四層同開就卡）。

