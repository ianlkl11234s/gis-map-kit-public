---
id: 13-02
title: 底圖預設深色單色，衛星只在要看地表實況時用，淡色不是預設
topic: 13-author-taste
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [底圖, 深色, 單色, 衛星, 淡色, 標籤, 對比]
---

這是作者的設計偏好，不是業界規範；你可以不同，但要說得出理由，偏離時在 README 或 PR 寫一句。

## 原則
底圖預設用深色單色（接近黑），讓資料浮上來；衛星只在要看地表實況時用，淡色依情境並寫理由。

## 症狀
- 底圖顏色太多、道路與地名太搶，資料色被吃掉。
- 預設用衛星影像，疊上圖層後雜訊很高；或不需要地表資訊卻載了大量影像圖磚。

## 原因
底圖是背景。資料要浮上來，底圖就要退後（見 [02-08](../02-basemaps/02-08-dark-light-basemap-vs-data-contrast.md)）。

## 解法
1. 預設深色單色（接近黑），道路與面只留低對比骨架（壓低底圖對比的做法與深淺取捨見 [02-08](../02-basemaps/02-08-dark-light-basemap-vs-data-contrast.md)）。
2. 衛星只在需要看地表實況時用：土地利用、海岸線、建物現況這類問題。用完可切回深色。
3. 淡色不設為預設。依情境使用：投影在亮教室、要列印、或讀者主要在白天閱讀時，可以用淡色，並寫理由。
4. 標籤保留：地名不要整層關掉，語言跟著介面（降低對比的做法見 [02-08](../02-basemaps/02-08-dark-light-basemap-vs-data-contrast.md)）。
5. 提供底圖切換時，預設仍是深色。

## 怎麼偵測
- 通用：打開預設畫面，底圖是否搶過資料；預設是否為衛星；是否把地名全關。
- 搜尋：style URL 含 `satellite`、`light`、`streets`、`outdoors` 作為預設（適用 stack：mapbox-gl、maplibre）；`"symbol"` 圖層被整批 `visibility: none` 而沒有替代地名。
- gis-review 檢查：預設 style 是衛星，卻沒有土地利用／海岸／建物的需求描述。

## 出處
- 見 [02-08](../02-basemaps/02-08-dark-light-basemap-vs-data-contrast.md)（深淺底圖與資料對比）、[02-02](../02-basemaps/02-02-basemap-selection-decision.md)（底圖選型）。
