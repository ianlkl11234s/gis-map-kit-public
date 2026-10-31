---
id: 09-06
title: 圖層控制項：用規格自動產生，固定順序與元件種類
topic: 09-design-system
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [控制項, 滑桿, 開關, 選單, 分段, 篩選, select, filter, opacity, 規格驅動, 連動選單]
---

## 原則
圖層控制項由一份宣告式規格自動產生，固定順序與元件種類，不在元件內手寫；選項 ≥ 4 用原生下拉，2～3 個互斥選項才用分段。

## 症狀
每個圖層的控制區長得不一樣：滑桿樣式不同、開關有三種尺寸、篩選選單在不同位置、選項太多時用按鈕排滿、期別／指標選單彼此連動卻各寫各的而出現不合法組合。

## 原因
控制項由各圖層手寫 JSX。

## 解法
1. **規格驅動**：每個圖層的控制項寫在一份宣告式規格（類型：滑桿、開關、分段、選單、多選、色盤、連動選單；標籤、範圍、預設值、類別），UI、URL 參數、場景存檔、AI agent 控制都讀同一份規格。不要在元件內手寫控制項。
2. **固定順序**：資料篩選 → 顏色 → 透明度 → 大小 → 其他外觀 → 說明・來源。類別由規格或標籤詞彙表決定，並有測試：新標籤分不出類就失敗。
3. **版面**：標籤＋數值同一行，控件全寬在下一行；標籤小字、數值等寬字靠右。
4. **元件種類與使用時機**：
   - 滑桿：統一共用元件，禁用原生 `type="range"`（樣式不一致）；細軌道、小圓點、已拖段較亮。
   - 開關：只有兩階——「整層開／關」（中性黑白，依主題）與「層內細項」（強調色），不做第三種尺寸；`role="switch"`＋`aria-checked`＋`aria-label`。
   - 分段：2～3 個互斥選項；選中以 `aria-pressed` 表達。
   - 下拉：≥ 4 個選項用原生 `<select>`；要畫色條的（色盤）才用自製元件，且不可自由取色，只能從驗證過的色盤庫挑。
   - 多選：展開清單＋「全選／清除」。
   - 連動選單：選項非同步載入且彼此連動時，上游改變後，下游目前值仍合法就保留，否則改成第一個合法值；只有一個值的維度不顯示；選項載入中保留佔位列避免版面跳動；值只存在一個 store，不複製。
5. **圖示按鈕**一定有 `title` 與 `aria-label`；focus-visible 有明確外框；停用統一降低不透明度。
6. **避免多餘或不一致的控制**：不放沒有功能的按鈕（「規劃中」「敬請期待」），也不要再加一個與開關重複功能的「隱藏」鈕；中文介面不出現英文控制項標籤，標籤用目前語系。

## 怎麼偵測
- 通用：開不同圖層的控制區，比對滑桿、開關、順序；選項 ≥ 4 的控制是否是下拉。
- 搜尋：`type="range"`；元件內自己寫 `<select>`／`<input type="checkbox">` 作為圖層控制；`labelPrefix:\s*["'][A-Za-z]`；規格陣列的順序與類別不一致（適用 stack：有集中控制規格的架構；其他架構可借用「順序與元件種類」的規則）。

## 出處
- 一般表單與無障礙實務（WAI-ARIA switch、listbox、button pressed 屬性）。
- 實例：[design-system/spec.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)、[src/data/layerParamsSpec.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/layerParamsSpec.ts)、[src/components/controls/Slider.tsx](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/controls/Slider.tsx)、[src/state/__tests__/layerParamsOrder.test.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/state/__tests__/layerParamsOrder.test.ts)（順序與類別測試）。
