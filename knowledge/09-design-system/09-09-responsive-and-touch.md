---
id: 09-09
title: 圖台 RWD 與觸控最低清單：手機標頭、底部抽屜、hover 替代、safe-area、浮層全開檢查
topic: 09-design-system
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [RWD, 手機, 觸控, hover, safe-area, 底部抽屜, bottom sheet, 橫式, 浮層, 斷點]
---

## 原則
手機與桌機共用同一個資料面板，只換外殼；任何 hover 才出現的資訊都要有觸控可達的替代路徑，並在「全部浮層同時展開」的狀態下驗收。

## 症狀
- 在桌機拉窗測過 RWD，手機一轉橫式就壞；底部面板蓋住版權列或時間軸。
- 滑過才出現的提示（tooltip）在觸控裝置完全看不到。
- 瀏海與 Home 指示條切到按鈕；`100vh` 在網址列收合時跳動。
- 手機另寫一套面板，桌機改了手機沒跟上。
- 各個浮層單看都正常，疊在一起互相蓋住。

## 原因
把手機當縮小的桌機；沒有驗收「全部浮層同時展開」。

## 解法
以下是最低清單：
1. **斷點與面板元件**：斷點用 `matchMedia` 監聽（含 orientation），不要只讀一次寬度；底部抽屜依直式／橫式給不同高度（橫式不吃掉大半地圖）。手機與桌機共用同一個資料面板元件，只換外殼與入口，不另寫一套。
2. **手機標頭**：高度固定（含 safe-area），外露按鈕數量上限（例如 AI、拍攝、更多、帳號），新入口一律收進「更多」選單，不加第二排。觸控目標至少約 30 px，避免過小的純圖示；下拉保留原生以使用手機選擇器；外文名稱長度可能是中文的 2～3 倍，統一「最多兩行＋省略號＋title 帶全名」，不要 `nowrap` 撐爆。
3. **觸控沒有 hover**：任何只在 `mouseenter`／`mousemove` 才出現的資訊，必須有點擊可達的替代路徑；用 `(hover: hover) and (pointer: fine)` 判斷，不用寬度。時間軸等「膠囊展開」型控制在手機固定展開。會影響解讀的關鍵說明（例如「兩份資料法源不同，不可合併」）直接放在畫面上，不只放在 hover 才出現的 `title`。
4. **safe-area 與浮層**：設了 `viewport-fit=cover` 的頁面，所有貼邊的固定元件都要加 `env(safe-area-inset-*)`；用 `dvh`／可見視窗高度，不用 `100vh`。手機開一個面板時其他面板強制收合；底部抽屜高度以 CSS 變數告知地圖，讓地圖角落的 logo 與版權列讓到抽屜上方；版權標示必須常駐，不可被覆蓋或收進卡片。
5. **內嵌地圖與無障礙取捨**：內嵌的地圖（iframe、文章內）開 cooperative gestures（單指捲頁、雙指移圖），全螢幕地圖不開。互動動畫（展開、選取圈、載入條）遵守 `prefers-reduced-motion`，載入狀態的顯示節奏見 [09-07](09-07-loading-data-time-and-stale.md)。viewport 設 `user-scalable=no` 會與 WCAG 1.4.4（文字可放大）衝突：地圖需要自己的縮放手勢所以常被關掉頁面縮放，但要在 PR 說明理由，並提供替代的文字放大方式（見 [11-10](../11-extras/11-10-accessibility-keyboard-ime.md)）。
6. **驗收**：手機尺寸直式、橫式各一張；「全部浮層同時展開」一張（圖例、popup、選單、面板、時間軸、版權列）；窄螢幕不橫向溢出。viewport 模擬不可稱為實體手機驗收。

## 怎麼偵測
- 通用：DevTools 切手機尺寸直橫各看一次，並把所有浮層同時打開；關掉滑鼠（或用觸控模擬）看資訊是否仍可達。
- 搜尋：`mouseenter|onMouseEnter|:hover` 作為唯一互動路徑；`100vh`；`window.innerWidth <` 只在載入時讀一次；`position:\s*fixed;\s*bottom:` 未見 `safe-area-inset`；`user-scalable=no`（需說明替代的文字放大方式）（適用 stack：any）。

## 出處
- MDN：`env()`、`matchMedia`、`(hover: hover)` media feature；MapLibre MapOptions `cooperativeGestures`；WCAG 2.2 SC 1.4.4（文字縮放）、SC 2.5.8 目標尺寸。
- 實例：[design-system/spec.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)（手機標頭、展開卡的左右邊距）。

