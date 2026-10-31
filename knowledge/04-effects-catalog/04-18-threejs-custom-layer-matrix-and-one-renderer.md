---
id: 04-18
title: Three.js 掛進地圖 custom layer：拿對投影矩陣，否則什麼都不畫也不報錯
topic: 04-effects-catalog
kind: pitfall
scope: public
evidence: Observed
stacks: [mapbox-gl, maplibre, three.js]
tags: [three.js, custom layer, CustomLayerInterface, 投影矩陣, mainMatrix, modelViewProjectionMatrix, 畫面外, 什麼都不畫]
---

## 原則
Three.js 掛進 custom layer 時，投影矩陣只從一個轉接函式取（Mapbox 用 `render` 的 `matrix`，MapLibre 新版用 `options.defaultProjectionData.mainMatrix`），並用 `map.project` 驗證數值，不要只看有沒有報錯。

## 症狀
- Three.js 物件接進 Mapbox 或 MapLibre 的 custom layer，資料都到了、沒有錯誤，畫面卻什麼都沒有。
- 從 Mapbox 移植到 MapLibre 後物件消失；用 `map.project` 一比，物件被投到畫面外數萬 px。

## 原因
Mapbox 的 `render(gl, matrix)` 第二參數就是 mercator 投影矩陣；MapLibre 新版的第二參數是**物件**，投影矩陣在 `options.defaultProjectionData.mainMatrix`。把整個物件或別的矩陣欄位（例如 `modelViewProjectionMatrix`）餵給 Three.js camera 不會報錯，只會靜默把物件投到畫面外。

## 解法
1. 寫一個轉接函式，只在那裡依引擎與版本取矩陣：Mapbox 用 `matrix`；MapLibre 第二參數為物件的版本用 `options.defaultProjectionData.mainMatrix`。升級引擎時查 changelog，這個簽名改過。
2. 數值驗證：取幾個已知經緯度，用你的矩陣算螢幕座標，與 `map.project(lngLat)` 比對，誤差應在 1 px 內；超過就是矩陣或座標轉換錯了。
3. globe 投影見 [04-13](04-13-custom-layer-on-globe.md)；大座標精度抖動見 [04-06](04-06-ripple-and-wavefront.md)；多個 renderer 互相干擾見 [04-19](04-19-threejs-one-renderer-per-gl-context.md)。

## 怎麼偵測
- 通用：資料筆數正確、沒有錯誤，畫面空白。
- 搜尋：`render\(gl,\s*\w+\)` 裡把第二參數直接 `fromArray` 進 `projectionMatrix`，而套件是 maplibre 新版（maplibre、three.js）。

## 出處
- MapLibre GL JS `CustomLayerInterface`、`CustomRenderMethodInput` 文件；Mapbox GL JS `CustomLayerInterface` 文件與官方 Three.js 範例。
- 相關卡：[04-01](04-01-native-vs-custom-layer-decision.md)、[04-13](04-13-custom-layer-on-globe.md)、[04-17](04-17-effect-prototyping-workflow.md)、[04-19](04-19-threejs-one-renderer-per-gl-context.md)。
- 實例：[mini-taiwan-pulse LESSONS.md 小實驗 13](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/LESSONS.md)（MapLibre × Three.js spike，與 `map.project` 比對）、[GLOSSARY.md 的 mainMatrix 條目](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/GLOSSARY.md)。
