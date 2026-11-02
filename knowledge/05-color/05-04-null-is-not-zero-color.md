---
id: 05-04
title: 缺值（null）要有獨立畫法，不能畫成 0 級或最淺色
topic: 05-color
kind: pitfall
scope: public
evidence: Implemented
stacks: [any]
tags: [缺值, null, 斜線, hatch, 未涵蓋, 遮蔽, 零值, 圖例]
---

## 原則
缺值、遮蔽、未涵蓋一律用獨立畫法和獨立圖例項，不使用色階的任何一級，也不顯示成 0。初學骨架可用色階沒用到的中性灰＋圖例「無資料」；進階（面圖層）用透明底＋斜線。

## 症狀
- 行政區沒有資料的地方被畫成最淺色或灰色，讀者把它當成「0」或「很低」。
- 來源把某些值遮蔽（suppressed），也被當成 0。
- 圖例沒有對應項目，使用者無從分辨「真的是 0」和「沒有資料」。

## 原因
繪圖函式對 null 做了預設處理：`step`／`interpolate` 的 input 缺值會落到第一級，或程式碼寫 `null ?? 0`。灰色若和色階某一級接近，也會被誤認為那一級，所以色階不要用灰。

## 解法
1. 先分清楚真 0（用數值色階）、缺值、遮蔽（來源刻意隱藏）、未涵蓋四種狀態（資料層定義見 [06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)），本卡只管畫法。
2. 初學骨架（點或少量面）：缺值用色階完全沒用到的中性灰（如 `#9e9e9e`），圖例放獨立的「無資料」項。進階（面圖層，或色階含灰、淺色時）：缺值用「透明底＋單向 45° 細斜線」，遮蔽用「透明底＋交叉斜線」，都不上色。未涵蓋的地區寫「未涵蓋」，不寫 0。
3. 用斜線時，pattern 用 `fill-pattern`（Mapbox／MapLibre）或 SVG pattern（Leaflet）；暗底用白色約 35%、淡底用黑色約 35%，8px 圖磚。缺值面積在透明底上外框會消失，外框改用中性灰細線。
4. 圖例一定要有「缺值／遮蔽」（或「無資料」）項，與地圖用同一組顏色或 pattern，並附文字說明。
5. 用 MapLibre／Mapbox expression 時，在前處理階段就把 null 轉成明確 sentinel（例如 -1），再用 `case` 分支畫斜線圖層，不要靠 step 的預設級。
6. 彈窗與表格：缺值顯示「—」或「無資料」並保留原因；值為 null 的欄位直接不渲染，不要顯示 0。

## 怎麼偵測
- 通用：資料中有 null 的區域，地圖上顏色和最低級相同；圖例找不到「無資料」項；彈窗出現 0。
- 搜尋：`\?\? 0`、`\|\| 0`、`Number\(.*\) *\|\| *0`、`coalesce\(.*, *0\)`、`["to-number", ["get",` 沒有 fallback、`step` 第一個輸出色就是最淺色（適用 stack：mapbox-gl、maplibre；SQL 端看 `COALESCE(x, 0)`）。

## 出處
- 統計製圖慣例：缺值與零值要在圖上可區分（ColorBrewer 的 "No data" 說明）。
- 相關卡：[05-01](05-01-color-ramp-decision-table.md)、[05-08](05-08-legend-key-mismatch.md)、[06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)。
- 實例：[圖層樣式規範 §3.3（缺值斜線）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)、[統計圖層規則 §2](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/statistics-layer-guidelines.md)、[斜線樣式常數 MISSING_HATCH](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/mapStyleScale.ts)、[空氣品質色階（null 轉 -1）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/aqiColorScale.ts)。
