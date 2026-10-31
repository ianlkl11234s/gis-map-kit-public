---
id: 12-01
title: 即時軌跡的時間戳差 ±8 小時：naive datetime、UTC 日界與上游時區錯
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Evaluated
stacks: [any]
tags: [timezone, UTC, naive-datetime, 時區, 日界, AIS, flight, earthquake, collector, backfill]
---

## 原則
軌跡類資料要對每個來源、每個欄位逐一確認時區，不套同一個假設；時間軸出問題時先查資料時間範圍，再改前端。通用的時區規則見 [01-13](../01-taiwan-apis/01-13-time-zone-and-update-time.md)。

## 症狀
- 時間軸回放載入上萬筆，畫面卻是 0 艘船；或「今天」出現比現在晚 8 小時的資料。
- 用「某一天」抓歷史航班只拿到約 2/3，凌晨到上午整段不見。
- 同一場地震在兩種報告裡時間剛好差 8 小時，join 不起來或被算成兩起。
- 從歸檔回填後，一種資料正常、另一種整批平移。

## 原因
1. 上游本身不一致：同一來源的不同報告類型，有的用 UTC、有的用本地時間。
2. 不同來源的歸檔欄位時區不同（例如船舶 AIS 是本地時間字串、航班是 UTC），回填時卻套同一個時區。
3. 以「日」抓取的 API 常以 UTC 日界切，等於本地時間 08:00 到隔天 08:00。

## 解法
1. 寫入帶時區、依本地日改用明確的 UTC 範圍、回填時逐來源標註時區、修正後整段重灌，做法都照 [01-13](../01-taiwan-apis/01-13-time-zone-and-update-time.md)。
2. 已知上游有時區錯的報告類型，計數與排名只用權威的那一類（例如正式地震目錄），不要拿另一類去重或補值。

## 怎麼偵測
- 通用：印出「資料時間 − 目前時間」的小時數；接近 ±8（或你的 UTC 偏移）就是時區問題，數小時不等則是資料缺漏。SQL：`max(ts) - now()` 不應大於 0。
- 通用：除錯順序是資料層 → API → 前端；確認資料時間範圍之前，不要先改前端時間軸。
- 搜尋（Python 抓取端）：`rg -n 'datetime\.now\(\)|datetime\.utcnow\(\)|fromtimestamp\([^,)]*\)$'`
- 搜尋（JS/TS）：`rg -n "new Date\(['\"][0-9]{4}-[0-9]{2}-[0-9]{2}[ T][0-9:]+['\"]\)"`（無時區字串會被當成瀏覽器本地時間）
- 搜尋（SQL schema）：`rg -n -i 'timestamp without time zone|\btimestamp\b(?! ?with)' --pcre2`
- 搜尋（依日期抓取）：`rg -n -- '--date|date=' scripts/`，確認是否被當成 UTC 日。

## 出處
- PostgreSQL 文件：Date/Time Types（`timestamptz` 的輸入解讀規則）。
- 相關卡：[01-13](../01-taiwan-apis/01-13-time-zone-and-update-time.md)（時區通用規則）、[03-04](../03-dynamics/03-04-data-time-vs-playback-time-vs-wall-clock.md)（資料時間、播放時間與掛鐘時間）。
- 實例：[gis-data-collectors 時區事故紀錄](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/.claude/pitfalls/2026-04-07-timezone-bug.md)、[修正 commit](https://github.com/ianlkl11234s/gis-data-collectors/commit/6e2e2d029206ad6e9cf313593b716f80a19c92a0)；[mini-taiwan-pulse 船舶航班空白事故](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/pitfalls/2026-04-07-empty-ships-flights.md)。

