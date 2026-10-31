---
id: 04-02
title: 移動物件（車、船、飛機）：用時間插值，而且只在資料窗內動
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [lerp, 插值, 時刻表, GPS, progress, 沿線, 切段, 船舶, 公車, 列車, InstancedMesh]
---

## 原則
移動物件的位置一律由「資料時間」線性插值得出，資料窗外不外推、不畫；時刻表資料不用曲線平滑，要貼路線的車改插值「路線進度」再投回線上。

## 症狀
- 車子切過街廓、瞬移、跳回起點。
- 時刻表列車在站間先倒退再前進。
- 船在資料範圍外還在漂、斷訊兩端被畫成一條實線。
- 時間軸一播放整個 App 每幀重繪。

## 原因
位置直接吃了 GPS 誤差；曲線平滑套在「邏輯順序」資料上會 overshoot；插值外推到資料窗外；時間放在 React state。

## 解法
先分資料類型，再挑插值法：

| 資料 | 插值 | 備註 |
|---|---|---|
| 真實 GPS／AIS 軌跡（密集） | 相鄰兩點時間線性插值；平滑曲線只能用在這類 | 資料窗外不外推，直接不畫 |
| 時刻表（站序＋到離站時間） | 站間直線（或沿路網）線性插值，停站段停住 | 不可 Catmull-Rom |
| 公車／要貼路線的車 | 狀態變數改成「路線進度 0–1」，lerp 進度，再投回 LineString | 位置永遠在線上；換趟次時淡出／淡入，不跨趟插值 |
| 斷訊 | 超過門檻切段；中等缺口畫虛線標「推測」；更長則斷開 | 門檻依取樣頻率定，寫在 README |

實作要點：
- 畫面用 `InstancedMesh`（光球）或 deck `ScatterplotLayer`，一個 draw call。
- 時間來源是外部 store：RAF 內同步讀（`getTime()`），篩選／查表用節流訂閱（200–1000ms），跨日載入只在日期變時觸發。禁止把 `currentTime` 放進 React deps。
- 視覺平滑（柱高、位置）可加每幀 lerp（factor 約 0.05）避免 5 分鐘輪詢造成瞬切。
- 平面（2D）降階：節流 25fps 左右更新 GeoJSON `setData`，數百個物件以內可行；暫停＝不通知＝不更新。
- 使用者開 `prefers-reduced-motion` 時，動畫應降為即時跳轉或停用。

## 怎麼偵測
- 通用：播放時車子轉角切對角、站間倒退、資料窗外仍有點、換日後所有物件偏移 8 小時（時區）。
- 搜尋：`Catmull|CatmullRom` 同時出現 `schedule|timetable|stops`；`useState\(.*[Tt]ime` + `setInterval|requestAnimationFrame`；插值函式沒有 `clamp|return null` 邊界處理（適用 stack：any）。

## 出處
- 一般建議：沿線插值與時間資料的時區處理為地圖動畫通用做法。
- 相關卡：[07-06](../07-performance/07-06-float32-timestamp-precision.md)（時間戳不要存 Float32，用相對時間才不會一格一格跳）。
- 實例：[mini-taiwan-pulse 公車 progress 插值設計](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/bus/design.md)；[3D 與平面共用的純函式](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/wasteTruckFrames.ts)；[平面節流更新](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/flatMovingController.ts)。

