---
id: 15-05
title: 第一張網頁地圖的最小骨架：MapLibre＋免 key 示範底圖＋一個 GeoJSON 圖層、圖例、popup
topic: 15-getting-started
kind: pattern
scope: public
evidence: General
stacks: [maplibre]
tags: [MapLibre, 最小範例, 骨架, GeoJSON, addSource, addLayer, popup, 圖例, 免 key, 入門, 範本]
---

## 原則
第一張地圖至少要有底圖、資料圖層、圖例、點擊 popup 四件事；圖例與樣式用同一組門檻與顏色，popup 用 `textContent` 顯示資料，缺值顯示「無資料」而不是 0。

## 症狀
- 第一次做網頁地圖，不知道最少要寫哪些東西，網路上的範例不是要 token 就是一大包框架。
- 地圖出來了，但點不能點、沒有圖例，別人看不懂顏色代表什麼。

## 原因
一張「看得懂」的地圖至少要四件事：底圖、資料圖層、圖例、點擊後的說明（popup）。少了圖例和 popup，畫面只是一堆色點。

## 解法
存成 `index.html`，旁邊放 `points.geojson`，用本機 server 打開（見 [15-03](15-03-local-server-file-protocol-cors.md)）。程式碼為通用範例，版本號與樣式網址以 MapLibre 官方文件為準。

```html
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <title>我的第一張地圖</title>
  <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@5/dist/maplibre-gl.css" />
  <script src="https://unpkg.com/maplibre-gl@5/dist/maplibre-gl.js"></script>
  <style>
    html, body, #map { margin: 0; height: 100%; }
    #legend { position: absolute; left: 12px; bottom: 24px; background: #fff;
              padding: 8px 10px; border-radius: 8px; font: 13px sans-serif; }
    .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
  </style>
</head>
<body>
  <div id="map"></div>
  <div id="legend">
    <div><span class="dot" style="background:#e4572e"></span>數量 ≥ 10</div>
    <div><span class="dot" style="background:#4c8bf5"></span>數量 &lt; 10</div>
  </div>
  <script>
    const map = new maplibregl.Map({
      container: 'map',
      style: 'https://demotiles.maplibre.org/style.json', // 官方示範樣式：免 key，只供練習
      center: [121.0, 23.7],  // [經度, 緯度]
      zoom: 6.5,
    });

    map.on('load', () => {
      map.addSource('pts', { type: 'geojson', data: 'points.geojson' });
      map.addLayer({
        id: 'pts-circle',
        type: 'circle',
        source: 'pts',
        paint: {
          'circle-radius': 6,
          'circle-color': ['case', ['>=', ['get', 'count'], 10], '#e4572e', '#4c8bf5'],
          'circle-stroke-color': '#fff',
          'circle-stroke-width': 1,
        },
      });

      map.on('click', 'pts-circle', (e) => {
        const p = e.features[0].properties;
        const box = document.createElement('div');
        box.textContent = `${p.name}：${p.count ?? '無資料'}`; // 用 textContent，不把資料當 HTML
        new maplibregl.Popup().setLngLat(e.lngLat).setDOMContent(box).addTo(map);
      });
      map.on('mouseenter', 'pts-circle', () => (map.getCanvas().style.cursor = 'pointer'));
      map.on('mouseleave', 'pts-circle', () => (map.getCanvas().style.cursor = ''));
    });
  </script>
</body>
</html>
```

重點：
1. **`center` 與 GeoJSON 座標都是 [經度, 緯度]**（[15-02](15-02-geojson-structure-and-bad-files.md)）。
2. **圖例的顏色與門檻和 `circle-color` 寫同一組值**；改了一邊忘了另一邊，是最常見的圖例錯誤（[05-08](../05-color/05-08-legend-key-mismatch.md)）。
3. **popup 用 `textContent`／`setDOMContent`**，不要把資料欄位直接塞進 `setHTML`，避免資料裡的 HTML 被執行。
4. **缺值顯示「無資料」**，不要顯示成 0（[05-04](../05-color/05-04-null-is-not-zero-color.md)）。
5. 示範底圖只適合練習；要正式公開時，底圖選型與授權見 [02-02](../02-basemaps/02-02-basemap-selection-decision.md)、[13-01](../13-author-taste/13-01-sdk-maplibre-default.md)，標示見 [02-07](../02-basemaps/02-07-attribution.md)。
6. 資料超過數 MB 或點數上萬，改成 PMTiles（[06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)），點太多時的畫法見 [14-02](../14-scale-density/14-02-point-count-thresholds.md)。

## 怎麼偵測
- 通用：地圖上有色點但沒有圖例；點下去沒反應；正式站還在用示範樣式。
- 搜尋：`addLayer\(` 存在但整個專案沒有 `Popup\(` 或圖例元素；`setHTML\(.*properties`（資料直接當 HTML）；`demotiles\.maplibre\.org` 出現在正式站設定（適用 stack：maplibre）。

## 出處
- MapLibre GL JS 官方文件與範例（Add a GeoJSON source、Display a popup on click）。
- 相關卡：[05-08](../05-color/05-08-legend-key-mismatch.md)（圖例一致性）、[09-02](../09-design-system/09-02-layer-ux-four-iron-rules.md)（圖層 UX 必備項目）。
