---
id: 14-03
title: 隨縮放換畫法的交界坑：熱區提早消失、透明圖層仍攔截點擊、切換點來回閃
topic: 14-scale-density
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [minzoom, maxzoom, 縮放切換, 熱區, 格網, H3, 解析度, 遲滯, hysteresis, 標籤密度, queryRenderedFeatures, 尺度接力]
---

## 原則
隨縮放換畫法時，在交界處兩側各驗收一次：熱區 maxzoom 取出點縮放 +0.01，用 maxzoom 精確停用上一段（不只靠透明度），距離門檻用進出兩個值，標籤獨立設 minzoom。

## 症狀
- 熱區設 `maxzoom: 12`、點設 `minzoom: 12`，結果在 z11.5–12 之間兩者都不見，畫面空白一段。
- 粗格網用透明度淡出，但拉近後點不到下面的點：點擊被已經看不見的格網吃掉。
- 依相機距離切換「光點／模型」，鏡頭停在門檻附近時每幀來回閃。
- 拉近後標籤一次全冒出來，互相疊。

## 原因
- Mapbox GL／MapLibre 在 z ≥ x.5 就改載下一級圖磚；圖磚 zoom ≥ 圖層 `maxzoom` 時不為該圖層建資料，所以熱區在名義 maxzoom 前半級就消失。
- `fill-opacity` 為 0 不等於圖層不存在，`queryRenderedFeatures` 仍會命中。
- 單一門檻在邊界上沒有緩衝。
- 標籤沒有獨立的 minzoom 與防重疊。

## 解法
1. **熱區 maxzoom＝出點縮放 +0.01**，讓同一級圖磚仍建熱區資料；點的 minzoom 維持整數。
2. **尺度接力**（粗格網 → 細格網 → 點）時，每段同時做兩件事：用 `maxzoom` 精確停用上一段（maxzoom 是 exclusive，到該縮放就不畫），並在交界前把 opacity 插值到 0 避免硬切。例：1.5 km 格網 z4–10、細格網 z10–12、點 z12 起。
3. **網格解析度隨 zoom 換**：H3 z < 9.5 用 res7、以上 res8；更細的解析度如果檔案太大就不產，寧可拉近換回點。
4. **依距離切換的 LOD 用遲滯**：進入與退出用兩個門檻（例：距離 < 7 換模型、> 10 才換回光點）。
5. **標籤分開管**：POI 名稱 minzoom 約 13、不允許重疊；計數徽章可以早出現、可重疊；分析結果只標前 N 名。
6. **行政界分層出現**：縣市界全尺度、鄉鎮界約 z6 起、村里界約 z8 起才切片。
7. **線寬隨 zoom 插值**（兩個縮放點線性），點的尺寸預設固定三階，隨縮放的特例見 [14-02](14-02-point-count-thresholds.md) 與 [09-10](../09-design-system/09-10-map-symbol-size-tiers.md)。
8. 每個切換點都要在交界兩側各截一張圖驗收，不是只看單一縮放。

## 怎麼偵測
- 通用：慢慢從 z9 拉到 z13，看有沒有空白段、閃爍、點不到東西。
- 搜尋：`type: ['"]heatmap['"]` 的 `maxzoom` 是整數且等於同 source circle 的 `minzoom`；`fill-opacity` 用 zoom 插值到 0 卻沒有對應的 `maxzoom`；距離或 zoom 門檻只有一個常數（如 `if (dist < LOD)` 而沒有 enter／exit 兩值）（適用 stack：mapbox-gl、maplibre、three.js）。
- `symbol` 圖層沒有 `minzoom` 且 `text-allow-overlap: true`。

## 出處
- 官方：MapLibre／Mapbox GL style spec 對 layer `minzoom`／`maxzoom` 的定義（maxzoom 為 exclusive）。
- 實例：[mini-taiwan-pulse 熱區 maxzoom 與標籤 minzoom 的處理](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/mapStyleScale.ts)。
- 實例：[格網尺度接力與 maxzoom 停用](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/overlayRegistry.ts)。
- 實例：[H3 解析度隨縮放切換](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/h3LayerFactory.ts)。

