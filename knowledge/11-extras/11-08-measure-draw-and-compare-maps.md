---
id: 11-08
title: 量距離面積與雙圖比較：做法選項與手機替代
topic: 11-extras
kind: decision
scope: public
evidence: Candidate
stacks: [mapbox-gl, maplibre]
tags: [量測, 距離, 面積, 繪製, 框選, 雙圖比較, swipe, 捲簾, 前後比較, 手勢衝突]
---

## 原則
量面積與距離用測地函式、不在 Web Mercator 平面上量；前後比較優先做「同一張圖疊兩個顏色」，雙圖並排與捲簾只在真的需要時才做，且手機要有單一視圖替代。

## 症狀
- 使用者想量兩點距離、框一塊範圍算面積，圖台沒有工具，只能另開別的軟體。
- 想做「前後比較」，直覺做成左右兩張同步地圖，手機上每張都小到看不出差異。
- 手機上畫多邊形與地圖拖曳搶手勢。

## 原因
量測與比較看似小功能，實際牽涉座標系、手勢衝突與版面，容易一次做太大。

## 解法
本卡為候選設計，量測與雙圖並排未經實作驗證。

**量測／框選**
1. 繪製用既有的 draw 套件（如 `mapbox-gl-draw`、`terra-draw`），計算用 turf 之類的測地函式（球面或橢球面），不要在 Web Mercator 平面上直接量面積。
2. 結果標單位與方法（球面近似）；多邊形要處理自相交與跨 180° 經線。
3. 手機：繪製模式要明確進入與離開，進入時停用地圖拖曳。
4. 開發用的範圍選取工具若只在 localhost 使用，不要打包進 production。

**前後比較**
1. 最便宜且手機友善：同一張圖疊兩個顏色（例如變前橘、變後藍），主敘事用文字寫「前 N → 後 M」加增減徽章，不要只靠目視。
2. 手機改成底部 sheet 加分段控制，一次只看一條，必須有單一視圖替代。
3. 真的要雙圖並排（兩個 Map 同步鏡頭）或 swipe 捲簾時，手機改上下排列或切換。
4. 時間比較的核心是「同一位置、不同時刻」，配合分享網址的時間參數（[11-04](11-04-share-camera-og-image-saved-scene.md)）。

## 怎麼偵測
- 通用：手機尺寸下開比較視窗，兩張圖是否都能看清；量測結果是否標單位。
- 搜尋：`mapbox-gl-draw|terra-draw|@turf/(area|length|distance)`；`new (maplibregl|mapboxgl)\.Map` 在同一頁出現兩次且有鏡頭同步（`move` 互相呼叫）（適用 stack：mapbox-gl、maplibre）。

## 出處
- turf.js 文件（`area`、`length`）；各 draw 套件文件（用前查）。
- 相關卡：[11-04](11-04-share-camera-og-image-saved-scene.md)。
- 實例：[mini-taiwan-pulse 單圖疊兩條軌跡、手機分段切換](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/satelliteConsole/ManeuverCompareModal.tsx)。
