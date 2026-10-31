---
id: 04-11
title: 3D 量體編碼數值：光柱高度、長條柱、水位杯——能用 fill-extrusion 就別用 Three.js
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, three.js]
tags: [3D, 柱狀, extrusion, 光柱, 水位, 高度編碼, lerp, 量體, 水庫]
---

## 原則
能用原生 `fill-extrusion` 就不用 Three.js；用高度編碼數值時先正規化並夾住範圍，輪詢更新只改目標值、由每幀 lerp 趨近。

## 症狀
想用高度表示數值（發電量、用電、蓄水率），但柱子在輪詢更新時瞬間跳高；或 3D 讓比較變困難。

## 原因
高度編碼本身有誤導風險（透視縮短、遮擋）；而資料每 5 分鐘才更新，直接寫入會跳。

## 解法
1. 選型：棱柱用原生 `fill-extrusion`；模型用原生 `model` layer；需要發光、逐幀平滑、instancing 動畫才用 Three.js。
2. 編碼規則：
   - 高度 ∝ 數值，**先正規化並夾住範圍**（例如出力率 0–1.5 clamp）；右偏分布用 sqrt。
   - 柱色用另一個維度（燃料別、警戒燈號），不要與高度編碼同一變數。
   - 「容量 vs 當前量」用雙層：外殼固定高（半徑 ∝ 容量立方根）、內部水柱高＝蓄水率；固定外殼讓比較成立。
3. 平滑：frame lerp（每幀 `current += (target - current) * 0.05`），輪詢寫入只改 target。
4. 單 draw call：`InstancedMesh`，per-instance 顏色與縮放。
5. 靜態量體（水庫、車站柱）不要自己 `triggerRepaint`；資料／可見性變更時才喚醒重繪。
6. 溫度曲面：BufferGeometry grid，海洋 cell 剔除三角形，頂點高度＝正規化溫度，色＝色帶；兩個相鄰時間 frame 之間逐頂點 lerp。
7. 何時不用：只有 ≤ 十來個值要比較時，條狀圖或標籤更準；> 1,000 個點的密度改 h3／heatmap；使用者要精確讀值時必須提供 popup 數字。
8. 圖例要寫「高度 = 何者」，並標示是否為推估。

## 怎麼偵測
- 通用：資料更新時柱子瞬跳；高度與顏色重複編碼同一變數；3D 柱遮住後方柱子且沒有傾斜視角控制。
- 搜尋：`mesh.scale.y\s*=` 直接賦值為最新資料值，沒有 `lerp|damp`（three.js）。

## 出處
- 相關卡：[04-01](04-01-native-vs-custom-layer-decision.md)、[04-15](04-15-animation-repaint-budget.md)。
- 實例：[mini-taiwan-pulse PowerGenerationBeamScene.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/PowerGenerationBeamScene.ts)（高度編碼出力率）、[PowerRegionBarsScene.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/PowerRegionBarsScene.ts)（frame lerp）、[ReservoirScene.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/ReservoirScene.ts)（雙層水位杯）。
