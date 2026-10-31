---
id: 12-16
title: 事件型即時資料「0 筆是合法結果」，上游靜默斷供時沒人發現：0、沒資料與過期要分開
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [silent outage, stale, freshness, heartbeat, ledger, 0 vs null, 落雷, 地震, 颱風, 共機, 新鮮度, monitoring]
---

## 原則
事件型資料的「0 筆」是合法結果，不能當健康判準：用執行帳本監控，並在畫面上分開「0」、「無資料」與「過期」，「更新於」顯示資料本身的時間。

## 症狀
- 落雷、地震、颱風、事件型圖層連續幾週沒有點，但 collector 每分鐘都在跑、HTTP 200、沒有錯誤。
- 監控面板上 `last_success_at` 停在很久以前，看起來像程式掛了；`last_error` 顯示一個無關的舊錯誤（例如連線池 timeout），把人導向錯的方向。
- 新鮮度監控對「本來就會長時間沒事件」的表一直誤報，久了沒人理。
- 每日發布的工作連續失敗，但監控看的是「開始時間」，所以一直顯示正常。
- 地圖上的誤導：「沒有點」被讀成「沒有雷雨／沒有地震／海上沒有船」，但其實是上游停供；同一張圖上若同時寫「更新於 1 分鐘前」（抓取時間），可信度看起來更高。

## 原因
1. 事件型資料（落雷、地震、颱風、軍機架次）沒事發生時本來就是 0 筆，所以「這輪沒資料」不能當健康判準。
2. heartbeat 只在有資料寫入時更新，上游回空檔就停在最後一次有資料的時刻。
3. 上游可能端點活著但內容是空的（只剩標頭行），不會有任何 HTTP 錯誤。
4. 監控看的欄位語意錯：看 `max(資料時間)` 會把「沒事發生」當成壞；看「開始時間」會把「每次都失敗」當成好；看 `updated_at` 若 UPSERT 不更新它，也證明不了新版程式在寫。

## 解法
1. 為 pipeline 建執行帳本（ledger）：每個處理單位（每日、每次輪詢）必有一列，記錄產出筆數（0 合法）、成功與否、錯誤；監控指向 ledger 的 `max(run_at)` 與失敗列，而不是產出表。
2. 同一現象有第二來源時並行收（見 [12-14](12-14-lightning-dual-source.md)）：一邊有一邊沒有立刻現形。
3. 診斷時用第三方訊號反證：例如同期有雷雨特報、時雨量很大，但落雷 0 筆，就是上游壞了。
4. 歸檔檔案大小是免費的時間軸：連續多天大小完全相同＝內容沒變，可以據此定出停供起點，不必下載。
5. 前端分開三種狀態：0（有觀測、確實沒有）、無資料（沒收到）、過期（資料時間超過該來源的更新週期）；「更新於」顯示資料本身的時間，不是抓取或傳輸成功時間。
6. 驗證新版 collector 是否生效，看只有新版才會產生的內容特徵，不看時間戳。

## 怎麼偵測
- 通用：對每個事件型來源列出「最後一筆資料時間」與「最後一次成功執行時間」兩欄；前者很舊、後者很新時，要用第三方訊號判斷是沒事還是停供。
- 通用：歸檔或下載檔大小的序列出現長串完全相同值。
- 搜尋（heartbeat 被短路）：`rg -n -B2 -A2 'if not records:\s*$' ` 或 `rg -n 'if not (records|rows|data):\s*return'` 在寫入層，看 return 前有沒有回報執行成功。
- 搜尋（前端把傳輸成功當新鮮）：`rg -n -i 'status.*(ready|success)|lastUpdated|fetchedAt' ` 在監看／即時面板，確認有比對資料時間。
- 搜尋（0 兜底）：`rg -n '\?\? 0|\|\| 0|COALESCE\([^,]+, *0\)'`，事件計數若用 0 兜底，要能區分「沒收到」。

## 出處
- 一般資料管線監控做法（execution ledger、freshness SLO）。相關卡：[12-14](12-14-lightning-dual-source.md)。
- 實例：[共機航跡斷 5 天、落雷斷 28 天、警政資料停更 6 週，監控卻顯示正常](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/.claude/pitfalls/2026-08-07-silent-upstream-outage.md)；[監看卡依更新週期判斷即時／延遲／過期／停更](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/71eac186c4afd26a30f061bdc4e060039879baa2)；[事件紀錄：UPSERT 不更新 updated_at，改看新欄位判斷部署生效](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)。

