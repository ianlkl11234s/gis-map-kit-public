---
id: 06-03
title: PMTiles 本機正常、上線一個點都沒有：伺服器 gzip 讓 Range 請求回 200 而不是 206
topic: 06-data-formats
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [PMTiles, Range, 206, gzip, nginx, content-range, CORS, 反向代理, 部署]
---

## 原則
PMTiles 所在路徑一律關閉 gzip，部署後用 `curl -I -H "Range: bytes=0-16383"` 確認回 206 且 content-range 總大小正確，再宣告上線。

## 症狀
- 本機開發完全正常，部署後圖層空白，沒有 JS 錯誤。
- Network 面板的 PMTiles 請求狀態是 200，而不是 206 Partial Content。
- 伺服器日誌只看到讀 header（前 16 KB）的一次請求，後面沒有任何 tile 範圍請求。

## 原因
- PMTiles 靠 HTTP Range 讀檔案的一部分。反向代理（如 nginx）若對該路徑開了 gzip，Range 請求會被當整檔壓縮回應，回 200 而不是 206，前端 reader 就讀不到正確位移。
- PMTiles 本身的 tile 已壓縮，再 gzip 沒有收益。
- 跨網域時，儲存端的 CORS 也必須允許 `Range` 請求標頭，並 expose `Content-Range`／`ETag`。

## 解法
1. PMTiles 所在 location 關閉 gzip（nginx：`gzip off;`），並確認不被外層壓縮設定覆蓋。
2. CDN 也不要對該路徑重壓縮或改寫 Range。
3. 部署後必做驗證：
   - `curl -I -H "Range: bytes=0-16383" <url>` 必須是 `206`；
   - `content-range` 的總大小要等於本機檔案大小（不等＝CDN 吐了舊檔，見 [06-04](06-04-cache-immutable-404-and-stale-edge.md)）。
4. 把這項驗證放進部署檢查清單，而不是靠人眼看地圖。完整上線檢查（CORS、託管選項、計費）見 [10-03](../10-ops/10-03-pmtiles-range-cdn-cors.md)。

## 怎麼偵測
- 通用：PMTiles 圖層上線後空白；請求狀態 200；日誌只有 header 讀取。
- 搜尋：nginx／反向代理設定中，`\.pmtiles` 的 location 沒有 `gzip off`，或全站 `gzip on` 且 `gzip_types` 含 `application/octet-stream`（適用 stack：任何用 pmtiles 的前端）。

## 出處
- 官方：PMTiles 文件的 Range 與 CORS 需求。
- 相關卡：[06-04](06-04-cache-immutable-404-and-stale-edge.md)、[10-03](../10-ops/10-03-pmtiles-range-cdn-cors.md)。
- 實例：[mini-taiwan-pulse nginx.conf（PMTiles location 的 `gzip off`）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/nginx.conf)。

