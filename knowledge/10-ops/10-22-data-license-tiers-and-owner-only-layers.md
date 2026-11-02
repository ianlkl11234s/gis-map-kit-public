---
id: 10-22
title: 資料授權分級決定能放到哪裡：未標示授權要選邊，授權不允許公開的資料走站主限定圖層
topic: 10-ops
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [授權, 政府資料開放授權條款, CC BY, ODbL, 未標示授權, 僅供瀏覽, 商業 API 條款, 個資, 站主限定, 私有圖層, 後端代理, 白名單, Range, 衍生資料, HOLD]
---

## 原則
每份資料上線前先判斷授權分級，分級決定它能進公開 CDN、只能展示不能下載、還是只有站主能看。授權不明確或不允許公開的資料，不要靠「藏起來的網址」，要放在私人儲存、經後端驗證身分後才轉送。

## 症狀
- 來源頁寫「僅供瀏覽」或重利用條件未確認的資料，被放進公開目錄，任何人可直接下載原始檔。
- 衍生圖層的授權只寫了其中一個輸入的條件。
- 私人 API 路徑在反向代理沒有精確設定，請求落到單頁應用的 fallback，回的是首頁 HTML，前端把 HTML 當資料解析而報錯。
- 新增私人資料家族後，只有正式環境壞，開發環境正常。

## 原因
- 授權條件分散在各來源頁，上線流程沒有統一欄位與關卡。
- 私人家族要在代理、開發環境 proxy、反向代理、白名單多處同時登記，漏一處就失效。

## 解法
1. **先分級**（以來源頁與條款原文為準，下表不是法律意見）：

| 種類 | 公開展示 | 下載／二次散布 | 要做什麼 |
|---|---|---|---|
| 政府資料開放授權條款第 1 版 | 可 | 可（含改作、再轉授權） | 依條款附件標示來源；官方說明與 CC BY 4.0 相容 |
| CC BY | 可 | 可 | 標示作者、來源、授權、是否修改 |
| CC BY-SA | 可 | 可，衍生品須同條款 | 標示並以相同條款釋出衍生品 |
| CC BY-NC | 非商業站可 | 限非商業 | 站台是否算商業不確定就當 HOLD |
| ODbL（OSM，見 [02-03](../02-basemaps/02-03-osm-data-license-vs-tile-policy.md)） | 可 | 可，衍生資料庫 share-alike | 標示「© OpenStreetMap contributors」 |
| 來源頁未標示 | 見解法 2 | 未知 | 來源卡標「授權待確認」、留原始連結 |
| 明示僅供瀏覽、不得重製、不得下載，或重利用條件未確認 | 不得放進公開檔案 | 否 | 站主限定（解法 3）或 HOLD |
| 商業 API 條款（地點與地理編碼 [16-05](../16-spatial-analysis/16-05-geocoding-precision-and-routing.md)） | 依該服務條款 | 常禁止快取、另存、散布 | 只即時呼叫、不入庫；入庫前讀條款 |
| 含個資的開放資料（[07-14](../07-performance/07-14-open-data-pii-column-exclusion.md)） | 去除個資欄後 | 去除個資欄後 | 入庫時拿掉欄位 |
| 公司內部或客戶營運資料 | 否 | 否 | 不進任何發布管道，先問資料擁有者 |

衍生資料繼承**所有輸入中最嚴格**的條件；任一輸入是 HOLD，衍生品就是 HOLD。

2. **「未標示授權」有兩種做法，依情況選一種**：
   - (a) 照常展示：來源卡標「授權待確認」、保留原始連結與取得日期，接到權利人異議就下架。適合政府或公共機構來源（多數未標示但本意公開），隱藏會讓網站缺很多基本圖層；風險是權利人事後異議，要有下架流程。
   - (b) 先 HOLD 不公開，詢問來源機關。適合商業或個人來源、含第三方權利或明顯不打算公開的資料。
   (a) 不是通則；不是公共機構來源時預設走 (b)。
3. **站主限定（owner-only）圖層**：
   - 資料放私人儲存，不進 git、公開 CDN、建置產物。
   - 瀏覽器向自己的後端代理請求；代理驗證登入與站主身分，才從私人儲存轉送。
   - 代理只接受**白名單裡的精確 key**，不接受任意路徑；檔名用內容雜湊，重產時白名單的大小與雜湊要同步更新。
   - PMTiles 要支援 Range 請求，並限制單次 Range 大小（見 [10-03](10-03-pmtiles-range-cdn-cors.md)）。
   - 反向代理對每個私人家族寫精確 location，家族前綴下其他路徑一律回 404，不要落到單頁應用 fallback。
   - 寫部署契約測試：每個私人家族在代理白名單、開發環境 proxy、反向代理、公開上傳白名單的「排除」四處都有登記；漏一處測試就紅。
   - 圖例或來源卡標「站主限定」與原因代碼；授權解除前不得公開。
4. **分析或資料倉庫端**：受限資料標 `DISPLAY_ONLY` 或 `HOLD` 與解鎖條件，對外分析工具不回傳原始值，只回彙總或「不可用」。

## 怎麼偵測
- 通用：公開目錄或 CDN 同步清單出現授權欄為 HOLD 或未確認的檔案；來源卡缺授權欄；新增私人家族後正式環境回首頁 HTML。
- 通用：匿名請求私人 API 應回 401 或 403；家族前綴下未登記路徑應回 404 而非 200。
- 搜尋：`location\s+(/|\^~)\s*/?api/private` 沒有對應「家族前綴 `return 404`」的 location（反向代理設定檔，僅限 nginx）。
- 搜尋：授權欄為 `HOLD|UNCONFIRMED` 的資料集，檔名出現在公開上傳清單內（any）。

## 出處
- 政府資料開放授權條款第 1 版（含第二條授權範圍、第三條標示、第四條與 CC BY 4.0 相容）：https://data.gov.tw/license ；ODbL 見 [02-03](../02-basemaps/02-03-osm-data-license-vs-tile-policy.md)。
- 相關卡：[02-03](../02-basemaps/02-03-osm-data-license-vs-tile-policy.md)、[07-14](../07-performance/07-14-open-data-pii-column-exclusion.md)、[10-03](10-03-pmtiles-range-cdn-cors.md)、[10-04](10-04-public-token-vs-secret.md)、[16-05](../16-spatial-analysis/16-05-geocoding-precision-and-routing.md)。
- 實例：[mini-taiwan-pulse 私人 Range 代理](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/server/coral-private/coral-private-server.mjs)、[反向代理精確 location](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/nginx.conf)、[部署契約測試](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/__tests__/deployContract.test.ts)、[土壤液化站主限定交接](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/soil-liquefaction/handoff.md)（新增私人家族漏改反向代理，正式站回首頁 HTML）。

