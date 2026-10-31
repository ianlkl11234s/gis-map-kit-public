---
id: 01-13
title: 時間欄位：+8 小時、UTC 日界、UpdateTime 不是變動時間
topic: 01-taiwan-apis
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [時區, UTC, +8, naive datetime, 日界, 民國年, LastUpdateTime, 時間軸]
---

## 原則
全程使用帶時區的時間，資料庫存 UTC、顯示時轉 Asia/Taipei；依「本地日」查詢時明寫 UTC 範圍；新鮮度看資料內的觀測時間，不看 `UpdateTime`。

## 症狀
- 最新資料出現在「未來」，時間軸今天是空的。
- 台北一整天只抓到約三分之二的資料。
- 跨日、跨月統計差一天。
- 用「更新時間」判斷有沒有新事件，結果幾乎都是新的。

## 原因
- 程式用沒有時區的 `datetime.now()`（台灣時間）寫進以 UTC 解讀的資料庫，差 8 小時。
- 台北的一天跨兩個 UTC 日。
- 上游標 UTC 實為本地時間；民國年月（如 `yyymm`）要換算。
- `UpdateTime` 類欄位多是快取刷新時間。

## 解法
1. 全程使用帶時區的時間；資料庫存 UTC，顯示時轉 Asia/Taipei。
2. 切日／切月界線先 +8 再切。依「本地日」查詢時明寫範圍：本地 D 日＝UTC `(D-1)T16:00Z` 到 `DT16:00Z`，不要只給日期參數（只給日期會被當 UTC 日，漏掉約三分之一）。
3. 回填歷史資料時，對每個來源的時間欄位逐一標註時區，不共用一個預設（同一批歸檔裡，有的欄位是本地時間字串、有的是 UTC，例如船舶 `+08:00`、航班 `+00:00`）；修好之後，偏移的歷史資料從原始歸檔整段重灌，不要在前端加 offset 遮掩。
4. 驗收三處時區：資料庫 session、collector、前端顯示；印出 `data_time − now`，差 ±8 小時就是時區問題。
5. 來源沒有時間戳時，使用收集時刻並標明。
6. 新鮮度用資料內的觀測時間（見 [01-10](01-10-realtime-api-has-no-history.md)）。

## 怎麼偵測
- 通用：資料時間比現在晚；跨日統計與官網對不上。
- 搜尋：`datetime\.now\(\)`（沒有 tz）、`new Date\(.*\)` 解析無時區字串（適用 stack：any）。

## 出處
- 一般建議：以帶時區時間存取、顯示時轉換為通用做法。
- 相關卡：[01-10](01-10-realtime-api-has-no-history.md)、[10-09](../10-ops/10-09-schedule-taipei-timezone.md)（排程的「今天」在 UTC 主機上於台北 00:00–08:00 會算錯）、[12-01](../12-domain-pitfalls/12-01-timestamp-timezone-offset.md)。
- 實例：[時區事故：船、航班圖層全空](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/pitfalls/2026-04-07-empty-ships-flights.md)、[collector 修正 commit](https://github.com/ianlkl11234s/gis-data-collectors/commit/6e2e2d029206ad6e9cf313593b716f80a19c92a0)。

