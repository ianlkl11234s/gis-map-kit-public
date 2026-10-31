---
id: 11-13
title: 敘事頁與 scrollytelling：地圖嵌入而不重畫，正文每個數字都要在 data.json 台帳有出處
topic: 11-extras
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [scrollytelling, story mode, 敘事, 資料新聞, IntersectionObserver, 嵌入地圖, iframe, 靜態圖 fallback, data.json, 數字台帳, 可追溯, 查詢, 口徑]
---

## 原則
敘事頁嵌入地圖站的 embed 頁，不在文章裡重畫地圖；正文每個數字都要在結構化台帳（`data.json`）有一筆，含資料日期、口徑與可重跑的查詢。

## 症狀
- 想把地圖站上的發現寫成有互動地圖的長文，結果每篇文章都自己重寫一份地圖程式。
- 文章發出半年後被問「這個數字怎麼算的」，找不到當時的查詢，也不知道是哪一天的資料。
- 多篇文章共用的數字（站數、班次）每篇寫得不一樣。
- 捲動式故事頁在手機上卡頓，或轉貼到社群平台時 iframe 被擋、地圖整塊空白。

## 原因
- 敘事頁和地圖站是兩種產品：地圖站要能自由探索，敘事頁要固定鏡頭、時間、圖層講一件事；在文章裡重做地圖，兩邊很快不一致。
- 數字散在正文裡，沒有結構化記錄口徑、資料日期與產生方法。
- 很多平台與內嵌環境（社群貼文、部分 CMS、有 CSP 的頁面）不允許 iframe。

## 解法
**地圖**
1. 嵌入地圖站，不在文章重畫：地圖站提供 embed 頁，網址參數帶鏡頭、圖層、時間、播放速度與語言（[11-04](11-04-share-camera-og-image-saved-scene.md)）；文章只放 iframe，並開協作手勢避免攔截頁面捲動（[11-05](11-05-embed-page-security-billing-gestures.md)）。
2. 回放類地圖固定日期：用匯出的快照檔，不依賴即時資料，文章一年後打開仍一樣。
3. 每張嵌入圖都備一張靜態圖（同參數拍攝）加「在地圖站開啟」連結；轉貼到不允許 iframe 的地方改用靜態圖。

**捲動敘事**
1. 用 `IntersectionObserver`（例如 threshold 0.5）偵測哪一章節在視窗中並切換場景；不要在 `scroll` 事件裡每幀計算。
2. 側邊或頂部放章節導覽，點擊用 `scrollIntoView` 跳轉。
3. 場景切換以鏡頭與圖層狀態為單位；尊重 `prefers-reduced-motion`，改成直接切換而不是長飛行。
4. 給 AI 與搜尋引擎讀的長文，內容要在原始 HTML 裡、一篇一個網址（[11-01](11-01-spa-empty-html-seo-prerender.md)）。

**數字台帳**
1. 每篇文章一份 `data.json`：正文每個數字一筆，含 `value`、`as_of`（資料日期）、`method`（口徑）、`query`（可重跑的查詢檔）。
2. 口徑先寫再寫數字：同一指標的官方定義與體感定義可能差很多，正文要點名用哪個。
3. 官方數字優先，自算只用在官方沒有的維度；資料有缺口就明講，不用推估值補。
4. 多篇共用的數字只存一份，其他文章引用；要更新時改台帳、重跑查詢，再回頭改正文。
5. 每篇另留工作紀錄（研究、確認、複核）與資料盤點（品質警訊）；尚未成篇的現象先記到題庫。

## 怎麼偵測
- 通用：文章中的數字沒有日期或口徑；嵌入地圖沒有靜態替代；文章內有自己的地圖初始化程式。
- 搜尋：文章 Markdown 中的數字（`\d[\d,]*\s*(件|座|站|班|人|%)`）在 `data.json` 找不到對應條目（any，可寫腳本比對）。
- 搜尋：故事頁用 `addEventListener\(['"]scroll` 做場景判斷，而沒有 `IntersectionObserver`（any）。
- 搜尋：`<iframe` 沒有相鄰的 `<img`／`<noscript>` 靜態替代（any）。

## 出處
- MDN `IntersectionObserver`、`scrollIntoView`、`prefers-reduced-motion`。
- 相關卡：[00-12](../00-system-thinking/00-12-pattern-to-insight-confounding-claim-check.md)（發布前檢查主張強度）、[11-01](11-01-spa-empty-html-seo-prerender.md)、[11-04](11-04-share-camera-og-image-saved-scene.md)、[11-05](11-05-embed-page-security-billing-gestures.md)。
- 實例：[mini-taiwan-pulse 文章系統（嵌入 /embed、回放必帶 date=、iframe 內協作手勢）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/blog/README.md)。

