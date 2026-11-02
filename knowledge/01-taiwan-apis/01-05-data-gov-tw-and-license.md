---
id: 01-05
title: data.gov.tw：只是目錄，metadata 用 /api/v2/rest/dataset/<id>（不是 package_show）、要帶自訂 UA；授權要顯名標示提供機關
topic: 01-taiwan-apis
kind: decision
scope: public
evidence: Observed
stacks: [any]
tags: [data.gov.tw, 授權, OGDL, 顯名標示, metadata API, User-Agent, 403, 資料集更新, 編碼]
---

## 原則
把 data.gov.tw 當目錄：用 metadata API 取真實下載網址，再到機關主機抓檔；出處一律寫釋出機關而不是 data.gov.tw；授權「未載明」就照實標示，不自行推定。

## 症狀
- 目錄上拿到的下載連結失效、資源 id 被截斷、檔名一換就抓不到。
- SHP ZIP 解壓後檔名亂碼。
- 地圖頁尾寫「資料來源：data.gov.tw」。
- 部分資料的授權欄「未載明」，不知能不能用。

## 原因
- data.gov.tw 是目錄；真正檔案放在各機關主機，真實下載網址要從 metadata 的 distribution 取。
- 檔名常含日期，新版換檔名；ZIP 內檔名可能為 cp950 編碼。
- 政府資料開放授權條款（第 1 版）要求依「顯名聲明」標示提供機關（機關、年份、資料名稱與版本號、依本條款釋出）；官方條文寫明未盡顯名義務視為自始未取得授權。條款不含專利與商標，與 CC BY 4.0 相容（官方 data.gov.tw/license）。

## 解法
1. 讀 metadata 用 `GET https://data.gov.tw/api/v2/rest/dataset/<資料集ID>`（回傳標題、欄位、格式、更新頻率、授權、下載網址）；**不是 CKAN 的 `package_show`**（實測回 404）。再到 distribution 裡的機關主機抓檔，記錄抓取日期與檔名。
   - 全文搜尋沒有公開文件化的 API；網站前台用 `POST /api/front/dataset/list`（JSON body 帶 `bool:[{fulltext:{value:關鍵字}}]`），格式可能變動，建議包成腳本集中維護。
   - 搜尋關鍵字一次只放一個短詞（例：「電廠」而不是「發電廠 燃煤」）：多個詞會變成更嚴的查詢，常常 0 筆（實測「發電廠 燃煤」0 筆、「發電廠」10 筆、「電廠」50 筆）。下「找不到」的結論前，至少用 2 個不同的單詞同義詞都搜過。
   - 要帶自訂 User-Agent：Python `urllib` 預設 UA（`Python-urllib/x.y`）會被回 403，瀏覽器或 curl 預設 UA 正常。
   - 下載網址常是「檔案清單 API」：先拿到一串檔名與 url，再逐一下載，預估量要算兩段。
2. 出處寫釋出機關，不寫 data.gov.tw；格式「機關、年份、資料名稱（版本）、依政府資料開放授權條款第 1 版釋出」。圖台應有每個圖層的來源 footer。
3. 授權「未載明」時：照常記為未載明，並於圖層註明；不要自己推定為某一授權。
4. 偵測資料有無更新：用 metadata 比對（更新日期、檔名）。
5. 注意部分 access_url 夾帶他人的 api_key，不要留存或公開。

## 怎麼偵測
- 通用：頁尾來源是平台名稱而不是機關；圖層 popup 沒有來源與授權；抓取程式把檔名寫死。
- 搜尋：`data\.gov\.tw`（出現在 attribution 字串中）、寫死含日期的檔名（適用 stack：any）。

## 出處
- 官方：data.gov.tw/license（授權條款）。

