# 01-taiwan-apis 台灣開放資料 API

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [01-00](01-00-platforms-overview.md) | 台灣開放資料平台總覽：要不要 key、限流、格式、適合做什麼圖層 | 開始做台灣的圖台時，不知道某類資料（公車、天氣、水位、行政界…）該去哪個平台拿、要不要申請、能不能前端直接呼叫、拿到後要… | catalog | Observed | any | TDX, 氣象署, CWA, 環境部, 水利署, data.gov.tw, NLSC, TGOS, NCDR, 台電, 農業部, OSM, Overpass, 平台清單 |
| [01-01](01-01-tdx-integration.md) | TDX 接法：OAuth token、全域節流、站牌 ID 與更新時間的坑 | 多個城市／多支程式同時呼叫後大量 429，甚至 401 與 429 一起出現。 | pattern | Observed | any | TDX, 公車, YouBike, 台鐵, 國道, OAuth2, 429, StationUID, LastUpdateTime, 節流 |
| [01-02](01-02-cwa-integration.md) | 中央氣象署接法：三種取得管道、路徑錯誤回 200、地震多筆報告與落雷覆寫 | fileapi 回 HTTP 200，內容卻是官網首頁 HTML，JSON parse 失敗。 | pattern | Observed | any | 氣象署, CWA, fileapi, datastore, 地震, 落雷, 溫度格點, KMZ, 授權碼 |
| [01-03](01-03-moenv-integration.md) | 環境部開放平台接法：純 list 分頁、欄名座標不可信、社群感測不可混算 | 空氣品質測站畫出來全部掉到海裡或跑到別的國家。 | pattern | Observed | any | 環境部, moenv, AQI, 分頁, offset, twd97lon, LASS, 微型感測, 憑證 |
| [01-04](01-04-wra-integration.md) | 水利署接法：單頁 10 萬筆靜默截斷、_3826 欄名、IoT 的 200 回 HTML | 抓到的筆數剛好是整數（例如 100,000），下游統計比實際少。 | pattern | Observed | any | 水利署, WRA, 水位, 水庫, 地下水, IoT, GIC, 截斷, 分頁, EPSG:3826 |
| [01-05](01-05-data-gov-tw-and-license.md) | data.gov.tw：只是目錄，metadata 用 /api/v2/rest/dataset/<id>（不是 package_show）、要帶自訂 UA；授權要顯名標示提供機關 | 目錄上拿到的下載連結失效、資源 id 被截斷、檔名一換就抓不到。 | decision | Observed | any | data.gov.tw, 授權, OGDL, 顯名標示, metadata API, User-Agent, 403, 資料集更新, 編碼 |
| [01-06](01-06-nlsc-ris-boundaries-population.md) | 行政界與人口：NLSC／TGOS 邊界、戶政司 RIS 人口的代碼與層級陷阱 | 村里 join 後少了一些列，或對不上（代碼前導零不見）。 | pitfall | Observed | any | NLSC, TGOS, 國土測繪, 行政區, 村里, VILLCODE, RIS, 戶政司, 人口, choropleth, 分母, 通用版電子地圖 |
| [01-07](01-07-local-and-other-platforms.md) | 縣市平台與其他來源：個資、IP 限制、覆寫、OSM Overpass 使用政策 | 用到這些來源時常遇到：沒有歷史版本、本機能抓部署後不能抓、API 回應含個資、瀏覽器抓不到。 | catalog | Observed | any | data.taipei, NCDR, 台電, 農業部, 航港局, AIS, Overpass, OSM, 行道樹, CORS, 個資 |
| [01-08](01-08-token-secret-throttle-backoff.md) | 要 key 的 API：secret 放後端、token 快取、全域節流與退避 | 前端 bundle 裡找得到 client secret／授權碼。 | pattern | Observed | any | token, key, secret, OAuth2, 節流, rate limit, 429, 退避, backoff, 打包掃描 |
| [01-09](01-09-http-200-not-success-and-pagination.md) | HTTP 200 不等於拿到資料：回 HTML、靜默截斷、分頁漂移 | 地圖空白但 Network 全是 200。 | pitfall | Observed | any | 200, HTML, content-type, 截斷, 分頁, offset, page, 10000, 20000, 100000, PostgREST |
| [01-10](01-10-realtime-api-has-no-history.md) | 即時 API 只給「現在」：要比較時間就得自己存快照，並防靜默斷供 | 想做「昨天 vs 今天」才發現 API 只有最新值。 | pattern | Observed | any | 快照, 歷史, collector, 覆寫, 靜默斷供, stale, 心跳, 新鮮度, 歸檔 |
| [01-11](01-11-cors-and-direct-calls.md) | 瀏覽器直呼外部 API：先查 CORS，本機 proxy 部署後會失效 | curl 正常，瀏覽器 console 出現 CORS error 或 403；本機開發正常，部署後全壞。 | decision | Observed | any | CORS, proxy, 403, preflight, vite, nginx, Cloudflare Worker, 快照, Range |
| [01-12](01-12-coordinates-crs-and-column-names.md) | 座標系與欄名不可信：TWD97/WGS84、經緯度互換、單位錯誤 | 點全掉到海裡、赤道附近、或別的國家。 | pitfall | Observed | any | 座標系, TWD97, EPSG:3826, WGS84, 經緯度互換, bbox, 單位, 英呎, prj, 編碼, BOM, cp950 |
| [01-13](01-13-time-zone-and-update-time.md) | 時間欄位：+8 小時、UTC 日界、UpdateTime 不是變動時間 | 最新資料出現在「未來」，時間軸今天是空的。 | pitfall | Observed | any | 時區, UTC, +8, naive datetime, 日界, 民國年, LastUpdateTime, 時間軸 |
| [01-14](01-14-semantics-drift-and-upstream-loss.md) | 表名不等於內容、欄位與 ID 漂移、IP 封鎖與上游停更 | 資料集名叫「水庫蓄水量」卻沒有蓄水量數值；叫「船舶」卻只是港口名冊。 | pitfall | Observed | any | 口徑, 欄位漂移, ID 對應, 停更, 台灣 IP, 疊檔, 分母, row unit, 模擬資料 |
| [01-15](01-15-source-update-detection.md) | 來源更新偵測：比對 metadata、檔名與更新日期，產生更新清單 | 靜態或半動態圖層的來源資料早就更新了，但沒人知道；檔名換了、舊連結抓到舊版或 404。 | pattern | Implemented | any | 更新偵測, metadata, 檔名含日期, 更新清單, 變更紀錄, 週期排程, data.gov.tw |
| [01-16](01-16-data-source-types.md) | 資料來源六類：直接取得三類、加工產生三類，各自要先確認什麼 | 不知道某個主題該去哪裡找資料，或找到之後不知道該先檢查什麼。 | catalog | Implemented | any | 資料來源, 開放資料, 縣市拼接, OSM, collector, API 收集, 行政區統計, choropleth, 衛星影像, 航照, 影像辨識, YOLO, 都市熱島, 地表溫度, Landsat |
