---
id: 02-08
title: 深淺色底圖與資料層對比：底圖要「退後」，動態物件才看得清
topic: 02-basemaps
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [深色底圖, 淺色底圖, 對比, Pure Black, 暗色主題, 色階, 衛星, 資料層, 透明度]
---

## 原則
不論深色或淺色，都要壓低底圖對比讓底圖退後，並在深、淺兩種底圖上都驗色階；資料層插在底圖地名之下。

## 症狀
同一組色階在深色底圖上清楚，換淺色底圖後某些級距消失；動態物件被街道與地名淹沒；衛星底圖上資料像貼紙。

## 原因
底圖內容（道路、地名、建物）與資料層爭奪視覺注意力；色階的最淺或最深一端容易與底色相近。

## 解法
1. 深色或淺色是取捨，沒有通用預設：深色底圖讓發光與高亮的資料更突出，適合夜間或螢幕展示；淺色底圖在亮環境（投影、列印、白天閱讀）較清楚，也較貼近報表與公民資訊類作品。風格偏好見 [13-02](../13-author-taste/13-02-basemap-dark-mono-default.md)、[13-03](../13-author-taste/13-03-color-dark-accent-glow.md)。
2. 無論選哪一種，都要壓低底圖對比，讓底圖退後：背景與水域、道路只比背景略有差異，地名文字用低對比色加同調 halo（深底用黑 halo、淺底用白 halo）。
3. 色階在深、淺兩種底圖都要驗：最高級與最低級不能與底色、灰色參考線、描邊相同。
4. 資料面層插在底圖地名之下（見 [02-05](02-05-style-customization-by-code.md)），保持地名可讀。
5. 提供「底圖地名開關」與透明度，讓使用者自己降低干擾。
6. 衛星底圖上用描邊或較高不透明度，並降低面圖層填色。
7. 切換底圖後重驗圖例與對比（色階方向見色彩主題卡片）。

## 怎麼偵測
- 通用：把底圖切成淺色後，某些級距看不到；動態點看不見。
- 搜尋：寫死的 `#ffffff|#000000` 描邊；沒有依主題切換的色票（適用 stack：any）。

## 出處
- 一般建議：底圖降低彩度與對比以突顯主題資料，為資訊視覺化通則。
- 相關卡：[02-05](02-05-style-customization-by-code.md)。
- 實例：[Pure Black 暗色主題套用](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/MapView.tsx)（[commit 6afa7165](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/6afa7165b77818b8ecf032b2db26eb10d8fa9583)）、[圖層設計規則](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)。
