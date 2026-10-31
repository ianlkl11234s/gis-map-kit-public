---
id: 12-15
title: 同一場地震有多份報告：正式目錄、顯著報告、地方報告與初報修訂不能混算或等值 join
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Evaluated
stacks: [any]
tags: [earthquake, 地震, catalog, report type, 初報, 修訂, join, dedup, event_id, 震度, USGS]
---

## 原則
地震件數、排名與規模只用正式目錄（catalog）這一類報告；其他報告類型不混算，跨表配對用時間窗而不是等值 join。

## 症狀
- 地震件數比官方多，排名第一的「最大地震」其實是同一場地震的另一份報告。
- 地震事件表與鄉鎮震度表等值 join 後，某些地震的震度資料「消失」。
- 依月份統計時，最近一個月看起來地震很少。
- 地震回放清單以為會自動累積歷史，結果上線前的事件永遠補不回來。
- 地圖上的誤導：重複的震央點疊在一起像餘震群；少算的月份看起來「地震變少了」。

## 原因
1. 同一來源提供多種報告：正式目錄（規模、時間經修正）、顯著有感報告、地方性報告；後兩者有一部分和目錄重複，且規模下限不同。
2. 初報與修訂報的發震時間、規模、位置可能不同（例如時間差 1 秒），用時間當 join 鍵會對不上。
3. 不同報告類型的更新進度不同：目錄可能只更新到上個月，報告類已到本月下旬。
4. 有些上游端點只保留最近 N 筆或只留最新一次快照，沒有自己存檔就無法回補。
5. 上游編號欄位可能是常數（每筆一樣），不能單獨當去重鍵。

## 解法
1. 件數、排名、規模分析一律只用權威的正式目錄；其他報告只用來補「目錄還沒涵蓋的時段」，並明寫來源。
2. 跨表配對用時間窗取最近者（例如 ±5 秒），窗不要開太大，以免誤配到短時間內的另一起地震；回傳實際配到的鍵讓下游可驗證。
3. 時間欄若是 UTC，依本地日或月彙總前先轉時區（見 [12-01](12-01-timestamp-timezone-offset.md)）。
4. 依月份比較前，先查各報告類型的最晚時間，避免拿未涵蓋的月份比較。
5. 只保留最新快照的上游，要自己排程輪詢存檔；去重鍵用「編號＋完整時間」之類的組合，並固定格式不再更改，否則會產生重複。

## 怎麼偵測
- 通用：`group by report_type` 看各類筆數與最晚時間；任何計數 SQL 沒有過濾報告類型就要檢查。
- 通用：把事件表與震度表做時間窗 join，統計「有事件但沒配到震度」的比例。
- 搜尋：`rg -n -i 'report_type|catalog' ` 對照地震相關查詢；`rg -n -i 'join .* on .*(origin_time|occurred_at) *='` 找時間等值 join。
- 搜尋（去重鍵）：`rg -n -i 'EarthquakeNo|event_id' ` 在地震 collector，確認不是單用上游編號。

## 出處
- USGS ComCat 文件：事件可有多個來源的 origin，偏好的 origin 會隨修訂改變。相關卡：[12-01](12-01-timestamp-timezone-offset.md)。
- 實例：[全球氣候改版紀錄：USGS feed 改 all_day 修漏抓空洞](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/global-climate/changelog.md)；[事件紀錄：事件與震度差 1 秒，改 ±5 秒時間窗；源頭只留最新快照無法回補](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)；[去重 key 改為「編號＋完整時間」（上游編號為常數）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/collectors/earthquake_common.py)；[event_id 格式不可更改的註記](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/collectors/earthquake_catalog.py)。

