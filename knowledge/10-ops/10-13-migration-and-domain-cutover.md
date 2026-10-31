---
id: 10-13
title: 搬家與網域切換：先盤點依賴與金鑰，測試網址逐頁比對通過，才切正式網域
topic: 10-ops
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [搬遷, 網域切換, 平台停運, 金鑰輪換, 驗收, 測試網址, DNS, 退回]
---

## 原則
搬家前先盤點依賴、金鑰名稱與要帶走的狀態，在測試網址逐頁與舊站比對通過並寫好退回步驟後，才切正式網域。

## 症狀
- 託管平台宣布停止營運或發生資安事件，時間緊迫。
- 搬完切網域後才發現：底圖 403、大檔 404、前端路由壞、金鑰沒換。
- 新舊兩邊同時在跑，寫入重複。

## 原因
選平台時看好不好用與價格，沒想過平台本身會消失；也沒有維護「依賴清單、金鑰名稱清單、要帶走的狀態」。

## 解法
1. **平時就維護**：每個服務的依賴清單（用到哪些外部服務與內網位址）、金鑰名稱清單（只列名稱）、搬遷時要帶走的狀態（本地 volume、尚未上傳的緩衝）。
2. 平台出事（外洩環境變數）→ 放在上面的**所有金鑰**都要輪換，輪換與搬家一起排。
3. 分流：純靜態站搬靜態託管；動態服務另開主機；需要台灣 IP 的來源留在台灣 VM（見 [10-12](10-12-upstream-ip-block-deploy-env.md)）；已經搬走的任務要在舊處維持停用。單一實例任務的切換順序見 [10-18](10-18-single-instance-and-unuploaded-state.md)。
4. 每個站依序：讀舊部署規則 → 寫新託管設定（headers、SPA fallback、`.assetsignore`）→ 檢查檔數與單檔大小 → dry-run／本機模擬逐條 curl → 部署到**測試網址**，瀏覽器逐頁與舊站並排比對（截圖）→ 補 CI 自動部署 → 使用者看過才切網域，**寫好退回步驟**。
5. 測試網域要加入 token 網域白名單、CORS 允許清單、OAuth 回呼清單（見 [10-04](10-04-public-token-vs-secret.md)、[10-05](10-05-local-vs-production-differences.md)）。
6. 切換後驗證：用兩種 UA 與無痕視窗開首頁、抽幾個資料檔看 content-type（[10-05](10-05-local-vs-production-differences.md)），並確認 `robots.txt`／sitemap 沒被舊設定覆蓋。

## 怎麼偵測
- 通用：問「平台明天消失，哪些金鑰要換、哪些檔案要帶走？」答不出來。
- 搜尋：專案缺 `docs/*dependencies*` 或金鑰名稱清單；部署設定寫死舊平台內網位址（如 `*.internal`）（適用 stack：any）。

## 出處
- 一般搬遷實務。託管平台官方公告（用前查）。相關卡：[10-04](10-04-public-token-vs-secret.md)、[10-05](10-05-local-vs-production-differences.md)、[10-12](10-12-upstream-ip-block-deploy-env.md)、[10-18](10-18-single-instance-and-unuploaded-state.md)。

