---
id: 02-09
title: 自託管 PMTiles 底圖：MapLibre＋Protomaps，與 Mapbox 的接法差異
topic: 02-basemaps
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, leaflet]
tags: [PMTiles, Protomaps, MapLibre, addProtocol, HTTP Range, R2, 自託管, glyphs, sprite, 離線, mapbox-pmtiles]
---

## 原則
要免 key、免 per-load 費用或離線的底圖，用 MapLibre＋自託管 PMTiles（需 HTTP Range）；Mapbox GL 只能靠第三方非公開 API 接 PMTiles，能換 MapLibre 就換。

## 症狀
想要免 key、無 per-load 費用、可離線的底圖；或同一份 PMTiles 在 Mapbox GL 與 MapLibre 的接法不一樣，升版後壞掉。

## 原因
PMTiles 是單檔圖磚金字塔，用 HTTP Range 讀取，不需圖磚伺服器。MapLibre 官方以 `addProtocol` 支援；Mapbox GL 沒有官方支援，需第三方套件以非公開 API 註冊 source type。

## 解法
1. 取得或自製 Protomaps basemap 的 PMTiles（OSM 衍生，須標 OSM，見 [02-03](02-03-osm-data-license-vs-tile-policy.md)）。
2. 放到支援 Range 的靜態主機或物件儲存（例如 R2 儲存每 GB-月 $0.015、egress 免費，另有免費額度；以官方定價為準）。跨網域時 CORS 必須允許 `range` header。
3. MapLibre：註冊 pmtiles protocol，手寫或用 Protomaps 工具產生 Style JSON；網址由環境變數指定，開發環境可指向本機檔。
4. Mapbox GL：必須用第三方 pmtiles source 套件，且是非公開 API；重複註冊會 throw；套件升版要比對。若可行，優先改用 MapLibre。
5. glyphs 與 sprite 也是外部依賴：Protomaps 預設指向其公開 GitHub Pages，正式站建議自託管。
6. 上線前驗：`curl -r 0-16383` 回 206；打開地圖有後續 Range 請求；中文地名與整體美觀度目視確認（未必優於 Mapbox 官方底圖）。
7. 單一 PMTiles 檔不適合高頻更新的即時資料。

## 怎麼偵測
- 通用：Network 沒有 206；底圖空白但沒有錯誤；glyph 請求失敗。
- 搜尋：`addProtocol\(['"]pmtiles`、`pmtiles://`；Mapbox 專案內出現 `setSourceType`（適用 stack：maplibre, mapbox-gl）。

## 出處
- 官方：docs.protomaps.com/pmtiles/、docs.protomaps.com/basemaps/downloads、developers.cloudflare.com/r2/pricing/。Protomaps 官方 PMTiles 頁列出支援 MapLibre、Leaflet、OpenLayers，未提 Mapbox。
- 相關卡：[02-03](02-03-osm-data-license-vs-tile-policy.md)、[02-04](02-04-mapbox-billing-token-license.md)。
- 實例：[嵌入頁自託管底圖設定](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/embed/basemapStyle.ts)（[commit d36d7871](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/d36d78715a671181f7edd691c4a450cb9aa3577f)）、[Mapbox 版第三方 pmtiles 註冊](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/pmtilesSourceType.ts)。
