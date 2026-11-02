---
id: 14-02
title: 點的數量級門檻：1 千、1 萬、10 萬三條線，分別調透明度、低縮放換熱區、延後出點
topic: 14-scale-density
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [數量級, 門檻, 熱區, heatmap, cluster, 出點縮放, minzoom, 透明度, 密集點, 10k, 100k]
---

## 原則
以「全圖總點數」決定畫法：1 千以下直接畫、1 萬以上低縮放換熱區、10 萬以上延到 z12 才畫單點；門檻寫成共用函式，各層只傳入點數。低縮放不用 cluster 數字泡泡。

## 症狀
- 一份幾十萬點的資料在全國視角糊成一整片，看不出哪裡密。
- 有些層用 cluster、有些用 heatmap、有些直接隱藏，切換圖層時規則不同。
- 門檻是每層作者憑感覺定的，換人就變。

## 原因
密度的問題要用「全圖總點數」判斷，不是看當下畫面點數；把門檻寫進共用函式，每層傳入點數就得到同一套結果，才能一致。

## 解法
本卡是點數量級的門檻正本；渲染技術怎麼選（circle、PMTiles、instancing）見 [07-02](../07-performance/07-02-many-points-rendering.md)。以全圖點數決定（下列數字可依自己的地圖範圍調整）：

| 全圖點數 | 低縮放 | 出點縮放 | 點的預設不透明度 |
|---|---|---|---|
| < 1 千 | 直接畫點 | 不限 | 0.85 |
| 1 千–1 萬 | 直接畫點 | 不限 | 0.8 |
| 1 萬–10 萬 | 熱區 | z10 起換點 | 0.75 |
| > 10 萬 | 熱區（或密度格網） | z12 起才畫單點 | 0.6 |

規則：
1. **低縮放用熱區，不用 cluster 數字泡泡**（作者偏好）。cluster 適合「要點進去看個別點」的少量資料；作者的地圖以分布為主，熱區比一堆數字圓圈好讀。
2. 圖層本來就有較高的 minzoom 時保留原值，熱區補在它下面；不要讓點因為套門檻反而更早出現。
3. 門檻寫成一個函式（輸入點數，輸出出點縮放與預設透明度），各層只呼叫它，不寫字面值。
4. 點數改變（資料更新）時重算門檻；點數寫在程式或登記簿裡，讓審查看得到。
5. 熱區與點共用同一個 filter，篩選時兩者顯示同一批資料（[14-05](14-05-honest-aggregation.md)）。
6. 數萬到數十萬、要動畫或 3D 的，改走 GPU instancing（技術選型見 [07-02](../07-performance/07-02-many-points-rendering.md)、[14-07](14-07-moving-objects-and-trails-at-scale.md)）。

點徑（作者偏好，不是業界規範）：
- 預設：點徑固定三階（[09-10](../09-design-system/09-10-map-symbol-size-tiers.md)），靠透明度與熱區處理密度，不靠縮小點。
- 特例：全圖點數超過 10 萬、而且所有縮放都要顯示的圖層，才讓點徑隨縮放變化（填充量與效能考量，[07-02](../07-performance/07-02-many-points-rendering.md)）。起點：半徑 z0 0.7、z7 1、z11 2 px，z14 起回到該層的階；描邊 z11 以下 0、z13 起 1 px。
- 不當預設的做法：低縮放直接 minzoom 隱藏（會讓遠看沒有資料）、全部畫出（糊成一片）。資料本來就只在近看有意義時，隱藏仍可用。
- 熱區半徑與強度不全作品統一，依資料的空間尺度調，起點為 z10 半徑 12、z14 半徑 20。
- 點的尺寸分階：圖層依語意（密集／一般／強調），分析結果依點數，兩者並存。
- 同類資料的出現縮放不統一，依密度自行決定。

## 怎麼偵測
- 通用：在全國視角打開圖層，若是一整片同色、或有幾百個 cluster 數字圈，回頭查點數。
- 搜尋：`cluster:\s*true`、`clusterRadius`（看資料是否其實是分布型）；`type: ['"]circle['"]` 的 source 檔 > 2 MB 或點數 > 1 萬，卻沒有 `minzoom` 也沒有同 source 的 `heatmap` 圖層（適用 stack：mapbox-gl、maplibre）；Leaflet 用 `markerClusterGroup` 包數十萬點。
- 靜態檢查：`find public -name "*.geojson" -size +2M` 後逐檔查有沒有 cluster、heatmap 或改用向量圖磚。

## 出處
- 官方：Mapbox GL／MapLibre heatmap 與 cluster 文件。
- 繪製效能角度（填充量、instancing）見 [07-02](../07-performance/07-02-many-points-rendering.md)；尺寸三階見 [09-10](../09-design-system/09-10-map-symbol-size-tiers.md)。
- 實例：[mini-taiwan-pulse 縮放門檻與熱區參數](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/mapStyleScale.ts)（門檻、出點縮放、透明度）、[點徑特例](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/pointSpec.ts)（單層 8–18 萬點、全國視角合計約 35 萬點的全縮放點層）。
- 實例：[圖層樣式規範（密集點規則）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)。
