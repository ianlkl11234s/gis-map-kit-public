---
id: 10-17
title: 全有全無的批次會讓一個失敗放大成整條 pipeline 停擺：單批隔離、checkpoint 才能前進
topic: 10-ops
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [checkpoint, 批次, 全有全無, 重試, LLM 額度, 佇列, TTL, 隔離, pipeline 停滯]
---

## 原則
批次處理只讓失敗的那一批被跳過或隔離，不要讓單批失敗使整輪作廢；checkpoint 只在確定完成的範圍推進，佇列要有界。

## 症狀
- pipeline 停滯一天以上，上游其實正常。
- 外部付費服務（LLM、地理編碼）額度用完加值後，仍因「只要一批失敗整輪不寫」又卡了好幾個小時。
- 同一批候選每小時重播同一個錯誤；狀態表顯示沒事。
- 上游「只保留最近 N 則」，卡住期間的資料永久補不回來。

## 原因
把「一個 chunk 失敗」放大成「整輪作廢、checkpoint 不動、pending 原封重送」；溫度 0 的 LLM 對同一批輸入會重複同樣的錯誤。

## 解法
1. **單批失敗只跳過該批**，下一輪重送；**全部**批次失敗才算整輪失敗。
2. 失敗 chunk 拆半重送，找出毒資料後隔離，不讓一個毒 cohort 卡住整個佇列。
3. checkpoint 只在確定處理完成的範圍推進；落後超過門檻時進入 catch-up 模式（每輪追更多檔）。
4. 佇列要有界：TTL（過期只記 receipt 不再送）、newest-first、每輪必抓最新一份。上游滾動視窗的資料今天沒抓到就沒了（見 [10-11](10-11-retention-registry-and-cold-archive.md)）。
5. 錯誤訊息保留 HTTP 狀態碼與原因類別；額度用盡（402／429）要獨立告警（見 [10-08](10-08-alert-dedup-recovery-and-root-cause.md)）；在 receipt 記版本、chunk 數、失敗數、deferred／expired 數，作為驗收依據。

## 怎麼偵測
- 通用：pipeline 輸出的 `max(observed_at)` 與現在差距持續擴大，而 collector 狀態仍顯示成功或只是偶爾失敗。
- 搜尋：`if any\(.*fail` / `if failed: return` 在批次迴圈之後直接放棄整輪；重試無拆分／無 TTL；checkpoint 更新放在迴圈外且依賴全部成功（適用 stack：any）。
- 與事件 feed 的靜默斷供比較，見 [12-16](../12-domain-pitfalls/12-16-event-feed-silent-outage.md)。

## 出處
- 一般批次處理設計（poison message、bulkhead）。相關卡：[10-16](10-16-batch-duplicate-pk-upsert.md)（同批主鍵重複讓 UPSERT 整批失敗）。
- 實例：[repair-2026-09-05.md（拆掉全有全無耦合後，落後大幅縮短）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/global-events/repair-2026-09-05.md)、[news-llm-all-or-nothing（LLM 額度用盡後積壓、整輪不寫）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/.claude/pitfalls/2026-10-21-news-llm-all-or-nothing.md)。
