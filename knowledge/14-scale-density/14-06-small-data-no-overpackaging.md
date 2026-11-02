---
id: 14-06
title: 資料少時不要過度包裝：數百點以內直接畫，個位數到數十點用大一階的點加名稱
topic: 14-scale-density
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [少量資料, cluster, 熱區, 過度包裝, 點大小, 標籤, 個位數, 數百點]
---

## 原則
數百點以內直接畫點，不用 cluster、熱區或高 minzoom；個位數到數十點用大一階的點加名稱。

## 症狀
- 全圖只有數百個測站，卻套了 cluster，使用者看到一堆「12」「37」的圓圈，要點好幾下才看到站。
- 20 個重點設施用最小的點，縮遠就找不到。
- 只有幾個點的分析結果，套了熱區，畫面是幾團模糊的光。

## 原因
聚合、熱區、網格都是為了「點太多看不清」設計的。資料少時，它們只會把原本可以直接讀的資訊藏起來。

## 解法
1. **數百點以內直接畫點**（點數門檻見 [14-02](14-02-point-count-thresholds.md)），不用 cluster、不用熱區、不設高 minzoom。
2. **個位數到數十點用大一階的點**，並直接標名稱；這時每一點都值得被看見。
3. **少量結果不要用熱區**：熱區要有足夠的點才有「密度」可言。分析結果可以依點數自動選階（數字見 [14-02](14-02-point-count-thresholds.md)）。
4. 點少但分布很集中時，先拉近鏡頭（自動 fit bounds），而不是換聚合。
5. 資料少不代表要裝飾：不要為了讓畫面「看起來有東西」加脈衝或光暈；脈衝只給進行中的事件（[04-09](../04-effects-catalog/04-09-emphasis-pulse-beam.md)）。

## 怎麼偵測
- 通用：數一下全圖點數；低於 [14-02](14-02-point-count-thresholds.md) 第一條線卻有 cluster 數字圈或熱區，就是過度包裝。
- 搜尋：`cluster:\s*true` 或 `markerClusterGroup` 的資料檔只有數百筆（看檔案大小 < 200 KB 或 features 長度）；`type: ['"]heatmap['"]` 的 source 點數低於 [14-02](14-02-point-count-thresholds.md) 第一條線（適用 stack：mapbox-gl、maplibre、leaflet）。

## 出處
- 一般建議：cluster 與 heatmap 的適用前提是點數多到互相遮蔽。
- 實例：[mini-taiwan-pulse 圖層樣式規範（少量點不聚合）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)。
- 實例：[分析結果依點數分階的規格](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/viz-library/DECISIONS.md)。
