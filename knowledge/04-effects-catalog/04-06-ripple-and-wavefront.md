---
id: 04-06
title: 擴散漣漪與波前：每幀改 circle-radius 會讓地圖永遠 loading，改用 GPU 或 CSS 圈
topic: 04-effects-catalog
kind: pitfall
scope: public
evidence: Observed
stacks: [mapbox-gl, maplibre, three.js]
tags: [漣漪, ripple, 擴散, 地震, 脈衝, setPaintProperty, map.loaded, idle, 波前]
---

## 原則
不要每幀對 `circle-radius` 呼叫 `setPaintProperty` 做擴散圈；少量點節流處理，較多點改用 Three.js／raw WebGL 的 instanced 四邊形，單一選取點用 DOM／CSS 圈。

## 症狀
地震、新聞、警報點的「向外擴散圈」播放期間：`map.loaded()` 恆為 false、`idle` 事件不觸發（截圖、等待載入完成的流程卡住）；CPU 偏高。

## 原因
最直覺的做法是每幀對 data-driven `circle-radius` 呼叫 `setPaintProperty`。Mapbox 會把整份 GeoJSON source 標成需要 reload，漣漪播放期間地圖一直處於「載入中」。

## 解法
依規模選：
- 少量（數十點）且可容忍：節流到約 20fps 更新 paint，動畫相位用「時間」算而不是數幀，且圖層關閉／無新事件時停止迴圈。仍會有上述 loaded 副作用，需評估。
- 較多點或要乾淨的 `idle`：用 Three.js／raw WebGL 自繪。一個 `InstancedBufferGeometry` 四邊形 + `ShaderMaterial` = 1 draw call；每個震央 2 圈、相位差半個週期；`eased = 1 - (1-phase)^2`；半徑用螢幕像素；描邊在外側；不要用 `gl_PointSize`（最大圈在 DPR 2 可能超過 GPU point size 上限）。
- 座標精度：instance 位置存相對參考原點的偏移，平移在 JS（float64）先乘進矩陣，避免高 zoom float32 抖動。
- globe：zoom 5→6 之間 mercator 與 ECEF 混合；背面的圈整個收掉（見 [04-13](04-13-custom-layer-on-globe.md)）。
- 只想強調一個被選取的點：用 DOM／CSS 動畫圈（不經地圖資料管線）。
- 「新事件才扭動」：用 `now - event_ts < 窗口` 判斷，例如 15 分鐘內的新聞才有圈、重大事件延長到 60 分鐘，讓動畫帶資訊而不是裝飾。
- 若漣漪代表「傳播」（地震波）而不只是強調，半徑必須對應真實規則（速度×時間），見 [04-07](04-07-event-replay-scoped-clock.md)；否則只當裝飾，不要暗示傳播範圍。

## 怎麼偵測
- 通用：播放漣漪時 `map.loaded()` 一直是 false；e2e 或截圖腳本永遠等不到 idle。
- 搜尋：`setPaintProperty\(.*circle-radius`；`startThrottledRaf|requestAnimationFrame` 與 `setData\(` 同一函式（mapbox-gl、maplibre）。

## 出處
- 相關卡：[04-01](04-01-native-vs-custom-layer-decision.md)、[04-07](04-07-event-replay-scoped-clock.md)、[04-13](04-13-custom-layer-on-globe.md)、[04-15](04-15-animation-repaint-budget.md)。
- 實例：[mini-taiwan-pulse QuakeRippleScene.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/QuakeRippleScene.ts)（檔頭說明取代舊 setPaintProperty 做法）；[useNewsTimeline.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/hooks/useNewsTimeline.ts)（新鮮窗）。
