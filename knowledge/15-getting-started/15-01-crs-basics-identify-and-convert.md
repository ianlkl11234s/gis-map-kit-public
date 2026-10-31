---
id: 15-01
title: 座標系統入門：先認出資料是 WGS84 還是 TWD97，網頁地圖一律用經緯度，轉換在預處理做
topic: 15-getting-started
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [座標系統, 投影, CRS, WGS84, EPSG:4326, TWD97, EPSG:3826, Web Mercator, EPSG:3857, ogr2ogr, proj4, 面積失真, 入門]
---

## 原則
拿到資料先認出座標系；網頁地圖只收 WGS84 經緯度（EPSG:4326），轉換在預處理做，不在瀏覽器逐點轉；量距離與面積用投影座標或測地函式，不用畫面座標。

## 症狀
- 第一次拿到政府資料，不知道 X、Y 欄位是經緯度還是公尺，放上地圖什麼都看不到。
- 看到 EPSG:4326、3826、3857 三個代碼，不知道差在哪、要用哪個。
- 在網頁地圖上量出來的面積，高緯度國家大得離譜。

## 原因
座標系統（CRS）決定「一組數字代表地球上哪一點」。網頁地圖函式庫（MapLibre、Mapbox、Leaflet）吃的是經緯度，畫面上再自己投影成 Web Mercator；資料若是其他座標系，必須先轉。

| 代碼 | 名稱 | 數值長相（以台灣為例） | 用途 |
|---|---|---|---|
| EPSG:4326 | WGS84 經緯度 | 本島經度約 120–122、緯度約 21.9–25.3（小數）；金門約 118.3 | GeoJSON、網頁地圖的輸入 |
| EPSG:3826 | TWD97 / TM2（121 分帶） | 本島 X 約 15 萬–35 萬、Y 約 240 萬–280 萬（公尺） | 台灣政府資料、量距離與面積 |
| EPSG:3825 | TWD97 / TM2（119 分帶） | 公尺值，X 範圍與 3826 不同 | 澎湖、金門、馬祖的部分政府資料；用錯分帶會整批偏移 |
| EPSG:3857 | Web Mercator | X、Y 都是數百萬到上千萬的公尺值 | 圖磚與畫面投影，一般不用自己存資料 |

Web Mercator 為了讓方向不變形，越往高緯度放得越大：格陵蘭看起來和非洲差不多大，實際約只有非洲的 1/14。所以**不要在畫面座標上量面積或距離**。

## 解法
1. **先認座標系**：看副檔名旁的 `.prj`、metadata，或直接看數值。小數且落在台灣範圍（經度 118–122、緯度 21–27） → 經緯度；數十萬以上 → 公尺（多半是 TWD97）。值落在別的國家，通常是經緯度兩欄互換。
2. **前端只收 EPSG:4326**。轉換在預處理做，不要在瀏覽器裡逐點轉大量資料。
3. 轉換工具：
   - 命令列：`ogr2ogr -s_srs EPSG:3826 -t_srs EPSG:4326 out.geojson in.shp`（GDAL；來源有 `.prj` 時可省略 `-s_srs`）。
   - Python：`geopandas` 的 `to_crs(4326)`。
   - 只有少量點要在前端轉：`proj4js`，3826 的定義字串從 epsg.io 複製。
4. **量距離與面積**：用投影座標（台灣用 3826）或測地函式（turf 的 `distance`、`area`，見 [11-08](../11-extras/11-08-measure-draw-and-compare-maps.md)），不要用 Web Mercator 平面。
5. 欄名寫錯、離島偏移、單位錯等踩坑細節見 [01-12](../01-taiwan-apis/01-12-coordinates-crs-and-column-names.md)。

## 怎麼偵測
- 通用：圖層開了卻看不到點；點出現在非洲外海（0,0 附近）或別的國家；面積統計和官方差很多。
- 搜尋：`EPSG:3826|twd97|TWD97` 出現在前端程式卻沒有對應的轉換；`turf\.area` 以外用像素或 `project\(` 結果算面積（適用 stack：any）。
- 靜態檢查：讀第一筆座標，`Math.abs(x) > 1000` 就是公尺座標。

## 出處
- EPSG.io：EPSG:4326、EPSG:3826、EPSG:3857 定義。
- GDAL ogr2ogr 文件；proj4js 文件。
- 相關卡：[01-12](../01-taiwan-apis/01-12-coordinates-crs-and-column-names.md)（座標踩坑：欄名、互換、單位、編碼）、[11-08](../11-extras/11-08-measure-draw-and-compare-maps.md)（量測工具）、[15-04](15-04-toolchain-when-to-use.md)（入門工具總覽）。

