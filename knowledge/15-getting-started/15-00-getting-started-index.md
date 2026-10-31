---
id: 15-00
title: 入門總表：拿到資料到第一張網頁地圖，遇到什麼先看哪張
topic: 15-getting-started
kind: catalog
scope: public
evidence: General
stacks: [any]
tags: [入門, 總表, 座標系統, GeoJSON, 本機 server, 工具鏈, 最小骨架]
---

## 原則
入門依資料流程走：先認座標系，再確認 GeoJSON 結構，接著用本機 server 開頁面，需要轉檔時挑工具，最後套最小骨架。每一步畫面空白或位置不對時，回到同一步的卡檢查，不要跳去改樣式。

## 對照表

| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 第一次拿到政府資料，欄位是經緯度還是公尺不確定；點跑到海上或完全看不到 | [15-01](15-01-crs-basics-identify-and-convert.md) | 網頁地圖只收 WGS84 經緯度；先認出座標系，轉換在預處理做，量距離與面積用投影座標或測地函式 |
| 自己寫或從 CSV 轉出的 GeoJSON，點跑到南極或印度洋；檔案打不開 | [15-02](15-02-geojson-structure-and-bad-files.md) | 一律 FeatureCollection、座標順序 [經度, 緯度]，數字屬性存數字，缺值用 null |
| 雙擊 HTML，底圖有但自己的資料沒畫 | [15-03](15-03-local-server-file-protocol-cors.md) | 一律透過本機 HTTP server 開，不用 `file://`；本機 PMTiles 要用支援 Range（回 206）的 server |
| 拿到 SHP、KML、CSV，不知道先用什麼工具 | [15-04](15-04-toolchain-when-to-use.md) | 重的事（轉座標、轉格式、簡化、切圖磚）在進網頁前用命令列做，且每一步可重跑；前端只畫與互動 |
| 第一次做網頁地圖，不知道最少要寫什麼 | [15-05](15-05-first-web-map-skeleton.md) | 底圖、資料圖層、圖例、點擊 popup 四件事；圖例與樣式共用同一組顏色與門檻，缺值顯示「無資料」 |

## 閱讀順序
[15-01](15-01-crs-basics-identify-and-convert.md) 座標 → [15-02](15-02-geojson-structure-and-bad-files.md) GeoJSON → [15-03](15-03-local-server-file-protocol-cors.md) 本機 server → [15-04](15-04-toolchain-when-to-use.md) 工具鏈 → [15-05](15-05-first-web-map-skeleton.md) 最小骨架。

## 相關主題
- 骨架完成後選底圖：[02-02](../02-basemaps/02-02-basemap-selection-decision.md)；資料格式怎麼選（GeoJSON、PMTiles 何時換）：[06-01](../06-data-formats/06-01-format-selection-decision.md)、[06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)。
- 資料量變大、不知道怎麼畫：[14-00](../14-scale-density/14-00-scale-density-decision-table.md)；一路到靜態形式的選擇：[04-20](../04-effects-catalog/04-20-static-forms-catalog.md)。
- 圖層該有透明度、圖例、popup、選單：[09-02](../09-design-system/09-02-layer-ux-four-iron-rules.md)。
- 作者預設的技術選擇與偏好：[13-00](../13-author-taste/13-00-taste-overview.md)。

## 出處
各項依據見對應卡片。
