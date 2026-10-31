---
id: 13-06
title: 鏡頭總覽俯視、場景才傾斜；立體要有理由，預設平面且每層可開
topic: 13-author-taste
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [鏡頭, pitch, bearing, 3D, 立體, 總覽, 傾斜]
---

這是作者的設計偏好，不是業界規範；你可以不同，但要說得出理由，偏離時在 README 或 PR 寫一句。

## 原則
總覽用俯視（pitch 0、bearing 0），進入特定場景才傾斜；立體要有理由，預設平面、每層可開。

## 症狀
- 一打開地圖就是傾斜視角，總覽時比較面積與位置會失真。
- 平面資料硬做成立體，反而遮擋與難以讀值。

## 原因
傾斜與立體是強烈的視覺語言，只有在「場景」（機場、車站、地形）才增加資訊。

## 解法
1. 總覽 pitch 0、bearing 0，以全區或單一城市框景。
2. 進入特定場景才傾斜（常見 pitch 45–60），並提供回到俯視的方式；鏡頭動作規範見 [04-12](../04-effects-catalog/04-12-camera-motion.md)。
3. 立體要有理由：高度、體積要對應資料量（見 [04-11](../04-effects-catalog/04-11-3d-volumes-data-encoding.md)）；沒有理由就維持平面。
4. 預設平面、每層可開：預設只有移動物件這類必須立體的才立體；其他圖層提供「立體效果」開關。
5. 不用 chase cam（固定尾隨視角），除非任務明確需要。
6. 低縮放是否用 globe 沒有預設，依專案需求決定。

## 怎麼偵測
- 搜尋：初始化 `pitch:\s*([1-9][0-9])`（總覽預設就傾斜）、`fill-extrusion` 用在沒有高度意義的欄位（適用 stack：mapbox-gl、maplibre）。
- 通用：總覽畫面是否 pitch 0；每個 3D 圖層是否有關閉選項與使用理由。

## 出處
- 見 [04-11](../04-effects-catalog/04-11-3d-volumes-data-encoding.md)、[04-12](../04-effects-catalog/04-12-camera-motion.md)。
- 實例：[mini-taiwan-pulse 鏡頭預設（總覽 pitch 0、場景傾斜）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/cameraPresets.ts)。
