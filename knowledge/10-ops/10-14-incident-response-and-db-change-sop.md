---
id: 10-14
title: 事故處置與資料庫變更 SOP：先止血、先留證據、逐項套用並跑健康檢查
topic: 10-ops
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [事故, 止血, 連線池, pg_stat, migration, 健康檢查, 回滾, 餐期, 變更管理]
---

## 原則
出事先切斷最大來源並在統計歸零前留下證據；資料庫變更逐項套用，每項之後跑同一支健康檢查，有異常就停下並回滾。

## 症狀
- 資料庫連線池被佔滿；直覺是馬上重啟，統計歸零、證據消失。
- 一晚上套了多個 migration，出事時分不清是哪一個造成。
- 把 QueryCanceled 當成斷線，往錯的方向處理。

## 原因
出事時急著恢復；變更一次整包套用；沒有基準值可比。

## 解法
**事故**
1. 先切斷最大來源（停用該 collector、終止佔鎖連線；**正式環境操作要人工同意**）。
2. 在統計歸零前 dump `pg_stat_*`（io、activity、statements）。
3. 區分壅塞與斷線（逾時取消不是斷線）。
4. 唯讀調查 → 寫事故長文（時間線、根因、處置、回滾）。
5. 原始資料若仍在本地，確認不會遺失。

**資料庫變更**
1. 開始前跑一次健康檢查留基準（失敗的 cron、各狀態次數、collector 連續錯誤或超過 3 倍間隔未成功）。
2. 依相依順序**一項一項**套用，每項之後跑同一支健康檢查；有新異常就停在那一項，執行該變更檔頭寫的回滾。
3. 重負載操作避開台灣餐期 10:00–20:00。
4. 全部完成後存一份累計快照（記錄時間與重啟時間），約一週後同口徑複量。
5. 沒變就不寫：內容 hash 或 `IS DISTINCT FROM` 擋掉無變化的 UPDATE。

**部署後 smoke**：見 [10-05](10-05-local-vs-production-differences.md)。

## 怎麼偵測
- 通用：變更 PR 沒有回滾段落、沒有健康檢查；事故沒有留下 `pg_stat` 快照。
- 搜尋：migration 檔頭缺 `rollback|回滾` 註解；無「沒變不寫」的高頻 UPSERT（`ON CONFLICT .* DO UPDATE` 沒有 `WHERE .* IS DISTINCT FROM`）（適用 stack：PostgreSQL）。

## 出處
- PostgreSQL 統計檢視（pg_stat_io、pg_stat_activity）文件。
- 實例：[operations.md（連線池被佔滿的事故紀錄）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/handbook/operations.md)。

