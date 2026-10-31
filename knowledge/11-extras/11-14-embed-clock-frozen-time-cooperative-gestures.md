---
id: 11-14
title: 嵌入頁的互動：自帶回放時鐘、凍結時間、cooperativeGestures 不攔截頁面捲動
topic: 11-extras
kind: pattern
scope: public
evidence: Observed
stacks: [mapbox-gl, maplibre]
tags: [嵌入, iframe, cooperativeGestures, replayClock, 凍結時間, 快照, 手勢, requestAnimationFrame]
---

## 原則
嵌入頁的時間要凍結、時鐘自己持有，被嵌入的地圖要開協作手勢，不攔截頁面捲動。嵌入入口的安全與計費見 [11-05](11-05-embed-page-security-billing-gestures.md)。

## 症狀
- 手機讀者捲不過文章裡的地圖，單指被地圖吃掉。
- 嵌入的回放圖層打即時 API，內容每次打開不同，流量也隨頁面瀏覽放大。
- 分頁切走再切回，第一幀的時間暴衝；暫停時動畫仍在跑。

## 原因
嵌入頁沒有主站的全域時間迴圈，也沒有主站「不在 iframe 內」的假設；地圖預設吃掉所有單指手勢。

## 解法
1. 凍結時間：嵌入的回放圖層要帶日期參數，且該日有凍結快照；不要讓嵌入版直接打即時 API。
2. 回放時鐘自帶：時鐘自持 RAF（暫停時取消）、通知節流約 10 Hz、單幀 dt 設上限（避免切回分頁的第一幀暴衝）；多層共用同一個時鐘（singleton）。時間模型見 [03-01](../03-dynamics/03-01-time-model-global-vs-scoped-clock.md)。
3. cooperativeGestures：被嵌入或與長頁面共存的地圖開啟（單指捲頁、雙指移圖；桌機需按 Ctrl／Cmd 才縮放），只在偵測位於 iframe 內時開，並補多語提示文字；全螢幕地圖不開。MapLibre 有此選項（官方 MapOptions）；Mapbox GL JS 同名選項請查當期文件。

## 怎麼偵測
- 通用：用手機在長頁面中捲過嵌入地圖；切走分頁再切回，看時間是否跳動。
- 搜尋：`new (maplibregl|mapboxgl)\.Map\(` 的嵌入頁缺 `cooperativeGestures`（適用 stack：maplibre、mapbox-gl）。

## 出處
- MapLibre GL JS MapOptions `cooperativeGestures`：https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapOptions/ 。
- 相關卡：[03-01](../03-dynamics/03-01-time-model-global-vs-scoped-clock.md)、[11-05](11-05-embed-page-security-billing-gestures.md)、[11-13](11-13-scrollytelling-story-and-number-ledger.md)。
- 實例（mini-taiwan-pulse）：[自帶回放時鐘](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/embed/replayClock.ts)、[framed 時開協作手勢](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/embed/EmbedApp.tsx)。
