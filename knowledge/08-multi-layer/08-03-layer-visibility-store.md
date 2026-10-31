---
id: 08-03
title: 圖層開關狀態：細粒度訂閱的 store，預設全關，快照 identity 只在真的變動時換
topic: 08-multi-layer
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [圖層開關, visibility, store, useSyncExternalStore, 訂閱, identity, 預設狀態, 全部關閉, 狀態管理]
---

## 原則
圖層開關放在模組級 store 並支援 per-key 訂閱，snapshot identity 只在真的變動時才換，預設全關。

## 症狀
- 任何一個圖層切換，整個 App 重新渲染；圖層一多，開關就卡。
- 呼叫 `setVisibility({...prev})` 值沒變，仍造成一次空轉渲染。
- 進站就自動開了一堆圖層，首屏載入很慢，或使用者找不到哪個是自己開的。
- 「全部關閉」在多國家／多面板時，關掉了使用者沒預期的東西。

## 原因
把「全部圖層開關」放成一個大物件進根元件的 state，任何一個 key 變動都換掉整個物件。

## 解法
1. **圖層開關放在模組級 store**（不是根元件 state），提供 `getVisibility(key)`、`getSnapshot()`、`set(key, bool)` 或批次變更、`subscribe(cb)`、**per-key 訂閱**。snapshot 的 identity 只在真的有 key 變動時才換、才通知：這是 `useSyncExternalStore` 的硬性要求（getSnapshot 每次回傳新物件會無限迴圈），也消滅空轉渲染。通知順序固定：先換 snapshot，再通知；先 per-key、後 global，global 只發一次。
2. **key 全集從登記簿派生**（見 [08-01](08-01-layer-registry-single-source.md)），新增圖層不用改 store。元件只訂閱自己關心的 key（`useLayerVisible(key)`），不要讀整包再自己挑。
3. **預設全關**：進站不自動開任何圖層；只有「預設開啟」需要明確的產品決定。換視角（例如移動到另一個國家）只改鏡頭，不改圖層狀態。
4. **地圖 `load` 完成前停用圖層開關**；建立圖層時讀開關的實際狀態（store 當下的值），不要假設預設值。否則使用者在地圖還沒好時打開開關，圖層沒建出來而狀態顯示已開，畫面卡在「載入中」。
5. **「全部關閉」的範圍要寫進規則**：有多個面板／國家時，只關「目前面板」的圖層，並用測試固定這個範圍。
6. **過渡期**：舊程式還在用 `[state, setState]` 時，先用「橋接 hook」讓舊呼叫點不改仍讀寫同一個 store，再逐步改成直接訂閱，不要一次改完。

```tsx
// React：只訂閱自己的 key
const visible = useSyncExternalStore(
  (cb) => layerStore.subscribeKey(key, cb),
  () => layerStore.getVisibility(key),
);
```
Vue 可用 `shallowRef` 搭配 per-key 訂閱；純 JS 直接 `subscribeKey`。

## 怎麼偵測
- 通用：用 Profiler 切一個圖層，看有幾個元件重新渲染（應只有該圖層相關者）；進站時看是否自動開了圖層。
- 搜尋：
  - 大物件：`useState<Record<string, boolean>>\(|ref<Record<string, boolean>>\(`（React、Vue）。
  - 無條件換 identity：setter 內 `return \{ ?\.\.\.prev` 沒有先比較（React）。
  - 預設開啟：`DEFAULT_ON|defaultVisible|initialLayers` 的集合非空，且無備註決策來源（any）。

## 出處
- React 官方文件：`useSyncExternalStore` 對 snapshot 穩定性的要求。
- 相關卡：[08-10](08-10-multi-country-country-selector-no-cross-mix.md)（多國化的國家選單與全部關閉範圍）。
- 實例：[src/state/layerVisibilityStore.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/state/layerVisibilityStore.ts)、[layerConsistency.test.ts（全部關閉範圍測試）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/sidebar/__tests__/layerConsistency.test.ts)。
