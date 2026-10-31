---
id: 12-03
title: 衛星地面軌跡、跨太平洋航班與全球連線在 ±180° 換日線被畫成橫跨全圖的線
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, leaflet, openlayers, deck.gl, three.js]
tags: [antimeridian, dateline, 換日線, longitude unwrap, satellite ground track, 跨太平洋, fitBounds]
---

## 原則
凡是會跨經度 ±180° 的線與 bounds（全球軌跡、跨太平洋航線、全球事件連線），畫線前一律依用途拆段、展開經度或走最短方向，不要把相鄰點直接連線。

## 症狀
- 衛星地面軌跡每繞一圈就有一條水平線從地圖右緣拉到左緣。
- 跨太平洋航線畫成鋸齒或繞地球反方向一整圈。
- 兩個事件之間的關聯弧線從亞洲往西繞到美洲。
- 鏡頭 fitBounds 到跨太平洋航班時，縮到整個世界。
- 地圖上的誤導：一條穿越歐亞非的假線，看起來像真實航路或衛星經過那些地區；繞遠路的連線會誇大兩點距離。

## 原因
經度在 +180 與 −180 之間不連續。相鄰兩點 179.9° 與 −179.9° 實際只差 0.2°，但線段直接連就是 359.8°。很多引擎還會把座標正規化回 [−180, 180]，讓手動展開的經度失效。

## 解法
依用途選一種，不要混用：
1. **拆段**（2D 線、地面軌跡）：相鄰經度差 > 180° 就斷開成 MultiLineString。適合衛星地面軌跡、要保留真實取樣點的航跡。
2. **經度展開（unwrap）**（連續動畫、3D 航線）：讓經度連續（170 → 190 而不是 → −170）；若引擎會正規化經度，就自己計算 Mercator x，或用支援 world copies 的繪法。
3. **最短方向**（兩點關聯弧線）：先比較 `|Δlng|` 與 `360 − |Δlng|`，走短的那邊。
4. **bounds**：跨換日線的範圍不能用 min/max 經度算，要用展開後的經度，或改成以中心點加距離。

3D 球面（笛卡兒座標）繪圖不受影響，問題只出現在平面投影。資料只在小範圍（例如單一國家沿海）、確定不跨換日線時可以不處理，但要在程式註明範圍假設。

## 怎麼偵測
- 通用：在地圖上找長度接近地圖寬度的水平線；對資料算「相鄰點經度差 > 180° 的比例」，非零就必須有處理。
- 搜尋（有沒有處理）：`rg -n -i 'antimeridian|dateline|unwrap|splitAtDateline|> ?180'`；全球軌跡相關檔沒有任何命中就是疑點。
- 搜尋（bounds）：`rg -n 'fitBounds|LngLatBounds|getBounds'`，再看是否以 min/max lng 計算。

## 出處
- GeoJSON RFC 7946 §3.1.9（Antimeridian Cutting）。
- Mapbox GL JS／MapLibre：`renderWorldCopies` 與經度超過 ±180 的行為說明。
- 實例：[衛星軌跡拆段](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/satelliteSGP4.ts)、[歷史航跡經度展開](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/HistoricalFlightTrailsScene.ts)、[關聯弧線取最短方向](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/globalEventsPresentation.ts)。

