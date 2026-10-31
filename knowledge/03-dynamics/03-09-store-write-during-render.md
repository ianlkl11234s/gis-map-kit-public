---
id: 03-09
title: 在 render 階段寫入被訂閱的 store：警告只在 remount／HMR 時才出現
topic: 03-dynamics
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [React, render, useSyncExternalStore, StrictMode, HMR, 副作用, store write, 警告, remount, useEffect]
---

## 原則
render 階段（元件或 hook 本體，含裸 `if`）不寫入任何被訂閱的 store；所有寫入都放進 effect、事件處理器、async 回呼或 RAF。

## 症狀
Console 出現「Cannot update a component (A) while rendering a different component (B)」。乾淨載入時看不到，開了 StrictMode、HMR 熱更新或元件 remount 後才穩定出現，因此容易在驗收時漏掉。

## 原因
在元件或 hook 的 render body 裡直接呼叫 store 的寫入（例如初始化時 `timeStore.setTime(...)`）。若該 store 同時被 `useSyncExternalStore` 之類的機制訂閱，寫入會在 render 期間同步通知訂閱者，等於「渲染 B 時更新 A」。Vue 對應情境是在 `computed` 或 template 表達式裡寫外部 store。

## 解法
1. 所有 store 寫入都搬進 `useEffect`（Vue：`onMounted`／`watch`）；一次性初始化用 `useRef` guard 或 `useState` 的 lazy initializer。
2. 用結構判斷，不必重現警告：「render 階段是否呼叫任何 `*Store.set*`／`emit`」，只要該 store 被訂閱就算違規。
3. 全專案盤點時，列出所有 store 的所有寫入呼叫點，逐一確認落在 effect、事件處理器、async 回呼或 RAF，而不是 render。

```tsx
// 錯：render 期間寫 store
function useTimeline() { if (!inited) { timeStore.setTime(start); } }
// 對：掛載後寫
useEffect(() => { timeStore.setTime(start); }, []);
```

## 怎麼偵測
- 通用：用 StrictMode 與 HMR 各跑一遍，開 Console 看有無上述警告；只看第一次載入不夠。
- 搜尋（React）：在函式元件／`use\w+` 的函式本體（非 `useEffect`、事件處理器、`async`）內出現 `\w+Store\.(set|emit|push|update)\w*\(`；ESLint 可自訂規則掃描。
- 搜尋（Vue）：`computed\(\(\) => \{[^}]*Store\.set`。純 JS 沒有 render 階段，不適用。

## 出處
- React 官方文件：`useSyncExternalStore`、「在 render 中更新其他元件」警告說明。相關卡：[03-02](03-02-time-in-reactive-state-rerender-storm.md)。
- 實例：[mini-taiwan-pulse 時間軸 hook](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/hooks/useTimeline.ts)（初始化時間寫入曾在 render 階段，後改為 effect）。

