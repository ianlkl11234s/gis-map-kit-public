---
id: 04-07
title: 事件回放（地震、災害）：視覺是時鐘的純函數，時鐘獨立於全站時間軸
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [回放, replay, scoped clock, 傳播, propagation, 地震, 波前, scrub, 編排]
---

## 原則
事件回放用獨立的 scoped clock（單位是「事件後經過秒數」），畫面上每個元素都是這個時鐘的純函數；推算出來的傳播時刻要在圖例標明是模型假設。

## 症狀
事件回放（地震震後 N 秒）掛在全站時間軸上，單位對不上（事件秒 vs 日曆時間）；拖曳時畫面錯亂；回放期間整個 App 重繪。

## 原因
事件回放的時間單位是「事件後經過幾秒」，不是日曆時間；而且只有一個面板在用。

## 解法
1. **獨立 scoped clock**：external store（不是 React state）；寫入即時、通知節流到 10Hz；React 只有進度條訂閱；回放引擎自帶 RAF。
2. **視覺 = 時鐘的純函數**：每個元素的透明度／半徑／亮起與否都由 `t` 算出，不累積狀態。這樣 scrub 只要 `set(t)`，任意跳轉畫面都正確。
3. **分段編排**（範例：地震）：t=0 震央爆開 → t=距離/波速 測站逐顆亮起（色＝觀測震度）→ 同步等震度格網依波前淡入 → 波前掃完後鄉鎮面量圖定格淡入（格網壓暗）→ 收尾彈出震源機制球。資料不足時降階（只有測站就三步）。
4. **時間壓縮**：把回放總長換算成約 26 秒牆鐘時間，倍率夾在 0.4～4；告知使用者「回放秒 ≠ 真實秒」。
5. **標示模型假設**：「亮起時刻」來自 距離÷3.5 km/s 的等速近似，不是觀測；觀測值（震度）與推算值（抵達時刻）在圖例要分開寫。
6. 多圖層共用同一個 scoped clock 時，時間範圍取聯集，`setRange` 只呼叫一次。
7. 接收點多時，預先算好 `arrival_t` 寫進屬性，播放時只改 filter／feature-state，不要每幀重算距離。

## 怎麼偵測
- 通用：回放時整個 App 卡；拖曳進度條後某些元素殘留；圖例沒說明傳播速度假設。
- 搜尋：回放元件內 `useState\(.*(t|time|elapsed)`＋`setInterval|requestAnimationFrame`；動畫函式讀取上一幀狀態（`prev|last[A-Z]`）而不是從 `t` 計算（any）。

## 出處
- 相關卡：[04-06](04-06-ripple-and-wavefront.md)、[04-16](04-16-dont-fake-dynamics.md)。
- 實例：[mini-taiwan-pulse useEarthquakeReplayLayer.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/hooks/useEarthquakeReplayLayer.ts)（五步編排）、[earthquakeReplayClock.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/state/earthquakeReplayClock.ts)（scoped clock）、[earthquakeReplayTypes.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/earthquakeReplayTypes.ts)（S 波速度假設）。

