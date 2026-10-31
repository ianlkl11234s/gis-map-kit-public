---
id: 04-17
title: 效果原型工作流：案例庫挑元件、sandbox 調參數、再接進正式圖層
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, three.js]
tags: [原型, showcase, 案例庫, sandbox, 參數, 零 build, 工作流, 元件庫]
---

## 原則
新視覺效果先在零 build 的單檔案例庫調好參數、抄下順眼的數值，再接進正式圖層；不要直接在真實地圖上反覆調。

## 症狀
「上線後覺得太亮／太大」，且改一次要跑完整 build；元件散落在各圖層，沒有人記得有哪些可用。

## 原因
視覺參數在真實地圖上很難一次調準；沒有案例庫就重複造輪子。

## 解法
1. 建一個**零 build 的單檔 HTML 案例庫**：每個元件獨立可調（大小、透明度、速度、顏色），CDN 載 three。每個元件在目錄表記「適合表達什麼」與「技術」。
2. 流程：看到喜歡的案例 → 存截圖與拆解 → 同一變因 N 種 variant 並排（grid）→ 贏家做成完整實驗 → 要上線才走正式的新增圖層流程。
3. 在案例庫調參數，**抄下順眼的數值**再接線；跳過這步是「太亮／太大」的主因。
4. 元件分類（便於依語意挑）：基礎幾何、光效、動畫事件、shader 變形、粒子、線條路徑、數據視覺化、體積大氣、場景科幻、系統關係。
5. 命名編號不重編；實驗與正式圖層分開。
6. 接線必過清單：共用 GL context、座標轉換統一函式、blending 狀態備份還原、重繪驅動、dispose、動態時間源、性能（見 [04-18](04-18-threejs-custom-layer-matrix-and-one-renderer.md)、[04-15](04-15-animation-repaint-budget.md)）。

## 怎麼偵測
- 通用：同一個效果在多個圖層各寫一份；新增 3D 圖層的 PR 沒有 dispose 或 blending 還原。
- 搜尋：`new THREE\.WebGLRenderer\(` 沒有 `context:` 參數且在 custom layer 內；`onRemove` 無 `dispose\(\)`（three.js、mapbox-gl）。

## 出處
- 相關卡：[04-15](04-15-animation-repaint-budget.md)、[04-18](04-18-threejs-custom-layer-matrix-and-one-renderer.md)（接線時矩陣與 GL context 的坑）。
- 實例：[mini-taiwan-pulse three-showcase.html](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/public/three-showcase.html)（單檔案例庫）、[three-3d-component skill](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/skills/three-3d-component/SKILL.md)。

