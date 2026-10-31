---
id: 05-07
title: 透明度疊加會變色與糊掉：單層 alpha 要依疊加層數回推
topic: 05-color
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [透明度, alpha, 疊圖, 熱區, fill-opacity, 底圖透色, 疊加]
---

## 原則
做「疊加密度」視覺前，先估典型重疊層數 n，再回推單層 alpha；面與線的透明度分幾個固定階，不要每層自訂。

## 症狀
- 疊加很多半透明面／線（例如上百天的活動範圍、多層覆蓋面）後，整塊變成不透明，密度差異全部看不見。
- 同一個色階在不同底圖上看起來顏色不同（半透明會混底色）。
- 兩個圖層同時開，下方圖層改變了上層看起來的顏色，圖例與畫面對不上。

## 原因
alpha 疊加是 1 − (1 − a)^n，不是線性。單層 0.22 疊 20 層就約 0.99。半透明填色也一定會混入底圖。

## 解法
1. 先估典型重疊層數 n，再回推單層 alpha，不要做完再用眼睛調。可參考的縮放：單層 alpha 依 n 的負 0.6 次方縮放，使典型區域落在 0.3～0.6 的可讀區間；線框衰減比填色慢（負 0.35 次方）並收細，因為輪廓才是形狀感的來源。
2. 面的透明度分階：統計分級面約 0.55、覆蓋範圍面約 0.35、背景參考面約 0.15、規則網格約 0.7。階數少，多層同開時才能預期結果。
3. 線的透明度不低於約 0.3（淡底圖上幾乎看不見）。
4. 透明度是使用者可調的控制項（見 [09-02](../09-design-system/09-02-layer-ux-four-iron-rules.md)），但預設值要先選對；滑桿必須作用在該圖層所有主體子圖層，並測 0.1 與 1.0 兩端。
5. 圖例色票用不透明色並註明「實際地圖為半透明」，或圖例色票也套相同透明度並取樣驗證。
6. 切換底圖時只換色，不改透明度，避免圖層忽濃忽淡。

## 怎麼偵測
- 通用：資料很密的地方顏色飽和成一塊；圖例顏色與地圖實際畫出來的顏色明顯不同。
- 搜尋：`fill-opacity|line-opacity|circle-opacity` 的字面值 > 0.2 且該圖層是重疊事件／軌跡；`isDark ?` 裡改 opacity（適用 stack：mapbox-gl、maplibre；deck.gl 看 `opacity`／`getFillColor` alpha 通道）。

## 出處
- Alpha compositing 公式（Porter–Duff over operator）。
- 相關卡：[05-03](05-03-dark-light-ramp-direction.md)、[09-02](../09-design-system/09-02-layer-ux-four-iron-rules.md)。
- 實例：[專案原則「疊圖的單層 alpha 要依疊加層數縮放」](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/PRINCIPLES.md)、[圖層樣式規範 §3.3、§3.6（切底圖只換色）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)。
