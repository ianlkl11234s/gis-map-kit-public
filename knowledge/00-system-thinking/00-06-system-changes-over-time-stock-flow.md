---
id: 00-06
title: 系統隨時間變化：Stock、Flow、State、Trigger、Delay、Feedback、Threshold
topic: 00-system-thinking
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [System Dynamics, stock, flow, state, trigger, delay, feedback, threshold, 動態圖台, 時間]
---

## 原則
動態圖台要先找出隨時間變化的是哪個量（Stock、Flow、Threshold），沒有時序證據就不畫迴圈、不補動畫，推估與實測要分開標示。

## 症狀
動態圖台只是把靜態資料做成時間滑桿；或在沒有證據的地方畫出「因為塞車所以改道又回頭加重塞車」的迴圈；或把容量瓶頸造成的非線性反應畫成線性。

## 原因
沒有區分七個動態概念，也不知道哪些是標準概念、哪些是教學分類。

| 概念 | 意思 | 來源性質 |
|---|---|---|
| Stock | 累積量（車上乘客數、積水量） | System Dynamics 標準概念 |
| Flow | 改變 Stock 的速率（上車、下車、逕流、排水） | 標準概念 |
| Feedback | 結果回頭改變原因（塞車促使改道，改變路網流量） | 標準概念（因果迴圈） |
| Delay | 因果之間的時間落差（上游下雨，下游不一定立即淹） | 標準概念 |
| Threshold | 容量或門檻使反應不線性 | 常見分析概念，非 SD 標準符號 |
| State | 描述當前運作情況的標籤（擁擠、暢通） | 教學上方便使用的分類 |
| Trigger | 引發變化的事件或輸入（豪雨） | 教學上方便使用的分類 |

## 解法
1. 找 Stock 與改變它的 Flow，能寫成式子就寫（下一站人數＝上一站＋上車−下車）。
2. 把 State 當成由 Stock 或門檻推出的標籤，並說明門檻；Trigger 標在起點。
3. 標出已知 Delay（單位與依據）；沒有依據就標 unknown，不假設即時。
4. Feedback 需要時序或行為證據才可畫成迴圈；沒有證據只能列為待驗證，不得無依據補迴圈。
5. 畫動態圖台時，要畫的是哪個量隨時間變：Stock 的變化、Flow 的方向與速率、跨過 Threshold 的瞬間、Trigger 事件點。資料粒度不足就不要補出看起來合理的動畫（見 [04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)）；時間軸的時鐘模型（全站或各圖層）見 [03-01](../03-dynamics/03-01-time-model-global-vs-scoped-clock.md)。
6. 實測、推估、模擬在動態上要分別標示，例如沒有上下車刷卡資料時，公車擁擠度只能是模型推估，不能說成實測。

## 怎麼偵測
檢查對象：圖台說明文字、system map JSON（node type 與 edge delay／polarity 欄位）、動態圖層設計文件。
- 通用：動畫比資料更平滑；時間軸上出現資料沒有的中間狀態；feedback 敘述沒有時序證據。
- 搜尋（JSON）：`delay` 全為空卻有「延遲」敘述；有 feedback loop 的 edge 但 `evidence_status` 是 hypothesized 卻畫成實線。
- 搜尋（文字）：`回饋|迴圈|惡性循環`沒有對應時序圖或數據；`即時`用於月或日更新資料。
- 僅在圖台有時間維度時適用。

## 出處
- Meadows (2008) Thinking in Systems（stock、flow、feedback、delay）。
- System Dynamics Glossary (2019), System Dynamics Review（CLD 因果箭頭、極性、延遲）。
- 內部交叉參考：[04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md) 不假造動態、[03-01](../03-dynamics/03-01-time-model-global-vs-scoped-clock.md) 時間模型。

