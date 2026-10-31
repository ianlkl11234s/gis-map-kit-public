---
id: 09-01
title: 圖台設計系統骨架：token 單一來源＋規格文件＋只降不升的自動檢查
topic: 09-design-system
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [design system, token, SSOT, lint, ratchet, guard, 暗色, 淡色, 字型]
---

## 原則
設計 token 只有一個來源（TS 常數檔，CSS 變數與它 1:1 同值），元件只取 token；可機器判斷的禁止項寫成 lint 並用只降不升的基準管理舊違規。

## 症狀
圖台長大後，每個面板的圓角、字級、灰階、陰影都略有不同；有人寫死 hex、有人引入 web font；暗色模式修好了，淡色模式沒跟上；規格文件寫了沒人遵守。

## 原因
規格只存在文件裡，沒有程式碼層的唯一來源與自動檢查；舊程式碼太多，一次改完不現實。

## 解法
1. **Token 單一來源**：顏色、字級、圓角、間距、陰影、z-index、控制項尺寸各一個 TS 常數檔，CSS 變數檔與它 1:1 同值，另用測試強制兩邊同值。元件只取 token，不寫死 hex／rgba。資料色（圖層識別色、分級色、特效色）屬資料語意，放在圖層或資料檔常數，不進 token；token 只管介面 chrome（面板、按鈕、文字、邊框）。
2. **暗／淡並行，系統字**：每個元件都有暗色（預設）與淡色兩套值，淡色值只來自一個 `LIGHT` 色票，設計稿與驗收都並排看。不載 web font：一般文字用系統字 stack；數字／時間／座標／代碼用等寬系統字，只包在「只含數字」的最小節點上並開 `tabular-nums`。新的根容器（portal、獨立頁）要明確設字型，否則會落到襯線字。
3. **規格文件 + checklist**：規格寫「用途、結構、尺寸、暗/淡、狀態、禁止、實作檔」；另有一份 PR 前逐項勾的 checklist。
4. **ratchet 式自動檢查（lint）**：把可機器判斷的禁止項（寫死 z-index、原生 range、▶▼ 字元當 chevron、uppercase eyebrow、web font、英文控制項標籤、等寬字包中文）寫成 lint 規則；舊違規記錄成基準（每檔每規則的筆數），**只准減少**；計數減少時強制降低基準，違規增加或新檔案出現違規就失敗。禁止用 inline disable 繞過。紅燈要修程式碼而不是改基準，唯一例外是先在規格登記的刻意例外。
5. **不抽通用元件庫**：業務元件與地圖深耦合時，共用的是規格與少數已存在的共用元件（面板標頭、資訊列、來源 footer、按鈕、圖層控制項、滑桿），不為了「整齊」另做一套 Button/Card。

## 怎麼偵測
- 通用：同類型元件圓角／字級不一致；淡色底圖下某個面板還是深色；出現未載入的字族名。
- 搜尋：`#[0-9a-fA-F]{3,8}` 或 `rgba?\(` 出現在元件 CSS 與 TSX 的 style；`fontFamily:\s*["'](Inter|Georgia|JetBrains)`；`@font-face|fonts\.googleapis`；`z-index:\s*\d{2,}`；`type="range"`；`textTransform:\s*"uppercase"`（適用 stack：任何前端框架，lint 規則寫法依工具而異，ESLint／Stylelint 皆可）。

## 出處
- 一般 design token 做法（W3C Design Tokens 社群規格、各大設計系統的 token 分層）；ESLint bulk suppressions 的概念（只減不增的基準）。
- 實例：[design-system/spec.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)、[src/styles/designTokens.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/styles/designTokens.ts)、[src/styles/__tests__/designSystemGuard.test.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/styles/__tests__/designSystemGuard.test.ts)（token 兩邊同值的守門測試）。
