---
id: 01-07
title: 縣市平台與其他來源：個資、IP 限制、覆寫、OSM Overpass 使用政策
topic: 01-taiwan-apis
kind: catalog
scope: public
evidence: Observed
stacks: [any]
tags: [data.taipei, NCDR, 台電, 農業部, 航港局, AIS, Overpass, OSM, 行道樹, CORS, 個資]
---

## 原則
縣市平台與雜項來源逐一看下表的限制再接：自己存快照、剔除個資欄位、需要台灣 IP 的來源放國內主機、Overpass 查一次存成 GeoJSON，不在頁面載入時即時打。

## 症狀
用到這些來源時常遇到：沒有歷史版本、本機能抓部署後不能抓、API 回應含個資、瀏覽器抓不到。

## 原因
| 來源 | 要注意 |
|---|---|
| 臺北市資料大平臺 | 目錄 API 免認證；當期資料每月覆寫、無官方歷史版本；`dataset.view` 回應含承辦人姓名電話 |
| 新北、台中、高雄、台南等縣市平台 | 認證、格式、授權都未驗證，不當成正式接法 |
| NCDR 示警／震度網格 | 示警 CAP 為 Atom feed；震度網格只存最新事件；颱風 KML 無 CORS |
| 台電即時電力／輻射 | CSV 可能有 UTF-8 BOM（第一欄名多一個不可見字元）；機組名稱與主檔對不上 |
| 農業部開放資料 | 文件記載 CORS 全開；單次 9,999 筆靜默截斷；少帶特定參數回 HTML |
| 航港局 AIS | 某些端點需台灣 IP 或 Referer |
| OpenStreetMap Overpass | 官方政策：每日少於 10,000 次查詢、少於 1 GB；長期定期使用更低；收到 429/406 暫停 30 秒（官方 wiki） |

OSM「資料」授權（ODbL，須標示）不等於 OSM「公用圖磚伺服器」使用政策（禁止大量下載、預抓、離線，須清楚標示與有效 User-Agent）；後者見 [02-03](../02-basemaps/02-03-osm-data-license-vs-tile-policy.md)。

## 解法
1. 臺北市資料大平臺：自己定期存快照；不留存個資欄位；缺的年份可用網頁封存備份，但要標明。
2. 其他縣市平台：官方原文未取得前，不收為正式接法。
3. NCDR：後端抓取，歷史自存。
4. 台電：讀檔用 `utf-8-sig`；join 前先對名稱。
5. 農業部：分頁取；驗 content-type（見 [01-09](01-09-http-200-not-success-and-pagination.md)）。
6. 航港局 AIS：在國內主機執行（見 [01-14](01-14-semantics-drift-and-upstream-loss.md)）。
7. Overpass：查一次、存 GeoJSON；不要每次載入頁面都打。

## 怎麼偵測
- 通用：頁面載入時直接打 Overpass；popup 出現承辦人電話；本機正常、部署後逾時。
- 搜尋：`overpass-api\.de|overpass`（出現在前端 src）、`dataset\.view`（適用 stack：any）。

## 出處
- 官方：wiki.openstreetmap.org/wiki/Overpass_API、operations.osmfoundation.org/policies/tiles/、data.taipei/rule。
- 相關卡：[01-09](01-09-http-200-not-success-and-pagination.md)、[01-14](01-14-semantics-drift-and-upstream-loss.md)、[02-03](../02-basemaps/02-03-osm-data-license-vs-tile-policy.md)。
- 實例：[外部 collector 的台灣 IP 限制](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/EXTERNAL_COLLECTORS.md)。

