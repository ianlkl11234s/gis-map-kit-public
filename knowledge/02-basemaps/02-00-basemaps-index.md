---
id: 02-00
title: 底圖總表：選型、授權計費、客製、切換、attribution、深淺色、自託管與地形
topic: 02-basemaps
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [總表, 底圖, 選型, 授權, 計費, attribution, setStyle, PMTiles, 地形, 深淺色]
---

## 原則
先把地圖拆成地理資料、底圖服務、渲染 SDK、格式儲存四層，先定 SDK 與計費授權，再選底圖；流量不可控的頁面預設自託管。要做事前先查下表對應的卡。

## 對照表

### 選型、授權與計費
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 比較廠商時拉成一張大表 | [02-01](02-01-four-layers-data-tiles-sdk-format.md) | 四層分別決定，先定 SDK 與計費授權，再選底圖與格式 |
| 要挑底圖來源 | [02-02](02-02-basemap-selection-decision.md) | 流量不可控的公開頁用自架 PMTiles，不用 OSM 公用圖磚；費用以官方當期頁面為準，上線前目視確認國界與中文地名 |
| 想用 OSM 公用圖磚 | [02-03](02-03-osm-data-license-vs-tile-policy.md) | OSM 資料可自由用不代表圖磚伺服器可用；正式站、嵌入頁、離線版改自託管或條款清楚的圖磚，並標示 OSM |
| 用 Mapbox 想省錢或管 token | [02-04](02-04-mapbox-billing-token-license.md) | 只換圖磚省不到錢，要連函式庫一起換；流量不可控頁預設 MapLibre＋自託管；token 只用 public scope 並限網域 |

### 客製與切換
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 要改底圖配色、地名、語言、字型 | [02-05](02-05-style-customization-by-code.md) | 優先用執行期 API 覆寫官方 style，不先進 Studio 重做；覆寫要能還原，在 style.load 重套 |
| 換底圖後自己的圖層或 terrain 消失 | [02-06](02-06-setstyle-wipes-custom-layers.md) | 一律 `setStyle(url, { diff: false })` 完整重載，自管 source、layer、terrain 全放進單一 style.load handler 重建 |
| 底圖與資料看不清楚、深淺色切換 | [02-08](02-08-dark-light-basemap-vs-data-contrast.md) | 壓低底圖對比讓它退後，深、淺兩種底圖都驗色階；資料層插在地名之下 |

### Attribution
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 畫面要乾淨、窄螢幕放不下版權 | [02-07](02-07-attribution.md) | 底圖版權與資料來源分開標示，版權列留在最上層且窄螢幕可見，不為美觀隱藏 |

### 自託管與地形
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 要免 key、免 per-load 費用或離線 | [02-09](02-09-self-hosted-pmtiles-basemap.md) | MapLibre＋自託管 PMTiles（需 HTTP Range）；Mapbox GL 只能靠非公開 API 接，能換就換 |
| 自烘 DEM 的 terrain-RGB | [02-10](02-10-dem-terrain-rgb-encoding-and-bathymetry.md) | 編碼、nodata 哨兵、缺磚策略、誇張倍率在一處定義前後端共用；nodata 用精確哨兵不用深度門檻 |
| 山體陰影、坡度坡向、等深線選哪種形態 | [02-11](02-11-hillshade-slope-aspect-isobath-forms.md) | 只當襯底用預烤影像；要點選查值與分級說明才用分級向量（PMTiles） |

## 相關主題
- 深淺色下的色階：[05-03](../05-color/05-03-dark-light-ramp-direction.md)。
- PMTiles 部署與 Range：[06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)、[06-03](../06-data-formats/06-03-gzip-breaks-range-requests.md)。

## 出處
各項依據見對應卡片。
