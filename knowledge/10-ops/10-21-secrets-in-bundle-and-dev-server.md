---
id: 10-21
title: 金鑰進前端 bundle：VITE_ 前綴的值是公開的，dev server 轉譯後的模組也會印出它
topic: 10-ops
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [金鑰, secret, VITE_, bundle, 環境變數, dev server, 對話外洩, 公開 token, 網域限制, BYOK]
---

## 原則
前端環境變數前綴（`VITE_` 等）的值一律視為公開，不放 secret；檢查環境設定與排錯時只列 key 名稱、不印值，也不要 curl dev server 轉譯後的模組。

## 症狀
- 用 curl 抓 dev server 的轉譯後模組，輸出裡帶出環境變數的值，貼進 AI 對話或 CI log。
- 平台 CLI 列出環境變數時印出實際值。

## 原因
- 前綴變數會被內嵌進前端程式碼（機制見 [10-04](10-04-public-token-vs-secret.md)），開發期也一樣。
- dev server 轉譯模組時把 `import.meta.env` 的值寫進輸出。
- 部分 CLI 列變數時預設顯示值。
- 公開 key 與 secret 怎麼分、怎麼保護見 [10-04](10-04-public-token-vs-secret.md)。

## 解法
公開 key 與 secret 的分類、BYOK、bundle 掃描、外洩後輪換，完整說明見 [10-04](10-04-public-token-vs-secret.md)；CSP 見 [10-24](10-24-csp-for-map-sites.md)。本卡只留開發期的外洩路徑：
1. 檢查環境設定、排錯時**只列 key 名稱**（`env | cut -d= -f1`），不印值。
2. 禁止 curl dev server 轉譯後的模組；派工給 AI agent 的 prompt 明列這項禁止。
3. 平台 CLI 的列變數指令導向 `/dev/null`，只取 key 名稱。

## 怎麼偵測
- 通用：對話、CI log、派工紀錄裡出現 dev server 轉譯模組的輸出或環境變數的值。
- 搜尋：腳本或派工 prompt 中的 `curl[^\n]*(localhost|127\.0\.0\.1):[0-9]+/(src|@fs|@id)/`（抓 dev server 轉譯模組）；`printenv|env\s*$`、平台 CLI 列變數指令沒有只取 key 名稱（適用 stack：vite 等有 dev server 的 bundler）。前端變數名稱與打包產物的金鑰掃描見 [10-04](10-04-public-token-vs-secret.md)。

## 出處
- Vite 環境變數說明（VITE_ 前綴會暴露給客戶端）；MDN CSP Report-Only。
- 相關卡：[10-04](10-04-public-token-vs-secret.md)。
- 實例：[mini-taiwan-pulse BYOK 對話框說明](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/byok-chat/README.md)（金鑰由使用者自填，網站不代付）。
