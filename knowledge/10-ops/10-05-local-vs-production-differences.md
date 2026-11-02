---
id: 10-05
title: 本機正常、上線就壞：環境差異清單與上線 smoke test
topic: 10-ops
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [上線, 環境差異, smoke test, 25 MiB, charset, SPA fallback, token 網域, gitignore, lock 檔, 健康檢查]
---

## 原則
上線後逐項核對本機與正式環境的差異，並用無痕視窗確認每個資料檔的 content-type 不是 `text/html`；SPA fallback 會讓缺檔回 200 加 HTML。

## 症狀
- 本機 curl／dev server 都好，部署後某圖層消失；Network 裡資料檔回 200，但內容是 `index.html`，`JSON.parse` 失敗。
- 加了自訂網域後，測試網址整站 404。
- 用需要 token 的底圖時，測試網址上底圖 403。
- 中文亂碼；前端路由重新整理 404。
- 雲端 `npm ci` 失敗；啟動時同步大檔太久，健康檢查逾時。
- 某些資料檔線上 404：被 gitignore，又沒上傳。

## 原因
本機與正式環境在網域、IP、快取、檔案是否真的存在、託管預設行為上都不同。最危險的一類是 **SPA fallback 把不存在的檔案也回 200＋HTML**。

## 解法
差異清單：

| 差異 | 做法 |
|---|---|
| 底圖 token 有網域限制（僅限需 token 的底圖，如 Mapbox；預設 OpenFreeMap 免 key 不受影響） | 測試網域（如 `*.workers.dev`、`*.pages.dev`）要加入白名單，否則底圖 403 |
| 託管預設不帶 `charset=utf-8` | `_headers` 補 `Content-Type` charset |
| SPA 路由 | 有前端路由 → 託管設 SPA fallback；沒有 → 設 `none`，否則缺檔回 200 HTML |
| 單檔上限（常見 25 MiB 等級） | 建置後檢查 `dist/` 最大檔；超過改放物件儲存 |
| 設了自訂網域後測試網址失效 | Workers 的 `routes` 與 `workers_dev: true` 要明確同時寫 |
| 本機能抓、雲端不能抓 | 見 [10-12](10-12-upstream-ip-block-deploy-env.md)（出口 IP 被封） |
| lock 檔不同步 | CI 用 `npm ci`，移除套件後記得更新 lock |
| 啟動同步大檔 | 改背景同步、web server 先起；否則健康檢查逾時 |
| gitignore 的資料檔 | 上線清單逐一確認「有上傳／有同步」 |
| build 期 `VITE_*` 缺少 | CI 用 `test -n` 擋缺少的變數 |

**上線 smoke（必做）**
1. 用無痕視窗開測試網址；DevTools Network 逐個資料檔確認 `content-type` 不是 `text/html`。
2. 程式端：fetch 資料檔後檢查 Content-Type，收到 `text/html` 要報錯，不要交給 `JSON.parse`。
3. 部署契約測試：新增資料子目錄時，若 nginx／同步腳本沒跟著改就讓測試紅燈。
4. 手機、桌機各開一次；console 無錯誤。

## 怎麼偵測
- 通用：上線後某圖層空白，Network 看資料檔的 response 開頭是 `<!doctype html>`。
- 搜尋：`curl -s <url>/nonexistent.json -o /dev/null -w "%{http_code}\n"` 回 200 即有 SPA fallback 吞缺檔；託管設定缺 `charset`；`.gitignore` 中的資料副檔名在部署腳本找不到對應上傳（適用 stack：any）。

## 出處
- Cloudflare Workers Static Assets 文件（`not_found_handling`、`_headers`）；各託管 limits 頁（用前查）。
- 實例：[PLAYBOOKS.md（新增大檔漏改 nginx，缺檔回 index.html 導致 JSON 解析失敗）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/PLAYBOOKS.md)、[deployContract.test.ts（部署契約測試）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/__tests__/deployContract.test.ts)。

