---
id: 11-11
title: 出處標示不可被嵌入參數拿掉；隱私說明要和瀏覽器實際請求的第三方一致
topic: 11-extras
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [attribution, 版權, 授權, 隱私, CDN beacon, Web Analytics, OAuth 品牌驗證, 隱私權政策, 嵌入]
---

## 原則
任何模式都不得隱藏 attribution；隱私頁列出的第三方，要以瀏覽器 Network 面板實際出現的網域為準，不能只讀程式碼。

## 症狀
- 嵌入版或拍攝模式把出處標示一起隱藏，違反底圖或開放資料的 attribution 要求。
- 隱私頁寫「沒有追蹤」，瀏覽器 Network 卻出現 CDN 自動注入的統計 beacon。
- OAuth（Google 登入）同意畫面顯示陌生網域，品牌驗證要求首頁連到隱私權政策。
- 隱私頁用嚴格 CSP 後，自動注入的統計腳本被擋掉。

## 原因
- 簡化嵌入版時，UI 參數一併關掉 attribution。
- 只讀程式碼找不到 CDN 在邊緣層自動注入的腳本。
- 「又沒蒐集資料」的假設，遇到登入、使用者自填 API key、統計後不再成立。

## 解法
1. 任何 UI 參數、Capture／拍攝模式、嵌入模式都不得隱藏 attribution；底圖右下角保留，頁尾列資料來源與授權；即時資料同時標資料時間。
2. 程式碼授權與資料授權分開聲明（例如 MIT 只管程式碼）。
3. 隱私頁列出所有第三方（資料庫、地圖 SDK 的使用統計、物件儲存、LLM 服務、統計服務），並與 Network 面板實際出現的第三方網域一致。
4. 有 Google 登入就備好隱私頁（多語、含自行刪除帳號），並在首頁可達；首頁靜態說明加隱私連結。
5. 隱私頁若設 enforcing CSP，它會擋 CDN 自動注入的 beacon，並要在頁面揭露有使用該統計；CSP 整體做法見 [10-24](../10-ops/10-24-csp-for-map-sites.md)。
6. 品牌驗證被自動檢查回報「首頁沒有回應」時，先用多種 UA 實測再申訴。
7. 學生版（必做）：地圖右下角保留底圖 attribution，頁尾列資料來源與授權。

## 怎麼偵測
- 通用：用拍攝／嵌入參數載入，看 attribution 是否仍在；對照隱私頁清單與 Network 面板的第三方網域。
- 搜尋：`attributionControl:\s*false` 無替代標示；`ui=` 參數處理中同時移除版權元素；隱私文字缺 CDN 統計揭露（適用 stack：any）。

## 出處
- OpenStreetMap 授權與使用政策（attribution）；Google OAuth 品牌驗證說明（用前查）。
- 相關卡：[11-05](11-05-embed-page-security-billing-gestures.md)、[11-06](11-06-canvas-capture-export-print.md)。
- 實例（mini-taiwan-pulse）：[嵌入版 ui= 參數不得移除出處](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/embeddable-map/changelog.md)、[隱私頁內容](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/privacy/privacyContent.ts)、[補揭露 Cloudflare Web Analytics](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/075dd5c920f2aeddc9d204a44d0cc13a34132ff3)、[首頁隱私連結](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/f3f8fc1c5cfc53a76ecd050aa86a893c83d7ebd1)、[隱私頁三語與刪除帳號](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/47c6cb9e6b01aa2bf8ad773de849eb6491a607fa)。
