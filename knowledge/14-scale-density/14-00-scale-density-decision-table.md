---
id: 14-00
title: 尺度與密度決策總表：資料分類 × 數量級 × 縮放尺度 → 預設畫法
topic: 14-scale-density
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [決策表, 數量級, 縮放, 熱區, 網格, cluster, PMTiles, 點, 線, 面, 移動物件, 總表]
---

## 原則
畫法由三個變數決定：資料分類、全圖總數量級、縮放尺度；先查下表定預設，再到細卡看門檻與坑。密度先調透明度，再用熱區或網格，最後才縮小點。

## 症狀
- 每加一個圖層都重新決定「要不要聚合、要不要熱區、幾級開始出點」，結果每層做法不一樣。
- 全台尺度和街區尺度用同一種畫法，遠看糊成一片、近看又太空。

## 原因
「怎麼畫」其實由三個變數決定：資料是什麼（分類）、有多少（數量級，以**全圖範圍內的總數**算）、從多遠看（縮放尺度）。少了任何一個就會選錯。

## 解法
先查下表定預設，再到細卡看門檻與坑。縮放尺度粗分：**總覽**（全國，約 z5–8）、**區域**（縣市，約 z9–11）、**街區**（z12 以上）。

| 分類 | 數量級（全圖） | 總覽 | 區域 | 街區 | 細卡 |
|---|---|---|---|---|---|
| 點（設施、POI） | ≤ 數百 | 直接畫點，不包裝 | 同左 | 點＋名稱標籤 | [14-06](14-06-small-data-no-overpackaging.md) |
| 點 | 數千（< 1 萬） | 直接畫點，透明度略降 | 點 | 點＋標籤（約 z13 起） | [14-02](14-02-point-count-thresholds.md) |
| 點 | 1–10 萬 | 熱區 | z10 起換點 | 點 | [14-02](14-02-point-count-thresholds.md)、[14-03](14-03-zoom-handoff-pitfalls.md) |
| 點 | > 10 萬 | 熱區或密度格網（向量圖磚） | 熱區或格網 | z12 起才畫單點 | [14-02](14-02-point-count-thresholds.md)、[14-05](14-05-honest-aggregation.md) |
| 線（路網、河川） | 任意 | 只留主幹或細線；線寬隨 zoom 插值 | 全部 | 全部＋端點樣式 | [09-10](../09-design-system/09-10-map-symbol-size-tiers.md)、[14-03](14-03-zoom-handoff-pitfalls.md) |
| 面（分區、覆蓋範圍） | 大面積或高頂點 | 向量圖磚、低 zoom 簡化 | 同左 | 原解析度 | [06-01](../06-data-formats/06-01-format-selection-decision.md)、[06-05](../06-data-formats/06-05-shrink-geometry-precision-simplify-columns.md) |
| 行政區統計 | 縣市 22／鄉鎮 368／村里 7,900 級 | 縣市 | 鄉鎮（界線約 z6 起） | 村里（界線約 z8 起） | [14-03](14-03-zoom-handoff-pitfalls.md)、[05-04](../05-color/05-04-null-is-not-zero-color.md) |
| 規則網格（H3、方格） | 依解析度 | 粗格（H3 res7、1–1.5 km） | 換細格（約 z9.5–10） | 細格或換回點（約 z12） | [14-03](14-03-zoom-handoff-pitfalls.md)、[14-05](14-05-honest-aggregation.md) |
| 軌跡（航跡、船跡） | 數千條以上 | 抽稀檔（每條上限點數） | 中階抽稀 | 全解析度 | [14-07](14-07-moving-objects-and-trails-at-scale.md) |
| 即時移動物件 | 數百–數萬 | 平面點（GPU 一次畫完） | 同左 | 方向箭頭（約 z12 起） | [14-07](14-07-moving-objects-and-trails-at-scale.md) |
| 事件（地震、災害、通報） | 數十–數千 | 點＋語意色；疊加多時用熱區 | 點 | 點＋popup | [14-04](14-04-overlap-order-and-opacity.md) |
| 連續場（風、溫度、雨量） | 格點 | 影像或粒子；粒子數隨 zoom 自適應 | 同左 | 同左 | [14-07](14-07-moving-objects-and-trails-at-scale.md)、[06-09](../06-data-formats/06-09-bake-vector-field-to-png.md) |

共通規則：
1. 密度的處理順序是**透明度 → 熱區／網格 → 才是縮小點**（點徑預設固定三階，見 [14-02](14-02-point-count-thresholds.md)）。
2. 聚合後的數字與未涵蓋區域要誠實表示（[14-05](14-05-honest-aggregation.md)）。
3. 少量資料不要套聚合或熱區（[14-06](14-06-small-data-no-overpackaging.md)）。
4. 疊在一起時決定誰在上面（[14-04](14-04-overlap-order-and-opacity.md)）。

作者偏好（不是業界規範；有理由可以偏離，偏離時在 README 或 PR 寫一句理由）：點徑三階與特例、遠看熱區近看單點、尺寸分階、熱區參數起點、出現縮放不統一，正本在 [14-02](14-02-point-count-thresholds.md)；軌跡抽稀兩種策略見 [14-07](14-07-moving-objects-and-trails-at-scale.md)。

## 怎麼偵測
- 通用：在總覽、區域、街區三個縮放各截一張圖；任一張糊成一片或空白，就回來查表。
- 搜尋：圖層數量級與畫法不符，例如 >1 萬點的 `type: ['"]circle['"]` 沒有 `minzoom` 也沒有配對的 `heatmap`（適用 stack：mapbox-gl、maplibre）；Leaflet 直接 `L.circleMarker` 迴圈數萬筆。
- gis-review：要求每個新圖層在描述裡寫「全圖點數」與「出點縮放」。

## 出處
- 一般地圖學：依比例尺選擇符號化與綜合（generalization）。
- 細卡：[14-01](14-01-default-by-data-type.md)～[14-07](14-07-moving-objects-and-trails-at-scale.md)；相關既有卡 [07-02](../07-performance/07-02-many-points-rendering.md)、[09-10](../09-design-system/09-10-map-symbol-size-tiers.md)、[06-01](../06-data-formats/06-01-format-selection-decision.md)、[06-05](../06-data-formats/06-05-shrink-geometry-precision-simplify-columns.md)、[08-06](../08-multi-layer/08-06-how-many-layers-at-once.md)。
- 實例：[mini-taiwan-pulse 圖層樣式規範（點、網格、熱區的規則）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)、[縮放門檻與熱區參數的共用函式](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/mapStyleScale.ts)。
