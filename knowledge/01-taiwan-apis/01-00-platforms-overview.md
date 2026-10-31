---
id: 01-00
title: 台灣開放資料平台總覽：要不要 key、限流、格式、適合做什麼圖層
topic: 01-taiwan-apis
kind: catalog
scope: public
evidence: Observed
stacks: [any]
tags: [TDX, 氣象署, CWA, 環境部, 水利署, data.gov.tw, NLSC, TGOS, NCDR, 台電, 農業部, OSM, Overpass, 平台清單]
---

## 原則
找台灣資料先查下表選平台，再讀對應的接法卡；官方配額、價格、授權原文若表中標「官方原文未取得」，就照實寫未取得，不要自己補數字。data.gov.tw 多半只是目錄，真正的檔案在各機關自己的站。

## 症狀
開始做台灣的圖台時，不知道某類資料（公車、天氣、水位、行政界…）該去哪個平台拿、要不要申請、能不能前端直接呼叫、拿到後要先防什麼。

## 原因
台灣開放資料分散在各機關主機；各平台的認證、分頁、座標、時區習慣都不同，且「有 API」不代表「有歷史」。

## 解法
先用下表選平台，再看對應的接法卡。

| 平台 | 典型資料 | 認證 | 限流／配額 | 格式 | 適合的圖層 | 接法卡 |
|---|---|---|---|---|---|---|
| TDX 運輸資料流通服務 | 公車即時位置、公共自行車車位、台鐵即時／時刻表、國道偵測器 | OAuth2 client_credentials，token 約 24 小時 | 依訂閱方案；token 端點另有每 IP 每分鐘上限；每秒／每日數字官方原文未取得 | REST JSON | 移動點、站點滿空率、路段速度 | [01-01](01-01-tdx-integration.md) |
| 中央氣象署開放資料 | 溫度格點、地震、落雷、雷達 | 會員授權碼 | 一般會員日配額官方原文未取得 | JSON／XML／KMZ | 格網場、事件點 | [01-02](01-02-cwa-integration.md) |
| 環境部環境資料開放平臺 | 空氣品質 AQI 等 | api_key 參數 | 未公告，實務約每秒 2–3 次（經驗值） | JSON list | 測站點 | [01-03](01-03-moenv-integration.md) |
| 水利署 opendata／IoT／GIC | 河川水位、水庫、地下水、淹水感測、圖資 SHP | opendata 免認證；IoT 需 OAuth2；GIC 免申請下載 | 單頁 10 萬筆上限 | JSON/CSV/XML、SHP/KML | 測站、範圍面 | [01-04](01-04-wra-integration.md) |
| data.gov.tw 政府資料開放平臺 | 目錄＋授權；各機關資料 | 多數免 | 依實際資料主機 | 各種 | 找資料、授權標示 | [01-05](01-05-data-gov-tw-and-license.md) |
| 內政部 NLSC／TGOS／戶政司 RIS | 行政界、村里、人口 | 下載免；TGOS 主題 API 需 Apikey（綁 IP） | 土地利用點查實測約 2.6 次/秒（非官方） | SHP/GML、JSON | choropleth 的面與分母 | [01-06](01-06-nlsc-ris-boundaries-population.md) |
| 縣市資料平台（臺北 data.taipei 等） | 行道樹、垃圾車、都市計畫 | 多數免 | 未遇到 | JSON/SHP | 在地主題 | [01-07](01-07-local-and-other-platforms.md) |
| NCDR、台電、農業部、航港局、OSM Overpass | 示警、電力、農產行情、AIS、POI | 各異 | 各異（OSM 見 [01-07](01-07-local-and-other-platforms.md)） | 各異 | 災害、能源、船舶、POI | [01-07](01-07-local-and-other-platforms.md) |

跨平台的共同結論（各有專卡）：
- key／token 放後端（[01-08](01-08-token-secret-throttle-backoff.md)）；「200 OK」不等於拿到資料（[01-09](01-09-http-200-not-success-and-pagination.md)）；即時 API 只給現在（[01-10](01-10-realtime-api-has-no-history.md)）；瀏覽器直呼要先確認 CORS（[01-11](01-11-cors-and-direct-calls.md)）；欄名不可信（[01-12](01-12-coordinates-crs-and-column-names.md)）；時間欄要驗時區（[01-13](01-13-time-zone-and-update-time.md)）；表名不等於內容、上游會停更（[01-14](01-14-semantics-drift-and-upstream-loss.md)）。
- 授權：data.gov.tw 的開放授權要求顯名標示提供機關，細節見 [01-05](01-05-data-gov-tw-and-license.md)。

## 怎麼偵測
- 通用：程式裡寫死某平台網址卻沒有認證、節流、錯誤處理；README 沒說資料來自哪個機關。
- 搜尋：`tdx\.transportdata|opendata\.cwa|data\.moenv|opendata\.wra|data\.gov\.tw`（適用 stack：any）。

## 出處
- 官方：data.gov.tw/license（授權條款）、github.com/tdxmotc/SampleCode（TDX 呼叫限制說明）。TDX 與氣象署官方網頁需 JavaScript，配額原文未取得。

