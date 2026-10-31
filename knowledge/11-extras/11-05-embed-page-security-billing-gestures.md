---
id: 11-05
title: 嵌入頁的安全與計費：frame-ancestors 只開給嵌入入口、圖層白名單、嵌入版不依賴即時 API
topic: 11-extras
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [嵌入, iframe, frame-ancestors, CSP, X-Frame-Options, 計費, 白名單, clickjacking]
---

## 原則
嵌入入口與有登入的主站分開：只有嵌入路徑開放 `frame-ancestors`，嵌入版只載入不產生後端流量的圖層。嵌入頁的手勢與時鐘見 [11-14](11-14-embed-clock-frozen-time-cooperative-gestures.md)。

## 症狀
- 文章裡的 `<iframe>` 被瀏覽器擋下（X-Frame-Options）。
- 嵌入後帳單隨別人的頁面流量增加（地圖 SDK 依載入次數計費）。
- 有登入的主站被開放 `frame-ancestors *`，有被 clickjacking 的風險。
- 動態圖層的資料庫流量被別人的頁面流量放大。
- 嵌入入口被快取，部署後拿到舊 HTML、指向已換雜湊的資產。

## 原因
以為放一個 `<iframe src=主站>` 就完成，沒有區分「對外可嵌入的入口」與「有登入的主站」。

## 解法
1. 入口分離：專用嵌入路徑（例如 `/embed`）設 `frame-ancestors *`；有登入、站主後台、使用者自填金鑰的主站設 `frame-ancestors 'self'` 加 `X-Frame-Options: SAMEORIGIN`；卡片與文章頁若不該被嵌入，設 `'none'`。
2. `X-Frame-Options` 不支援白名單語法，要白名單用 CSP `frame-ancestors`；它放在 Report-Only 下不生效，必須另立一條 enforcing CSP。
3. 嵌入版只允許不會產生後端流量的圖層：白名單只收純靜態資料，排除私有／站主限定圖層；動態圖層逐案評估 egress 後加例外。
4. 計費：若 SDK 依「地圖初始化次數」計費，嵌入版改用開源程式庫加自管或開放底圖（需核實該廠商當期計費規則）；上線後實測計費量與後端請求量確實為 0。
5. 嵌入入口加 `Cache-Control: no-cache`。
6. 版權標示不可被嵌入參數移除（[11-11](11-11-attribution-and-privacy-disclosure.md)）。

## 怎麼偵測
- 通用：用另一個網域的測試頁 iframe 嵌入主站與嵌入頁，確認前者被擋、後者可載入。
- 搜尋：`frame-ancestors \*` 出現在非嵌入路徑；`Content-Security-Policy-Report-Only` 內含 `frame-ancestors`；嵌入白名單裡含 owner-only 或動態圖層（any）。

## 出處
- MDN `Content-Security-Policy: frame-ancestors`。
- 相關卡：[10-24](../10-ops/10-24-csp-for-map-sites.md)、[11-11](11-11-attribution-and-privacy-disclosure.md)、[11-13](11-13-scrollytelling-story-and-number-ledger.md)、[11-14](11-14-embed-clock-frozen-time-cooperative-gestures.md)。
- 實例（mini-taiwan-pulse）：[嵌入版決策紀錄（計費與出處）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/embeddable-map/changelog.md)、[圖層白名單](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/embed/embedWhitelist.ts)、[主站改 'self'](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/62cb222bd6a32f627459efa50cf3b64e079730f1)、[入口 no-cache](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/b2fb1d232f9d9fad344b6cb43c1a4fc54311f5d5)。
