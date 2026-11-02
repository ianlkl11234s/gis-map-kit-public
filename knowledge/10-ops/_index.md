# 10-ops 上線維運與持續收集

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [10-00](10-00-ops-index.md) | 上線維運總表：部署、金鑰、監控、排程、搬家事故、測試守門 | 先判斷問題屬於哪個子題再選卡；上線前先看部署與金鑰兩組，上雲端才出問題先看搬家與事故組。 | catalog | Observed | any | 總表, 維運, 部署, 金鑰, 監控, 告警, 排程, 搬家, 事故, 測試 |
| [10-01](10-01-deploy-option-decision.md) | 部署選型：把網站拆成「前端程式、資料檔、會變的來源」三件事，各自選放哪 | 以為「部署網站」就是把整包丟上去，結果大檔進 git、換資料每次都要重建前端。 | decision | Implemented | any | 部署, 靜態站, Cloudflare, Pages, Workers, R2, 物件儲存, 資料庫, 容器, nginx, 選型 |
| [10-02](10-02-data-update-vs-redeploy-and-cache.md) | 資料更新不等於重建前端：換內容就換檔名，快取政策跟著版本化 | 資料補上了，使用者（或自己）仍看到舊檔。 | pattern | Observed | any | 快取, cache-control, immutable, 版本化, 指標檔, manifest, CDN, 404 快取, purge, 退版 |
| [10-03](10-03-pmtiles-range-cdn-cors.md) | PMTiles 上線檢查：要回 206、CORS 放行 range、不被 CDN 快取成錯誤頁 | 回 200 而非 206、log 只有 header 讀取：見 [06-03](../06-data-formats/0… | pattern | Implemented | any | PMTiles, Range, 206, CORS, ETag, CDN, 大檔, 物件儲存, 同源 |
| [10-04](10-04-public-token-vs-secret.md) | 公開 client token 與真 secret 要分開：VITE_ 前綴的變數一定會進前端 bundle | 把 service role、API client secret、S3 金鑰放進 `VITE_*` 變數，打包後任何人 … | pitfall | Implemented | any | token, secret, 金鑰, 環境變數, VITE_, bundle, anon key, RLS, 輪換, 網域限制 |
| [10-05](10-05-local-vs-production-differences.md) | 本機正常、上線就壞：環境差異清單與上線 smoke test | 本機 curl／dev server 都好，部署後某圖層消失；Network 裡資料檔回 200，但內容是 `index… | pitfall | Observed | any | 上線, 環境差異, smoke test, 25 MiB, charset, SPA fallback, token 網域, gitignore, lock 檔, 健康檢查 |
| [10-09](10-09-schedule-taipei-timezone.md) | 排程的「今天」是哪一天：資料庫與雲端主機是 UTC，台北 00:00–08:00 會算錯 | 台北凌晨到早上 8 點之間，「今天」的聚合資料永遠是空的。 | pitfall | Observed | any | 時區, UTC, Asia/Taipei, current_date, cron, pg_cron, GitHub Actions, 日界, 排程 |
| [10-12](10-12-upstream-ip-block-deploy-env.md) | 上雲端才連不上：來源封鎖雲端出口 IP；ConnectTimeout 先懷疑被擋，不是網路慢 | 本機（台灣 ISP）測試都正常，部署到雲端後某來源持續 ConnectTimeout，資料停更數天。 | pitfall | Observed | any | IP 封鎖, ConnectTimeout, 出口 IP, 台灣 IP, 政府 API, collector, 雲端, blackhole |
| [10-21](10-21-secrets-in-bundle-and-dev-server.md) | 金鑰進前端 bundle：VITE_ 前綴的值是公開的，dev server 轉譯後的模組也會印出它 | 用 curl 抓 dev server 的轉譯後模組，輸出裡帶出環境變數的值，貼進 AI 對話或 CI log。 | pitfall | Observed | any | 金鑰, secret, VITE_, bundle, 環境變數, dev server, 對話外洩, 公開 token, 網域限制, BYOK |
| [10-22](10-22-data-license-tiers-and-owner-only-layers.md) | 資料授權分級決定能放到哪裡：未標示授權要選邊，授權不允許公開的資料走站主限定圖層 | 來源頁寫「僅供瀏覽」或重利用條件未確認的資料，被放進公開目錄，任何人可直接下載原始檔。 | decision | Implemented | any | 授權, 政府資料開放授權條款, CC BY, ODbL, 未標示授權, 僅供瀏覽, 商業 API 條款, 個資, 站主限定, 私有圖層, 後端代理, 白名單, Range, 衍生資料, HOLD |
| [10-23](10-23-database-public-exposure-tables-functions.md) | 前端帶公開金鑰時，資料庫的表、欄位、函式、schema 都要當成對全世界開放來盤點 | 匿名使用者能呼叫內部的清理、refresh 函式，拖慢或改動共用資料庫。 | pitfall | Implemented | any | Supabase, PostgREST, anon, authenticated, RLS, GRANT, REVOKE, PUBLIC, default privileges, SECURITY DEFINER, search_path, exposed schemas, 欄位權限, 個資 |
| [10-24](10-24-csp-for-map-sites.md) | 地圖站的 CSP：先 Report-Only 觀察，把 SDK 必要指令與所有圖磚、API 網域列進白名單，再轉 enforcing | 直接上 enforcing 後地圖整張空白，console 出現 worker 或 blob 被擋的訊息。 | pattern | Implemented | any | CSP, Content-Security-Policy, Report-Only, connect-src, worker-src, blob, img-src, frame-ancestors, report-to, beacon, 白名單, 圖磚網域 |
| [10-25](10-25-frontend-error-monitoring.md) | 地圖站的前端錯誤監控：除了 JS 錯誤，還要接地圖 SDK 的 error 事件與 WebGL context lost，送出前去掉位置資料 | 使用者回報「地圖空白」，開發者重現不了。 | pattern | General | any | 錯誤監控, error tracking, Sentry, GlitchTip, window.onerror, unhandledrejection, map error, webglcontextlost, source map, 取樣, 個資, breadcrumb, release |

