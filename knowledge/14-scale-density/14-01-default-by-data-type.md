---
id: 14-01
title: 先看資料是什麼，再決定畫法：點、線、面、網格、行政區統計、軌跡、移動物件、事件各自的預設
topic: 14-scale-density
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [資料分類, 點, 線, 面, 網格, H3, 行政區, 統計, 軌跡, 移動物件, 事件, 預設畫法]
---

## 原則
先看資料「讀者要讀到什麼」，再選畫法：幾何型別不等於語意，設施點、事件點、移動物件都是 Point 但畫法不同。同一類資料全站用同一種畫法。

## 症狀
- 行政區統計被畫成一堆點；軌跡被當成獨立點畫；事件和設施用同一種點，看不出哪個在「發生中」。
- 同一份資料在不同圖層裡有不同畫法，使用者要重新學。

## 原因
幾何型別（Point／LineString／Polygon）不等於語意。設施點、事件點、移動物件都是 Point，但讀者要從圖上讀到的東西不同。

## 解法
| 分類 | 讀者要讀到 | 預設畫法 | 要避免 |
|---|---|---|---|
| 設施點（POI） | 在哪、什麼類 | 圓點＋類別色，固定尺寸階；形狀本身有語意才用 icon | 每類一種 icon、數萬個 icon |
| 線（路網、河川、管線） | 連通與階層 | 線寬隨 zoom 插值、階層用 sort-key 讓主幹在上 | 低 zoom 線寬太粗蓋住面 |
| 面（分區、覆蓋範圍） | 範圍與類別 | 半透明填色＋獨立外框子圖層 | 多層覆蓋面疊成不透明（[05-07](../05-color/05-07-alpha-stacking-and-fill-opacity.md)） |
| 行政區統計 | 區域之間的比較 | 分級面量圖，同時只開一張（[08-06](../08-multi-layer/08-06-how-many-layers-at-once.md)）；層級由使用者選或隨尺度換 | 用點代表行政區、把缺值畫成 0（[05-04](../05-color/05-04-null-is-not-zero-color.md)） |
| 規則網格（H3、方格） | 密度與熱點，不受行政界影響 | H3 預設；官方方格資料才用方格；空格不畫 | 把空格補 0 |
| 泡泡（比例符號） | 量的大小 | 面積∝值、上下限固定、大的先畫 | 半徑∝值（誇大差距） |
| 軌跡 | 路線與頻率 | 線，依縮放換抽稀層級（[14-07](14-07-moving-objects-and-trails-at-scale.md)） | 把每個軌跡點畫成圓 |
| 即時移動物件 | 現在在哪、往哪走 | 平面點，拉近換方向箭頭；GPU 批次繪製 | 每台車一個 DOM marker |
| 事件 | 發生在哪、多嚴重、多新 | 點＋語意色或大小；「進行中」才加脈衝 | 舊事件和新事件同樣顯眼 |
| 連續場 | 空間變化 | 影像圖磚或粒子 | 用點陣模擬連續場 |

分類之後再看數量（[14-02](14-02-point-count-thresholds.md)）與縮放（[14-03](14-03-zoom-handoff-pitfalls.md)）。

## 怎麼偵測
- 通用：讀圖例，問「這層讀者要讀到什麼」；答案和畫法對不上就是選錯。
- 搜尋：行政區統計資料用 `circle` 圖層（看 source 名稱或欄位含 `county|town|village|admin`）；泡泡半徑直接 `["get", value]` 沒有開根號（`sqrt`）（適用 stack：mapbox-gl、maplibre）；`new mapboxgl.Marker` 或 `L.marker` 出現在迴圈裡且資料是移動物件。

## 出處
- 一般地圖學：比例符號面積編碼、面量圖用於比率而非總數。
- 尺寸與透明度數值見 [09-10](../09-design-system/09-10-map-symbol-size-tiers.md)；icon 與 circle 選用、疊放順序見 [09-10](../09-design-system/09-10-map-symbol-size-tiers.md)、[08-05](../08-multi-layer/08-05-layer-stacking-order.md)。
- 實例：[mini-taiwan-pulse 圖層樣式規範（icon、網格空格不畫等規則）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)。
- 實例：[移動物件的平面點與方向箭頭](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/flatMovingLayers.ts)。
