---
id: 07-07
title: 後端預先彙總：慢查詢先分流成靜態快照、預彙總表、即時 RPC 三條路
topic: 07-performance
kind: decision
scope: public
evidence: Evaluated
stacks: [any]
tags: [預彙總, pre-aggregate, matview, RPC, 快照, CDN, cron, advisory lock, OOM, 索引, 併發排隊]
---

## 原則
慢查詢先依資料特性分流：靜態資料預匯出走 CDN，可預先算的時序或大表做預彙總表加薄 RPC，只有真動態的才走即時 RPC；改之前先用 `EXPLAIN` 量過。

## 症狀
- 時序或大表的查詢動輒數秒到逾時，使用者看到空白或轉圈。
- 多人同時開同一份靜態資料，資料庫連線被打滿。
- 預彙總的 refresh 本身把資料庫記憶體或磁碟 IO 吃爆。

## 原因
- 每次請求都對原始大表做 `GROUP BY`／排序，成本隨資料量成長。
- 靜態資料走 RPC：多人各自打同一份，資料庫讀取量是 O(人數)；前端若有全域併發上限，靜態請求還會擠到真動態資料的排隊。
- refresh 缺索引造成全表排序；today／yesterday 在同一個排程裡循序跑，自我重疊。

## 解法
先分類，再選路徑：

| 資料特性 | 路徑 |
|---|---|
| 月更或更慢、無參數、非時序 | 預匯出成靜態檔，走 CDN（O(1)） |
| 半動態、共享快照 | 物件儲存快照＋指標檔 |
| 時序或大表、可預先算 | **預彙總表**＋薄 RPC |
| 真動態、參數多 | RPC，但要有逾時、範圍上限（見 [07-08](07-08-public-rpc-timeout-clamp-rowcap.md)） |

預彙總表做法：
1. 先 `EXPLAIN (ANALYZE, BUFFERS)` 確認是 plan 問題還是資料量，先量再改（見 [07-01](07-01-performance-budget-and-measurement.md)）。觸發門檻例：RPC 超過 1 秒或超過 1 萬列。
2. 用**普通表**（不是 materialized view，一次重建會爆排序），主鍵＝（日期, key）。
3. 每日 refresh 函式：先取 advisory lock，再 DELETE＋INSERT 一天，避免與手動執行撞唯一鍵。
4. 排程：今天的資料每 N 分鐘（分鐘錯開），昨天的每日一次，拆成兩個 job；另有清理 job。排程內的日期用業務時區，不用資料庫 session 的 `current_date`（UTC 下會漏一天）。
5. OOM 守則：WHERE／ORDER BY 必有對應索引；聚合用 `MAX` 不用 `mode()`；必要時調高 `work_mem`；避免 job 互相重疊。
6. 前端 RPC 變成薄查詢，簽名不變，前端零改動。refresh 與清理函式是內部函式，**不要對前端角色開放**（見 [10-23](../10-ops/10-23-database-public-exposure-tables-functions.md)）。

Supabase／PostgREST 專用細節：函式要明寫 `SET statement_timeout`（pooler 會覆寫連線層設定）、改簽名後 `NOTIFY pgrst, 'reload schema'`。

## 怎麼偵測
- 通用：某 RPC 回應時間隨資料量成長；同一份靜態資料每個使用者都打一次資料庫。
- 搜尋：`rpc\(['"]get_.*_(day|frames|snapshots)` 的函式內有 `GROUP BY` 直接掃大表；`cron\.schedule` 裡出現 `current_date`（適用 stack：Postgres＋任何前端）。

## 出處
- PostgreSQL EXPLAIN、pg_cron、advisory lock 文件。
- 相關卡：[07-01](07-01-performance-budget-and-measurement.md)、[07-08](07-08-public-rpc-timeout-clamp-rowcap.md)、[10-10](../10-ops/10-10-cron-overlap-advisory-lock.md)（排程自我重疊與監控本身就是負載）。
- 實例：[mini-taiwan-pulse 預彙總指南](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/supabase-optimization.md)；[gis-data-collectors 預彙總 SQL 範本](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/sql/matview_disaster_alerts.sql)（同目錄另有國道壅塞、船舶軌跡等）。

