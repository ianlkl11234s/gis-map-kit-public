---
id: 08-06
title: 同時開幾個圖層：上限不要憑感覺，分「每種資源」各自設限
topic: 08-multi-layer
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [圖層數量, 上限, 可讀性, 效能, 面量圖, 單一, 可重疊, 同時只開一個, 選取圈, 面板, 脈衝]
---

## 原則
同時開幾個圖層要依資源分別設規則（填色圖層預設只畫一個、popup／選取圈／浮動面板同時只有一個），上限數字來自量測，不憑感覺。

## 症狀
- 同時開十幾個圖層，畫面糊成一片，使用者看不出誰是誰；或兩張面量圖互相蓋住，顏色變成混色。
- 使用者以為「資料不見了」，其實是被別的圖層蓋住。
- 動態圖層疊多了，掉幀或後端被打滿（見 [03-02](../03-dynamics/03-02-time-in-reactive-state-rerender-storm.md)、[03-05](../03-dynamics/03-05-time-window-and-prefetch.md)）。

## 原因
「同時開幾個」其實是好幾個獨立的資源上限，被當成一個數字：

| 資源 | 為什麼會爆 |
|---|---|
| 視覺可讀性 | 色彩通道有限，兩張以上的填色圖需要刻意設計才分得開 |
| 主執行緒／GPU | 動態圖層是 O(圖層數 × 更新頻率)（[03-02](../03-dynamics/03-02-time-in-reactive-state-rerender-storm.md)） |
| 後端連線 | 按日分檔 × 天數 × 圖層（[03-05](../03-dynamics/03-05-time-window-and-prefetch.md)） |
| 注意力／介面空間 | 面板、popup、圖例都爭同一塊畫面 |

## 解法
每種資源各設規則，並把規則寫成可測試的行為，而不是一個全域數字：

1. **填色（面量）圖層：預設同一時間只畫一個。** 提供「單一／可重疊」兩種模式，預設單一；網址分享要把模式也帶上，舊連結只要列出填色圖層就安全退回單一。開第二個時自動關掉最近開的前一個，並讓使用者知道。
2. **同一介面元素同一時間只有一個**：popup、選取圈、展開的資料來源卡（開新的就關舊的）；左側浮動面板的互斥做法見 [09-03](../09-design-system/09-03-panels-layering-and-portal.md)。圖例面板高度要有上限，圖例多了在面板內捲動，不要把 popup 擠出畫面。
3. **自動疊上去的分析結果設上限**（例如一次回答最多疊 3 個結果層；數字是示例，依自己的量測調整），超過就要使用者選擇或淘汰最舊的，並明確回報「已顯示」與否。
4. **裝飾性動畫（脈衝、漣漪）設同時上限**（例如 ≤ 20 個，同為示例），且只給即時或進行中的資料。
5. **動態圖層的成本用量測決定**：驗收項目是「全關＋暫停時 render 次數 = 0」與「開四層動態圖層仍順」。沒有實測門檻就不要寫成「同時最多 N 個圖層」的規則。
6. **全部關閉要好找**，且範圍明確（見 [08-03](08-03-layer-visibility-store.md)）；進站不預設開啟，降低首屏成本與選擇負擔。

## 怎麼偵測
- 通用：把可開的填色圖層全部打開，看是否出現「看不出是哪層」；同時開 4–5 個動態圖層，看掉幀；點一下地圖，看是不是同時彈出兩個資訊面板。
- 搜尋：沒有數量限制的疊加迴圈，例如 `layers\.forEach\(.*(show|add|enable)` 無上限檢查（any）；填色圖層的開關沒有互斥邏輯：兩個 `fill` 類圖層可同時 `visibility: 'visible'`（mapbox-gl、maplibre）。

## 出處
- 一般地圖設計建議（視覺變數有限）。
- 實例：[statisticsDisplayModeStore.ts（single／overlap 模式，URL 優先、舊連結退回 single）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/state/statisticsDisplayModeStore.ts)、[design-system/spec.md（浮動面板、選取圈、資料來源卡同時只有一個）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)。
