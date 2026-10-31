---
id: 07-01
title: 先量再改：效能預算與量測方法（推測不等於實測，TypedArray 不在 JS heap）
topic: 07-performance
kind: pattern
scope: public
evidence: Evaluated
stacks: [any]
tags: [效能預算, 量測, DevTools, performance.now, 閒置, render 次數, 記憶體, backingStorage, DPR, A/B]
---

## 原則
先訂可自動量的預算，優化前後都用同一套量測對照；沒有前後數字的優化與「很慢」的結論都不算數。

## 症狀
- 花了半天優化，畫面沒有變順。
- 審查報告標出「很慢」的項目，實測其實很快。
- 規則寫在文件裡，三個月後仍有大量圖層違反。
- 記憶體量測看不到大陣列的成長。

## 原因
- 憑直覺或類比優化常打在錯的地方；推測不是量測。
- 規則文字不會自己執行；沒有量測腳本就沒有回饋。
- 常見量測工具有盲點：JS heap 指標看不到 TypedArray（backing store 在外部記憶體）；Resource Timing 只留有限筆數；GPU「忙碌 %」與每段程式耗時不是同一個量。
- 高 DPR 的 framebuffer 本身就吃掉大量 GPU 記憶體，與資料量無關。

## 解法
1. **訂預算**：例如首屏下載量、首屏 JS、全部圖層關閉並暫停時 5 秒內 render 次數＝0、拖曳單幀耗時、穩態記憶體。預算要能自動量，不是口號。
2. **先量再改**：在更新迴圈各段包 `performance.now()`；用 Performance 面板錄「什麼都不做」5 秒；Network 面板看首屏總量。用 A/B 開關（調 DPR、關地形、關單一圖層）縮小範圍，比憑感覺準。
3. **估算要標「估算」**：用類比推出的數字（例如「類似的圖層應該省八成」）在實測後更正。
4. **量記憶體用對指標**：`Runtime.getHeapUsage().backingStorageSize` 與 renderer 行程的 footprint，不要只看 `usedJSHeapSize`。測試腳本先分配已知大小的 TypedArray，驗證量測手段看得到。
5. **DPR 上限當效能旋鈕前，先量它有沒有用**：實測像素增加約 3.5 倍、幀率只掉約 10%，代表瓶頸在頂點而非 fill-rate，降 DPR 換不到什麼。它還有副作用：有些函式庫沒有 pixelRatio 選項，只能覆寫全域 `devicePixelRatio`，會連帶讓其他 canvas（如 three.js）變糊、1 px 線變粗；截圖式視覺回歸的基準也要同時記錄 DPR。要降階時，優先給使用者自選的開關（例如立體效果預設關，見 [09-10](../09-design-system/09-10-map-symbol-size-tiers.md)），比偷偷降畫質可預期。
6. **一次只修一個根因**：同一症狀可能有兩個無關根因，修好一個、驗證指標，再查下一個。量測腳本放進 repo，改完用同一套對照。

## 怎麼偵測
- 通用：優化 PR 沒有前後數字；量測只用單一指標；「很慢」的結論沒有計時證據。
- 搜尋：`performance\.now\(\)|console\.time` 在效能相關程式碼中缺席；`usedJSHeapSize` 被當成唯一記憶體指標（適用 stack：any）。

## 出處
- Chrome DevTools Performance／Memory 面板說明。
- 相關卡：[04-15](../04-effects-catalog/04-15-animation-repaint-budget.md)（全關暫停 5 秒 render＝0 的驗收）、[07-09](07-09-bundle-size-lazy-load-on-demand.md)（首屏 JS 按需載入）。
- 實例：[mini-taiwan-pulse 效能稽核（含 DPR 與像素量測）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/audit/perf-audit-2026-09-30.md)。

