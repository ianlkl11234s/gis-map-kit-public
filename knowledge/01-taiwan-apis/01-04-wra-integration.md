---
id: 01-04
title: 水利署接法：單頁 10 萬筆靜默截斷、_3826 欄名、IoT 的 200 回 HTML
topic: 01-taiwan-apis
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [水利署, WRA, 水位, 水庫, 地下水, IoT, GIC, 截斷, 分頁, EPSG:3826]
---

## 原則
水利署筆數等於已知上限（1 萬、2 萬、10 萬）一律視為疑似截斷並改走分頁；欄名帶 `_3826` 也要驗座標範圍；用資料表前先確認它真的有你要的數值欄。

## 症狀
- 抓到的筆數剛好是整數（例如 100,000），下游統計比實際少。
- 圖層只有部分測站，沒有任何錯誤。
- IoT 平台路徑打錯，回 200 與 HTML。
- 「河川水位即時」「水庫蓄水量」這類資料表打開才發現沒有水位或蓄水量數值。

## 原因
- opendata 單頁最多 10 萬筆，超過靜默截斷，必須加 `page=N`。
- 欄名帶 `_3826` 不保證真的是 TWD97。
- IoT 平台經度欄曾有拼字錯誤；路徑錯誤不回 404。
- 資料集名稱與內容不一定相符（見 [01-14](01-14-semantics-drift-and-upstream-loss.md)）。
- GIC 圖資的後端為 EPSG:3826，且網站對部分連線有阻擋。
- 水利署主機憑證缺 Subject Key Identifier；Python 3.13 以上預設開啟 `VERIFY_X509_STRICT`，會拒收，curl 與瀏覽器卻正常。

## 解法
1. 筆數等於已知上限（10000／20000／100000）一律標「疑似截斷」，改走分頁。
2. 取得後驗證欄位型別與座標範圍；SHP 無 .prj 時可用面積交叉驗證投影。
3. IoT 需 OAuth2，token 約 30 分鐘，要快取與提前更新（見 [01-08](01-08-token-secret-throttle-backoff.md)）。
4. 靜態圖資（GIC SHP/KML）下載一次、轉 WGS84、存 GeoJSON，不要每次開頁都抓。
5. 使用前先 describe 一次資料表：列的單位是什麼、是否只有測站名冊。
6. Python 3.13 以上 TLS 驗證失敗時，只關掉 `VERIFY_X509_STRICT` 這一個旗標（`ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT`），保留憑證鏈與網域驗證；不要整個 `verify=False`。

## 怎麼偵測
- 通用：資料筆數恰為整數上限；時序比預期少一半；測站數遠少於官方公告。
- 搜尋：`opendata\.wra|iot\.wra`（旁邊沒有 `page=`／分頁迴圈）、`_3826`（沒有範圍驗證）（適用 stack：any）。

## 出處
- 官方：opendata.wra.gov.tw（swagger 於 /openapi/swagger/index.html）。授權與限流細節官方原文未取得。
- 相關卡：[01-08](01-08-token-secret-throttle-backoff.md)、[01-09](01-09-http-200-not-success-and-pagination.md)、[01-14](01-14-semantics-drift-and-upstream-loss.md)。

