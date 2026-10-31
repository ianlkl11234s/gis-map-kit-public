---
id: 05-12
title: 值編碼 raster 的驗收：一律用畫面像素取樣，nodata 靠來源 alpha 而不是透明 stop
topic: 05-color
kind: pitfall
scope: public
evidence: Evaluated
stacks: [mapbox-gl]
tags: [raster-color, raster-color-mix, raster-value, raster-color-range, 值編碼, 像素取樣, nodata, alpha, shader, 驗收]
---

## 原則
值編碼 raster 的上色是否正確，只用畫面像素取樣驗收，不用原始碼推導或 code review 定案；nodata 靠來源影像的 alpha 通道，不要用透明 stop 或位元組哨兵。係數的算法見 [05-11](05-11-raster-value-encoding-color-mix-pixel-sampling.md)。

## 症狀
- nodata 區域被塗上色階最低色，蓋住底圖。
- 係數看起來「推導正確」，驗收紀錄卻只有推導、沒有實際畫面數字，結果上線後整層單色。

## 原因
- shader 的換算鏈很長，紙上推導本身就是漏掉 0–1 正規化（見 [05-11](05-11-raster-value-encoding-color-mix-pixel-sampling.md)）的來源。
- nodata 若用某個位元組值（例如 0）當哨兵，量化後 0 可能是合法物理值；用透明 stop 或哨兵值判斷都不可靠。

## 解法
1. **寫法 A 的驗算例子**：地表溫差 ΔT 編成 `b = (ΔT + 30) × 5`（每 0.2 K 一個 DN，`min = −30`、`max = 21`）→ `raster-color-mix: [51, 0, 0, -30]`、`raster-color-range: [-30, 21]`。驗算：像素 `b = 150` → 取樣 `150/255` → `51 × 150/255 − 30 = 0 K` ✓；`b = 0` → `−30 K`；`b = 255` → `+21 K`。若誤寫成 `[0.2, 0, 0, -30]`，`b = 150` 會算成 `0.2 × 0.588 − 30 ≈ −29.9`，整層都貼在下限。
2. **寫法 B 的例子**：樹高 `b = 公尺`（`k = 1`、`0–40 m`）→ `[255/40, 0, 0, 0] = [6.375, 0, 0, 0]`、range `[0, 1]`，20 m 對應 stop `0.5`。6.375 是「斜率 1/40（每 DN 在 0–1 尺度上的增量）× 255」，和寫法 A 的「物理斜率 × 255」是同一條規則，只是輸出單位不同。
3. **驗收用畫面像素取樣**：在已知值不同的幾個位置取畫面 RGB，彼此要相異（有漸層），且顏色對得上該值的 stop。
4. 有一個已經正常運作的同類圖層時，它就是對照組；要推翻它的寫法，先實測它。
5. nodata 處要透明、看得到底圖。做法是**靠來源影像的 alpha 通道**（spec：source alpha 會當成上色結果的不透明度），不要加透明 stop，也不要用位元組哨兵判斷。
6. 驗收紀錄要寫取樣位置、已知值與取到的 RGB，不能只寫「依原始碼推導」。
7. 其他引擎（MapLibre、deck.gl）用 custom layer 自寫 shader 解碼時，同樣以像素取樣驗收。

## 怎麼偵測
- 通用：nodata 區不透明、蓋住底圖。
- 搜尋：`raster-color` 裡有 `"rgba\(0,\s*0,\s*0,\s*0\)"` 透明 stop 當 nodata（mapbox-gl）。
- 驗收記錄裡只有「依原始碼推導」而沒有像素取樣數字（any）。

## 出處
- Mapbox GL JS style spec（layers › raster）：`raster-color-mix` 的 source alpha 當不透明度。
- 相關卡：[05-11](05-11-raster-value-encoding-color-mix-pixel-sampling.md)（係數算法）、[05-04](05-04-null-is-not-zero-color.md)（null 不等於 0 的上色）。
- 實例：[都市熱島圖層交接文件（像素取樣驗收與已知不對稱）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/urban-heat-lst/handoff.md)、[經驗總集 §7 小實驗](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/LESSONS.md)。
