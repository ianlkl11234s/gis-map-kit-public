---
id: 09-04
title: 圖例規格：標題、色票型態、與地圖同源、可收合的範圍
topic: 09-design-system
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [圖例, legend, 色票, swatch, 漸層, 缺值, 收合, 精簡版, 標題]
---

## 原則
圖例用共用元件組成（標題、內容列、註記），色票與地圖 paint 共用同一個顏色常數；整體可收合，但色階、分界數字與單位不可收。

## 症狀
各圖層圖例長得不一樣：標題大寫英文在前、色票尺寸各寫各的、有的有單位有的沒有、popup 打開時圖例擠掉畫面。

## 原因
沒有共用的圖例元件與型別規格。

## 解法
1. **共用元件**：標題、列、註記、色票類型各一個小元件，圖層只提供資料。圖例結構固定為：標題 → 內容列 → 註記（方法、缺值、來源）。組間距、列間距、色票與文字間距統一。
2. **標題**：主要語言在前，次要語言小字在後，不轉大寫；標題要含指標與單位。
3. **色票型態**（8 種就夠）：點類別（圓＋描邊，描邊同地圖）、面類別（方塊，只畫外框的面用同色外框）、序列分級（每級一格，下方標實際分界數字）或連續漸層條（兩端「低／高」＋單位）、線型（含虛線 dasharray 一致）、大小（小/中/大三圓，直徑＝地圖實際直徑）、icon（與地圖同一 sprite）、缺值／遮蔽（斜線，同地圖 pattern）、熱區／影像漸層。
4. **色票與地圖同源**：常數共用、依主題取色、門檻數與色數對齊的規則見 [05-08](../05-color/05-08-legend-key-mismatch.md)；本卡只補一條：面外框用與地圖細縫同一個色。
5. **文字與數值**：文字色走主題 hook，不直接用全域 token；數字、分界、單位用等寬字加 `tabular-nums`，中文用一般字。大數用「1.2 萬」等單位縮寫、千分位；百分比固定小數位；必寫單位；缺值寫「無資料」。
6. **收合與高度**：圖例面板整體可收合（使用者控制）；註記與來源可收，**色階、分界數字、單位不可收**；popup 開啟時進入精簡版（只收註記）；分析結果出現時自動展開一次。右下停靠區（popup＋圖例）上緣封頂在工具列下，popup 保留自身高度，圖例吃剩下的空間，標題列固定、內容捲動。

## 怎麼偵測
- 通用：比對各圖層圖例的標題格式、色票尺寸、數字字型；popup 開啟時圖例是否仍顯示色階與單位。
- 搜尋：圖例檔案內手寫 `width:\s*\d+px;\s*height:\s*\d+px` 的色票；標題字串全大寫英文；`text-transform: uppercase`（適用 stack：any）。

## 出處
- 一般地圖製圖：圖例需完整、與符號一致。
- 實例：[design-system/spec.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)、[design-system/map-layers.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)、[src/components/legend/legendKit.tsx](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/legend/legendKit.tsx)。
