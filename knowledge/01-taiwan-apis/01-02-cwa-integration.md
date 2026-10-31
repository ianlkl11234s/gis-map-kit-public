---
id: 01-02
title: 中央氣象署接法：三種取得管道、路徑錯誤回 200、地震多筆報告與落雷覆寫
topic: 01-taiwan-apis
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [氣象署, CWA, fileapi, datastore, 地震, 落雷, 溫度格點, KMZ, 授權碼]
---

## 原則
氣象署資料取得後先驗 content-type 與可否 parse；地震件數、規模、排名只用 catalog 報告；覆寫型端點（落雷等）要自己排程存檔；溫度格點標明是內插場。

## 症狀
- fileapi 回 HTTP 200，內容卻是官網首頁 HTML，JSON parse 失敗。
- 地震筆數、規模統計比官方多；同一場地震出現多筆，其中一種的時間晚 8 小時。
- 落雷端點「200 但只有標題行」，圖層悄悄變空。
- 溫度格點被當成測站觀測。

## 原因
- 同一類資料有三種管道：datastore（JSON、可 limit）、fileapi（302 轉址、content-type 常是 octet-stream）、免金鑰的 S3 鏡像（只存最新一份、直接覆寫）。路徑寫錯不報錯。
- 地震有 catalog（正式目錄）、significant、local 等不同報告，彼此是不同來源；部分報告的時間有上游時區問題。
- 落雷類端點是整檔覆寫，沒有人定時抓就永久消失。
- 溫度格點是內插場（0.03 度格網），不是測站值。

## 解法
1. 取得後先驗 content-type 與是否可 parse 為 JSON；非 JSON 視為失敗，不重試超過 2 次。
2. 地震件數、規模、排名一律只用 catalog；時間以 UTC 存放，換日前先 +8（見 [01-13](01-13-time-zone-and-update-time.md)）。
3. 覆寫型端點要自己排程存檔，間隔小於來源覆寫週期；連續 N 次空回應要告警（見 [01-10](01-10-realtime-api-has-no-history.md)）。
4. 圖例／popup 標明「格點內插」vs「測站觀測」。
5. 授權碼放後端，經 `Authorization` header 或參數帶入。
6. 官方配額與使用條款原文未取得；「一般會員每日 20,000 次／2 GB」只是第二手轉述，不要當成官方數字。

## 怎麼偵測
- 通用：資料抓取成功但 feature 數為 0；地震表同一時間附近重複列；時間比官網晚 8 小時。
- 搜尋：`fileapi|opendataapi`（旁邊沒有 content-type 檢查）、`report_type`（沒有過濾 catalog）（適用 stack：any）。

## 出處
- 官方入口：opendata.cwa.gov.tw（內容需 JavaScript，條款原文未取得）。
- 相關卡：[01-10](01-10-realtime-api-has-no-history.md)、[01-13](01-13-time-zone-and-update-time.md)、[12-01](../12-domain-pitfalls/12-01-timestamp-timezone-offset.md)。
- 實例：[落雷端點整檔覆寫與第二資料源](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/config.py)、[加入氣象署落雷 commit](https://github.com/ianlkl11234s/gis-data-collectors/commit/570a1dcb340f11c23a1f10a824139e9556ab7fae)。

