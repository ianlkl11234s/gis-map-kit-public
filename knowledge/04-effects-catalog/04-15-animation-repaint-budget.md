---
id: 04-15
title: 動畫的重繪預算：custom layer 的 triggerRepaint 會重畫整張地圖
topic: 04-effects-catalog
kind: pitfall
scope: public
evidence: Evaluated
stacks: [mapbox-gl, maplibre, deck.gl, three.js]
tags: [triggerRepaint, 效能, 節流, 暫停, 閒置, draw call, 量測, DPR, requestAnimationFrame]
---

## 原則
重繪一律走全域排程器：靜態圖層不自己 repaint，裝飾動畫節流並在暫停、閒置時停止；優化前先量測，驗收標準是「全部圖層關閉並暫停 5 秒，map render 次數 = 0」。

## 症狀
暫停時間軸、全部圖層關閉，GPU 仍然很忙；一加幾個動畫圖層就掉幀；優化了半天沒有改善。

## 原因
- custom layer 呼叫 `map.triggerRepaint()` 重畫的是**整張地圖**（底圖、地形、globe、所有 style layer 與所有 custom layer），不是自己那層。
- 依掛鐘時間跑的純裝飾動畫（呼吸、閃爍、極光）在暫停時也要求重繪。
- 優化常常打在錯的地方：靜態軌跡量、光球數量都不是瓶頸。

## 解法
1. 區分三種圖層並各自處理：
   - 靜態幾何（水庫、車站柱、歷史軌跡）：**不自己 repaint**；資料或樣式變更時才喚醒一次。
   - 時間驅動（列車、船）：只有時間軸在走或資料時間改變才重繪。
   - 純裝飾（漣漪、閃爍）：節流（約 20fps），圖層關閉、無事件、時間軸暫停時停止。
2. 做一個全域重繪排程器：所有重繪走它。暫停且相機靜止 → 單一 `setTimeout` 排程（約 50ms）；連續約 30 秒無互動 → 完全停止裝飾重繪；任何互動／播放／控制項變更立即重繪並重置閒置計時；`document.hidden` 停止。只保留一個 pending timer。
3. 驗收標準：**全部圖層關閉並暫停 5 秒，map render 次數 = 0**。
4. 動畫相位用「時間」計算，不要數幀，這樣改節流頻率不會改變動畫速度。
5. 每幀位置更新用 typed array 直接寫 buffer（約 0.01ms），不要 `source.setData`（每幀 2–3ms，且被標 reload；逐幀改 paint 的同類問題見 [04-06](04-06-ripple-and-wavefront.md)）。
6. 軌跡類：批次成一個 draw call；slot 逐出用 min-heap（見 [04-03](04-03-trail-tails.md)）。
7. **先量測再優化**，同一症狀可能有多個根因、修完要重新驗收；量測方法見 [07-01](../07-performance/07-01-performance-budget-and-measurement.md)。

## 怎麼偵測
- 通用：DevTools Performance 顯示暫停時仍有連續 frame；風扇狂轉；`map.on('render')` 計數持續增加。
- 搜尋：`triggerRepaint\(\)` 出現在 `render\(` 方法內且沒有 `visible|playing|active` 的 early return；`requestAnimationFrame` 沒有對應 `cancelAnimationFrame`（mapbox-gl、maplibre、three.js）。

## 出處
- Mapbox／MapLibre `Map.triggerRepaint` 文件。相關卡：[04-03](04-03-trail-tails.md)、[04-06](04-06-ripple-and-wavefront.md)。
- 實例：[mini-taiwan-pulse reservoirCustomLayer.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/reservoirCustomLayer.ts)（靜態 3D 不自行 repaint）、[fireStationCustomLayer.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/fireStationCustomLayer.ts)（關閉後 0 repaint）。

