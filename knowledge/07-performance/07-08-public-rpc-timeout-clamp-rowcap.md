---
id: 07-08
title: 對外 RPC 的三個守門：逾時有層級、範圍要 clamp、列數上限會靜默截斷
topic: 07-performance
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [statement_timeout, clamp, PostgREST, 20000, 206, content-range, 靜默截斷]
---

## 原則
每個對外函式都要明寫逾時、在函式內 clamp 時間範圍與筆數（權限見 [10-23](../10-ops/10-23-database-public-exposure-tables-functions.md)），並讓前端對列數上限零容忍。

## 症狀
- 大查詢在 3 秒被砍，前端拿到空結果。
- 資料只有一部分，筆數剛好是 20,000：某些站消失、只剩排序在前的區域（例如北部有資料、南部只剩一站）。
- 少數並發請求就能讓共用資料庫變慢。

## 原因
1. **逾時有多層**：連線池（pooler）、角色預設、函式屬性各有設定，彼此覆寫。在 session 設 `statement_timeout=0` 對 pooler 連線無效；函式屬性上的長逾時又會蓋過匿名角色的短預設。
2. **範圍沒有上限**：前端只會請求最近 24 小時，後端卻允許任意範圍；帶長逾時時就是拖垮資料庫的入口。
3. **REST 層列數硬上限**：PostgREST 預設最大 20,000 列，超過以 HTTP 206 加 `content-range` 靜默截斷，沒有錯誤，客戶端 Range 標頭也覆寫不了。

## 解法
1. 每個對外函式**明寫** `SET statement_timeout`（一般薄查詢約 30 秒，大 payload 才放寬到約 60 秒；cron 內部函式不經 pooler 可為 0），並**同時**在函式內 clamp 時間範圍與筆數。
2. clamp 上限：盤點前端實際最大請求，設約其 2 倍（例：25 小時→48 小時）；**超出就縮回上限、不報錯**，避免前端因此壞掉。
3. 診斷「資料少一半」：(a) 直接對資料庫 `SELECT count(*)` 該函式；(b) `curl -D -` 看 `content-range`；(c) 看到 `0-19999/N` 就是命中上限。解法是降頻（時序抽樣）、分批（依區域或時間）、或改成 grouped JSONB／預彙總（見 [07-07](07-07-backend-preaggregate-and-data-path-triage.md)）；不要靠加 `limit` 賭。前端在筆數等於已知上限時標「疑似截斷」（見 [01-09](../01-taiwan-apis/01-09-http-200-not-success-and-pagination.md)）。
4. 權限（誰能呼叫、預設權限、既有函式怎麼收回）見 [10-23](../10-ops/10-23-database-public-exposure-tables-functions.md)。

## 怎麼偵測
- 通用：資料筆數是整數上限；回應 206；函式逾時設定大於匿名預設卻沒有範圍參數 clamp。
- 搜尋：`SET statement_timeout`（超過匿名預設）所在函式缺少 `LEAST\(|GREATEST\(|LIMIT`；`ORDER BY station_id` 的大集合 RPC（適用 stack：Supabase／PostgREST；其他框架概念通用）。

## 出處
- PostgREST `db-max-rows`。
- 相關卡：[01-09](../01-taiwan-apis/01-09-http-200-not-success-and-pagination.md)、[07-07](07-07-backend-preaggregate-and-data-path-triage.md)、[10-23](../10-ops/10-23-database-public-exposure-tables-functions.md)。
- 實例：[mini-taiwan-pulse 資料庫優化指南（逾時與列數上限的關鍵坑）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/supabase-optimization.md)。

