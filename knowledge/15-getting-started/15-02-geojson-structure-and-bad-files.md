---
id: 15-02
title: GeoJSON 結構：FeatureCollection、geometry、properties，座標順序一律 [經度, 緯度]
topic: 15-getting-started
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [GeoJSON, FeatureCollection, Feature, geometry, properties, lng lat, 座標順序, RFC 7946, 壞檔, 驗證, 入門]
---

## 原則
GeoJSON 一律用 FeatureCollection、座標寫數值且順序為 [經度, 緯度]、座標系為 WGS84；數字屬性存成數字，缺值用 null。

## 症狀
- 自己手寫或從 CSV 轉出來的 GeoJSON，丟進地圖後點跑到南極或印度洋。
- 地圖報錯「Input data is not a valid GeoJSON object」，或靜默什麼都不畫。
- popup 想顯示欄位，卻拿不到值；數字欄位排序結果怪怪的。

## 原因
GeoJSON（RFC 7946）有固定結構，最常錯在三件事：座標順序、外層結構、properties 型別。

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": { "type": "Point", "coordinates": [121.5170, 25.0478] },
      "properties": { "name": "臺北車站", "count": 12 }
    }
  ]
}
```

- `coordinates` 是 **[經度, 緯度]**（lng, lat），和 Google Maps 網址、多數人口語的「緯度, 經度」相反。台灣的點，第一個數字應該在 118–122 之間。
- 幾何類型：`Point`、`LineString`、`Polygon`（外環＋洞，每個環頭尾座標相同）、以及 `Multi*` 版本。
- `properties` 放屬性；地圖的樣式運算式與 popup 都從這裡取值。

## 解法
1. **外層用 FeatureCollection**，每筆是 Feature；不要只給 geometry 陣列或自訂外殼（例如 `{ "data": [...] }`）。
2. **座標寫數值、順序 [lng, lat]**。從 CSV 轉時明確指定欄位：`[Number(row.lon), Number(row.lat)]`。
3. **properties 的數字存成數字**，不要存成字串（`"12"` 排序與分級會出錯）；缺值用 `null`，不要用 0 或空字串（缺值畫法見 [05-04](../05-color/05-04-null-is-not-zero-color.md)）。
4. **座標系一律 WGS84**（RFC 7946 不收其他 CRS；舊檔的 `crs` 欄位多半會被忽略），轉換見 [15-01](15-01-crs-basics-identify-and-convert.md)。
5. **精度**：小數 5–6 位（約 1 公尺到 0.1 公尺）就夠，多的只是讓檔案變大（見 [06-05](../06-data-formats/06-05-shrink-geometry-precision-simplify-columns.md)）。
6. 常見壞檔與檢查：
   - 經緯度互換 → 點跑到別的國家；算 bbox 檢查（[01-12](../01-taiwan-apis/01-12-coordinates-crs-and-column-names.md)）。
   - Polygon 沒閉合、自相交 → 填色破洞或不畫；用 QGIS 的「檢查有效性」或 `ST_IsValid`、turf `booleanValid` 檢查。
   - 檔案太大（數十 MB）→ 首屏卡住；改向量圖磚（[06-01](../06-data-formats/06-01-format-selection-decision.md)、[06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)）。
   - 編碼與 BOM：用 UTF-8 存檔。
7. 寫好先丟到 geojson.io 或 QGIS 看一眼，再接進程式。

## 怎麼偵測
- 通用：載入後印出 `features.length` 與第一筆 `coordinates`；第一個數字不在當地經度範圍就是順序錯。
- 搜尋：`coordinates:\s*\[\s*(lat|row\.lat|.*latitude)`、`\[\s*lat\s*,\s*lng\s*\]`（適用 stack：any）；Leaflet 的 `L.marker([lat, lng])` 是緯度在前，和 GeoJSON 相反，混用時特別注意（適用 stack：leaflet）。
- `properties` 內數字欄位的值帶引號（`"count":\s*"\d`）。

## 出處
- RFC 7946 The GeoJSON Format（§3.1.1 座標順序、§4 CRS）。
- geojson.io（線上檢視與編輯）。
- 相關卡：[01-12](../01-taiwan-apis/01-12-coordinates-crs-and-column-names.md)（座標踩坑）、[06-05](../06-data-formats/06-05-shrink-geometry-precision-simplify-columns.md)（檔案縮小）、[06-01](../06-data-formats/06-01-format-selection-decision.md)（格式選擇）。

