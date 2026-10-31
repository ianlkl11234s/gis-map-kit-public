---
id: 02-03
title: OSM 的「資料授權」不等於「圖磚伺服器使用政策」
topic: 02-basemaps
kind: pitfall
scope: public
evidence: General
stacks: [any]
tags: [OSM, ODbL, tile.openstreetmap.org, 使用政策, 預抓, 離線, User-Agent, 封鎖, 標示]
---

## 原則
「OSM 資料可自由使用」不代表可以用 OSM 公用圖磚伺服器：正式站、嵌入頁、離線版一律改用自託管或條款清楚的圖磚，並一律標示 OSM。

## 症狀
因為「OSM 資料可以自由使用」，就把 `tile.openstreetmap.org` 寫進正式站、離線版，或做批量預抓；之後被限流或封鎖。

## 原因
兩件事分開：
- **資料授權**：OSM 資料為 ODbL，用了要標示（可寫「© OpenStreetMap contributors」，或把「OpenStreetMap」連到 /copyright，標示須可見、可讀）。
- **圖磚伺服器政策**：OSM 基金會的公用圖磚伺服器是共享的免費資源，政策禁止大量下載、預抓、離線使用，要求清楚標示授權、送有效 Referer 與可辨識的 User-Agent，並保留「無預警封鎖」的權利。

## 解法
1. 正式站、嵌入頁、離線版不要用 OSM 公用圖磚；改用自託管圖磚（見 [02-09](02-09-self-hosted-pmtiles-basemap.md)）或有條款可循的商業／開放服務。
2. 只在原型或低流量實驗用公用圖磚，並遵守標示與 User-Agent。
3. 無論用哪個底圖，只要內容源自 OSM，都要標示 OSM。
4. Protomaps 的官方 basemap build 屬 OSM 衍生，同樣須標 OSM（Produced Work，ODbL）。

## 怎麼偵測
- 通用：打開 Network 看到 `tile.openstreetmap.org`；離線包內仍有外部圖磚請求。
- 搜尋：`tile\.openstreetmap\.org`、`\{s\}\.tile\.openstreetmap`（適用 stack：any）。

## 出處
- 官方：operations.osmfoundation.org/policies/tiles/、osmfoundation.org/wiki/Licence/Attribution_Guidelines、docs.protomaps.com/basemaps/downloads。
- 相關卡：[02-09](02-09-self-hosted-pmtiles-basemap.md)、[11-09](../11-extras/11-09-pwa-offline.md)（離線圖磚快取的授權問題）、[10-22](../10-ops/10-22-data-license-tiers-and-owner-only-layers.md)（資料授權分級）。
- 實例：[嵌入頁底圖評估提案（曾評估公用圖磚後否決）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/archive/2026-10-04/proposal/embed-basemap-osm.md)。
