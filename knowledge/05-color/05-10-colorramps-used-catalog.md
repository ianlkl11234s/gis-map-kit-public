---
id: 05-10
title: 用過的色階清單與語意對照（序列、發散、類別、官方色）
topic: 05-color
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [色階清單, ColorBrewer, viridis, magma, YlOrRd, PuOr, RdBu, 官方色, 色盤庫]
---

## 原則
選色階前先查本表：同主題沿用既有色系，再依資料型態選類型（[05-01](05-01-color-ramp-decision-table.md)），最後檢查與同頁圖層是否太像（[05-06](05-06-colorblind-and-similar-ramps.md)）、暗淡底圖是否都過對比（[05-03](05-03-dark-light-ramp-direction.md)）。

## 對照表
下表是實務上用過、且有選擇理由的色階；「用在什麼語意」說明為什麼選它。

| 色階 | 類型 | 用在什麼語意 | 備註 |
|---|---|---|---|
| viridis | 序列（多色相） | 資料多寡（區域深淺、泡泡、格點）；分級面的預設；分級數少（3～4）的回放類圖層 | 暗底「越高越亮」、淡底「越高越深」；亮端黃綠，比 magma 更不容易和灰色、白描邊撞 |
| magma | 序列（多色相） | 熱力、密度熱區的預設 | 亮端米黃，要避開灰色 0 級與白描邊（[05-02](05-02-gray-zero-and-outline-collision.md)）；需用經驗證的截取版 |
| YlOrRd／YlOrBr／Oranges | 序列（暖） | 人口、市值、總量、密度（橙紅＝多） | 與 inferno 太像時選其一；兩個相鄰模式要可區分 |
| inferno | 序列（暖） | 總量（長尾分佈、9 級） | 同頁與 viridis 的人均模式刻意拉開 |
| Blues／Greens／Purples／BuGn／GnBu／BuPu／PuBu／YlGn | 序列（單色） | 統計主題色系：交通藍、教育紫、醫療藍綠、農業黃綠、漁業紫藍、環境藍紫… | 同一主題的原始數、人均、面積平均保持同色系 |
| Greys＋Oranges | 序列 | 土壤：黏土灰、砂土橙 | 去掉兩端以便暗底可辨 |
| OrRd／PuRd／YlOrBr／Greens | 序列 | 建築密度、總量體、建蔽率、樹冠覆蓋 | 0 值淡出（透明），不給最淺色 |
| PuOr | 發散 | 有正負的變化率、模擬差異（棕負、紫非負）；門檻對稱於 0 | 不用紅綠 |
| RdBu（反轉） | 發散 | 地表溫度差（冷藍→白→熱紅） | 色階範圍刻意拉開都市內部對比，山區在藍端飽和可接受 |
| BrBG | 發散 | 灰綠指數（褐＝灰主導、綠＝綠主導） | 0 是有意義的中點 |
| 官方 6 級色 | 離散，官方定義 | 空氣品質指標：良好綠→危害暗紅 | 使用者熟悉，不重新設計；缺值用獨立的「無資料」畫法（[05-04](05-04-null-is-not-zero-color.md)） |
| 自訂 5 點線性色階 | 序列（多色相） | 風場速度（藍→青→綠→黃→橘→紅→紫紅）、海流（深藍→亮藍→青→米黃→橘） | 對齊既有氣象視覺慣例；粒子與圖例共用同一份色表 |
| 品牌藍 3 級 | 序列（單色） | 分析範圍（等時圈） | 與資料色階分工，避免混淆 |
| 藍／琥珀單色 | 序列 | 結果疊在其他彩色圖層上時的備用 | 對比於底圖的彩色 |
| 類別 7 色＋其他 | 類別 | 分析結果類別（藍、金、洋紅、綠、紫、青、橘＋灰） | 紅色不收；其餘圖層類別色各自訂 |
| 熱區／網格色盤庫（暗淡各 7 階） | 序列 | 讓使用者在熱區與網格上換色 | 建議清單只收兩兩分得開的組合；見 [05-06](05-06-colorblind-and-similar-ramps.md) |

## 怎麼偵測
- 通用：新圖層的色階與同主題既有圖層差異很大；兩個預設色階相同的圖層預期會同時開啟。
- 搜尋：新增 `color` 陣列／`interpolate` 色票時先搜尋既有常數檔（`*Types.ts`、`palettes.ts`、`statisticsVisuals.ts` 類）是否已有同色系（適用 stack：any）。

## 出處
- ColorBrewer、Matplotlib、cmocean、Crameri scientific colour maps、CARTO Colors 的公開色表。
- 相關卡：[05-01](05-01-color-ramp-decision-table.md)、[05-02](05-02-gray-zero-and-outline-collision.md)、[05-03](05-03-dark-light-ramp-direction.md)、[05-06](05-06-colorblind-and-similar-ramps.md)。
- 實例：[統計主題色系](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/statisticsVisuals.ts)、[熱區色盤庫](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/palettes.ts)、[視覺化函式庫決策 §1.2–1.3](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/viz-library/DECISIONS.md)、[氣候色階](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/climateRamps.ts)、[空氣品質色階](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/aqiColorScale.ts)。
