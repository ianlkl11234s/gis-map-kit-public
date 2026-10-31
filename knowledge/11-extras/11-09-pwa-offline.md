---
id: 11-09
title: PWA 與離線：地圖站要不要做、可安裝條件，以及離線圖磚的授權問題
topic: 11-extras
kind: decision
scope: public
evidence: Candidate
stacks: [any]
tags: [PWA, service worker, manifest, 離線, 可安裝, 圖磚快取, 授權, 弱網]
---

## 原則
先分清楚要的是「可安裝」還是「離線可用」；離線是資料策略與底圖授權問題，不是加一個 service worker 就好。原型與學生作品不做離線。

## 症狀
- 使用者在山區、地下、展場等弱網環境打不開圖台。
- 想「加到主畫面」像 App 一樣使用。
- 加了 service worker 以為能離線，結果底圖與資料都沒有。

## 原因
- 地圖站的資料量大且多半是遠端或即時資料，離線要先決定哪些資料可以帶走。
- 公用圖磚服務的使用政策常禁止大量預抓，離線快取底圖可能違反授權。

## 解法
1. 只要「可安裝」：照瀏覽器的可安裝條件做（HTTPS、manifest 含 name／short_name、192 與 512 px 圖示、start_url、display），以官方當期頁面為準。
2. 要「離線可用」：App shell（HTML／JS／CSS）用 cache-first；資料檔用 stale-while-revalidate 並顯示資料時間（[09-07](../09-design-system/09-07-loading-data-time-and-stale.md)）；即時圖層離線時標「離線，顯示舊資料」。
3. 底圖要離線前先確認授權（[02-03](../02-basemaps/02-03-osm-data-license-vs-tile-policy.md)）；自架 PMTiles 底圖（[02-09](../02-basemaps/02-09-self-hosted-pmtiles-basemap.md)）較適合離線。
4. 寫清楚 service worker 的更新策略並提示新版本，避免舊 SW 一直提供舊 bundle。
5. 原型、學生作品：不做離線，改成預先抓好的靜態檔加資料時間標示。

## 怎麼偵測
- 通用：DevTools Application → Manifest／Service Workers；Lighthouse 的 installable 檢查；斷網後重新整理。
- 搜尋：`webmanifest|serviceWorker|workbox` 零命中即未做；有做的話檢查 SW 是否快取了第三方圖磚網域（適用 stack：any）。

## 出處
- web.dev〈Installation criteria〉：https://web.dev/articles/install-criteria
- 離線圖磚的授權限制以各底圖服務的使用政策為準（待官方驗證）。
- 相關卡：[02-03](../02-basemaps/02-03-osm-data-license-vs-tile-policy.md)、[02-09](../02-basemaps/02-09-self-hosted-pmtiles-basemap.md)、[09-07](../09-design-system/09-07-loading-data-time-and-stale.md)。
