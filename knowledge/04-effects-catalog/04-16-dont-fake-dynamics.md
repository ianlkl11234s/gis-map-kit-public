---
id: 04-16
title: 不假造動態：資料不夠時，不要補出一個看起來合理的動畫
topic: 04-effects-catalog
kind: decision
scope: public
evidence: Observed
stacks: [any]
tags: [假動態, 插值, 外推, 缺測, 推估, 模擬, 資料誠實, Change, Flow, Propagation, Scenario]
---

## 原則
資料撐不起來的動態就不要做：缺測不補 0、不外推，不補中間期，OD 表不畫成沿線移動，模型推估必須與觀測分開標示；資料不足時降階成靜態分級圖。

## 症狀
動畫流暢好看，但內容是編出來的：車輛在斷訊期間「照常行駛」、兩期資料之間「平滑過渡」出不存在的中間年份、OD 表被畫成車沿直線跑、模型推估的擴散被當成觀測。

## 原因
動畫天生帶有「這是真的在發生」的暗示。缺測補 0、外推、曲線平滑、模型假設都會被視覺放大成事實。

## 解法
先判斷動態屬於哪一種路徑，再套對應規則：

| 路徑 | 問題 | MVP（不用動畫） | 不要做 |
|---|---|---|---|
| Change（狀態增減） | 哪裡變多變少 | 兩期切換或差值圖 | 兩期資料不補中間年份；口徑不同的期別不放同一 slider；缺整期畫「此期無資料」，不用 0 或上一期代替 |
| Flow（移動與流量） | 往哪走、哪條最忙 | 軌跡依時間上色、OD 線粗細 | 相鄰點間隔超過門檻不畫實線（切段或虛線＋「推測」）；OD 表不做沿線移動；時刻表不用曲線平滑；插值不外推 |
| Propagation（傳遞） | 影響怎麼傳 | 依抵達時間或距離分級著色 | 沒有傳遞規則也沒有觀測抵達時間就不做擴散動畫；規則算出的抵達時間，圖例要寫規則與參數；缺機制模型的傳遞不做或標弱版 |
| Scenario（如果…） | 條件改變會怎樣 | select 切換預先算好的情境 | 不在瀏覽器跑模型；情境圖例含「推估／模擬」；不做連續 slider（除非每格已預先算好） |

通用做法：
- 畫面顯示**資料時間**，不是抓取時間；Live 模式沒有即時來源就隱藏，不要拿舊資料冒充。
- 缺測不補 0、不外推（見 [06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)）。
- 圖例分開寫「觀測」與「推估」。
- 動畫降階路徑：動畫 → 靜態分級圖；全格網 → 只畫測站。

## 怎麼偵測
- 通用：播放時所有物件持續移動但資料點其實稀疏；圖例沒有時間或推估說明；缺資料區顯示 0。
- 搜尋：插值函式沒有最大間隔檢查（`gap|maxGap|threshold`）；`?? 0|\|\| 0` 用在時序值上（any）。

## 出處
- 相關卡：[04-02](04-02-moving-objects-interpolation.md)、[04-05](04-05-od-great-circle-arcs.md)、[04-07](04-07-event-replay-scoped-clock.md)、[06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)。
- 實例：[mini-taiwan-pulse 公車設計文件](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/bus/design.md)（資料窗外不外推）；[flightTrails.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/flightTrails.ts)（航班 30 分鐘切段）。

