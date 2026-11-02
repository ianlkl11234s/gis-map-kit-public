---
id: 09-10
title: 地圖符號尺寸分三階，切換底圖只換色不改尺寸與透明度
topic: 09-design-system
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre]
tags: [點大小, 線寬, 面透明度, 描邊, 熱區, 三階, 密集點, 底圖切換, 尺寸]
---

## 原則
點、線、面的尺寸與透明度只用少數固定階，改階只改分階表一處；切換底圖只換色，不改尺寸與透明度。

## 症狀
同一個圖台裡，A 圖層的點半徑 3、B 圖層 8，線寬從 0.5 到 4 都有，面透明度 0.04 到 0.85；切換暗淡底圖時有些圖層連尺寸、透明度一起變。密集點拉遠時糊成一團，淡底圖上的低透明度線幾乎看不見。

## 原因
每個圖層作者自訂數值，缺少統一的尺寸階與「換底圖只換色」的規則。

## 解法
1. **點：固定半徑三階**（小 3／標準 4.5／強調 6.5 px），不隨縮放變化（特例見 [14-02](../14-scale-density/14-02-point-count-thresholds.md)），再乘使用者的大小滑桿。小＝密集點（點數門檻見 [14-02](../14-scale-density/14-02-point-count-thresholds.md)）與參考點；標準＝一般 POI；強調＝少量重點設施與即時事件。低縮放的高密度點不靠縮小半徑，改用密度透明度或熱區。資料驅動大小（泡泡）面積正比於值，下限與上限固定。點描邊 1 px，暗底用深色、淡底用白色，讓點在任何底圖上與背景分開。形狀本身有語意才用 icon，且點數約 5 千以內；更多改用圓點。
2. **線：細／標準／強調三階**，z10→z14 線性插值（細 0.5→1、標準 1→2、強調 2→3.5 px）；虛線只用於四種語意（規劃或施工中、推估或非實體、法定界線、網格外框），兩種 dasharray；實線不得用來表示「不確定」；路網與軌跡用圓頭圓角，界線與網格用尖角；透明度不低於約 0.3。
3. **面：透明度分階**（統計分級、覆蓋範圍、背景參考、網格各一個值），外框一律用獨立的 line 子圖層（不用 `fill-outline-color`，因為它固定 1 px 且不能隨縮放）；統計分級面用底圖色細縫，無數值的面用中性灰外框（底圖色縫在透明底上會消失）。
4. **換底圖只換色**：會換的是點描邊色、行政界線色、文字與 halo、序列色階方向、類別色淡版；不會換的是半徑、線寬、面與點的透明度、虛線、高度。若淡底真的需要更不透明，調整整體的階，而不是單層例外。
5. **預設用平面的點線面圖層**，立體效果做成可選開關（預設關）；移動物件的平面點放大後改成帶方向的箭頭符號，停止時用圓點（[14-07](../14-scale-density/14-07-moving-objects-and-trails-at-scale.md)）。
6. **改階與驗收**：改階只改一處（分階表檔案），不改各圖層的字面值；每改一層，低、中、近三種縮放各截圖一次，暗、淡各一組。

## 怎麼偵測
- 通用：打開十個圖層看點大小、線寬、透明度是否一致；切底圖看符號尺寸有沒有跳動。
- 搜尋：`circle-radius":\s*\d|circle-radius:\s*\d`（字面值）；`isDark\s*\?\s*0\.\d.*:\s*0\.\d`（底圖切換改透明度）；`fill-outline-color`；`line-dasharray` 的值不在兩種標準內（適用 stack：mapbox-gl、maplibre）。

## 出處
- 一般地圖符號設計（視覺階層與可辨識性）；MapLibre／Mapbox GL style spec 對 `fill-outline-color` 的限制。
- 實例：[design-system/map-layers.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)、[src/map/mapStyleScale.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/mapStyleScale.ts)、[src/map/pointTiers.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/pointTiers.ts)、[src/map/lineFillTiers.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/lineFillTiers.ts)、[R6-PROPOSAL.md（平面預設、立體可選）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/map-layer-restyle/R6-PROPOSAL.md)。
