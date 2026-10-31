---
id: 07-03
title: 沒開任何圖層，地圖仍一直重畫：對隱藏圖層 setPaintProperty 會讓 transition 卡住
topic: 07-performance
kind: pitfall
scope: public
evidence: Observed
stacks: [mapbox-gl]
tags: [多圖層, 全關, 耗電, setPaintProperty, transition, hasTransitions, idle, 隱藏圖層, visibility none, 重畫, 風扇]
---

## 原則
不要對 `visibility: none` 的圖層呼叫 `setPaintProperty`；隱藏時暫存樣式，顯示時才寫入。全部圖層關閉並暫停後，render 次數必須歸零。

## 症狀
- 所有圖層關閉、時間軸暫停，`map.on('render')` 仍持續觸發，風扇不停。
- `map.style.hasTransitions()` 恆為 `true`。
- 堆疊顯示重畫來自地圖引擎內部排程，不是任何 custom layer 的 `triggerRepaint`。

## 原因
- 對一個圖層呼叫任何 `setPaintProperty`，引擎會為該圖層的**所有** paint 屬性建立 transition，不只被改的那一個。
- `visibility: none` 的圖層不會被重新計算，transition 永遠不會結束，`hasTransitions()` 恆真，地圖每幀都排程重畫，永遠不 idle。
- 只把被改的那個屬性 transition 設 0 擋不住。
- 常見觸發：圖層一掛載就把初始樣式寫進還沒顯示的圖層；圖層隱藏後仍有同步樣式的 effect 在改 paint；每幀改 paint 的漣漪、脈動動畫，在圖層被關掉的那一刻卡住。

## 解法
1. 對隱藏圖層不寫 paint：隱藏時把樣式暫存，重新顯示時才寫入（封裝成 `setPaintPropertyGuarded` 之類）。
2. 每幀都會改 paint 的圖層（漣漪、閃爍），把所有 paint 屬性的 transition 設 `duration: 0`。
3. 若不需要 GL 淡入，全域把 style 根層 transition 設為 0；「平滑」改由資料插值負責。
4. 「全部關閉」與逐一關閉走同一條程式路徑，避免殘留（多圖層開關情境見 [08-07](../08-multi-layer/08-07-new-layer-checklist.md)）。切換底圖（style 重新載入）後，暫存的 paint 要重新套用，並重新檢查 render 次數與 `hasTransitions()`。圖層關閉後仍在跑的計時器、輪詢、樣式寫入一併清掉。
5. 驗收：全關＋暫停 5 秒，render 次數＝0（見 [04-15](../04-effects-catalog/04-15-animation-repaint-budget.md)、[07-01](07-01-performance-budget-and-measurement.md)）。
6. 排查技巧：把疑似殘留的圖層暫時設 visible 再設回 none，若 render 立刻歸 0，就是這個問題。

## 怎麼偵測
- 通用：閒置時 GPU／CPU 不歸零；`hasTransitions()` 為 true。
- 搜尋：`setPaintProperty\(` 沒有前置 `getLayoutProperty\(.*visibility` 或 `visible` 判斷（適用 stack：mapbox-gl；maplibre 行為相近但未驗證）。
- 搜尋：動畫圖層（含 `requestAnimationFrame`）每幀 `setPaintProperty`；圖層 add 完成後立刻 `setPaintProperty` 初始化，而圖層預設 `visibility: 'none'`。
- Leaflet、OpenLayers 沒有這種 paint transition 機制，不適用。

## 出處
- 引擎行為屬實作細節，以實測為準。
- 相關卡：[04-15](../04-effects-catalog/04-15-animation-repaint-budget.md)、[07-01](07-01-performance-budget-and-measurement.md)、[08-07](../08-multi-layer/08-07-new-layer-checklist.md)。
- 實例：[mini-taiwan-pulse 事故紀錄](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/pitfalls/2026-09-30-hidden-layer-paint-transition.md)（修復前 5 秒 render 20–29 次，修復後 0 次）、[效能稽核](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/audit/perf-audit-2026-09-30.md)。
