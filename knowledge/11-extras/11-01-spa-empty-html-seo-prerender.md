---
id: 11-01
title: 地圖站原始 HTML 是空的：搜尋引擎看不到內容，要靜態說明、meta、結構化資料與一篇一個網址
topic: 11-extras
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [SEO, SPA, prerender, 預渲染, JSON-LD, meta description, noscript, 靜態產生, sitemap, 搜尋引擎]
---

## 原則
不要讓地圖站的原始 HTML 只剩一個空的根容器：在 HTML 內放靜態說明、meta 與結構化資料，想被收錄的結論一篇一個網址。

## 症狀
- Google `site:` 查自己的網站零結果，品牌詞也搜不到。
- view-source 只看到 `<div id="root"></div>` 和一個 script：h1 為 0，沒有 meta description、canonical，title 只有站名。
- 分享連結的預覽是空白；WebGL 初始化失敗時整頁空白，沒有任何說明。
- 圖層說明只寫在 popup 裡，popup 沒有網址，無法被收錄。

## 原因
地圖站的內容在 canvas 與 JS 狀態裡。搜尋引擎先抓原始 HTML，之後才（可能）渲染 JS；部分 AI 爬蟲不執行 JS（第三方研究，未自行驗證）。整站只有一個 URL，分享出去對方也只看到預設畫面。

## 解法
1. 在 `index.html` 的根容器內放一段靜態說明（h1、功能、資料來源、限制、隱私連結），掛載後由前端取代。畫面上用 visually hidden 隱藏（避免閃現整頁文字），但留在 DOM 與無障礙樹。
2. 補 `<title>`（含用途詞）、meta description、OG、`WebSite`／`WebApplication` JSON-LD、`<noscript>` 提示。
3. 一篇一個網址：想被引用的結論或分析做成建置期產生的靜態頁（Markdown → HTML，含 canonical、og:image、JSON-LD），文章內再用嵌入頁放互動地圖（[11-05](11-05-embed-page-security-billing-gestures.md)）。程式化的實體頁（例如每個機場一頁）以資料量門檻決定是否產生。
4. 新頁面登記到 sitemap；反向代理後的轉址用相對路徑，避免洩漏內部 `http://…:8080`。
5. 動態內容爬蟲看不到，另寫「這張圖在回答什麼問題」的靜態文字，並標資料截止日。
6. 整站預渲染（prerender／SSG）是進階選項；先做 1–4 通常已有明顯改善，效果以實際收錄結果驗證。
7. 原型版（約 10 分鐘）：title、description、og 兩個標籤、一個 h1、一段 noscript。

## 怎麼偵測
- 通用：`curl -s <站> | grep -c "<h1"` ≥ 1，且有 `<meta name="description"`；只看渲染後 DOM 不算數。
- 搜尋：`index.html` 的 body 只有空的 root；`<title>` 等於站名；缺 `application/ld+json`；文章／說明只存在於 JS bundle（適用 stack：任何 SPA；Next／Nuxt 等已 SSR 者不適用）。

## 出處
- Google Search Central〈JavaScript SEO basics〉：https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics ；schema.org `WebApplication`、`BlogPosting`。
- 相關卡：[11-02](11-02-robots-sitemap-soft404-canonical.md)、[11-05](11-05-embed-page-security-billing-gestures.md)。
- 實例：[mini-taiwan-pulse 首頁的靜態說明與 meta](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/index.html)、[文章靜態產生](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/blog/generator.ts)、[網站健檢紀錄](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/audit/site-health-2026-10-16.md)。

