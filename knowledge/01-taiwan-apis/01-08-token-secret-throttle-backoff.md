---
id: 01-08
title: 要 key 的 API：secret 放後端、token 快取、全域節流與退避
topic: 01-taiwan-apis
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [token, key, secret, OAuth2, 節流, rate limit, 429, 退避, backoff, 打包掃描]
---

## 原則
需要 secret 的 API 一律由後端呼叫，前端只讀後端產出的結果；token 在後端快取重用，同一把金鑰共用一個節流器，429 退避、401／403 另行處理。

## 症狀
- 前端 bundle 裡找得到 client secret／授權碼。
- 上線後 429，401 與 429 同時出現。
- 已授權的函式（例如資料庫 RPC）沒授權時只回空陣列，不報錯。

## 原因
- 把需要 secret 的 API 當成可前端直呼。
- 取 token 的請求也計入配額；多處程式共用一把金鑰卻各自節流。
- 某些服務對未授權呼叫回「成功但空」。

## 解法
1. 分清公開 client key 與真 secret，後者永遠不進前端（分類與做法見 [10-04](../10-ops/10-04-public-token-vs-secret.md)）。
2. 後端取 token 並快取，到期前重用；401 先看 token。
3. 限流與封鎖：共用節流器、429 退避、401／403／429 分流，完整說明見 [12-12](../12-domain-pitfalls/12-12-upstream-blocking-rate-limits.md)。
4. 後端把結果寫成快照或資料庫，前端只讀結果。
5. 部署前掃描打包產物，不得出現 secret 變數名稱對應的值（見 [10-04](../10-ops/10-04-public-token-vs-secret.md)）。

## 怎麼偵測
- 通用：DevTools Network 看到帶 key 的第三方請求；日誌連續 429。
- 搜尋：`SERVICE_ROLE|CLIENT_SECRET|api_key=`（出現在前端目錄或 `dist/`）；多個 `sleep|setTimeout` 各自節流同一來源（適用 stack：any）。

## 出處
- 一般建議：OAuth2 client_credentials、節流與退避為通用做法。
- 相關卡：[01-01](01-01-tdx-integration.md)、[10-04](../10-ops/10-04-public-token-vs-secret.md)、[12-12](../12-domain-pitfalls/12-12-upstream-blocking-rate-limits.md)。
- 實例：[TDX 限流事故與全域節流器](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/TDX_RATE_LIMITING.md)；[service role 不進 bundle 的規則](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/development-rules.md)。

