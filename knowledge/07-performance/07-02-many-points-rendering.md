---
id: 07-02
title: 大量點的渲染：縮放分階的點徑與描邊、PMTiles、cluster／heatmap、GPU instancing 怎麼選
topic: 07-performance
kind: decision
scope: public
evidence: Evaluated
stacks: [mapbox-gl, maplibre, leaflet, deck.gl, three.js]
tags: [大量點, cluster, heatmap, circle, instancing, 描邊, 低 zoom, 發熱, 點徑, symbol]
---

## 原則
點數多時，低縮放縮小點徑並取消描邊，依需求改用 heatmap、cluster 或 GPU instancing；不要用「固定大小加描邊的圓」或「每點一個 3D 物件」硬撐。

## 症狀
- 打開一個幾十萬點的圖層後，筆電風扇狂轉、拖曳卡頓。
- 全國視角下點全糊成一團，卻一樣吃效能。
- 把全部點都換成 3D 物件後掉到個位數 FPS。

## 原因
- 填充量（overdraw）：全國視角幾十萬個「固定 4–5 px 加描邊」的圓，填充面積可達畫面像素的 20 倍以上。
- 低 zoom 的圖磚同時帶太多點（見 [06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)）。
- 每個物件一個 draw call 或一個 DOM 元素，物件數一多就是瓶頸。

## 解法
依全圖點數決定低縮放畫法、出點縮放與預設透明度的門檻見 [14-02](../14-scale-density/14-02-point-count-thresholds.md)。依資料量與互動需求選型：

| 情境 | 做法 |
|---|---|
| 點少 | 原生 circle／symbol layer 即可（數量門檻見 [14-02](../14-scale-density/14-02-point-count-thresholds.md)） |
| 點多、只需看分布 | **低 zoom 縮小點徑、取消描邊**，隨 zoom 漸進放大；或 heatmap／density |
| 點多、要看個別點 | 向量圖磚（PMTiles／MVT）＋ cluster（聚合點）或依 zoom 分階顯示 |
| 數萬到數十萬、要動畫或 3D | GPU instancing（單一 draw call），位置寫入 typed array（見 [07-04](07-04-update-granularity-setdata-vs-buffer.md)） |
| 要精確保留每一點（不可抽稀） | 不抽稀；改減 buffer、降低點徑與描邊（見 [06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)） |

細節：
1. 點徑與描邊用 zoom 內插運算式，低 zoom 小點無描邊，高 zoom 回到正常。
2. 3D 立體只在需要時開（預設平面）；大量點不要用有幾何的 mesh 當點。
3. heatmap 的低值站大量疊加會看起來像極端值，weight 要壓低值。
4. 先不要預設抽稀（可能違反資料契約），也不要改成「圖磚只帶 id、點擊再查」（會改變 popup 的資料來源）；要採用前先確認。

## 怎麼偵測
- 通用：全縮放圖層開啟後 Performance 面板每幀 GPU 時間高；低 zoom 全是重疊的圓。
- 搜尋：`circle-radius['"]?:\s*\d+(\.\d+)?\s*[,}]`（固定半徑，沒有 `interpolate.*zoom`）搭配 `circle-stroke-width` 大於 0（適用 stack：mapbox-gl、maplibre）。

## 出處
- Mapbox GL／MapLibre 的 circle、heatmap、cluster 文件。
- 相關卡：[06-02](../06-data-formats/06-02-geojson-to-pmtiles-tippecanoe.md)、[07-04](07-04-update-granularity-setdata-vs-buffer.md)、[14-02](../14-scale-density/14-02-point-count-thresholds.md)。
- 實例：[mini-taiwan-pulse 效能稽核（數十萬個 4.5 px 加描邊的圓）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/audit/perf-audit-2026-09-30.md)、[分階點徑設定](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/pointSpec.ts)（低 zoom 無描邊，單幀耗時約少 45%）。
