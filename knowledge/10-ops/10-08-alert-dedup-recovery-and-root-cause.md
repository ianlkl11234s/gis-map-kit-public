---
id: 10-08
title: 告警降噪與找真因：倍增門檻、狀態轉換、恢復通知；401 會被 retry storm 的 429 蓋住
topic: 10-ops
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [告警, 降噪, 去重, 恢復通知, 401, 429, retry storm, backoff, 共用金鑰]
---

## 原則
告警只在狀態轉換與倍增門檻時發送並附恢復通知；排查 API 失敗先取得完整狀態碼與 error body，401 與 429 並存時先假設是認證問題。

## 症狀
- 同一則錯誤每 2 分鐘發一次，十幾小時刷了數百則，頻道被當成已知雜訊，真事故淹沒。
- 看到 429 就去調 rate limit，其實根因是金鑰被重置（401）。
- `raise_for_status()` 吃掉了回應 body，看不到 `Invalid client secret` 這種關鍵訊息。

## 原因
- 第一版告警寫成「失敗就通知」。
- 認證失敗時不 cache、直接 raise，多支 collector 每輪都重打 token 端點形成 retry storm，反而觸發 rate limit，429 蓋住真正的 401。
- 多支 collector 共用同一把金鑰＝單點故障。

## 解法
1. **降頻**：連續失敗只在第 3、6、12、24…次通知（門檻×2^k）。
2. **狀態轉換才發**：記錄 `ok／alerting` 狀態，只在轉換時發；**恢復時另發一則**。
3. 日報型摘要：異常記 `first_seen`，持續中的只在第 1、3、7 天重報；結尾附「今日該做的最多 3 件事」。
4. 新增任何告警都要說明去重或降頻策略，並有恢復通知；「每次失敗都發」視為缺陷。
5. **排查 API 失敗前先取得完整狀態碼與 error body**（遮掉金鑰）。同時出現 401 與 429 時，先假設是認證問題。
6. token 失敗的 backoff、`Retry-After`、全域限速器見 [12-12](../12-domain-pitfalls/12-12-upstream-blocking-rate-limits.md)；共用金鑰要有輪換流程（見 [10-04](10-04-public-token-vs-secret.md)、[10-13](10-13-migration-and-domain-cutover.md)）。
7. 通知管道要確認真的有人看（頻道是否仍運作、外部巡檢是否仍在執行）。

## 怎麼偵測
- 通用：告警頻道內同一訊息重複出現；失敗時 log 只有狀態碼沒有 body。
- 搜尋：`raise_for_status\(\)` 前沒有先記錄 `response.text`；告警函式在 `except` 內無條件呼叫；token 取得函式失敗路徑沒有 backoff／快取（適用 stack：Python requests／fetch 類，概念通用）。

## 出處
- RFC 6585（429）、`Retry-After` 標頭；一般告警疲勞（alert fatigue）實務。相關卡：[01-08](../01-taiwan-apis/01-08-token-secret-throttle-backoff.md)（認證與限流細節）、[12-12](../12-domain-pitfalls/12-12-upstream-blocking-rate-limits.md)（封鎖與限流）。
- 實例：[tdx-secret-reset-401（共用金鑰被重置，多支 collector 失敗並刷屏）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/.claude/pitfalls/2026-08-30-tdx-secret-reset-401.md)、[855af41](https://github.com/ianlkl11234s/gis-data-collectors/commit/855af41a214ee71b58849a48ba0a58002051e5c0)（加倍增門檻）、[utils/notify.py](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/utils/notify.py)、[utils/auth.py](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/utils/auth.py)。

