---
id: 11-07
title: 「我的位置」：只在 HTTPS、需使用者同意、被拒要有退路；別被自己的 Permissions-Policy 擋掉
topic: 11-extras
kind: pattern
scope: public
evidence: Candidate
stacks: [mapbox-gl, maplibre]
tags: [GPS, geolocation, GeolocateControl, Permissions-Policy, iframe, 定位, 隱私, secure context]
---

## 原則
定位只在 HTTPS 下提供，逐一處理授權、拒絕、逾時三條路徑，被拒時退回輸入地址或選縣市；部署標頭與 iframe 的 `allow` 要與定位功能一致。

## 症狀
- 加了「定位」按鈕，在區網 HTTP 測試的手機上完全沒反應。
- 之後新增定位功能，卻被部署設定裡的標頭靜默擋掉，找不到原因。
- 嵌在 iframe 的地圖定位無效。
- 使用者拒絕權限後，介面沒有任何替代路徑。

## 原因
Geolocation API 只在 secure context（HTTPS）可用、每次需使用者同意；`Permissions-Policy: geolocation=()` 會停用；第三方 iframe 預設沒有定位權限，父頁面需 `allow="geolocation"`。

## 解法
本卡為候選設計，未經實作驗證。
1. 用地圖庫內建的定位控制項（如 `GeolocateControl`），設定精度與逾時（預設 enableHighAccuracy:false、timeout:6000，以官方當期文件為準）；可選追蹤使用者位置與精度圈。
2. 錯誤碼分流：1 PERMISSION_DENIED、2 POSITION_UNAVAILABLE、3 TIMEOUT。被拒時退回「輸入地址或選縣市」。
3. 測試手機時用 HTTPS（隧道或本機憑證），不要用區網 HTTP。
4. 部署時決定立場：不需要定位就明寫 `Permissions-Policy: geolocation=()`；之後加功能要先檢查此標頭與 iframe `allow`。
5. 地址轉座標（geocoding）是另一件事：先離線或自家索引，再線上；把使用者輸入的地址送第三方前要取得明確同意，結果保留來源與精度欄位。
6. 定位資料不要上傳或記錄，除非有明確目的與揭露（[11-11](11-11-attribution-and-privacy-disclosure.md)）。

## 怎麼偵測
- 通用：在手機實測授權、拒絕、逾時三條路徑；檢查回應標頭。
- 搜尋：`GeolocateControl|getCurrentPosition|watchPosition`（有無錯誤回呼）；`Permissions-Policy` 中的 `geolocation=\(\)`；iframe 的 `allow=` 屬性（適用 stack：mapbox-gl、maplibre）。

## 出處
- MDN〈Geolocation API〉、`GeolocationPositionError.code`、`Permissions-Policy: geolocation`：https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API ；Mapbox GL JS GeolocateControl API（用前查）。
- 相關卡：[11-11](11-11-attribution-and-privacy-disclosure.md)。

