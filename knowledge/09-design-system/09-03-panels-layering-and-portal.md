---
id: 09-03
title: 面板、層級與彈出層：停靠位置、z-index 分層、互斥與 portal
topic: 09-design-system
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [面板, panel, z-index, 互斥, portal, 下拉, popover, 停靠, 標頭, 彈出層]
---

## 原則
每個浮層先決定屬於哪一個語意層級，用層級表而不是調大 z-index；左側面板同時只開一個，下拉等彈出層一律 portal 到 body（渲染在 `<body>` 底下，不受父面板的高度與裁切限制）。

## 症狀
- 面板、popup、圖例、時間軸互相蓋住；為了壓過別人把 z-index 越寫越大（21、41、9999）。
- 同時開了三個左側面板，擠成一團。
- 下拉清單在有高度上限的面板內往下展開，被面板底緣裁掉，要在面板裡再捲一次。
- 「更多」選單被底部面板蓋住、按鈕看得到點不到。

## 原因
沒有定義「每個東西屬於哪一層」與「同一區域同時只開一個」，彈出層放在會裁切它的容器裡。

## 解法
1. **面板外殼統一**：同一種底色、邊框、圓角、陰影、字型；標頭固定結構（小標 eyebrow＋標題＋關閉鈕）；關閉鈕有 aria-label，不用純文字「×」。左側面板一律停靠同一個位置與上緣，與工具列／座標列對齊。
2. **左側面板互斥**：左側浮動面板同時只開一個，開一個就關掉其他；用一個純函式（輸入目前開了哪些、新開哪個，輸出要關哪些）統一處理並有測試。圖層面板這種本來就是同一個抽屜的不在清單內。
3. **層級表取代數字競賽**：定義少數語意層（地圖覆蓋 < 浮動面板 < 工具列 < 彈出層 < 置中視窗 < 提示），token 與 CSS 變數同值，並用測試鎖住順序。要誰在上面，先決定它屬於哪一層。
4. **同層靠 DOM 順序**：同一層要誰蓋誰，調整渲染順序（後渲染者在上），不要改數字。時間軸屬於地圖控制列，比面板低一層，面板或 popup 展開時應蓋在它上面。
5. **彈出層用 portal**：下拉、色盤、選單等一律 portal 到 body，不在有高度上限的面板內行內展開；下方空間不足就往上開；鍵盤支援（↑↓、Home/End、Enter、Esc 並把焦點還給觸發鈕），點外面關閉。按鈕本身若在比彈出層高的容器（例如手機底部抽屜），彈出層改用更高的層並靠 DOM 順序蓋上。
6. **危險操作兩段式**：不可逆操作先展開確認區塊，寫清楚後果，要求輸入確認字才啟用；失敗時留在區塊內說明資料還在。不使用 `window.confirm`。

## 怎麼偵測
- 通用：開所有面板／popup／圖例／選單，檢查有無互蓋；縮小視窗高度，看下拉是否被裁掉。
- 搜尋：`z-index:\s*\d{2,}|zIndex:\s*\d{2,}`（寫死大數字）；下拉元件用 `position:absolute` 在 `overflow:auto` 的面板內；`window.confirm` 用在刪除操作（適用 stack：any）。

## 出處
- 一般 UI 實務（modal / popover 分層、WAI-ARIA listbox 鍵盤互動）。
- 實例：[design-system/spec.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)（層級表、面板互斥、色盤選單 portal、危險操作）、[src/state/leftPanelMutex.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/state/leftPanelMutex.ts)。
