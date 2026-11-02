---
id: 10-00
title: 上線維運總表：部署、金鑰、監控、排程、搬家事故、測試守門
topic: 10-ops
kind: catalog
scope: public
evidence: Observed
stacks: [any]
tags: [總表, 維運, 部署, 金鑰, 監控, 告警, 排程, 搬家, 事故, 測試]
---

## 原則
先判斷問題屬於哪個子題再選卡；上線前先看部署與金鑰兩組，上雲端才出問題先看搬家與事故組。

## 對照表

### 部署與資產
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 決定網站放哪 | [10-01](10-01-deploy-option-decision.md) | 拆成前端程式、資料檔、會變的來源三件事，各依更新節奏選放哪 |
| 資料更新要不要重建前端 | [10-02](10-02-data-update-vs-redeploy-and-cache.md) | 換內容就換檔名或改指標檔，不覆寫同名檔 |
| PMTiles 上線 | [10-03](10-03-pmtiles-range-cdn-cors.md) | 確認 Range 回 206、CORS 放行 range 與 etag、網址未被快取成錯誤頁 |
| 本機正常、上線就壞 | [10-05](10-05-local-vs-production-differences.md) | 逐項核對環境差異，確認資料檔 content-type 不是 text/html |


### 金鑰與安全
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 哪些 token 可以進前端 | [10-04](10-04-public-token-vs-secret.md) | 只有公開 token 能進 bundle，真 secret 留後端或 CI |
| 排錯或檢查環境設定時 | [10-21](10-21-secrets-in-bundle-and-dev-server.md) | 前綴變數的值視為公開，只列 key 名稱，不 curl dev server 的轉譯模組 |
| 資料授權不明或不允許公開 | [10-22](10-22-data-license-tiers-and-owner-only-layers.md) | 依授權分級決定放哪，不允許公開者走站主限定並經後端驗證 |
| 前端帶公開金鑰的資料庫 | [10-23](10-23-database-public-exposure-tables-functions.md) | 匿名與已登入角色可碰到的表、欄位、函式都要盤點，只給必要的 |
| 加 CSP | [10-24](10-24-csp-for-map-sites.md) | 先 Report-Only 收違規，補齊白名單後才轉 enforcing |

### 監控與告警
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 前端錯誤監控 | [10-25](10-25-frontend-error-monitoring.md) | 只對外部使用者的站接，同時收 SDK error 與 WebGL context lost，送出前去掉位置 |


### 排程與批次
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 排程的「今天」是哪天 | [10-09](10-09-schedule-taipei-timezone.md) | 明寫 Asia/Taipei，資料庫預設 UTC，排程表達式先換算 |


### 搬家與事故
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 上雲端才連不上來源 | [10-12](10-12-upstream-ip-block-deploy-env.md) | 部署前從部署環境實測，ConnectTimeout 先懷疑被擋 |



## 相關主題
- 對外 RPC 守門：[07-08](../07-performance/07-08-public-rpc-timeout-clamp-rowcap.md)。
- 後端預先彙總：[07-07](../07-performance/07-07-backend-preaggregate-and-data-path-triage.md)。
- 登記簿完整性測試：[08-02](../08-multi-layer/08-02-registry-completeness-tests-and-ledger.md)。
- 網站被搜尋引擎與 AI 爬蟲讀取：[11-03](../11-extras/11-03-llms-txt-and-ai-crawler-policy.md)。

## 出處
各項依據見對應卡片。
