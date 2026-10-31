---
id: 09-05
title: popup 與來源 footer：固定結構、null 不渲染、來源缺漏要明講
topic: 09-design-system
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [popup, 資訊面板, 來源, footer, 授權, null, 內部 id, 選取圈, 停靠]
---

## 原則
popup 用固定結構的停靠式資訊面板，空值整列不渲染；來源資訊由統一的 footer 輸出，缺漏時明講「來源待補」，不顯示內部識別碼。

## 症狀
- 每個圖層的 popup 長得不一樣；欄位出現內部代號（dataset id、layer key）。
- 值為空的欄位顯示 0 或空白。
- 看不出資料來自誰、何時抓的、授權為何；來源資訊缺漏卻不提示。
- 錨定式 popup 的尖角蓋住要點的物件，在手機上更糟。

## 原因
popup 內容由各圖層自己組版，來源與狀態沒有統一出口。

## 解法
1. **停靠式資訊面板**：統一停靠一個位置（例如右下），不用錨定的小氣泡；點擊處另畫「選取圈」（呼吸或擴散的環）標示被點的物件，色用主色、動畫可被 reduced-motion 關閉。
2. **固定結構**：eyebrow（主題・圖層名，小字，不轉大寫）→ 標題（色點＋名稱）→ 資訊列（標籤小字靠左、值靠右或下一行）→ 來源 footer。圖例色塊不放在 popup 內（圖例走圖例面板）。
3. **資訊列規則**：值為 null／空字串／"null" 時整列不渲染；不要用 0 或「—」冒充；純數字用等寬字，整個容器不套等寬字。
4. **來源 footer**：統一出口、不由各 panel 自己畫。內容：機關・資料等級・原始下載頁連結；第二行授權・抓取時間。多筆溯源用 `<details>` 收合。沒有來源資訊時整段顯示「來源資訊待補」並用警示色，而不是省略。
5. **不顯示內部識別碼**：dataset id、layer key 先過人類可讀映射。popup 的主題色從統一 hook 取得，子元件不自己判斷主題。

6. **點選高亮**（分析結果類）：選中者原色＋主色描邊，其他降透明度；popup 關閉即恢復。滑過提示僅在 `(hover: hover) and (pointer: fine)` 啟用，觸控裝置另有點擊路徑（見 [09-09](09-09-responsive-and-touch.md)）。

## 怎麼偵測
- 通用：點開不同圖層的 popup，比對結構；找 null／空值是否顯示成 0；找不到來源行。
- 搜尋：popup 組件內自己寫 `來源|source|license` 區塊（重複）；`datasetId|layerKey` 出現在 JSX 文字；`?? 0` 於 Row 值（適用 stack：any）。

## 出處
- 一般資訊揭露與授權標示做法（開放資料授權條款要求標示來源）。
- 實例：[design-system/spec.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)、[featureInfo/shared.tsx（SourceFooter）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/featureInfo/shared.tsx)。
