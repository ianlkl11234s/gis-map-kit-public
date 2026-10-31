---
id: 02-04
title: Mapbox 注意事項：以 Map 初始化計費、token 分兩種、v2 起非開源
topic: 02-basemaps
kind: decision
scope: public
evidence: Evaluated
stacks: [mapbox-gl]
tags: [Mapbox, map load, 計費, token, public token, secret token, URL restriction, 授權, TOS, 嵌入]
---

## 原則
只換圖磚省不到 Mapbox 的錢，必須連地圖函式庫一起換掉；流量不可控的頁面預設用 MapLibre＋自託管底圖，token 只用 public scope 並設定網域限制。

## 症狀
- 以為「換成自己的圖磚就不用付 Mapbox 費用」，帳單沒變。
- 嵌入頁、回放頁被大量載入，map load 暴增。
- token 被盜用，或把 secret token 放進前端。
- 網址搬家後底圖 403。

## 原因
- 計費單位：每次 Mapbox GL JS 的 `Map` 物件初始化算一次 map load，與圖磚來自誰無關（官方計費說明）。第三方圖磚搭配 mapbox-gl 是否計費，官方沒有書面說明，是灰色地帶。
- token：public scope token 設計上就給前端使用；secret token 不可在前端露出；URL restriction 官方稱為「best-effort mitigation」，不是強保證。
- 授權：v2 起依 Mapbox TOS，僅限搭配 Mapbox 產品、需有效帳號；v1.13 及以前為 BSD-3。

## 解法
1. 要省 map load 費用，連地圖函式庫一起換掉（改用 MapLibre）；只換圖磚不會省錢。
2. 流量不可控的頁面（嵌入、文章、被分享的回放頁）預設 MapLibre＋自託管底圖（見 [02-09](02-09-self-hosted-pmtiles-basemap.md)）。
3. token 從環境變數在 build 時注入，不寫死；只用 public token；設定 URL restriction 並於搬站時同步更新。
4. 定期查用量頁；免費額度（每月 50,000 map loads，之後每千次 $5.00）會變，以官方頁為準。
5. 隱私：Mapbox GL 會把地圖使用統計送到官方事件端點，隱私頁需揭露。

## 怎麼偵測
- 通用：嵌入頁預設 Mapbox；token 寫在原始碼；帳單曲線跟流量不成比例。
- 搜尋：`accessToken\s*=\s*['"]pk\.|sk\.`（寫死 token）；`new mapboxgl\.Map` 出現在被嵌入或多次載入的頁面（適用 stack：mapbox-gl）。

## 出處
- 官方：docs.mapbox.com/mapbox-gl-js/guides/pricing/、mapbox.com/pricing、docs.mapbox.com/accounts/guides/tokens/、github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt。
- 相關卡：[02-09](02-09-self-hosted-pmtiles-basemap.md)。
- 實例：[嵌入頁底圖評估提案（Mapbox 計費與改 MapLibre 的估算）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/archive/2026-10-04/proposal/embed-basemap-osm.md)。

