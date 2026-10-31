---
id: 11-10
title: 圖台無障礙最低清單：時間軸鍵盤操作、aria-live 通知、中文輸入法 Enter 不誤送出
topic: 11-extras
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [無障礙, a11y, 鍵盤, IME, isComposing, aria-live, slider, 焦點, reduced-motion, Safari]
---

## 原則
每個輸入框都判斷 IME 組字狀態，自訂控制項（時間軸滑桿）要能純鍵盤操作並有 ARIA 語意，通知用 `aria-live`，動畫遵守 `prefers-reduced-motion`。

## 症狀
- 中文使用者在注音／拼音選字階段按 Enter，訊息被直接送出。
- 鍵盤使用者無法操作時間軸；展開時焦點掉出去。
- 讀屏使用者不知道載入完成或通知出現。
- Safari 上網址同步被瀏覽器的 history API 頻率保護擋下。

## 原因
地圖被當成滑鼠專用物件；IME 與 Safari 行為不在測試清單裡。

## 解法
1. IME：處理 Enter 送出的輸入框，檢查 `e.nativeEvent.isComposing`（舊 Safari 另判 `keyCode === 229`），為真時不送出。
2. 自訂滑桿（時間軸）：`role="slider"` 加 `aria-valuemin/max/now/valuetext`，方向鍵微調、Shift＋方向鍵或 PageUp／PageDown 大步、Home／End 到兩端；展開時保持 focus。
3. 選單支援 Esc／Tab／Home／End；下拉保留原生 `<select>`（手機原生選擇器與無障礙）。
4. 通知類元件用 `aria-live="polite"`；開站前的靜態說明用視覺隱藏而非 `display:none`，輔助技術與爬蟲都讀得到（[11-01](11-01-spa-empty-html-seo-prerender.md)）。
5. 動畫與離開提示遵守 `prefers-reduced-motion`。
6. 網址同步綁 `moveend`（不是 `move`），避免 history API 被 Safari 節流。
7. 縮放：`user-scalable=no` 與 WCAG 1.4.4（文字可放大至 200%）有張力；使用時在 PR 說明理由與替代的文字放大方式（[09-09](../09-design-system/09-09-responsive-and-touch.md)）。
8. 本卡是最低清單，不等於完整無障礙驗收；完整驗收要加自動化檢測（如 axe）與跨瀏覽器測試。
9. 學生版：Tab 從頭走一遍；所有文字輸入框加 IME 判斷。

## 怎麼偵測
- 通用：只用鍵盤操作一遍主要流程；用中文輸入法在輸入框打字按 Enter。
- 搜尋：`onKeyDown.*Enter` 且無 `isComposing`；自訂 slider 缺 `role="slider"`；`map\.on\(['"]move['"]` 內呼叫 `history\.(replace|push)State`（適用 stack：any）。

## 出處
- MDN `KeyboardEvent.isComposing`；WAI-ARIA Authoring Practices〈Slider〉；WCAG 2.2 SC 1.4.4：https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html 。
- 相關卡：[09-09](../09-design-system/09-09-responsive-and-touch.md)、[11-01](11-01-spa-empty-html-seo-prerender.md)。
- 實例：[mini-taiwan-pulse 對話框的 isComposing／keyCode 229 判斷](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/chat/ChatPanel.tsx)、[aria-live 通知](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/TransientNotice.tsx)、[設計規格的時間軸鍵盤操作](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)、[靜態說明改視覺隱藏](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/66d6d09cbf58e10710fe2bffc8969bb659cddb37)。
