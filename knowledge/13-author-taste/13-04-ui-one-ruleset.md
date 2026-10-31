---
id: 13-04
title: UI 統一一套規則：系統字、不載 web font、圓角 8 以內、資訊密度適中
topic: 13-author-taste
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [UI, 字型, web font, 圓角, 玻璃面板, 圖例, popup, design token]
---

這是作者的設計偏好，不是業界規範；你可以不同，但要說得出理由，偏離時在 README 或 PR 寫一句。

## 原則
全部作品用同一套 UI 規則：系統字、不載 web font、圓角 ≤8、資訊密度適中、顏色字級圓角取 design token。

## 症狀
- 同一個人的作品，字型與圓角各自為政；載入 web font 造成首屏變慢與跳字。
- CSS 寫了字族但沒有載入，等於白寫。

## 原因
把「儀表板」與「藝術型」分成兩套視覺規則，會讓決策變多、維護變難。統一一套，展示字與大圓角視為例外，不當範本。

## 解法
1. 系統字，不載 web font；中文用系統中文字型，數字可用 monospace 系統字。
2. 圓角 ≤8（含 popup、卡片、按鈕），膠囊形按鈕除外時要有理由。
3. 資訊密度適中：不堆滿面板；詳細內容放展開區或 popup。
4. 玻璃深色面板：半透明深色底＋適度 backdrop blur。
5. 圖例與 popup 樣式一致：中文標題在前，不轉大寫，不用英文 eyebrow；規格見 [09-04](../09-design-system/09-04-legend-spec.md)、[09-05](../09-design-system/09-05-popup-and-source-footer.md)，文字層級見 [09-08](../09-design-system/09-08-text-hierarchy-dark-basemap.md)，RWD 見 [09-09](../09-design-system/09-09-responsive-and-touch.md)。
6. 顏色、字級、圓角取 design token（見 [09-01](../09-design-system/09-01-token-ssot-and-ratchet-guard.md)），不寫死。

## 怎麼偵測
- 搜尋：`@import url\(.*fonts\.googleapis\)`、`<link[^>]+fonts\.(googleapis|gstatic)`、`@font-face`（適用 stack：any）。
- 搜尋：`border-radius:\s*(9|[1-9][0-9]+)px`、`rounded-(xl|2xl|3xl)`（Tailwind 專案）。
- 搜尋：`font-family` 列了 Inter／JetBrains Mono 等字族，但 HTML 沒有對應載入（寫了等於白寫）。
- 通用：`text-transform:\s*uppercase`、英文 eyebrow 小標。
- 命中要求補偏離理由，不是一律判錯。

## 出處
- 見 [09-01](../09-design-system/09-01-token-ssot-and-ratchet-guard.md)、[09-04](../09-design-system/09-04-legend-spec.md)、[09-05](../09-design-system/09-05-popup-and-source-footer.md)、[09-08](../09-design-system/09-08-text-hierarchy-dark-basemap.md)、[09-09](../09-design-system/09-09-responsive-and-touch.md)。
- 實例：[mini-taiwan-pulse 設計規格（系統字與圓角 token）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)。
