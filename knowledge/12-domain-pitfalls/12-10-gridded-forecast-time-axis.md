---
id: 12-10
title: 格點場（風、海流、沙塵）時間軸：預報值冒充實況、最近幀沒有容差、抓取沒限時間範圍
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Evaluated
stacks: [any]
tags: [GFS, CMEMS, forecast, analysis, lead time, valid time, frame, tolerance, NetCDF, subset, 海流, 風場]
---

## 原則
格點場要同時存發布時間與預報時效，同一有效時間以時效最短者為準；選幀必須設容差；抓取一律帶時間範圍。

## 症狀
- 時間軸拉到任何一天，風場都顯示同一張圖（「換日期不會變」）。
- 「近 14 天實況」裡其實全是 3–5 天前做的預報。
- 抓取工作從幾 MB 突然變成單檔十幾 GB，容器被判死重啟、重跑、再爆。
- 地圖上的誤導：把預報畫成實況，使用者會以為「當時就是這樣」；舊幀被 clamp 到新日期，會讓人以為那幾天天氣沒變。

## 原因
1. 模式資料有兩個時間：發布（cycle／run）時間與有效（valid）時間；同一個 valid time 會有多個 lead time（f000 分析、f024、f120 預報）。若唯一鍵只用 `(dataset, valid_time)` 搭配「衝突就忽略」，舊 cycle 的長預報先佔位，新 cycle 的分析場被靜默丟掉。
2. 選幀用「最近的那一張」但沒有距離上限，資料缺幀時任何日期都會落到同一張。
3. 海洋／大氣資料服務的 subset 若沒帶起訖時間，會抓整條時間軸（多年分析加未來預報）；小範圍時看不出來，擴大範圍才爆量。

## 解法
1. 存檔時同時保留 cycle 時間與 lead time；同一 valid time 以 lead time 最短者為準（衝突時 update，而不是 ignore），或把 lead time 放進唯一鍵並在查詢時選最小。
2. 圖例或 popup 標示「分析」或「+N 小時預報」。
3. 選幀加容差：daily 幀最壞合法距離 12 小時，加緩衝約 18 小時；超出就回「無資料」並清空畫面，不要沿用舊幀。
4. subset／下載一律帶時間範圍（例如「今日 00Z 起 +48 小時」），並設單檔大小上限告警。
5. 表層海流要選對深度範圍（表層格點中心常不是 0 m）。

## 怎麼偵測
- 通用：在時間軸連續切幾個日期，截圖比對是否真的不同；對資料表查 `lead_time = 0` 的近 N 天筆數，0 筆代表實況被預報佔位。
- 通用：下載檔案大小的時間序列，有數量級跳升就查時間範圍參數。
- 搜尋（衝突策略）：`rg -n -i 'on conflict[^;]*do nothing|ignore_duplicates|INSERT OR IGNORE'` 在格點／預報寫入程式。
- 搜尋（選幀）：`rg -n -i 'nearest.?frame|pickNearest|closest' `，確認有 tolerance 參數。
- 搜尋（subset 時間）：`rg -n -i 'subset|open_dataset|copernicusmarine' ` 再看是否帶 `start|end|datetime`。

## 出處
- Copernicus Marine Toolbox `subset` 的 `--start-datetime`／`--end-datetime` 參數說明。
- NOAA GFS 檔名中的 cycle 與 forecast hour（fXXX）。
- 實例：[全球氣候改版紀錄](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/global-climate/changelog.md)（唯一鍵搭配「衝突就忽略」使近 14 天沒有分析場；最近幀無容差，缺幀時任何日期都 clamp 到同一張，加 18 小時容差）；[collector 改為衝突時更新](https://github.com/ianlkl11234s/gis-data-collectors/commit/bcd9d192c12dcfaa264938ac74aef7035b82ea00)；[抓取帶時間範圍後單檔由 18.7 GB 降到 27 MB](https://github.com/ianlkl11234s/gis-data-collectors/commit/fede62d0f15b226bdca7225ee92cd2cc5fbeaae7)；[事件紀錄：bbox 擴大後單檔暴增](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)。

