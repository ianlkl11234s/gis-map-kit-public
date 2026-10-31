---
id: 12-08
title: 即時車輛插值製造假動態：曲線 overshoot 倒退、GPS 直線切街廓、跨趟次倒飛
topic: 12-domain-pitfalls
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [interpolation, lerp, Catmull-Rom, overshoot, snap to route, progress, 公車, 火車, 即時車輛, 回放, frame rate]
---

## 原則
插值只用在真實高頻的軌跡；時刻表與站序用直線插值，公車改用「路線進度」插值並切分趟次，平滑改用經過時間而不是固定每幀比例。

## 症狀
- 時刻表動畫裡的車在某些站「先往回退一點再前進」。
- 公車點瞬間跳回路線起點、跳到幾百公尺外，或在轉角直接切過街廓。
- 公車從終點沿路線倒著飛回起點（其實是回程開始）。
- 平滑移動的速度在低效能裝置上明顯變慢。
- 地圖上的誤導：倒退、切角、倒飛都是插值做出來的動作，觀眾會讀成真實的車輛行為（「這班車迴轉了」「車開進巷子」）。

## 原因
1. Catmull-Rom 這類曲線假設輸入是連續的真實軌跡；拿「邏輯順序的站點」（時刻表）去擬合，曲線在 Z 字形站序會超出兩點之間，看起來倒退。
2. 直接在兩個 GPS 點之間做 2D 線性插值，會跨過街廓；snap 到路線「最近點」時，GPS 漂移可能投影到路線另一段（例如起點附近或對向）。
3. 一天多趟往返時，路線進度從 0.9 直接插到 0.1，就是沿路線倒退。
4. 每幀固定比例的 lerp（例如每幀 0.15）收斂速度跟幀率綁在一起。
5. 路線線形檔比軌跡晚載入時，軌跡先退回沒貼路線的插值。

## 解法
1. 曲線平滑只給真實、高頻的 GPS 軌跡；時刻表、站序這類邏輯點一律直線插值（或改用真實路網路徑）。
2. 公車改用「路線進度」當狀態：每個 GPS 點先投影成路線上的 progress ∈ [0,1]，播放時對 progress 做 1D 插值，再由 LineString 換回座標，位置幾何上保證在路線上。
3. 趟次切分：時間間隔 > 約 15 分鐘或 progress 倒退 > 30% 就視為新趟次，跨趟次不插值、改淡出淡入。
4. 異常點：progress 前進超過「合理最高速度 × 時間差」就拒收；連續拒收數次則強制接受並開新趟次，避免卡死。
5. 平滑改用經過時間計算（例如 `1 - exp(-dt/τ)`），並限制單幀 dt 上限。
6. 路線檔載入完成後重建已到達的軌跡投影。

## 怎麼偵測
- 通用：慢速播放看有沒有倒退、切角、從終點滑回起點；在 30fps 節流下比較移動是否變慢。
- 搜尋（曲線插值用在哪）：`rg -n -i 'catmull|spline|bezier|curve' ` 在車輛／時刻表動畫檔，確認輸入是否為真實 GPS。
- 搜尋（每幀固定 lerp）：`rg -n 'lerp\([^)]*0\.[0-9]+\)|\+= *\([^)]*\) *\* *0\.[0-9]+'`。
- 搜尋（snap 最近點）：`rg -n -i 'nearestPointOnLine|snapToRoute|pointOnLine'`，再看有沒有趟次與異常處理。

## 出處
- Turf.js `nearestPointOnLine`／`along` 文件（路線投影與沿線取點）。
- 實例：[公車引擎](<https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/engines/BusEngine.ts>)（趟次間隔 15 分鐘、進度倒退 30%、80 km/h 異常上限、連續拒收 3 次、淡出 60 秒）與[公車設計文件](<https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/bus/design.md>)。
- 實例：[路線檔晚於軌跡載入時退回無路線插值，改為載完補建](<https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/bus/backlog.md>)；[每幀 lerp 改依經過時間計算（dt 上限 100 ms）](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/7d47b0125ec6f3c250a62a72f6f396fcdae4726a)。
