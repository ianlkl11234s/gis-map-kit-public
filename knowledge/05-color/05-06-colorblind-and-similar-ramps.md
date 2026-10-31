---
id: 05-06
title: 色盲模擬與「太像」的色階：只靠色相區分的設計會失效
topic: 05-color
kind: pitfall
scope: public
evidence: Evaluated
stacks: [any]
tags: [色盲, protan, deutan, tritan, ΔE, OKLab, 色盤, 太像, 換色]
---

## 原則
用明度差而不是色相區分等級與類別；提供換色功能時，先量化色階兩兩相似度，太像的組合要提示，並在實際底圖與透明度下目視檢查。

## 症狀
- 色覺異常（約 8% 男性有紅綠色弱）的使用者無法分辨兩個類別或兩個等級。
- 提供「換色」功能後，兩個同時開啟的熱區圖層選到相似色階，疊圖時分不出誰是誰。
- 色票通過了色盲模擬測試，卻在底圖＋透明度下仍然看不清。

## 原因
- 只靠色相（尤其紅／綠）而不靠明度差。
- 色階之間的相似度沒有量化。
- 色票測試只檢查色票本身，沒有檢查底圖與透明度疊加後的真實畫面。

## 解法
1. 色階靠明度（L）單調辨識。用 protan／deutan／tritan 模擬後檢查相鄰級別的明度差（實用護欄：CIELAB L* 相鄰差 > 5，或 OKLab ΔL ≥ 0.06）。
2. 提供色盤選單時，先做兩兩相似度表（OKLab ΔE×100，7 階平均，暗、淡兩版都算，任一版 < 8 視為太像）。實測只有約七成候選通過序列色階驗證，彼此都分得開的組合窮舉後只剩一小撮，所以建議清單要刻意縮小，其餘標為「與某代表太像」。
3. UI 上選了太像的組合時即時提示，不要靜默允許。
4. 主題 icon 與配色只當分類提示：圖形或文字要和顏色一起辨識，不能只靠不同色相區分主題。
5. 色票測試不等於可及性保證，還要在實際底圖、實際透明度下目視檢查。
6. 避免彩虹色（jet、turbo）：明度非單調，色盲下會出現假邊界。

## 怎麼偵測
- 通用：用色盲模擬（瀏覽器 DevTools 的 Rendering → Emulate vision deficiencies）看圖例；兩層同時開時能否分辨。
- 搜尋：色票陣列沒有任何明度檢查測試；`jet|turbo|rainbow`；同一頁出現兩個預設色階為同一色系（適用 stack：any）。
- 方法參考：Machado 2009 色覺模擬矩陣；OKLab 色差。

## 出處
- Machado, Oliveira & Fernandes 2009（色覺缺陷模擬）；ColorBrewer 色盲安全標示；Matplotlib viridis 設計說明。
- 相關卡：[05-01](05-01-color-ramp-decision-table.md)、[05-03](05-03-dark-light-ramp-direction.md)、[05-10](05-10-colorramps-used-catalog.md)。
- 實例：[色階驗證紀錄](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/layer-color-picker/ramp-validation.md)、[統計圖層規則 §4（L* 相鄰差護欄，不是無障礙保證）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/statistics-layer-guidelines.md)、[色彩可及性測試](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/__tests__/statisticsColorAccessibility.test.ts)。
