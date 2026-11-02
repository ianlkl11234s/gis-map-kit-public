---
id: 08-05
title: 多圖層疊放順序：登記順序就是 z-order，大面積在底、選取圈在頂，動態重建會跑到最上層
topic: 08-multi-layer
kind: pattern
scope: public
evidence: Observed
stacks: [mapbox-gl, maplibre, leaflet, openlayers, deck.gl]
tags: [z-order, 疊放, 圖層順序, beforeId, addLayer, 遮蔽, 選取圈, 熱力圖, 底圖標籤, raster, 重建]
---

## 原則
用一份有序的登記陣列集中決定圖層的 z-order（陣列順序即疊放順序），新增圖層時明確決定位置；自訂圖層要放在底圖標籤之下，動態重建後重新排序。

## 症狀
- 打開一張全島 raster（例如熱島、影像）後，其他點圖層全被蓋住。
- 兩層同開時，其中一層的等級色被另一層的點遮住，改了圖層類型後它又跑到最上面。
- 選取高亮被別的圖層蓋住；熱力圖壓在點上面看不到點。
- 底圖的道路標籤被面圖層蓋掉。

## 原因
地圖庫的疊放順序通常等於「加入圖層的順序」。順序若散落在各圖層自己的 hook 裡，結果取決於誰先 mount；且動態 `remove`＋`addLayer`（例如切類型時重建）會讓該圖層跑到最上層。

## 解法
1. **順序集中管理**：用一份有序的登記陣列一次加入全部圖層，**陣列順序就是 z-order**；新增圖層時要明確決定插在哪，而不是附加在最後。順序有意義的地方在註解寫理由（「放最前是刻意的：全島滿版 raster 排後面會蓋掉所有點圖層」）。
2. **分層分帶（建議的通用規則）：**

| 由下到上 | 內容 |
|---|---|
| 最底 | 大面積 raster／影像、面量圖填色 |
| 中下 | 熱力圖、密度格網（要被點壓在下面） |
| 中 | 線、路網 |
| 中上 | 點、POI |
| 上 | 標籤、箭頭、動態物件 |
| 最上 | 選取圈／高亮（全站同時只有一個，用共用元件畫，各圖層不自己畫高亮） |

3. **底圖標籤用錨點**：自訂圖層加入時指定 `beforeId`（第一個標籤層的 id），讓標籤永遠在上面（mapbox-gl／maplibre）；OpenLayers 用 `zIndex`；Leaflet 用 `pane`；deck.gl 的 `getLayers()` 順序與 `beforeId`。
4. **動態重建後要重新排序**：會 `remove`＋`addLayer` 的圖層（切類型、切資料源），要在重建完成後重新放回應有的位置；彼此有遮蔽關係的圖層要監聽對方的重建事件，一起重建。
5. **多來源同一圖層**（總覽層＋細節層）：切換、透明度、z-order、縮放比例與圖例都要對兩個 source 一起驗收。
6. 驗收：開兩個彼此重疊的圖層，兩種開啟順序各看一次，再切一次其中一層的類型，順序應該不變。

```ts
// mapbox-gl／maplibre：自訂圖層放在標籤層之下
const firstLabel = map.getStyle().layers.find((l) => l.type === "symbol" && l.layout?.["text-field"])?.id;
map.addLayer({ id, type: "fill", source, paint }, firstLabel);
```

## 怎麼偵測
- 通用：開兩個彼此重疊的圖層（例如面圖層＋點圖層），兩種開啟順序各看一次；切換圖層類型後再看一次。
- 搜尋：
  - 附加在最後：`map\.addLayer\(\{[^}]*\}\)`（沒有第二個參數）散見於各 hook（mapbox-gl、maplibre）。
  - 動態重建：`removeLayer\(.*\)[\s\S]{0,200}addLayer\(` 且重建後沒有 `moveLayer|beforeId`（mapbox-gl、maplibre）。
  - Leaflet：`L\.(geoJSON|tileLayer)\(` 沒有指定 `pane`/`zIndex`；OpenLayers：`new (Vector|Tile)Layer\(` 沒有 `zIndex`。

## 出處
- Mapbox GL JS／MapLibre GL JS 文件：`addLayer` 的 `beforeId` 參數；Leaflet panes；OpenLayers layer `zIndex`。
- 相關卡：[14-04](../14-scale-density/14-04-overlap-order-and-opacity.md)（同一圖層內的 sort-key；本卡只管圖層之間的先後）。分帶表是通用整理，不是特定專案的正式規格。
- 實例：[src/map/overlayRegistry.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/overlayRegistry.ts)（依陣列順序加入圖層，順序即 z-order）。
