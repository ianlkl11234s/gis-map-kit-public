---
id: 10-19
title: CDN 快取規則要貼著不可變前綴設定，並事先備好只清單一 URL 的 purge
topic: 10-ops
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [Cloudflare, Cache Rule, Edge TTL, 指標檔, scoped purge, purge everything, 404, 回讀驗證, 前綴]
---

## 原則
CDN 快取規則只貼在不可變前綴，並同時設定錯誤碼不快取；改完用公開網址回讀驗證，事先備好只清單一 URL 或前綴的 purge。

## 症狀
- 新增一條「為了讓檔案走邊緣快取」的規則後，原本短 TTL 的指標檔（`current.json` 類）被凍成數小時，新版本已發布但使用者讀到舊版。
- 補檔後同一 URL 仍回 404，規則設成「忽略原站 cache-control、固定快取 N 天」把錯誤頁也快取了。
- 出事要清快取時，手上只有「整站清除」，會連大型底圖等不相干的大檔一起清掉，之後全部回源。

## 原因
- CDN 的規則會**覆寫原站 metadata**；規則罩住整個父路徑，就連本來該短 TTL 的檔一起套上長效策略。
- 404／5xx 被一併快取的機制見 [06-04](../06-data-formats/06-04-cache-immutable-404-and-stale-edge.md)。
- 只檢查物件儲存端的 HEAD 會看到正確的短 TTL，看不出邊緣實際回應。
- 緊急時才發現沒有 scoped purge 的憑證與腳本，代價不對稱。

## 解法
1. **規則只貼在不可變前綴**（檔名含日期或內容雜湊的目錄，例如 `/x/manifests/`、`/x/artifacts/`），不要罩住整個父路徑；指標檔所在路徑不套規則，保持原站的短 TTL。
2. 固定 TTL 的規則同時設定**錯誤碼（404／5xx）不快取**。
3. **改規則後用公開網址回讀**，不是看儲存端 HEAD：指標檔要看到短 `Cache-Control` 與 `DYNAMIC`（或等價的未快取狀態）；不可變檔第一次 MISS、第二次 HIT。
4. **事先備好 scoped purge**：憑證、腳本、文件都在（依 URL 清，或依前綴清，視方案支援），並驗證過；平常避免使用「清除全部」，只在沒有替代方案時用，並知道代價。
5. 把「purge 只清要清的」寫進部署回復步驟，與 [10-02](10-02-data-update-vs-redeploy-and-cache.md) 的發布順序放在一起。

## 怎麼偵測
- 通用：改完規則後用 `curl -I` 對指標檔連打兩次，看 `cache-control` 與 `age`、快取狀態；盤點 CDN 規則是否罩住含「會變的檔」的路徑；問「現在能不能只清一個 URL」。
- 搜尋：部署腳本中只有 `purge_everything|purge_cache.*everything`，沒有帶 `files`／`prefixes` 的版本；規則的路徑表達式是 `/data/*`、`/statistics/*` 這種父路徑而非具體版本前綴（適用 stack：任何 CDN，名稱依供應商而異）。

## 出處
- 各 CDN 的 Cache Rules／Edge TTL／Purge 文件（用前查當期，各方案的 purge 範圍不同）。
- 實例：[INCIDENTS.md（過寬的 Cache Rule 凍結指標檔；忽略 cache-control 的規則連 404 一起快取）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)。
