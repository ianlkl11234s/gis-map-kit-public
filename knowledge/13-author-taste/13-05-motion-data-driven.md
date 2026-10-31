---
id: 13-05
title: 動態要由資料驅動，用插值平滑，時間軸預設不播放
topic: 13-author-taste
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [動態, lerp, 插值, autoplay, reduced-motion, 時間軸, 假動態]
---

這是作者的設計偏好，不是業界規範；你可以不同，但要說得出理由，偏離時在 README 或 PR 寫一句。

## 原則
動態必須代表資料：用插值做平滑，不用 CSS／GL transition 冒充；時間軸預設不播放，並尊重 prefers-reduced-motion。

## 症狀
- 打開頁面就自己播放，使用者還沒看懂就跑掉了。
- 點在移動但不是真實位置；用 CSS／GL transition 冒充「平滑」，資料跳動時還是會抖。
- 對系統設定「減少動態」的使用者仍然在動。

## 原因
裝飾性動態讓人誤以為資料在動；transition 只是在兩個畫面之間補間，不代表資料中間狀態。

## 解法
1. 動態必須代表資料：位置來自真實軌跡、時刻表或插值，不為動畫而動畫（見 [04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)）。
2. 「平滑」＝資料 lerp 插值，不是 CSS／GL transition；map 的 style transition 設 0，移動物件的位置由純函式依時間插值（見 [04-02](../04-effects-catalog/04-02-moving-objects-interpolation.md)）。
3. 時間軸動態一律預設不播放（playing 初值 false），使用者按了才播。
4. 尊重 prefers-reduced-motion：脈衝、擴散圈、載入條在減少動態時改為靜止或只淡入淡出。
5. 不播放未來：播放頭不超過資料覆蓋範圍（見 [03-07](../03-dynamics/03-07-playhead-bounds-no-future.md)）。
6. 不做無限循環的明暗閃動；同時脈動的物件數要設上限。

## 怎麼偵測
- 搜尋：`playing:\s*true`、`autoplay\s*[:=]\s*true`、`useState\(true\).*play`（適用 stack：any）。
- 搜尋：map 的 `transition:\s*\{\s*duration:\s*[1-9]`（適用 stack：mapbox-gl、maplibre），且註解或文件宣稱「平滑」。
- 搜尋：有 `@keyframes`／`requestAnimationFrame` 但整個專案找不到 `prefers-reduced-motion`／`matchMedia\('(prefers-reduced-motion`。
- 通用：資料沒更新時畫面仍在動。

## 出處
- 見 [04-02](../04-effects-catalog/04-02-moving-objects-interpolation.md)、[04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)、[03-07](../03-dynamics/03-07-playhead-bounds-no-future.md)。MDN：prefers-reduced-motion。
- 實例：[mini-taiwan-pulse 時間軸 hook（playing 初值 false）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/hooks/useTimeline.ts)。
