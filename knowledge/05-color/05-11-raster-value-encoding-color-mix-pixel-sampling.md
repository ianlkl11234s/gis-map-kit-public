---
id: 05-11
title: 值編碼 raster 用 raster-color-mix 上色：係數作用在 0–1 取樣值上，漏乘 255 整層單色
topic: 05-color
kind: pitfall
scope: public
evidence: Evaluated
stacks: [mapbox-gl]
tags: [raster-color, raster-color-mix, raster-value, raster-color-range, 值編碼, 像素取樣, nodata, alpha, shader, 驗收]
---

## 原則
值編碼 raster 的 `raster-color-mix` 係數是「每個位元組單位的增量 × 255」，因為通道取樣值已正規化到 0–1；stop、range、圖例三者要用同一種寫法。驗算例子、驗收與 nodata 的做法見 [05-12](05-12-raster-value-pixel-sampling-and-nodata.md)。

## 症狀
- 把物理值（樹高、地表溫度、雨量）編進 PNG 像素，用 `raster-color` 上色，結果整層變成單一顏色、看不到漸層。
- 照原始碼推導出「正確」的係數，改上去後反而全層飽和在色階下限。

## 原因
- Mapbox GL JS v3 的 `raster-color-mix` 是 `[mR, mG, mB, offset]`，算式 `raster-value = mR·r + mG·g + mB·b + offset`（第四項是常數，不乘 alpha）。`r／g／b` 是紋理取樣值，**已正規化到 0–1**（位元組 ÷ 255），不是 0–255 的整數。style spec 沒寫明這點，是像素取樣實測得出；預設的亮度係數 `[0.2126, 0.7152, 0.0722, 0]` 配預設 range `[0, 1]`，也只有在 0–1 的通道值下才說得通。
- 漏乘 255，算出的值就小 255 倍，整層擠在 range 下限、只剩一種顏色。
- MapLibre 的 raster layer 沒有 `raster-color`／`raster-color-mix`／`raster-color-range`（以當期 style spec 為準）。

## 解法
1. **推導公式**：若編碼是 `b = (值 − min) × k`（`b` 為 0–255 的位元組，`k` 為每單位幾個 DN），則取樣值 `r = b / 255`，`值 = (255 / k) · r + min`。兩種等價寫法擇一，**stop、range、圖例三者用同一種**：
   | 寫法 | `raster-color-mix` | `raster-color-range` | stop 寫什麼 |
   |---|---|---|---|
   | A 物理值（建議） | `[255 / k, 0, 0, min]` | `[min, max]`（物理值） | 物理值（公尺、°C） |
   | B 正規化 0–1 | `[255 / (k · (max − min)), 0, 0, 0]`（offset 恆為 0） | `[0, 1]` | `(值 − min) / (max − min)` |
   多通道時把係數放到對應位置（例如用 G 通道就是 `[0, 255 / k, 0, min]`）。
2. 在程式旁註明編碼公式與採用寫法 A 或 B。

## 怎麼偵測
- 通用：值編碼 raster 圖層整層只有一種顏色。
- 搜尋：`raster-color-mix` 的係數小於 1（多半忘了 ×255；用 `[0.2126, 0.7152, 0.0722, 0]` 亮度預設的灰階影像除外），或附近沒有編碼公式註解（mapbox-gl）。
- 搜尋：`raster-color-range` 是 `[0, 1]`，stop 卻寫物理值（或反過來），寫法 A／B 混用（mapbox-gl）。
- 搜尋：`raster-color` 的 stop 用 0–255 的整數，而圖例寫物理單位（mapbox-gl）。

## 出處
- Mapbox GL JS style spec（layers › raster）：`raster-color-mix`、`raster-color-range`、`raster-color`。spec 未寫明通道值是 0–1，本卡以實測為準。
- 相關卡：[05-12](05-12-raster-value-pixel-sampling-and-nodata.md)（驗收與 nodata）、[02-11](../02-basemaps/02-11-hillshade-slope-aspect-isobath-forms.md)（地形衍生資料的形態選擇）、[05-04](05-04-null-is-not-zero-color.md)。
- 實例：[都市熱島圖層（寫法 A）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/urbanHeatTypes.ts)、[樹冠高度圖層（寫法 B）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/overlayRegistry.ts)。
