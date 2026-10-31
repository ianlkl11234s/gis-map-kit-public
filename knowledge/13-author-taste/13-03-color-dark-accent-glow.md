---
id: 13-03
title: 色彩：近黑底加單一強調色，發光只給進行中的東西
topic: 13-author-taste
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [色彩, 強調色, 發光, additive blending, 色階, bloom]
---

這是作者的設計偏好，不是業界規範；你可以不同，但要說得出理由，偏離時在 README 或 PR 寫一句。

## 原則
近黑底只配一個強調色；發光只給進行中的東西（即時、移動中、被選取），靜態資料不發光。

## 症狀
- 畫面彩度過高、每個圖層搶焦點；到處都在發光，看不出什麼是即時的。

## 原因
發光與強調色是稀缺的注意力資源，每個東西都用就等於沒有。

## 解法
1. 近黑底＋單一強調色：背景接近黑（略帶藍可），全專案選一個冷色或暖色當強調色，用在互動與焦點。
2. 資料色階：連續量用感知均勻的序列色階，類別色限制數量且不用紅（紅留給警示）；色階選擇見 [05-01](../05-color/05-01-color-ramp-decision-table.md)，缺值不用 0 的顏色（[05-04](../05-color/05-04-null-is-not-zero-color.md)）。
3. 發光只給「進行中」的東西：即時、移動中、被選取。靜態資料不發光。
4. 發光技法：疊加用 additive blending，點的光暈用多層半透明圓（見 [04-10](../04-effects-catalog/04-10-glow-bloom-points.md)）；光暈不透明度與半徑要設上限，避免糊成一片。
5. 顏色要有語意，先問「這個顏色代表什麼」，不是「我覺得這個好看」。

## 怎麼偵測
- 通用：靜態層也在發光；全畫面有三個以上互相競爭的亮色；紅色用在一般類別。
- 搜尋：`blending:\s*THREE\.AdditiveBlending`、`circle-blur`、`circle-radius` 於靜態資料層；hex 寫死散在元件裡而非 token（適用 stack：mapbox-gl、maplibre、three.js）。
- gis-review：發光圖層的資料是否為即時或選取狀態。

## 出處
- 見 [05-01](../05-color/05-01-color-ramp-decision-table.md)、[04-10](../04-effects-catalog/04-10-glow-bloom-points.md)、[05-04](../05-color/05-04-null-is-not-zero-color.md)。
