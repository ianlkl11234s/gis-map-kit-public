---
id: 02-02
title: 底圖選型：Mapbox、MapLibre＋自架 PMTiles、OpenFreeMap、CARTO、OSM 圖磚、NLSC 的費用／授權／離線取捨
topic: 02-basemaps
kind: decision
scope: public
evidence: Evaluated
stacks: [any]
tags: [底圖選型, Mapbox, MapLibre, PMTiles, Protomaps, OpenFreeMap, CARTO, OSM, NLSC, 通用版電子地圖, 離線, 費用, 國界, 地名]
---

## 原則
依情境選底圖：流量不可控的公開頁用自架 PMTiles，不用 OSM 公用圖磚；離線不用公用圖磚；費用與授權數字以官方當期頁面為準，上線前目視確認國界與中文地名。

## 症狀
不確定該用哪個底圖；流量變大後帳單暴增；被服務商封鎖；離線展示或嵌入頁出問題；中文地名或國界不符預期。

## 原因
各選項在費用、授權、離線能力與客製化上差異大，且官方條款會變。

## 解法
情境選型（建議，非唯一解；價格與條款會變，以官方當期頁面為準）：

| 情境 | 建議 | 取捨 |
|---|---|---|
| 要漂亮底圖與 3D、流量可控 | Mapbox GL JS＋官方 style＋public token | 計費照 map load 算；v2 起授權為 Mapbox TOS |
| 公開網址、流量不可控（嵌入頁、文章） | MapLibre＋自架 Protomaps PMTiles（物件儲存） | 只付儲存與少量請求，無 per-load 計費；底圖美觀度與中文地名需自行驗證 |
| 原型／課堂、不想申請帳號 | MapLibre＋OpenFreeMap（positron 適合疊資料） | 免 key、看得到街道，但無服務保證；MapLibre 官方 demo tiles 在城市尺度只剩海陸，只當備援 |
| 少量點、raster 底圖 | Leaflet＋條款清楚的 raster 圖磚 | 功能較少 |
| 離線展示 | PMTiles＋本機 HTTP server（需支援 Range） | **不可**用 OSM 公用圖磚做離線 |
| 台灣在地底圖 | NLSC 通用版電子地圖／正射影像（WMTS） | 授權與前端直連條件本卡未驗證，採用前以官方條款確認；也未驗證地名與國界處理 |
| 抽象、藝術、全球視角 | 不用外部底圖：純色背景＋自己的陸地／經緯網 | 沒有街道脈絡 |

各選項要點：
- **OSM 公用圖磚**：禁止大量下載、預抓、離線，須清楚標示並送有效 User-Agent，可能無預警封鎖，不適合正式站（見 [02-03](02-03-osm-data-license-vs-tile-policy.md)）。
- **CARTO**：條款寫明須使用其發出的 key，沒帶有效 key 的請求會加浮水印（2026-10-31 實測：沒帶 key 的 `basemaps.cartocdn.com/light_nolabels` raster 圖磚，整片蓋上「API KEY REQUIRED」字樣）；合理使用上限為非商用每月 500 萬次、商用每月 100 萬次 tile request；教育、研究屬非商用（官方 Basemap Terms）。
- **OpenFreeMap**（查證日期 2026-11-02）：不需註冊、沒有 API key；官方 FAQ 寫明可商用，公用實例不限地圖瀏覽與請求次數。須標示 OpenMapTiles 與 OpenStreetMap（OpenFreeMap 字樣官方說可省略但建議保留），MapLibre 會從樣式自動帶出完整字串，不要關掉 attribution。服務條款寫明 as-is、無 SLA、可能無預警停止；禁止自動化大量抓取（離線下載每次最多 3,000 張圖磚或 50 MB、最多 4 個平行請求）；把公用服務接進網站的人須年滿 18 歲。樣式網址：`https://tiles.openfreemap.org/styles/positron`（淺色）、`liberty`、`bright`。2026-10-31 在臺北市區縮放以瀏覽器實測：畫面清楚、無浮水印、attribution 完整。正式站流量大或需要保證時，改自架 PMTiles。
- **Mapbox**：計費、token 與授權見 [02-04](02-04-mapbox-billing-token-license.md)。
- **Protomaps／R2**：自託管接法與儲存費用見 [02-09](02-09-self-hosted-pmtiles-basemap.md)。
- **Google Maps JS API**：每 SKU 每月 10K 次免費（官方頁），Dynamic Maps 每千次單價本卡未驗證，以官方頁為準。

**國界與地名**：各底圖處理爭議地區與中文地名的方式不同，上線前以目視確認；未做系統性比對，其他底圖的國界與地名處理本卡未驗證。

## 怎麼偵測
- 通用：嵌入頁或公開頁預設 Mapbox；正式站寫了 `tile.openstreetmap.org`；CARTO URL 沒帶 key；離線版仍連外部圖磚；城市尺度用了只有海陸的 demo tiles。
- 搜尋：`tile\.openstreetmap\.org`、`basemaps\.cartocdn\.com`、`accessToken`（適用 stack：any）。

## 出處
- 官方：openfreemap.org（FAQ、/quick_start/、/tos/，條款版本 2026-10-14）、github.com/hyperknot/openfreemap（README）、mapbox.com/pricing、docs.mapbox.com/mapbox-gl-js/guides/pricing/、carto.com/legal/basemap-terms/、operations.osmfoundation.org/policies/tiles/、developers.cloudflare.com/r2/pricing/、mapsplatform.google.com/pricing/。
- 實例：[嵌入頁底圖評估提案（Mapbox 改 MapLibre＋Protomaps）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/archive/2026-10-04/proposal/embed-basemap-osm.md)、[改版 commit](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/d36d78715a671181f7edd691c4a450cb9aa3577f)。

