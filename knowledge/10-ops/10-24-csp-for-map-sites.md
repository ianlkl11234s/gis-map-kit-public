---
id: 10-24
title: 地圖站的 CSP：先 Report-Only 觀察，把 SDK 必要指令與所有圖磚、API 網域列進白名單，再轉 enforcing
topic: 10-ops
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [CSP, Content-Security-Policy, Report-Only, connect-src, worker-src, blob, img-src, frame-ancestors, report-to, beacon, 白名單, 圖磚網域]
---

## 原則
地圖站的 CSP 先用 `Content-Security-Policy-Report-Only` 上線收集違規，補齊 SDK 必要指令與所有圖磚、資料、API 網域後，才轉成 enforcing。不要一次直接 enforcing，會讓地圖空白。

## 症狀
- 直接上 enforcing 後地圖整張空白，console 出現 worker 或 blob 被擋的訊息。
- 圖磚、PMTiles 或 API 請求被 `connect-src` 擋掉，只有部分圖層消失。
- CDN 自動注入的統計 beacon 被擋。

## 原因
- 地圖 SDK 用 Web Worker 解析圖磚，worker 預設從 blob URL 建立，圖片也用 `blob:` 與 `data:`。
- 圖磚、API 網域分散，白名單易漏；Report-Only 不阻擋，header 存在不代表已受保護。

## 解法
1. **先上 Report-Only**。用 `report-to`（搭配 `Reporting-Endpoints` header）收違規。違規回報也是錯誤訊號，見 [10-25](10-25-frontend-error-monitoring.md)。
2. **SDK 必要指令**（以所用版本的官方文件為準）：
   - mapbox-gl：`worker-src blob:`、`img-src data: blob:`、`connect-src` 含官方 API 與事件網域；Standard 樣式或 3D 模型另需 `script-src 'wasm-unsafe-eval'`。
   - maplibre：官方要求 `worker-src` 與 `img-src data: blob:`；政策不允許 `blob:` worker 時，改用 `setWorkerUrl` 指向同源 worker 檔。
3. **白名單覆蓋所有網域**：每個圖磚、PMTiles、API、字型、外國官方圖磚網域都進對應指令（`connect-src`、`img-src`、`font-src`）。新增第三方網域的 PR 同步改白名單。圖片若是動態多來源，可只對 `img-src` 放寬 `https:`。
4. **用 `connect-src` 限制公開 token 的出口**，只能送往預期網域（見 [10-04](10-04-public-token-vs-secret.md)）。
5. **分區上線**：隱私頁等單純頁面可先用 enforcing，主站維持 Report-Only 並存。enforcing 會擋 CDN 自動注入的統計 beacon，要決定放行該網域或在隱私頁揭露（見 [11-11](../11-extras/11-11-attribution-and-privacy-disclosure.md)）。
6. **轉 enforcing 前**在真實瀏覽器開所有圖層、切底圖、開 popup，確認零違規，再把 header 名稱改成正式。

`frame-ancestors` 與嵌入設定見 [11-05](../11-extras/11-05-embed-page-security-billing-gestures.md)。

## 怎麼偵測
- 通用：Console 出現 CSP 違規訊息。
- 搜尋：只有 `Content-Security-Policy-Report-Only` 而文件寫已 enforcing（any）。
- 搜尋：用 `https?://[a-z0-9.-]+\.[a-z]{2,}` 列出程式中的圖磚與資料網域，逐一比對 `connect-src`（any）。
- 搜尋：專案用 mapbox-gl 或 maplibre，CSP 字串卻沒有 `worker-src` 或 `blob:`（mapbox-gl、maplibre）。

## 出處
- Mapbox GL JS 指南（CSP directives）：https://docs.mapbox.com/mapbox-gl-js/guides/browsers-and-testing/
- MapLibre GL JS 文件（CSP Directives）：https://maplibre.org/maplibre-gl-js/docs/
- MDN Report-Only：https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy-Report-Only
- 相關卡：[01-11](../01-taiwan-apis/01-11-cors-and-direct-calls.md)、[10-04](10-04-public-token-vs-secret.md)、[10-25](10-25-frontend-error-monitoring.md)、[11-05](../11-extras/11-05-embed-page-security-billing-gestures.md)、[11-11](../11-extras/11-11-attribution-and-privacy-disclosure.md)。
- 實例：[mini-taiwan-pulse nginx 設定](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/nginx.conf)（主站 Report-Only，隱私頁 enforcing）。
