---
id: 10-25
title: 地圖站的前端錯誤監控：除了 JS 錯誤，還要接地圖 SDK 的 error 事件與 WebGL context lost，送出前去掉位置資料
topic: 10-ops
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [錯誤監控, error tracking, Sentry, GlitchTip, window.onerror, unhandledrejection, map error, webglcontextlost, source map, 取樣, 個資, breadcrumb, release]
---

## 原則
有對外使用者的地圖站才接前端錯誤監控；接的時候要同時收一般 JS 錯誤、未處理的 Promise rejection、地圖 SDK 的 error 事件與 WebGL context lost，並在送出前去掉位置資料。個人原型與課堂作品可先不接。

## 症狀
- 使用者回報「地圖空白」，開發者重現不了。
- 圖磚 404 或 CORS 失敗只出現在使用者的 console，開發者不知道。
- 手機切到背景再回來，WebGL context lost，地圖變黑。
- 問題要等人來說才知道（與 [10-07](10-07-deadman-switch-outside-monitored-system.md) 同類）。

## 原因
- 地圖 SDK 的圖磚、樣式、source 載入失敗多半不丟到 `window.onerror`，而是走 SDK 自己的 `error` 事件。
- WebGL context lost 是 canvas 事件，不是 JS 例外。
- 沒人 catch 的 Promise 失敗只觸發 `unhandledrejection`。

## 解法
1. **先決定要不要接**：個人原型、課堂作品先用 [09-07](../09-design-system/09-07-loading-data-time-and-stale.md) 的四態讓使用者看得到錯誤即可；有對外使用者再接。
2. **要接的訊號**：
   - `window` 的 `error` 與 `unhandledrejection`。
   - 地圖實例的 `error` 事件（mapbox-gl、maplibre 都有；附上出錯的 source 與 HTTP 狀態，欄位以所用版本的型別定義為準）。同一 source 的圖磚失敗會大量觸發，要去重。
   - canvas 的 `webglcontextlost` 與 `webglcontextrestored`；lost 時提示並重建。
   - 資料載入失敗與逾時：與 [09-07](../09-design-system/09-07-loading-data-time-and-stale.md) 共用同一個錯誤出口，不要各寫各的。
   - CSP 違規回報（見 [10-24](10-24-csp-for-map-sites.md)）。
3. **工具選項，不指定**：託管 SaaS（如 Sentry，免維運，但有配額與費用、資料在第三方）；可自架的方案（如 GlitchTip，資料自管，但要自己維運，與 Sentry SDK 的相容程度先自行查證）；或只把錯誤 POST 到自己的極簡端點（最便宜，但沒有去重、告警與 source map 還原）。
4. **隱私**：地圖點擊、鏡頭位置、地址查詢、URL 參數都是位置資料。在送出前的 hook 裡（Sentry 稱 `beforeSend`，可修改事件或回傳 `null` 丟棄）去掉或降精度，breadcrumb 與 URL 也要處理，並在隱私頁揭露（見 [11-11](../11-extras/11-11-attribution-and-privacy-disclosure.md)、[11-07](../11-extras/11-07-geolocation-my-location-permissions.md)）。
5. **source map 上傳到監控服務**，不要公開掛在網站上；上傳後從部署產物刪除 `.map` 檔。官方建議把上傳放進建置流程。
6. **標 release 版號、設取樣率與每日上限**，避免帳單或配額被單一故障灌爆；告警降噪與去重規則見 [10-08](10-08-alert-dedup-recovery-and-root-cause.md)。

## 怎麼偵測
- 搜尋：`\.on\(\s*['"]error['"]` 在地圖實例上零命中（mapbox-gl、maplibre）。
- 搜尋：`webglcontextlost` 零命中（mapbox-gl、maplibre、three.js、deck.gl）。
- 搜尋：`unhandledrejection` 零命中（any）。
- 通用：部署產物（例如 `dist/`）含 `.map` 檔且可從網址直接下載。
- 通用：監控事件的 URL 或 breadcrumb 含經緯度、地址。

## 出處
- Sentry 文件〈Filtering events（beforeSend）〉：https://docs.sentry.io/platforms/javascript/configuration/filtering/
- Sentry 文件〈Source Maps〉：https://docs.sentry.io/platforms/javascript/sourcemaps/
- MapLibre GL JS〈Map〉事件表（error、webglcontextlost、webglcontextrestored）：https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/
- Mapbox GL JS Map：https://docs.mapbox.com/mapbox-gl-js/api/map/
- GlitchTip 文件：https://glitchtip.com/documentation
- 相關卡：[09-07](../09-design-system/09-07-loading-data-time-and-stale.md)、[10-06](10-06-heartbeat-is-not-health.md)、[10-07](10-07-deadman-switch-outside-monitored-system.md)、[10-08](10-08-alert-dedup-recovery-and-root-cause.md)、[10-24](10-24-csp-for-map-sites.md)、[11-07](../11-extras/11-07-geolocation-my-location-permissions.md)、[11-11](../11-extras/11-11-attribution-and-privacy-disclosure.md)。
