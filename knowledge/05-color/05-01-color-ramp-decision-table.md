---
id: 05-01
title: 資料型態 → 色階類型 → 建議色階的決策表
topic: 05-color
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [色階, choropleth, sequential, diverging, categorical, 決策表, ColorBrewer, viridis, magma]
---

## 原則
先判斷欄位是哪一種資料型態，再決定色階類型，最後才挑具體色階與色相；不要用「看起來好看」選色。

## 症狀
- 用彩虹色表示人口、用紅綠表示好壞、類別圖層用了連續色階，讀者看不出高低或看錯語意。
- 同一個主題在不同圖層換了三種色系。

## 原因
沒有先回答「這個欄位是哪一種資料」。色階類型必須由資料型態決定，色相只是第二步。

## 解法
依下表選色階類型與建議色階。

| 資料型態 | 色階類型 | 建議色階 | 為什麼 |
|---|---|---|---|
| 連續量（件數、密度、比率、占比） | 序列（sequential），淺→深＝低→高 | 主題色系的 ColorBrewer 單色或雙色序列（Blues、Greens、Purples、YlOrBr、BuGn…）；通用預設 viridis | 明度單調、淺→深符合直覺；ColorBrewer 已有色盲與印刷驗證 |
| 熱區／密度（heatmap、網格密度） | 序列，且「0＝完全透明」 | magma 或 viridis 的截取版；要提供換色就用經驗證的色盤庫 | 密度 0 不該有顏色，否則整張圖被染色 |
| 有正負、有基準點的變動（增減、差異、成長率） | 發散（diverging），以 0 或基準值為中心對稱 | PuOr、RdBu、BrBG；單向差異用序列 | 兩端各一色相、中間近中性；門檻必須對稱於基準 |
| 類別（土地使用、業別、設施種類） | 類別（categorical） | 每層自訂，固定順序、不循環；超過 7 類要有明確縮減規則 | 沒有大小關係，色相要容易區分；類別過多本來就讀不出 |
| 二元（有／無、達標／未達標） | 兩色，一個前景色、一個背景或中性灰 | 強調色＋淡灰 | 多餘的第三色會讓人去找意義 |
| 時間新舊（最近→很久以前） | 序列，新＝最顯眼 | 單色相序列，新＝深或亮（依底圖） | 時間是有序量，不是類別 |
| 風險／等級（法定或官方分級） | 沿用官方定義的離散色（例如空氣品質 6 級） | 官方色表；不自創 | 使用者已經熟悉官方色，改色等於改語意 |
| 缺值、未涵蓋、遮蔽 | 不是色階的一階 | 透明底＋斜線或獨立圖例項（見 [05-04](05-04-null-is-not-zero-color.md)） | null 不能畫成 0 級或最淺級 |

補充：
- 同一主題（例如教育、醫療）的原始數、人均值、面積平均用同一色系；語意不同的兩個模式（例如總量 vs 人均）刻意用可區分的色系，切換時才看得出「換了意義」。
- 現成的類別色盤（Okabe-Ito、Paul Tol）在深、淺底圖上不見得都通過對比檢查，採用前先在自己的底圖驗證。
- 狀態與警報色（綠＝正常、橘＝警告、紅＝錯誤）保留給狀態，不挪用成資料分類（見 [05-05](05-05-categorical-count-and-semantic-colors.md)）。
- 已用過的色階與語意對照見 [05-10](05-10-colorramps-used-catalog.md)。

## 怎麼偵測
- 通用：看資料欄位型態與圖例色階是否對得上——連續量卻是多色相彩虹；有正負卻用單向色階；類別卻是漸層。
- 搜尋：`jet|rainbow|turbo|interpolate.*hsl|"interpolate".*\["linear"\]`（找可能的彩虹或隨手拼的漸層）；`match` 用在類別、`step`／`interpolate` 用在連續量，兩者用反就是警訊（適用 stack：mapbox-gl、maplibre；deck.gl 看 `getFillColor` 的 colorScale）。
- 僅限 Mapbox／MapLibre expression 的寫法；其他函式庫看對應的 color scale 設定。

## 出處
- [ColorBrewer](https://colorbrewer2.org)；Matplotlib colormaps 文件（viridis／magma 的感知均勻性）。
- 相關卡：[05-04](05-04-null-is-not-zero-color.md)、[05-05](05-05-categorical-count-and-semantic-colors.md)、[05-10](05-10-colorramps-used-catalog.md)。
- 實例：[統計圖層規則 §4（各主題色系）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/statistics-layer-guidelines.md)、[視覺化函式庫決策 §1（資料多寡、熱力、正負色階）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/viz-library/DECISIONS.md)。
