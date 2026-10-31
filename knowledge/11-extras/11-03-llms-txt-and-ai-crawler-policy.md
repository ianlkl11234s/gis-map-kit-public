---
id: 11-03
title: llms.txt 與 AEO 是提案不是標準；robots.txt 說允許 AI 爬蟲，CDN 邊緣層可能照樣回 403
topic: 11-extras
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [llms.txt, AEO, GEO, AI 爬蟲, GPTBot, ClaudeBot, robots.txt, Cloudflare, bot 管理, 403]
---

## 原則
把 llms.txt 當低成本實驗，不承諾效果；robots.txt 允許 AI 爬蟲之後，要用各 bot 的 User-Agent 實測回應碼，不一致就回報站主，不自行改 CDN 設定。

## 症狀
- 站上放了 `llms.txt`，卻沒有任何證據有 AI 服務讀它或因此更常引用你。
- `robots.txt` 明寫允許 GPTBot／ClaudeBot，用這些 UA 去 `curl` 首頁卻回 403，而 Googlebot UA 回 200。
- 文件目的是「讓 AI 讀到全文」，實際被邊緣層擋掉。

## 原因
- `llms.txt` 是 2024 年提出的提案（頁面自稱 proposal），不是正式標準，效果未證實；「AEO／GEO」是業界用語，沒有標準機構定義。
- robots.txt 只是請求，不是門鎖。CDN／WAF 有自己的 bot 規則（例如託管的 robots.txt 段會加在既有內容前面、AI Crawl Control 可強制擋），與 repo 裡的檔案可能不一致。

## 解法
1. 要做 llms.txt：內容誠實寫明網站性質（純前端互動地圖、沒有逐筆資料文字版）、涵蓋限制（「未涵蓋不等於零」）、授權與資料時間；數字必須能追溯來源，查不到就不寫。
2. 不要在沒有量測前寫成「已提升引用」；要量測可定期抽問 AI 並記錄是否引用。
3. 上線驗收時對照意圖與實際：`curl -A "<bot UA>" -I <url>`，比較 robots.txt 的意圖與回應碼。
4. 偽造 UA 不是官方 IP，可能被邊緣層當冒名者擋下，不能直接推論真正的爬蟲也被擋；要到 CDN 的 bot／AI 爬蟲設定確認。
5. 結果不一致時回報站主，不自行改 CDN 設定。
6. Cloudflare 的 Content Signals（`search`／`ai-input`／`ai-train`）是該廠商機制，不是跨業界標準。
7. 原型版替代：README 開頭三行（這張圖回答什麼、資料來源、限制），人與 AI 都讀得懂。

## 怎麼偵測
- 通用：對照 robots.txt 與各 UA 的實際回應碼。
- 搜尋：repo 內 `llms.txt` 的數字沒有出處；文件宣稱「AI 可讀取」但專案沒有針對各 bot UA 的驗收腳本（適用 stack：any）。

## 出處
- llmstxt.org：https://llmstxt.org/ （自稱 proposal）；Cloudflare〈Managed robots.txt〉：https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/ 。
- 相關卡：[11-02](11-02-robots-sitemap-soft404-canonical.md)。
- 實例：[mini-taiwan-pulse llms.txt](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/public/llms.txt)。

