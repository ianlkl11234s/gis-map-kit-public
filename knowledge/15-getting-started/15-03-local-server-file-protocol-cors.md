---
id: 15-03
title: 雙擊打開 HTML 地圖卻讀不到資料：file:// 不能 fetch，要開本機 HTTP server
topic: 15-getting-started
kind: pitfall
scope: public
evidence: General
stacks: [any]
tags: [file://, 本機 server, python3 -m http.server, npx serve, CORS, 同源政策, fetch, Range, PMTiles, 入門]
---

## 原則
地圖頁一律透過本機 HTTP server 開（`http://localhost`），不要雙擊 `file://`；本機 PMTiles 要用支援 Range（回 206）的 server。

## 症狀
- 雙擊打開 index.html，底圖出得來，自己的 GeoJSON 卻沒畫。
- console 寫 `CORS policy`、`origin 'null'` 或 `Failed to fetch`。
- 同一份程式，同學用 VS Code Live Server 正常，自己雙擊打開就壞。
- 本機 PMTiles 用雙擊打開完全不動。

## 原因
- 網址是 `file:///...` 時，瀏覽器把頁面的來源（origin）當成 `null`。`fetch()`、`addSource({ data: 'x.geojson' })` 讀本機檔，被同源政策擋下。
- **CORS**（跨來源資源共享）是伺服器用回應標頭告訴瀏覽器「允許哪些網站讀我」。瀏覽器才會檢查，curl、Python 不檢查，所以「curl 抓得到、網頁抓不到」是常態。
- **Range 請求**：PMTiles 只下載檔案中的一小段（`Range: bytes=...`，伺服器要回 206）。`file://` 沒有 HTTP，也就沒有 Range。

## 解法
1. **開一個本機 HTTP server**，在專案資料夾執行其中一個：
   - `python3 -m http.server 8000`，然後開 `http://localhost:8000/`。
   - `npx serve .`，或 VS Code 的 Live Server 擴充。
   - 用 Vite 等工具建的專案：`npm run dev`。
2. **PMTiles 要用支援 Range 的 server**：Python 標準函式庫的 `http.server` 不處理 Range（一律回整個檔案），GeoJSON 可以用它，PMTiles 改用 `npx http-server` 或 `npx serve` 等支援 Range 的 server，並在 Network 分頁確認回應是 206。
3. **真的只能雙擊打開時**（例如作業要求單一檔案）：把資料寫成 `.js`，`const DATA = { "type": "FeatureCollection", ... }`，用 `<script src="data.js">` 載入，再 `addSource({ type: 'geojson', data: DATA })`。只適合小資料（數 MB 內）。
4. **外部 API 的 CORS** 是另一件事：本機 server 解決不了別人的伺服器不給讀。處理方式（先下載快照、後端轉送）見 [01-11](../01-taiwan-apis/01-11-cors-and-direct-calls.md)。
5. 上線後 PMTiles 的 206、CORS 與 gzip 問題見 [10-03](../10-ops/10-03-pmtiles-range-cdn-cors.md)、[06-03](../06-data-formats/06-03-gzip-breaks-range-requests.md)。

## 怎麼偵測
- 通用：網址列開頭是 `file://`；console 出現 `origin 'null'`。
- 搜尋：README 或作業說明叫人「直接打開 index.html」，但程式裡有 `fetch\(|addSource\(.*data:\s*['"]|new PMTiles\(`（適用 stack：any）。
- PMTiles：Network 分頁該請求是 200 而不是 206，或完全沒有發出。

## 出處
- MDN：Same-origin policy、CORS、HTTP Range requests。
- Python 文件：`http.server` 模組。
- 相關卡：[01-11](../01-taiwan-apis/01-11-cors-and-direct-calls.md)（外部 API CORS）、[10-03](../10-ops/10-03-pmtiles-range-cdn-cors.md)（PMTiles 上線檢查）、[15-05](15-05-first-web-map-skeleton.md)（第一張地圖範本）。

