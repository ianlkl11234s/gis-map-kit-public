# 11-extras 發布與分享（SEO、嵌入、截圖、PWA、無障礙…）

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [11-00](11-00-extras-index.md) | 發布與分享總表：被找到、分享嵌入、截圖、定位、PWA、無障礙、隱私、多語、敘事 | 站上線後，依「要讓誰用到什麼」選卡：被找到看 SEO 與宣傳組，被轉貼與嵌入看分享組，其餘按功能對應。 | catalog | Observed | any | 總表, 發布, SEO, llms.txt, 分享, 嵌入, 截圖, 定位, PWA, 無障礙, 隱私, 多語系, 敘事頁 |
| [11-01](11-01-spa-empty-html-seo-prerender.md) | 地圖站原始 HTML 是空的：搜尋引擎看不到內容，要靜態說明、meta、結構化資料與一篇一個網址 | Google `site:` 查自己的網站零結果，品牌詞也搜不到。 | pitfall | Observed | any | SEO, SPA, prerender, 預渲染, JSON-LD, meta description, noscript, 靜態產生, sitemap, 搜尋引擎 |
| [11-02](11-02-robots-sitemap-soft404-canonical.md) | robots.txt、sitemap 與 soft-404：SPA fallback 會讓這些檔都回 200 的首頁；多語版 canonical 不能寫死 | `/robots.txt`、`/sitemap.xml`、`/nonexistent` 全都回 200 的首頁 HTML… | pitfall | Observed | any | robots.txt, sitemap, soft 404, canonical, hreflang, RFC 9309, SPA fallback, 多語, Search Console |
| [11-03](11-03-llms-txt-and-ai-crawler-policy.md) | llms.txt 與 AEO 是提案不是標準；robots.txt 說允許 AI 爬蟲，CDN 邊緣層可能照樣回 403 | 站上放了 `llms.txt`，卻沒有任何證據有 AI 服務讀它或因此更常引用你。 | pitfall | Observed | any | llms.txt, AEO, GEO, AI 爬蟲, GPTBot, ClaudeBot, robots.txt, Cloudflare, bot 管理, 403 |
| [11-04](11-04-share-camera-og-image-saved-scene.md) | 分享與收藏補充：網址要帶鏡頭與時間、預覽圖（og:image）要自己做、持久化的場景要有版本號 | 貼到社群或通訊軟體只有文字卡，沒有預覽圖。 | pattern | Implemented | any | 分享網址, 鏡頭, og:image, twitter:card, 預覽圖, 收藏場景, localStorage, 版本號, 時間參數 |
| [11-05](11-05-embed-page-security-billing-gestures.md) | 嵌入頁的安全與計費：frame-ancestors 只開給嵌入入口、圖層白名單、嵌入版不依賴即時 API | 文章裡的 `<iframe>` 被瀏覽器擋下（X-Frame-Options）。 | pattern | Observed | any | 嵌入, iframe, frame-ancestors, CSP, X-Frame-Options, 計費, 白名單, clickjacking |
| [11-06](11-06-canvas-capture-export-print.md) | 截圖、匯出與列印：WebGL 畫布不是隨時讀得到（黑畫面），不要為了截圖整站開 preserveDrawingBuffer | `canvas.toDataURL()` 或錄影拿到全黑畫面。 | pitfall | Implemented | mapbox-gl, maplibre, three.js | 截圖, preserveDrawingBuffer, toDataURL, 黑畫面, Capture mode, 匯出, CSV, GeoJSON, 列印, 錄影, 逐格, 轉場, 防暈, wipe, 宣傳影片 |
| [11-07](11-07-geolocation-my-location-permissions.md) | 「我的位置」：只在 HTTPS、需使用者同意、被拒要有退路；別被自己的 Permissions-Policy 擋掉 | 加了「定位」按鈕，在區網 HTTP 測試的手機上完全沒反應。 | pattern | Candidate | mapbox-gl, maplibre | GPS, geolocation, GeolocateControl, Permissions-Policy, iframe, 定位, 隱私, secure context |
| [11-08](11-08-measure-draw-and-compare-maps.md) | 量距離面積與雙圖比較：做法選項與手機替代 | 使用者想量兩點距離、框一塊範圍算面積，圖台沒有工具，只能另開別的軟體。 | decision | Candidate | mapbox-gl, maplibre | 量測, 距離, 面積, 繪製, 框選, 雙圖比較, swipe, 捲簾, 前後比較, 手勢衝突 |
| [11-09](11-09-pwa-offline.md) | PWA 與離線：地圖站要不要做、可安裝條件，以及離線圖磚的授權問題 | 使用者在山區、地下、展場等弱網環境打不開圖台。 | decision | Candidate | any | PWA, service worker, manifest, 離線, 可安裝, 圖磚快取, 授權, 弱網 |
| [11-10](11-10-accessibility-keyboard-ime.md) | 圖台無障礙最低清單：時間軸鍵盤操作、aria-live 通知、中文輸入法 Enter 不誤送出 | 中文使用者在注音／拼音選字階段按 Enter，訊息被直接送出。 | pattern | Implemented | any | 無障礙, a11y, 鍵盤, IME, isComposing, aria-live, slider, 焦點, reduced-motion, Safari |
| [11-11](11-11-attribution-and-privacy-disclosure.md) | 出處標示不可被嵌入參數拿掉；隱私說明要和瀏覽器實際請求的第三方一致 | 嵌入版或拍攝模式把出處標示一起隱藏，違反底圖或開放資料的 attribution 要求。 | pitfall | Observed | any | attribution, 版權, 授權, 隱私, CDN beacon, Web Analytics, OAuth 品牌驗證, 隱私權政策, 嵌入 |
| [11-12](11-12-i18n-display-layer-lookup-and-fallback.md) | 地圖站多語系：只在顯示層查表、查不到退回原文，地名用官方英譯，外文長字要先決定截斷或換行 | 圖層 key、URL 參數或給 AI 讀的字串被一起翻掉，分享連結和搜尋壞掉。 | pattern | Implemented | any | i18n, 多語系, 翻譯, t(), fallback, 退回原文, 顯示層, 識別字, 地名英譯, 羅馬拼音, 外文欄位, 機器翻譯, setLanguage, 底圖地名, 長字, ellipsis, 防倒退 |
| [11-13](11-13-scrollytelling-story-and-number-ledger.md) | 敘事頁與 scrollytelling：地圖嵌入而不重畫，正文每個數字都要在 data.json 台帳有出處 | 想把地圖站上的發現寫成有互動地圖的長文，結果每篇文章都自己重寫一份地圖程式。 | pattern | Implemented | any | scrollytelling, story mode, 敘事, 資料新聞, IntersectionObserver, 嵌入地圖, iframe, 靜態圖 fallback, data.json, 數字台帳, 可追溯, 查詢, 口徑 |
| [11-14](11-14-embed-clock-frozen-time-cooperative-gestures.md) | 嵌入頁的互動：自帶回放時鐘、凍結時間、cooperativeGestures 不攔截頁面捲動 | 手機讀者捲不過文章裡的地圖，單指被地圖吃掉。 | pattern | Observed | mapbox-gl, maplibre | 嵌入, iframe, cooperativeGestures, replayClock, 凍結時間, 快照, 手勢, requestAnimationFrame |
| [11-15](11-15-promote-your-map-video-and-before-after.md) | 讓人知道你的地圖：除了搜尋引擎，還要有能轉貼的影片與前後對比動畫，素材一律用真實畫面 | 網站做好了但沒人知道；社群貼文只有連結，或一張靜態截圖。 | pattern | Observed | any | 宣傳, 推廣, 社群, 影片, 回顧影片, 前後對比, motion, GIF, 截圖, SEO, 分享預覽, 防暈, 真實畫面 |
