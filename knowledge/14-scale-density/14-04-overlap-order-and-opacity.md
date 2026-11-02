---
id: 14-04
title: 重疊與遮蔽：誰畫在上面要有規則——泡泡大的先畫、分級線高值在上，多層熱區要降透明
topic: 14-scale-density
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [重疊, 遮蔽, sort-key, circle-sort-key, line-sort-key, 繪製順序, 透明度, 熱區疊加, 高值在上, 泡泡]
---

本卡管「同一圖層內」的 sort-key 與疊加透明；圖層之間的先後（登記順序、beforeId）見 [08-05](../08-multi-layer/08-05-layer-stacking-order.md)。

## 原則
同一圖層內用 sort-key 決定誰在上面：大小編碼大的先畫，顏色或分級編碼高值在上；多層熱區同開時各自再降透明度。

## 症狀
- 大泡泡蓋住小泡泡，小值的點完全看不到、點不到。
- 擁擠路段的紅線被一般路段的灰線蓋掉，最重要的資訊反而在最下面。
- 兩層熱區同開，整片飽和。
- 密集點區域顏色疊到看不出差異。

## 原因
同一圖層內的繪製順序預設是資料順序，和數值無關；同層的重疊要靠 sort-key 控制。不同圖層的順序另見 [08-05](../08-multi-layer/08-05-layer-stacking-order.md)。

## 解法
同一圖層內有兩條規則，依符號型態選：
1. **大小編碼（泡泡、等時圈、出力圓）：大的先畫，小的在上**。sort-key 設成「負的大小」，小的才不會被蓋住、也點得到。
2. **顏色或分級編碼（擁擠線、計數點、道路等級）：高值在上**。sort-key 直接用數值或等級，重要的畫在最後。缺值給最小值（例：−1），永遠在最下。
3. sort-key 只讀 feature properties，不讀 feature-state；值會隨時間變的，要寫進 properties 再更新資料。
4. **透明度依密度**：點越多預設越透明（[14-02](14-02-point-count-thresholds.md) 表）；疊加型資料先估重疊層數再回推單層 alpha（[05-07](../05-color/05-07-alpha-stacking-and-fill-opacity.md)）。
5. **多層熱區同開時每層再乘一個倍率**（例：0.7），只剩一層時恢復；判斷依據是圖層開關，不看當下縮放。
6. **熱區的 weight 要壓低值**：大量低值點疊加會看起來像極端值（例：雨量熱區小雨站疊成豪雨）。
7. 點的描邊用底圖色細縫，讓相鄰點分開（[09-10](../09-design-system/09-10-map-symbol-size-tiers.md)）。

## 怎麼偵測
- 通用：在最密的區域拉近，看小值或高值是否被蓋住；同開兩層熱區看是否整片飽和。
- 搜尋：比例符號圖層（`circle-radius` 用 `["get", …]` 或 `sqrt`）沒有 `circle-sort-key`；分級線（`line-color` 用 `step`／`match` 數值）沒有 `line-sort-key`；`heatmap-weight` 是常數 1 但資料有數值欄位（適用 stack：mapbox-gl、maplibre；deck.gl 看資料排序後再傳入）。

## 出處
- 官方：MapLibre／Mapbox GL style spec `circle-sort-key`、`line-sort-key`、`symbol-sort-key`（值越大越後畫）。
- 圖層之間的順序：[08-05](../08-multi-layer/08-05-layer-stacking-order.md)；alpha 疊加公式：[05-07](../05-color/05-07-alpha-stacking-and-fill-opacity.md)。
- 實例：[mini-taiwan-pulse 分析結果的 sort-key 設定](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/research/warehouseResultStyle.ts)。
- 實例：[分級線高值在上、缺值最下](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/busCrowdingSimStyle.ts)。
- 實例：[多層熱區降透明度](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/mapStyleScale.ts)。
