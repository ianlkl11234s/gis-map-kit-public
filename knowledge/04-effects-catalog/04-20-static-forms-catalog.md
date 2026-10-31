---
id: 04-20
title: 靜態表現形式總表：想表達的語意 → 表現形式 → 樣式規格 → 卡片
topic: 04-effects-catalog
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [表現形式, 靜態, 點, 線, 面, 熱區, 網格, 標籤, 圖例, 樣式規格, 總表]
---

## 原則
先講清楚要讀者讀到什麼（位置、類別、量值、密度、範圍、缺值），再從下表挑表現形式，數值照「樣式要點」起手。動態效果見 [04-00](04-00-effects-index.md)。標「未實作」的列是一般建議，不是作者經驗。

尺寸與透明度只用固定階（[09-10](../09-design-system/09-10-map-symbol-size-tiers.md)）；切換深淺底圖只換色，不改尺寸與透明度（[02-08](../02-basemaps/02-08-dark-light-basemap-vs-data-contrast.md)、[05-03](../05-color/05-03-dark-light-ramp-direction.md)）。每個以顏色或大小編碼資料的圖層都要有圖例（[09-04](../09-design-system/09-04-legend-spec.md)）。畫法隨資料量與縮放換檔見 [14-00](../14-scale-density/14-00-scale-density-decision-table.md)。

## 對照表

### 點與密度
| 想表達的語意 | 表現形式 | 樣式要點 | 卡片 | 作者實作 |
|---|---|---|---|---|
| 這裡有一個東西（位置） | 單色圓點，分三階 | 半徑固定 3／4.5／6.5 px（密集參考點／一般／少量重點），再乘大小滑桿；1 px 描邊，深底用深色、淡底用白；不隨縮放 | [09-10](../09-design-system/09-10-map-symbol-size-tiers.md)、[14-06](../14-scale-density/14-06-small-data-no-overpackaging.md) | 是 |
| 這是哪一類 | 類別色圓點，必要時 icon | 類別約 7 類以內、不循環；形狀本身有語意才用 icon（≤5k 點）；紅橘綠留給狀態；圖例色票與渲染同一常數 | [05-05](../05-color/05-05-categorical-count-and-semantic-colors.md)、[09-04](../09-design-system/09-04-legend-spec.md)、[14-01](../14-scale-density/14-01-default-by-data-type.md) | 是 |
| 這個點的數值大小 | 比例符號（半徑依數值） | 保留單一半徑表達式與描邊；圖例畫小中大三圓並標值；排序讓大的先畫、小的在上 | [14-04](../14-scale-density/14-04-overlap-order-and-opacity.md)、[09-04](../09-design-system/09-04-legend-spec.md) | 是 |
| 這裡很密集（點很多） | 熱區 | 點數 ≥1 萬低縮放換熱區，≥10 萬延到 z12 才出單點；色盤暗底越密越亮、淡底越深；不用 cluster 數字泡泡 | [14-02](../14-scale-density/14-02-point-count-thresholds.md)、[14-03](../14-scale-density/14-03-zoom-handoff-pitfalls.md)、[05-03](../05-color/05-03-dark-light-ramp-direction.md) | 是 |
| 每個點代表固定數量，要看分布 | 點密度圖（dot density） | 一點代表 N 單位、隨機散在區內，不能讀成真實位置 | [14-05](../14-scale-density/14-05-honest-aggregation.md)、[06-08](../06-data-formats/06-08-label-estimates-and-models.md) | 未實作（一般建議） |

### 面與格網
| 想表達的語意 | 表現形式 | 樣式要點 | 卡片 | 作者實作 |
|---|---|---|---|---|
| 各行政區的統計值 | 分級面量圖 | 透明度 0.55；序列色階依資料型態選；門檻人工固定、跨期不重算；1 px 底圖色細縫；縣市、鄉鎮、村里隨縮放換級 | [05-01](../05-color/05-01-color-ramp-decision-table.md)、[05-09](../05-color/05-09-fixed-breaks-across-time.md)、[14-03](../14-scale-density/14-03-zoom-handoff-pitfalls.md) | 是 |
| 值不能用面積表示（人口多的小區被淹沒） | 比例面積變形圖（cartogram） | 面積依數值變形，形狀失真，要附原圖對照 | [14-01](../14-scale-density/14-01-default-by-data-type.md) | 未實作（一般建議） |
| 兩個變數同時看 | 雙變量配色 | 3×3 色格；圖例要能讀，否則改並排兩張圖 | [05-06](../05-color/05-06-colorblind-and-similar-ramps.md) | 未實作（一般建議） |
| 規則網格的密度或指標 | H3、方格 | 透明度 0.7；0.5 px 底圖色格縫；低縮放粗格、拉近換細格或換回點；空格與缺值不畫成 0；篩選時同步篩選網格 | [14-03](../14-scale-density/14-03-zoom-handoff-pitfalls.md)、[14-05](../14-scale-density/14-05-honest-aggregation.md) | 是 |
| 缺值、遮蔽、未涵蓋 | 透明底加 45° 斜線（遮蔽用交叉斜線） | 不使用色階任何一級；圖例有獨立項 | [05-04](../05-color/05-04-null-is-not-zero-color.md)、[06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md) | 是 |
| 服務區、潛勢區、保護區 | 覆蓋範圍面 | 半透明填色 0.35＋1 px 同色邊線 0.8；外框用獨立 line 子圖層；重疊多時降透明度 | [05-07](../05-color/05-07-alpha-stacking-and-fill-opacity.md)、[14-04](../14-scale-density/14-04-overlap-order-and-opacity.md) | 是 |
| 只提示範圍的底層分區 | 背景參考面 | 填色 0.15＋0.5 px 中性灰邊 | [05-07](../05-color/05-07-alpha-stacking-and-fill-opacity.md) | 是 |
| 灰色參考線與色階 0 級 | 「0／無」用細參考線 | 亮端色階不接近灰或描邊色 | [05-02](../05-color/05-02-gray-zero-and-outline-collision.md) | 是 |

### 線
| 想表達的語意 | 表現形式 | 樣式要點 | 卡片 | 作者實作 |
|---|---|---|---|---|
| 路網、河川、管線（類別） | 類別線 | 線寬三階（z10→z14 插值：細 0.5→1、標準 1→2、強調 2→3.5）；透明度 0.85，參考線 0.6；`round` 端點與接合，行政界與網格用尖角；一般圖層不加外框 | [09-10](../09-design-system/09-10-map-symbol-size-tiers.md)、[14-03](../14-scale-density/14-03-zoom-handoff-pitfalls.md) | 是 |
| 規劃中、推估、法定界線 | 虛線 | 只用這幾種語意；dasharray 只收 `[2,2]` 與 `[4,3]` 兩種；實線不用來表示不確定；圖例用同一 dasharray | [09-10](../09-design-system/09-10-map-symbol-size-tiers.md)、[09-04](../09-design-system/09-04-legend-spec.md) | 是 |
| 線的數值大小（流量、壅塞） | 線寬表示數值 | 寬度分級、不連續縮放；圖例畫線段；高值畫在上層 | [14-04](../14-scale-density/14-04-overlap-order-and-opacity.md)、[09-04](../09-design-system/09-04-legend-spec.md) | 未實作（一般建議） |

### 影像、地形、3D、文字
| 想表達的語意 | 表現形式 | 樣式要點 | 卡片 | 作者實作 |
|---|---|---|---|---|
| 連續量測值（熱島、雨量、淹水深度） | 值編碼影像上色 | 透明度 0.7、滑桿 0.3–1.0；量測值 `nearest`、照片雲圖 `linear`；係數作用在 0–1 取樣值；驗收取畫面像素；nodata 靠來源 alpha | [05-11](../05-color/05-11-raster-value-encoding-color-mix-pixel-sampling.md)、[05-12](../05-color/05-12-raster-value-pixel-sampling-and-nodata.md) | 是 |
| 地形起伏、坡度、海底深度 | 山體陰影、等高線、等深線 | 只當襯底用預烤影像；要點選查值或換色才用分級向量；陰影壓低讓底圖退後 | [02-11](../02-basemaps/02-11-hillshade-slope-aspect-isobath-forms.md)、[02-10](../02-basemaps/02-10-dem-terrain-rgb-encoding-and-bathymetry.md)、[02-08](../02-basemaps/02-08-dark-light-basemap-vs-data-contrast.md) | 是 |
| 數值大、水位高 | 3D 量體（fill-extrusion） | 高度編碼資料並夾住範圍；不透明度 0.85；高度倍率有滑桿；能用原生就不用 Three.js | [04-11](04-11-3d-volumes-data-encoding.md) | 是 |
| 地名、名稱、計數 | 文字標籤 | 名稱 z10 10 px、z14 12 px；halo 約 1.25 px 底圖色；名稱 minzoom 不早於 13 且不重疊；中文用系統字；計數徽章可重疊 | [09-08](../09-design-system/09-08-text-hierarchy-dark-basemap.md)、[14-06](../14-scale-density/14-06-small-data-no-overpackaging.md) | 是 |
| 深色與淺色底圖都要讀得出 | 兩版色票 | 深底越密越亮、淡底越深；描邊、文字、halo 隨底圖換色；半徑、線寬、透明度不換 | [02-08](../02-basemaps/02-08-dark-light-basemap-vs-data-contrast.md)、[05-03](../05-color/05-03-dark-light-ramp-direction.md)、[09-08](../09-design-system/09-08-text-hierarchy-dark-basemap.md) | 是 |

## 相關主題
- 規格要同時有透明度、圖例、popup、選單：[09-02](../09-design-system/09-02-layer-ux-four-iron-rules.md)。
- 色階類型與具體色階：[05-01](../05-color/05-01-color-ramp-decision-table.md)、[05-10](../05-color/05-10-colorramps-used-catalog.md)。
- 資料太少不要包裝：[14-06](../14-scale-density/14-06-small-data-no-overpackaging.md)；聚合要誠實：[14-05](../14-scale-density/14-05-honest-aggregation.md)。

## 出處
- 各項依據見對應卡片。
- 實例規格：[圖層視覺規格（點、線、面、網格、影像、文字、圖例）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)。
