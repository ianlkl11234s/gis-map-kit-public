---
id: 12-17
title: 事件圖層用「排序＋固定筆數上限」查詢，表一長畫面就凍結在舊資料或只露出一小段
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Evaluated
stacks: [any]
tags: [limit, order by, time window, 颱風, 地震, event layer, 時間軸, query, PostgREST]
---

## 原則
事件圖層的查詢以時間窗為主條件，`limit` 只當安全上限並在命中時警告；寫入地圖 source 遇到樣式未就緒要重試，不能略過。

## 症狀
- 颱風路徑圖層上線時正常，幾個月後永遠只顯示最早那幾個颱風。
- 全球地震圖層只顯示最近十幾天，資料庫明明有一個多月。
- 切換回溯天數變大時，約一半的點消失，沒有錯誤。
- 地圖上的誤導：使用者以為「最近沒有颱風」或「地震只集中在最近幾天」；時間分布被查詢上限而非真實資料決定。

## 原因
1. 查詢寫成「升冪排序＋limit N」：表短時取到全部，表長之後取到的是最舊的 N 筆。
2. 只寫 `limit N` 沒有時間條件：露出的時間範圍隨事件密度變動，密集時期只剩幾天。
3. 資料晚於地圖就緒才到時，`setData` 被「樣式還沒載入」的檢查擋掉且沒有重試，部分批次靜默丟失。

## 解法
1. 事件查詢一律以時間窗為主條件（例如時間軸選定日往回 N 天、往後到 now + 預報期），limit 只當安全上限，並在命中上限時警告。
2. 時間窗的錨點用時間軸選定日，不用牆鐘 now，否則回放歷史時會查錯範圍。
3. 上界也要設（例如 now + 7 天），順便擋掉上游時間錯誤的未來列。
4. 每個點帶有效區間 `[valid_from, valid_until)`，時間軸移動時只改 filter，不重新查詢。
5. 寫入地圖 source 前若樣式未就緒，用有界重試或等 `style.load`／`idle` 再寫，不能直接略過。

## 怎麼偵測
- 通用：比較圖層顯示的最早／最晚事件時間與資料表的 `min/max`；差距大就是查詢上限在決定畫面。
- 通用：回傳筆數剛好等於 limit 值時，幾乎一定有被截掉的資料。
- 搜尋：`rg -n -i "order\([^)]*ascending: *true|order by [a-z_]+ asc" ` 搭配 `rg -n 'limit\(|LIMIT [0-9]+'`，在事件 loader 找「升冪＋上限」。
- 搜尋（沒有時間條件）：`rg -n '\.limit\(' ` 再看同一查詢是否有 `.gte(`／`.lt(` 或 `WHERE .*time`。
- 搜尋（setData 被擋）：`rg -n -B2 'setData' | rg 'isStyleLoaded'`（適用 stack：mapbox-gl、maplibre）。

## 出處
- PostgREST 文件：伺服器端 `db-max-rows` 上限與 Range／Content-Range 回應（另一種靜默截斷，通用部分見其他 topic）。
- 實例：[全球氣候改版紀錄](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/global-climate/changelog.md)（颱風升冪加 limit 5000，表長後永遠是 7 月的舊颱風；地震裸 limit 只露 11.6 天，DB 有 46 天；setData 被樣式檢查擋掉，加有界重試）；[颱風 loader 的時間窗與列數上限](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/typhoonTracksLoader.ts)。
