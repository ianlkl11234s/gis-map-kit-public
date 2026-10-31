---
id: 10-03
title: PMTiles 上線檢查：要回 206、CORS 放行 range、不被 CDN 快取成錯誤頁
topic: 10-ops
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [PMTiles, Range, 206, CORS, ETag, CDN, 大檔, 物件儲存, 同源]
---

## 原則
PMTiles 上線要確認 Range 請求回 206、跨網域時儲存端 CORS 放行 range 與 etag、且網址沒有被 CDN 快取成錯誤頁；能同源提供就同源。

## 症狀
- 回 200 而非 206、log 只有 header 讀取：見 [06-03](../06-data-formats/06-03-gzip-breaks-range-requests.md)。
- 跨網域時 console 出現 CORS 錯誤，或 `etag` 讀不到。
- PMTiles URL 回的是 HTML 錯誤頁（被快取的 404，見 [06-04](../06-data-formats/06-04-cache-immutable-404-and-stale-edge.md)）。

## 原因
PMTiles 靠 HTTP Range Request 只抓需要的圖磚。伺服器 gzip 讓 Range 回 200 的原因與修法見 [06-03](../06-data-formats/06-03-gzip-breaks-range-requests.md)；本卡是上線檢查清單，另補儲存端 CORS 與託管選項。

## 解法
排查順序：
1. 回應是不是 **206**、`content-range` 總大小對不對：判斷與修法見 [06-03](../06-data-formats/06-03-gzip-breaks-range-requests.md)。
2. 前端與儲存不同網域 → CORS 允許 header `range`、`if-match`，exposeHeaders `etag`，methods GET／HEAD；自架 nginx／Caddy 要自己處理 OPTIONS 預檢。
3. 有沒有被 CDN 快取成錯誤頁或供舊檔（見 [06-04](../06-data-formats/06-04-cache-immutable-404-and-stale-edge.md)）。
4. `content-type` 與 MIME 設定。

做法選項：
- **同源提供**（放同網域路徑）最省事，避開 CORS。
- 託管有單檔上限時，用 Worker 讀物件儲存，實作 GET／HEAD、Range 回 206、`If-None-Match` 回 304。
- 計費注意：每個 Range 圖磚請求在多數雲端儲存計為一次 GET。
- 私有 PMTiles：後端 sidecar 代理並限制單次 Range 大小。

## 怎麼偵測
- 通用：開 DevTools Network，篩 `.pmtiles`，看 CORS 錯誤、`etag` 是否讀得到、content-type 是否正確（206 檢查見 [06-03](../06-data-formats/06-03-gzip-breaks-range-requests.md)）。
- 搜尋：前端設定 PMTiles URL 指向另一網域但儲存設定沒有 CORS 規則；託管設定缺 Worker／Range 處理而檔案超過單檔上限（適用 stack：mapbox-gl、maplibre + pmtiles protocol）。

## 出處
- PMTiles 官方文件〈Cloud Storage〉（https://docs.protomaps.com/pmtiles/cloud-storage）：需支援 Range、CORS 範例、R2／GCS 支援 HTTP/2、S3 僅 HTTP/1.1。
- 實例：[nginx.conf（私有 PMTiles 由 sidecar 代理並限制單次 Range 大小）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/nginx.conf)。

