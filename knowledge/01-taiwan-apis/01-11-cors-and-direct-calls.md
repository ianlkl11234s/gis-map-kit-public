---
id: 01-11
title: 瀏覽器直呼外部 API：先查 CORS，本機 proxy 部署後會失效
topic: 01-taiwan-apis
kind: decision
scope: public
evidence: Observed
stacks: [any]
tags: [CORS, proxy, 403, preflight, vite, nginx, Cloudflare Worker, 快照, Range]
---

## 原則
預設不讓瀏覽器直呼外部 API：先下載成快照或由後端抓取，前端只讀自家資料；只有官方文件記載允許跨域的公開服務才直連，且直連前在瀏覽器實測一次。

## 症狀
curl 正常，瀏覽器 console 出現 CORS error 或 403；本機開發正常，部署後全壞。

## 原因
- 來源沒有設 CORS，或對瀏覽器 User-Agent／preflight 回 403。
- 本機用 dev proxy 繞過，部署環境沒有同樣的轉送。
- 自家轉送沒帶 Range header，PMTiles 之類的 Range 請求會壞。

## 解法
由簡到繁，能用前面的就不用後面的：
1. 預先下載成快照放進自己的網站（最簡單最穩）。
2. 由後端抓取後寫入資料庫或靜態檔，前端只讀自家資料。
3. 正式環境用後端 proxy（nginx location、邊緣 Worker）；proxy 要轉送 Range。
4. 只有「官方允許跨域」的公開服務才前端直連；有文件記載才算數（例：農業部文件記載 CORS 全開；NCDR 颱風 KML 無 CORS）。多數平台沒有實測紀錄，直連前在瀏覽器實測一次。
5. 若程式依賴 dev proxy 才拿得到資料，README 必須寫明正式環境的替代路徑。
6. 網站若設 CSP，外部網域要列進白名單；做法見 [10-24](../10-ops/10-24-csp-for-map-sites.md)。

## 怎麼偵測
- 通用：只有開發環境能抓到資料；Network 的 preflight（OPTIONS）失敗。
- 搜尋：`server\.proxy|proxy_pass`（沒有對應的正式部署說明）；前端直接 `fetch\(['"]https://` 打政府主機（適用 stack：any）。

## 出處
- 一般建議：瀏覽器同源政策與 CORS 為標準行為（MDN）。
- 相關卡：[01-07](01-07-local-and-other-platforms.md)。
- 實例：[CelesTrak 對瀏覽器 UA 與 preflight 回 403，改讀後端同步的資料](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)、[修正 commit](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/3fb4d4b49108b0378205b25a4ecc8cbed41f3b83)；[nginx 轉送設定（帶 Range）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/nginx.conf)。
