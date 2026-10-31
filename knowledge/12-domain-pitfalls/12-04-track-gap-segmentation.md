---
id: 12-04
title: 船舶 AIS 與航班軌跡斷訊後被直接連線，畫出跨海峽、穿越陸地的虛構航跡
topic: 12-domain-pitfalls
kind: decision
scope: public
evidence: Evaluated
stacks: [mapbox-gl, maplibre, leaflet, openlayers, deck.gl, three.js]
tags: [AIS, gap, 斷訊, 切段, trips layer, flight track, great circle, 虛線, 推測航段]
---

## 原則
軌跡斷訊超過門檻就切段，不要把相鄰兩點無條件連線或插值；要畫推測航段就用不同線型並標「推測」，門檻用自己資料的間隔分布決定。

## 症狀
- 船的軌跡出現一條筆直、橫跨海峽或穿越島嶼的線。
- 航班軌跡在越洋段變成一條完美直線（或大圓弧），看起來像全程都有觀測。
- 回放動畫裡，船在斷訊期間以等速「滑」過幾百公里。
- 地圖上的誤導：使用者會把連線讀成真實航路，推論出「船走了這條航線」「飛機經過這個空域」；斷訊越長（常是關 AIS、出接收範圍或越洋）誤導越大，偏偏這些段落最常被拿來解讀。

## 原因
AIS 與 ADS-B 都是「有收到才有點」：接收站覆蓋不到、設備關閉、廣播間隔拉長都會留下空白。把相鄰兩點無條件連成線（或在回放時線性插值），等於替空白段捏造了一條路徑。用大圓弧補缺段也一樣，只是比較好看。

## 解法
先選一個門檻策略（兩種做法都有人用）：
| 選項 | 做法 | 適合 |
|---|---|---|
| A 單一門檻直接斷 | 間隔 > T 就斷開成 MultiLineString；T 取 30 分鐘（航班）～1 小時（AIS） | 「寧可斷也不要捏造」的監看、分析用途 |
| B 三段式 | < T1 實線、T1–T2 虛線標「推測航段」、≥ T2 斷開 | 想保留航程連續感的回放展示 |
再加上這些規則：
- 斷線門檻與「失聯／淡化」門檻是兩件事，分開設定（例如線 1 小時斷、船點 3 小時才淡化），避免整層都變淡。
- 門檻要用自己資料的間隔分布決定（看 P50／P90），不要照抄。
- 不拿大圓弧或插值補缺段；若要畫推測，用不同線型並在圖例寫「推測」。
- 一條 callsign 會被不同航班重用，航班軌跡一定要切段；同一 MMSI 的船只在時間間隔上切。
- 「完整」要分開驗：查詢涵蓋、航班有無取得、單班幾何連續；`done` 計數不等於有可畫的完整軌跡。

## 怎麼偵測
- 通用：對每條軌跡算相鄰點時間差的最大值與 P90；只要有大於門檻的間隔而程式沒有任何切段邏輯，就會出現虛構線。
- 通用：在地圖上找穿越陸地的船舶軌跡或越洋段的完美直線。
- 搜尋（有沒有切段）：`rg -n -i 'gap|maxGap|split.*(trail|track|path)|segment'` 在軌跡 loader／layer 檔；deck.gl `TripsLayer`、Mapbox `line` source 直接吃整條 path 時特別注意。
- 搜尋（大圓補線）：`rg -n -i 'greatCircle|great_circle|turf.*greatCircle|geodesic'`，確認只用於畫「航線示意」而不是填補觀測缺段。

## 出處
- ITU-R M.1371（AIS 廣播間隔依航速與狀態而變，停泊時可長達數分鐘）。
- 實例：[船舶監看的軌跡切段（間隔 1 小時斷、3 小時淡化）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/vesselWatchLoader.ts)與[改版紀錄](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/vessel-watch/changelog.md)（未切段時實測最大間隔 67 小時，59% 的船受影響）；[航班軌跡切段（預設 30 分鐘）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/flightTrails.ts)；[歷史航跡盤點](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/historical-flight-trails/inventory-2026-09-18.md)（12,232 班中 5,064 班有 > 15 分鐘間隔，規則「不拿大圓弧補成實測軌跡」）。

