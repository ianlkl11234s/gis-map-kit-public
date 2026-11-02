---
id: 09-02
title: 圖層 UX 四鐵則：透明度、圖例、popup、選單，缺一不可
topic: 09-design-system
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [圖層, 透明度, 圖例, popup, select, 驗收, checklist, 鐵則, 新增圖層]
---

## 原則
每個新圖層都要有透明度滑桿、圖例、popup、選單這四項，缺口不得用 `null` 靜默豁免；可測的交給自動測試，測不到的人工點一次。

## 症狀
新圖層上線後：看不出類別（沒圖例）、點了沒反應（沒 popup）、蓋住別的圖層又不能調（沒透明度）、篩選選項太多用按鈕排滿（沒用下拉）。這些問題每個新圖層都可能重複出現。

## 原因
每個圖層的作者各自決定要不要做這些 UX 項目，缺少統一的準入標準與自動守門。

## 解法
把四件事當成「圖層準入條件」，缺一不可，缺口不得用 null 靜默豁免：

1. **透明度滑桿**：所有圖層（填面、線、點、3D）都要有；必須作用在該圖層所有主體子圖層，驗收時測兩端（0.1 與 1.0）。
2. **圖例**：只要圖層用顏色區分 ≥ 2 類或級別，就要圖例。判斷三問：paint 是否用 `match`／`step`／依屬性 `interpolate`？同層會不會出現 ≥ 2 色？看到色塊能不能直覺對到資料意義？（見 [05-08](../05-color/05-08-legend-key-mismatch.md)）
3. **popup**：所有承載有意義屬性的 feature（點、面、線、3D）都要能點選出資訊；面與線不是點的豁免條件。popup 結構見 [09-05](09-05-popup-and-source-footer.md)。
4. **選單**：選項 ≥ 4 用原生下拉（保留無障礙與手機原生選擇器）；2～3 個互斥選項才用分段控制（[09-06](09-06-layer-controls-spec-driven.md)）。

自動守門與人工守門要分清楚：
- 可測試的（圖例對帳、`null` 豁免登記理由、每筆控制規格都有透明度滑桿）與測不到、要人工點的項目要分開標明。每個新圖層要人工點一次。
- 三邊配色（地圖 paint、popup、圖例）要共用同一份資料常數，避免改一邊忘另一邊。

## 怎麼偵測
- 通用：打開圖層，依序檢查四件事——有沒有透明度滑桿、顏色有沒有圖例、點一下有沒有資訊、選項多的控制是不是下拉。
- 搜尋：新圖層的註冊檔案裡 `legend: null|popup: null|params: null` 且沒有登記理由；`match`／`step` 的 paint 但圖例註冊表沒有該圖層 key（適用 stack：any；僅限有集中式圖層註冊的架構）。

## 出處
- 一般 GIS 圖台慣例（圖層面板 + 圖例 + 識別/popup + 透明度）。相關卡：[09-03](09-03-panels-layering-and-portal.md)（面板、z-index 分層、互斥與 portal）。
- 實例：[development-rules.md（四鐵則與三份清單分工）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/development-rules.md)、[design-system/map-layers.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)、[src/components/sidebar/__tests__/layerConsistency.test.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/sidebar/__tests__/layerConsistency.test.ts)、[src/data/__tests__/layerUxPolicy.test.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/__tests__/layerUxPolicy.test.ts)。
