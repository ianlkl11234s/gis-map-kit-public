---
id: 06-11
title: ID 只在某個範圍內唯一：StationID 跨縣市撞號，join 前先驗 key
topic: 06-data-formats
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [ID, 主鍵, 撞號, StationID, StationUID, 複合鍵, 前導零, join, count distinct, 重編號]
---

## 原則
join 或合併多個縣市、系統的資料前，先用 `count(*)` 對 `count(distinct key)` 驗證 ID 的唯一範圍；不唯一就改用全域唯一欄位或含範圍的複合鍵，代碼一律當字串。

## 症狀
- 公車站牌、軌道車站跨縣市／跨系統合併後，popup 內容張冠李戴，或站名對錯城市。
- join 後筆數暴增或少一些。
- 村里代碼、行政區碼的前導零不見，對不到邊界。
- 某實體「消失」，其實是被重新編號。

## 原因
- 來源系統的 ID 只在**城市內**或**系統內**唯一（公車 StationID 在不同縣市會重複；台鐵與高鐵站號可相同），全域唯一的是另一個欄位（如 UID）或複合鍵。
- 代碼被當數字處理，前導零掉了。
- 同一實體疊在多張表或多個時間版本，同 ID 出現多列。

## 解法
1. **join 前先驗**：`count(*)` 對 `count(distinct key)`；不等就找出範圍欄位。
2. 用全域唯一欄位（UID），或組複合鍵：`(city, id)`、`(system, id)`；程式裡用同一函式組 key，不要各處手寫。
3. 代碼欄一律當字串，不做數值轉換。
4. 注意「欄位名看似範圍」與實際不符（例如 CityCode 與實際位置所屬城市不一致），以位置所屬欄位為準。
5. 跨期 join 要確認 ID 是否被重編號，不能把「消失」直接解讀成「被移除」。
6. 前端用 Map 存 feature 時，key 也要含範圍，否則後寫蓋前寫。

## 怎麼偵測
- 通用：合併多個縣市／系統的資料後，id 出現重複；feature-state 或 popup 只在某些城市對。
- 搜尋：`new Map\(.*\)` 以單一 id 當 key 並載入多縣市資料；`feature-state` 的 `id: .*\.(StationID|station_id)`；SQL `GROUP BY (station_id|StationID)\b` 缺少範圍欄位（適用 stack：any）。

## 出處
- 一般建議：複合鍵與唯一性檢查。
- 相關卡：[06-07](06-07-ratio-denominator-and-double-counting.md)、[12-06](../12-domain-pitfalls/12-06-mmsi-not-unique-identity.md)（MMSI 不是唯一身分）。
- 實例：[mini-taiwan-pulse 模擬面板規劃（要求確認公車 StationID 是否跨城市撞號，並改用 StationUID）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/simulation/PLAN.md)。

