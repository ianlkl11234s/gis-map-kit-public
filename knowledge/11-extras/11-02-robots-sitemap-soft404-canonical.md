---
id: 11-02
title: robots.txt、sitemap 與 soft-404：SPA fallback 會讓這些檔都回 200 的首頁；多語版 canonical 不能寫死
topic: 11-extras
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [robots.txt, sitemap, soft 404, canonical, hreflang, RFC 9309, SPA fallback, 多語, Search Console]
---

## 原則
robots.txt、sitemap 一律放真實檔案，並讓「有副檔名但不存在的路徑」回 404；多語版的 canonical 指向各語版自己，不寫死單一網址。

## 症狀
- `/robots.txt`、`/sitemap.xml`、`/nonexistent` 全都回 200 的首頁 HTML；Lighthouse 判 robots.txt 有數十個語法錯誤。
- 不存在的頁面被當成重複內容收錄。
- AI 爬蟲的具名群組沒有重複寫 `Disallow`，原始資料目錄被爬走。
- 英日文版頁面都指向中文版的 canonical，外文版不被收錄。

## 原因
- SPA 的 fallback 對所有路徑回首頁。
- RFC 9309：具名 User-agent 群組不繼承 `*` 群組的規則。
- canonical 寫死在靜態 HTML，語言只靠 `?lang=` 切換。

## 解法
1. 在 `public/` 放真正的 `robots.txt`、`sitemap.xml`；web server 讓「有副檔名但不存在的檔案」回 404，只有無副檔名的 SPA 路徑回首頁。
2. 每個具名 User-agent 群組都重複寫 `Disallow`（原始軌跡、資料、API 目錄）。
3. sitemap 只放真正要被收錄的 URL，並帶 hreflang alternate；提交到 Search Console 並追蹤狀態。
4. 多語：hreflang 清單與各語版 canonical 指向自己，執行時依語言改寫 canonical；分享連結在非預設語言帶 `lang=`。
5. 路徑式語版（`/en/`）是進階選項，視收錄結果再決定。
6. 部署細節見 [10-05](../10-ops/10-05-local-vs-production-differences.md)。

## 怎麼偵測
- 通用：`curl -sI /robots.txt` 的 Content-Type 必須是 `text/plain`；`curl -sI /nonexistent.txt` 必須 404。
- 搜尋：`robots.txt` 中 `User-agent: GPTBot|ClaudeBot|…` 群組沒有 `Disallow`；`<link rel="canonical"` 在 `index.html` 寫死單一網址而專案有多語（適用 stack：any）。

## 出處
- RFC 9309 Robots Exclusion Protocol：https://www.rfc-editor.org/rfc/rfc9309 ；Google 多語版網站文件（hreflang）。
- 相關卡：[10-05](../10-ops/10-05-local-vs-production-differences.md)、[11-03](11-03-llms-txt-and-ai-crawler-policy.md)、[11-12](11-12-i18n-display-layer-lookup-and-fallback.md)。
- 實例：[mini-taiwan-pulse robots.txt](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/public/robots.txt)、[canonical 依語言改寫](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/i18n/canonical.ts)、[補 Disallow](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/b2fb1d232f9d9fad344b6cb43c1a4fc54311f5d5)、[副檔名缺檔回 404](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/0742af57bfcaa45986b40182401fe80caad278bc)。

