---
id: 13-00
title: 作者的地圖設計品味總表：每項偏好一句理由，對應到細卡
topic: 13-author-taste
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [設計品味, 偏好, 預設值, 總表, 深色底圖, MapLibre, 系統字]
---

這是作者的設計偏好，不是業界規範；你可以不同，但要說得出理由，偏離時在 README 或 PR 寫一句。

## 原則
新專案先照下表的預設開工；要偏離時，在 README 或 PR 寫一句理由。每項偏好的細節與偵測條件在對應的細卡。

## 症狀
- 新專案每次都重新決定 SDK、底圖、字型、圓角、動態預設，每個作品長得不一樣。
- 被問「為什麼預設是這樣」，答不出理由。

## 原因
偏好沒有寫下來。本卡把偏好與理由放同一頁；每項都是「預設」，有理由就可以換。

## 解法
| 面向 | 預設 | 一句理由 | 細卡 |
|---|---|---|---|
| SDK | MapLibre；同時申請 Mapbox token 備用 | 無 key、無 map load 計費壓力；需要 Mapbox 專屬樣式或功能才換 | [13-01](13-01-sdk-maplibre-default.md) |
| 底圖 | 深色單色（接近黑）；衛星只在要看地表實況時用；淡色不是預設 | 底圖退後，資料浮上來 | [13-02](13-02-basemap-dark-mono-default.md) |
| 色彩 | 近黑底＋單一強調色；發光只給「進行中」；發光用 additive blending | 顏色與光都要有語意 | [13-03](13-03-color-dark-accent-glow.md) |
| UI | 一套規則：系統字、不載 web font、圓角 ≤8、資訊密度適中、玻璃深色面板 | 少一個決策，也少一個字型載入 | [13-04](13-04-ui-one-ruleset.md) |
| 動態 | 資料驅動、lerp 平滑；時間軸預設不播放；尊重 reduced-motion | 動態要代表資料，不是裝飾 | [13-05](13-05-motion-data-driven.md) |
| 鏡頭與立體 | 總覽俯視 pitch 0；場景才傾斜；立體預設關、每層可開 | 立體要有理由 | [13-06](13-06-camera-and-3d.md) |
| 尺度與密度 | 點徑固定三階；全國尺度密集點遠看熱區、近看單點（超過 10 萬點且全縮放顯示才讓點徑隨縮放） | 密度先靠透明度與熱區 | [14-00](../14-scale-density/14-00-scale-density-decision-table.md) |
| 反面清單 | 見 [13-07](13-07-dont-list.md) | 不假造、不裝飾 | [13-07](13-07-dont-list.md) |

## 怎麼偵測
給 gis-review：逐項比對 [13-01](13-01-sdk-maplibre-default.md)～[13-07](13-07-dont-list.md) 的偵測條件；命中不等於錯，要求補一句偏離理由。
- 通用：專案 README 或設計文件有沒有寫偏離預設的理由。

## 出處
- 作者個人偏好整理，非業界標準。
