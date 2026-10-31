---
id: 10-07
title: 死人開關要放在被監控系統之外：程式死掉時，自己監控自己也一起死
topic: 10-ops
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [dead-man switch, 告警, 監控, pg_cron, watchdog, uptime, 外部巡檢, 單點]
---

## 原則
告警與存活檢查要放在被監控程式之外的元件（資料庫排程、外部排程、第三方 uptime），並逐來源檢查，不要讓程式自己監控自己。

## 症狀
- collector 卡死或整個進程掛掉，資料停寫十幾小時，沒有任何告警。
- 告警邏輯寫在 collector 裡，進程死了就沒人發通知。
- 外部定期打網址的 uptime 監測根本沒有，網站掛了要等使用者說。

## 原因
告警程式放在被監控的程式碼裡最方便，但它與被監控者同生共死。

## 解法
1. 回答一個問題：**被監控的程式整個死掉時，誰會發通知？** 答案若是它自己 → 不合格。
2. 把檢查放在**另一個還活著的元件**：例如資料庫排程（定時檢查 `max(last_success_at)`，超過門檻就用資料庫內建 HTTP 擴充或 webhook 發通知）；或外部免費排程（CI 的 schedule）每天打一次網址。
3. 進程內另外加 watchdog（主迴圈超過 N 秒沒心跳就自動重啟），屬輔助，不取代外部檢查。
4. 外部檢查要**逐來源**，不是全部的最大值（見 [10-06](10-06-heartbeat-is-not-health.md)）。
5. 對外服務加獨立的 uptime 監測（第三方定時請求），並對「回 200 但內容是 HTML 錯誤頁」做內容檢查。

## 怎麼偵測
- 通用：問「collector 主機整台關機，今天會不會有人收到通知？」；列出所有告警的發送者與被監控者是否同一個進程。
- 搜尋：告警發送函式只在 collector 程式碼內被呼叫，專案裡找不到 `cron|schedule|uptime|healthcheck` 之類外部排程（適用 stack：any）。

## 出處
- 一般監控設計（dead-man's switch / heartbeat monitoring）；Supabase pg_cron／pg_net 文件（用前查）。相關卡：[10-06](10-06-heartbeat-is-not-health.md)。
- 實例：[operations.md（collector watchdog 與告警運維）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/handbook/operations.md)。

