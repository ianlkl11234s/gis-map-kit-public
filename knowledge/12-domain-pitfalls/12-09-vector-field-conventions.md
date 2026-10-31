---
id: 12-09
title: 風場與海流的三個慣例：風向是「來向」流向是「去向」、經度 0–360、粒子跨世界邊界
topic: 12-domain-pitfalls
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [wind, ocean current, u/v, 風向, 流向, from/to, 0-360, GFS, GRIB, NetCDF, particle, wrap]
---

## 原則
風用「來向」、海流用「去向」，兩者公式不同並在 popup 寫明；全球網格先把經度從 0–360 重排成 −180–180；粒子跨世界邊界那一步不畫。

## 症狀
- popup 的風向和氣象局公布的差 180°。
- 全球風場只畫出東半球，或西半球整片錯位到東邊。
- 粒子動畫在地圖左右邊緣拉出一條橫跨全圖的線。
- 高緯度的粒子跑得比低緯快、軌跡變形。
- 地圖上的誤導：風向反 180° 會讓人讀成「颱風外圍風往外吹」或污染物往反方向擴散；錯位的格點會把海上的強風畫到陸地上。

## 原因
1. 慣例不同：氣象的風向是「風從哪裡吹來」（北風＝從北往南吹），海洋的流向是「水往哪裡流」。同樣從 u（東向）、v（北向）分量換算，公式差一個負號。
2. GFS 等全球模式的經度是 0–360，前端與 GeoJSON 慣用 −180–180；不重排就會只畫一半或錯位。緯度也常是 90 → −90 遞減，跟影像的列序要對齊。
3. 粒子位移若在全球場取模（wrap）後直接連線，跨越邊界那一步就是一條橫線。
4. u/v 是公尺每秒，換成經緯度位移時經度方向要除以 cos(緯度)；省略會在高緯變形，但若忘記在極區附近截斷，除以接近 0 的值也會爆。

## 解法
1. 同一份 u/v，風用 `dirFrom = (atan2(-u, -v)·180/π + 360) % 360`，流用 `dirTo = (atan2(u, v)·180/π + 360) % 360`；popup 文字寫清楚「來向」或「去向」。
2. 預處理時把 0–360 經度從 180° 切開重排成 −180–180，並檢查緯度方向。
3. 粒子：全球場 x 取模後，若單步位移超過半個世界寬就重生粒子，不畫這一段。
4. 經度位移用 `metersPerDegLon = 111320·cos(φ)`，並設下限（避免極區除以接近 0 的值）或在高緯不生成粒子。
5. 顯示時標明資料是分析場還是預報場（見 [12-10](12-10-gridded-forecast-time-axis.md)）。

## 怎麼偵測
- 通用：挑一個已知風向的測站時刻（例如東北季風日北部應為 NE 來向），比對 popup；全球場看格林威治與換日線兩側是否連續。
- 搜尋（方向公式）：`rg -n 'atan2\(' ` 在風場／海流相關檔，確認風與流使用不同符號且有註明慣例。
- 搜尋（經度範圍）：`rg -n -i 'longitude|lons?\b' ` 搭配 `rg -n '360'`，確認有 0–360 → −180–180 轉換。
- 搜尋（粒子 wrap）：`rg -n '% ?1\)|wrap|crossed' ` 在粒子 layer 檔。

## 出處
- WMO 風向定義（風的來向，以正北為 0°順時針）；海流方向慣例為去向。
- NOAA GFS（0.25° 全球網格，經度 0–359.75）。
- 實例：[風向與流向的換算](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/featureInfo/globalClimatePanels.tsx)（含經度方向的緯度修正與下限）；[0–360 經度重排](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/scripts/preprocess/extract_climate_uv.py)；[粒子全球場取模並在位移超過半個世界寬時重生](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/climateParticleLineLayer.ts)；[collector 端的經度重排與緯度翻轉](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/collectors/global_climate/climate_bake.py)。
