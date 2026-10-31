---
id: 10-09
title: 排程的「今天」是哪一天：資料庫與雲端主機是 UTC，台北 00:00–08:00 會算錯
topic: 10-ops
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [時區, UTC, Asia/Taipei, current_date, cron, pg_cron, GitHub Actions, 日界, 排程]
---

## 原則
判斷「今天」一律明寫時區（Asia/Taipei），資料庫與雲端主機預設是 UTC；時間戳用 `timestamptz`，排程表達式先換算成 UTC。

## 症狀
- 台北凌晨到早上 8 點之間，「今天」的聚合資料永遠是空的。
- 每日排程在預期之外的時間跑（cron 以 UTC 解讀）。
- 回補資料時目標分區不存在而寫入失敗。

## 原因
本機是台北時區，資料庫 session 與雲端主機卻是 UTC；`current_date`、`new Date().toISOString().slice(0,10)` 取到的是 UTC 日。台北比 UTC 快 8 小時，所以台北 00:00–08:00 的「今天」在 UTC 還是昨天。

## 解法
1. 判斷「今天」一律明寫時區：`(now() AT TIME ZONE 'Asia/Taipei')::date`；程式端用明確時區的日期函式。
2. 寫入資料庫的時間一律帶時區，通用規則見 [01-13](../01-taiwan-apis/01-13-time-zone-and-update-time.md)。
3. 排程表達式要換算：GitHub Actions 的 `schedule` 是 UTC；pg_cron 依資料庫設定；先確認再寫。
4. 回補分區前，先建前一個 UTC 日的分區。
5. 顯示層統一用固定時區（見 [09-07](../09-design-system/09-07-loading-data-time-and-stale.md)）。
6. 時間戳 +8 小時類的資料問題見 [12-01](../12-domain-pitfalls/12-01-timestamp-timezone-offset.md)。

## 怎麼偵測
- 通用：台北早上 8 點前看「今天」的統計是空的；晚上才有。
- 搜尋：`current_date|CURRENT_DATE`（SQL）；`toISOString\(\)\.slice\(0, ?10\)|new Date\(\)\.toISOString`；Python `datetime\.now\(\)|utcnow\(\)` 無 tz；cron 字串旁沒有 UTC 註記（適用 stack：任何有排程或日聚合的架構）。

## 出處
- PostgreSQL 文件（`AT TIME ZONE`、`timestamptz`）；GitHub Actions 文件〈schedule〉為 UTC；pg_cron 說明（用前查）。

