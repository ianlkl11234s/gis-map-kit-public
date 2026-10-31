---
id: 01-03
title: 環境部開放平台接法：純 list 分頁、欄名座標不可信、社群感測不可混算
topic: 01-taiwan-apis
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [環境部, moenv, AQI, 分頁, offset, twd97lon, LASS, 微型感測, 憑證]
---

## 原則
環境部資料載入後先做 bbox 目視檢查，不信欄名、不自動交換經緯度；分頁用「回傳筆數 < limit」判斷末頁；官方測站與社群微型感測分開呈現、不混算。

## 症狀
- 空氣品質測站畫出來全部掉到海裡或跑到別的國家。
- 翻頁後少了資料；不知道哪一頁是最後一頁。
- 社群微型感測（如 LASS）與官方測站數值混在一張圖上算平均。
- HTTPS 呼叫失敗，錯誤與憑證鏈有關。

## 原因
- 回應是純 JSON list，沒有總筆數；用 offset 翻頁在資料變動時會漂移漏資料。
- 欄名會騙人：名為 `twd97lon/lat` 的欄位其實是 WGS84，真正的 TWD97 在 `dtmx/dtmy`；時間標 UTC 實為本地時間；部分資料集經緯度兩欄互換。
- 微型感測屬低成本社群資料，品質與官方標準測站不同。
- 部分政府主機憑證缺 SKI 等欄位，嚴格的 TLS 函式庫會拒絕。

## 解法
1. 每頁固定 limit（上限 1000），以「回傳筆數 < limit」判斷最後一頁；翻頁中資料變動時，寧可重抓整批而不是補 offset。
2. 載入後畫幾個點目視驗證，並做 bbox 檢查（見 [01-12](01-12-coordinates-crs-and-column-names.md)），不自動交換欄位。
3. 官方測站與社群感測分開圖層或分開符號，標「非官方／Proxy」，不混算。
4. 憑證問題在後端 HTTP client 處理，不在前端繞過（做法見 [01-04](01-04-wra-integration.md)）。
5. 限流：官方未公告，實務經驗約每秒 2–3 次，視為保守值而非保證。

## 怎麼偵測
- 通用：測站點落在經度 119–122／緯度 21–26 之外；分頁筆數剛好是整數上限；官方與社群資料用同一色階。
- 搜尋：`offset` 迴圈但沒有終止條件、`twd97lon|twd97lat`（適用 stack：any）。

## 出處
- 官方：data.moenv.gov.tw（資料集頁；授權依各資料集）。
- 相關卡：[01-04](01-04-wra-integration.md)、[01-12](01-12-coordinates-crs-and-column-names.md)。
- 實例：[空氣品質 collector](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/collectors/air_quality.py)、[微型感測 collector](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/collectors/air_quality_microsensors.py)。

