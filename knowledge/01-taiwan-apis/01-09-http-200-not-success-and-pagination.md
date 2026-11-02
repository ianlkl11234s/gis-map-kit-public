---
id: 01-09
title: HTTP 200 不等於拿到資料：回 HTML、靜默截斷、分頁漂移
topic: 01-taiwan-apis
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [200, HTML, content-type, 截斷, 分頁, offset, page, 10000, 20000, 100000, PostgREST]
---

## 原則
每次回應都驗 content-type 與可否 parse，筆數等於任何已知上限就視為疑似截斷並改走分頁；不要只看 HTTP 200。

## 症狀
- 地圖空白但 Network 全是 200。
- 資料只有一部分，且筆數剛好是 9,999／10,000／20,000／100,000。
- 翻頁後漏資料。
- JSON parse 失敗，內容其實是官網首頁。

## 原因
- 許多政府 API 路徑或參數錯誤時回 200＋HTML，而不是 404／400。
- 單次回傳有上限，超過靜默截斷（例如 9,999、10 萬）；資料庫 REST 層（如 PostgREST）也可能因設定的列數上限回 206 而不報錯。
- 沒有總筆數的 list，用 offset 翻頁會在資料變動時漂移。
- 回應含個資欄位而被原樣存下。

## 解法
1. 每次回應先看狀態碼、content-type、前 200 字；content-type 非 JSON、parse 失敗，視為失敗並告警。
2. 筆數等於任何已知上限時標「疑似截斷」，改走分頁。
3. 分頁以「回傳筆數 < limit」判斷末頁；有 `page` 參數優先用 page。
4. 失敗重試最多 2 次，之後回報，不要無限重試。
5. 存檔前剔除個資欄位（姓名、電話）。
6. 抓取記錄「抓取時間」與筆數，趨勢突然腰斬先懷疑截斷。

## 怎麼偵測
- 通用：資料筆數是整數上限；時序突然少一半；欄位型別數字被當字串。
- 搜尋：`await.*\.json\(\)`（前面沒有 `ok|status|content-type` 檢查）；`limit=|\$top=|page_size`（適用 stack：any）。

## 出處
- 一般建議：驗證回應型別與筆數上限為通用做法。
- 相關卡：[01-02](01-02-cwa-integration.md)、[01-03](01-03-moenv-integration.md)、[01-04](01-04-wra-integration.md)。
- 實例：[PostgREST 2 萬列上限事故](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)（地下水井只畫出部分測站）。

