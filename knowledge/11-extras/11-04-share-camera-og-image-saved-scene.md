---
id: 11-04
title: 分享與收藏補充：網址要帶鏡頭與時間、預覽圖（og:image）要自己做、持久化的場景要有版本號
topic: 11-extras
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [分享網址, 鏡頭, og:image, twitter:card, 預覽圖, 收藏場景, localStorage, 版本號, 時間參數]
---

## 原則
分享網址要能還原鏡頭與時間，預覽圖自己準備，持久化的場景一律帶版本號且讀壞資料時退回預設。網址序列化的總原則見 [08-08](../08-multi-layer/08-08-shareable-layer-state-url.md)。

## 症狀
- 貼到社群或通訊軟體只有文字卡，沒有預覽圖。
- 分享連結打開後鏡頭是預設位置；`lng/lat/z` 沒生效。
- 還原收藏的場景後圖層參數或時間不對；舊收藏在改版後解析失敗。

## 原因
地圖是 canvas，沒有現成的代表圖；只存經緯度與 zoom 不足以還原畫面；持久化格式沒有版本。

## 解法
1. 鏡頭：經度、緯度、zoom 缺一就整組不用；有些實作要搭配版本參數才生效，驗收時用完整網址實測。動態作品多存一個時間參數 `t=`，讓特定時刻可分享與比較。
2. og:image：準備一張約 1200×630 的代表圖（截圖或 Capture 模式），絕對 URL 且回 200；`twitter:card` 用 `summary_large_image`。動態站選最有代表性的一個時刻。
3. 私人收藏：存的不只鏡頭，還有 pitch、bearing、底圖、圖層與各圖層參數、時間模式，並帶 `version`；使用者標記的地點另存幾何與精度來源。讀到不認得的版本或壞資料時不得 throw，退回預設。公開分享用網址，私人收藏存帳號或本機，兩者的 schema 都要版本化。
4. 原型版：`moveend` 時 `history.replaceState` 寫 `?lng&lat&z&t=`，載入時讀回；localStorage 存 `{v:1, center, zoom, layers, t}`。

## 怎麼偵測
- 通用：複製網址→開新分頁，鏡頭／圖層／時間是否一致；把網址貼到社群看預覽。
- 搜尋：`<meta property="og:image"` 缺漏或是相對路徑；`localStorage.setItem` 的 JSON 沒有 `version|v` 欄位；`JSON.parse` 讀取沒有 try/catch（適用 stack：any）。

## 出處
- Open Graph protocol；各社群平台的卡片文件（用前查）。
- 相關卡：[08-08](../08-multi-layer/08-08-shareable-layer-state-url.md)、[11-06](11-06-canvas-capture-export-print.md)（截圖）、[11-13](11-13-scrollytelling-story-and-number-ledger.md)（文章嵌入用的固定鏡頭與靜態圖替代）。
- 實例：[mini-taiwan-pulse 網址狀態序列化](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/lib/urlState.ts)、[收藏場景 schema](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/lib/memberSchema.ts)。

