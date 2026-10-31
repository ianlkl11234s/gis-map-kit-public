---
id: 10-10
title: 排程自我重疊與監控本身就是負載：advisory lock、頻率×單次成本、錯開分鐘
topic: 10-ops
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [cron, pg_cron, advisory lock, 預聚合, 資料庫負載, Disk IO, 連線池, 錯開排程]
---

## 原則
每個 refresh／聚合函式用 advisory lock 防止自我重疊；新增 cron 前評估頻率乘單次成本，同頻的 job 錯開分鐘，監控查詢本身也要估成本。

## 症狀
- 一次加了多個高頻 refresh job，資料庫 Disk IO 衝到接近滿載、連線池耗盡，整台掛掉。
- 某個 job 執行時間超過間隔，開始自我重疊，單條卡住數小時。
- 監控用的 RPC 單次跑很久、掃描大量資料，本身成了負載大宗。

## 原因
預聚合讓前端變快，卻把負載移到背景；排程變多後互相疊加。每次重算「昨天不會變的資料」又浪費。

## 解法
1. refresh 函式開頭用 `pg_try_advisory_lock`，搶不到就跳過，避免重疊。
2. **高頻聚合三鐵則**：昨天的資料一天只算一次；單次執行超過間隔的 1/3 就降頻或改增量；同頻的 job 錯開分鐘。
3. 新增 cron 的 PR 要寫出：頻率、預估單次執行時間、鎖策略。
4. collector 首輪加隨機偏移；會撞期的固定在空檔分鐘。
5. 監控與健康檢查查詢也要估成本，不要全表掃。
6. 一次套用多個資料庫變更的流程見 [10-14](10-14-incident-response-and-db-change-sop.md)。

## 怎麼偵測
- 通用：`cron.job_run_details` 中同一 job 有時間重疊的執行；執行時間 > 間隔；DB CPU／IO 在整點或固定分鐘出現尖峰。
- 搜尋：`cron\.schedule\(` 多筆相同頻率（如 `\*/10`）；refresh 函式內缺 `pg_try_advisory_lock`；函式整段重算而沒有「只算今天」條件（適用 stack：PostgreSQL＋pg_cron）。

## 出處
- PostgreSQL 文件〈Explicit Locking: Advisory Locks〉。
- 實例：[INCIDENTS.md（多個高頻 refresh cron 疊加，Disk IO 飆高、連線池耗盡）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)、[disk-io-cron-spiral（cron 自我重疊與健康檢查掃表）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/.claude/pitfalls/2026-07-23-disk-io-cron-spiral.md)、[docs/supabase-optimization.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/supabase-optimization.md)。

