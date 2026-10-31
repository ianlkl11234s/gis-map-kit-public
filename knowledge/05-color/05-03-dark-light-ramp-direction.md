---
id: 05-03
title: 暗底圖與淡底圖的序列色階方向相反，兩邊都要過對比檢查
topic: 05-color
kind: pattern
scope: public
evidence: Evaluated
stacks: [any]
tags: [色階, 暗色底圖, 淡色底圖, 對比, 熱區, 驗證, 底圖切換]
---

## 原則
每個序列色階準備暗底、淡底兩版，渲染時依底圖取用，並對實際會出現的所有陸地色驗證對比；切換底圖只換色，不改尺寸與透明度。

## 症狀
- 同一個熱區色階在暗底圖很漂亮，換到淡底圖後最密的地方幾乎看不見（淡黃對白底）。
- 在暗底圖，最低端和黑色陸地混在一起。

## 原因
「越多越亮」只在暗底成立。淡底圖要讓密度高處「越深」，低密度則融進底圖。同一條色階直接套兩種底圖，總有一端和底色對比不足。

## 解法
1. 每個序列色階準備兩版（通常各 5～7 階）：暗底「低→高＝暗→亮」，淡底「低→高＝淺→深」。程式在渲染時依底圖取對應版，登記表只寫色階名稱。
2. 兩版都裁掉最接近底圖的那一端，避免低密度被底圖吃掉；最高級也不能和底色同明度。
3. 用驗證器檢查：亮度單調、相鄰級距的明度差、最接近底圖那端對陸地色的對比比值。實測一條常用的 magma 截取版，暗底最低端、淡底最高端的對比都遠低於下限（淡底最高端幾乎等於白底），重新取樣後才達到 2:1 以上。
4. 底圖陸地色不止一種（純黑、深灰、淺灰、白），驗證時用實際會出現的所有陸地色。
5. 只改色，不改半徑、線寬、透明度，避免切換底圖時符號尺寸跳動。

## 怎麼偵測
- 通用：切換到淡底圖，最密集的區域是否「消失」；切到純黑底圖，最稀疏的區域是否看不見。
- 搜尋：`isDark|isDarkTheme|theme === "dark"` 只用在文字與邊框、色階卻沒有分支；色階常數只有一份卻會被兩種底圖使用（適用 stack：any）。
- 驗證：任何通用 WCAG／OKLab 工具皆可，重點是「對實際陸地色」計算。

## 出處
- Matplotlib／ColorBrewer 對感知均勻與亮度單調的說明；WCAG 2.2 SC 1.4.11 非文字對比。
- 相關卡：[05-02](05-02-gray-zero-and-outline-collision.md)、[05-06](05-06-colorblind-and-similar-ramps.md)、[05-07](05-07-alpha-stacking-and-fill-opacity.md)。
- 實例：[色盤選擇的設計稽核](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/layer-color-picker/design-audit.md)、[色階驗證紀錄](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/layer-color-picker/ramp-validation.md)。
