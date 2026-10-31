---
id: 04-14
title: 大氣與環境：天氣粒子、颱風、日夜、空域極光——純視覺要標明沒有資料
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, three.js]
tags: [天氣, 雨, 雪, 颱風, shader, 晨昏線, 日夜, 大氣, 極光, 空域, Fresnel]
---

## 原則
程序化的氣氛效果（雲型、極光、大氣光暈）一律標示「示意」，不與真實資料共用圖例語意，並提供關閉選項、尊重減少動態設定。

## 症狀
想讓地圖有「氣氛」：雨雪雷電、颱風雲、日夜交替、大氣邊緣光、禁航區的極光感。風險是氣氛被當成資料，使用者以為颱風雲型是真的。

## 原因
這類效果多是程序化 shader，沒有對應資料。

## 解法
| 效果 | 做法 |
|---|---|
| 雨／雪／雷 | 粒子；強度（0–1）與降雨率（mm/h）來自資料；跟隨相機的**單位盒**，依相機距離縮放，才不會拉近淹沒鏡頭、拉遠消失 |
| 颱風雲 | 位移網格（眼牆最高、眼是坑、雨帶為脊）+ 法線打光；fragment 重建對數螺旋雨帶、中央密雲區、亮眼牆、沿螺旋相位的雜訊絲縷、密度驅動透明度。**純視覺，不隨颱風實況變形**；真實路徑、預報用另一層（預報用虛線） |
| 日夜 | 白天／夜晚兩張貼圖依太陽方向混合 + Fresnel 大氣光暈；平面地圖用晨昏線多邊形（NOAA 太陽位置算法，逐經度算緯度避免換日線斷裂） |
| 空域極光 | custom layer shader 依空域分類索引上色、做流動光幕感；裝飾動畫走全域重繪節流（見 [04-15](04-15-animation-repaint-budget.md)） |
| 動態視域 | 扇形 mesh + 掃描線；buffer 直接更新（比 `setData` 快兩個數量級）；`depthTest:false` 避免地形遮擋 |

規則：
- 圖例或說明標示「示意」；不要把程序化雲型放在跟真實資料同一個圖例語意裡。
- 裝飾性氛圍預設可關閉，並尊重減少動態設定。

## 怎麼偵測
- 通用：氣氛效果沒有任何關閉選項或說明；颱風雲型與當前預報不符卻沒有標示。
- 搜尋：shader 檔名含 `typhoon|storm|rain` 但沒有對應資料 loader（three.js）。

## 出處
- NOAA 太陽位置算法（晨昏線）。相關卡：[04-15](04-15-animation-repaint-budget.md)、[04-16](04-16-dont-fake-dynamics.md)。
- 實例：[mini-taiwan-pulse useTyphoonTracksLayer.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/hooks/useTyphoonTracksLayer.ts)（真實路徑與預報虛線另成一層）。

