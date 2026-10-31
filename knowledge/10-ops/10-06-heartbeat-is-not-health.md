---
id: 10-06
title: 心跳不等於健康：「有跑」「解析成功」「有新資料」是三個問題；0 筆要用 ledger 或第二來源判斷
topic: 10-ops
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [心跳, 健康檢查, 靜默斷供, ledger, 0 筆, 新鮮度, collector, last_success, 監控]
---

## 原則
把「有執行」「解析成功」「資料內有新東西」分開記錄與監控；0 筆要用 ledger、第二來源或反證判斷是無事還是斷供，並且逐來源監控。

## 症狀
- 程序在跑、HTTP 回 200、沒有 exception、沒有告警，圖層卻悄悄停在幾天前，拖數天到數月才被發現。
- 狀態表一直顯示「連續錯誤 0」，因為失敗發生在寫心跳之前。
- 最後錯誤訊息停在很久以前一件無關的事，把人導向錯的方向。
- 事件型資料（地震、落雷、空襲警報）0 筆常是合法結果，用「超過 N 分鐘沒新資料」告警只會產生沒人理的噪音。

## 原因
- 心跳只在「有資料寫入」時更新：寫入函式遇到 0 筆就提早 return，`last_success_at` 停在最後一次有資料的時刻；或抓取本身失敗時根本沒寫心跳。
- 多個來源共用一張表時，一個壞掉的來源被其他來源的新資料蓋過去。
- 把「有沒有執行」「有沒有解析成功」「資料裡有沒有新東西」混成一個狀態。

## 解法
1. **三件事分開記**（每次抓取都寫一行 log 或一列紀錄）：執行時間、HTTP／解析結果、筆數、**資料內最新時間**。
2. 判斷「0 筆是沒事還是斷供」，依可靠度排序：
   - **Ledger 表**：每個處理單位（每輪、每檔）一定寫一列，`extracted = 0` 是合法值，`max(run_at)` 才是真心跳。
   - **第二資料源交叉驗證**：同一現象兩個來源，一邊有一邊沒有就現形。
   - **第三方訊號反證**：同一時間其他資料顯示「應該有事」（例如豪雨特報同日、落雷來源卻空白）。
   - **歸檔檔案大小**：連續好幾天大小完全相同，可定出停供起點（要抽樣下載確認內容）。
3. 監控要**逐來源**，不要只看「全部 collector 的最大值」（只要一支還在寫，其他停擺都不告警）。
4. 失敗（連抓取本身都沒成功）也要寫心跳，並記錯誤類別；成功時清掉舊的 `last_error`。
5. 前端同步顯示「資料時間」與過期狀態（見 [09-07](../09-design-system/09-07-loading-data-time-and-stale.md)）；事件型資料的過期判定不同（見 [09-07](../09-design-system/09-07-loading-data-time-and-stale.md) 解法 5）。
6. 原型版：每次抓取 log 四欄（抓取時間、HTTP 狀態、筆數、資料內最新時間），畫最近 7 次筆數。

## 怎麼偵測
- 通用：資料表最新一筆的觀測時間遠早於現在，而監控沒報；監控只有 `last_success`；0 筆回應沒有區分「無事件」與「斷供」。
- 搜尋：寫入函式內 `if not records: return` 在更新心跳之前；`last_success|heartbeat` 只在 success 分支更新；監控 SQL 只用 `max(last_success_at)` 而無 `GROUP BY` 來源；缺 `observed_at|data_time` 欄位（適用 stack：任何有 collector 的架構）。

## 出處
- 無官方標準，屬工程實務。相關卡：[10-07](10-07-deadman-switch-outside-monitored-system.md)（死人開關要放在被監控系統之外）、[01-10](../01-taiwan-apis/01-10-realtime-api-has-no-history.md)（即時 API 只給現在）、[12-16](../12-domain-pitfalls/12-16-event-feed-silent-outage.md)（事件 feed 靜默斷供）。
- 實例：[silent-upstream-outage（多個 collector 靜默斷供數週，同日查出）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/.claude/pitfalls/2026-08-07-silent-upstream-outage.md)、[news-llm-all-or-nothing（資料停寫但連續錯誤計數仍為 0）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/.claude/pitfalls/2026-10-21-news-llm-all-or-nothing.md)、[docs/handbook/operations.md](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/handbook/operations.md)。
