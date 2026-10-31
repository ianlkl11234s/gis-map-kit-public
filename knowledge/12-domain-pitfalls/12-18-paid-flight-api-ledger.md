---
id: 12-18
title: 付費航跡 API：「標記完成」不等於「有資料」，要用帳本對帳並在花錢前擋掉無效請求
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Evaluated
stacks: [any]
tags: [FR24, flight, credit, ledger, 對帳, 付費 API, retry, circuit breaker, 去重, completeness]
---

## 原則
花錢的請求要在送出前擋掉必定無產出的，「標記完成」只能在確認有寫入後做；定期用帳本對帳「完成數、資料數、去重後 ID 數」，並在驗過三層之前不稱「完整」。

## 症狀
- 抓取進度顯示全部完成，實際資料檔比完成數少一百多班。
- 實際花掉的 credit 是估算的好幾倍。
- 網路層錯誤時批次靜默跳過，事後才發現整段缺漏。
- 地圖上的誤導：「某日全部航班」其實缺了一部分（常是特定類型，例如未申報起訖的公務機、直升機），畫面看起來完整，統計卻偏低；以為已經「完整一天」的機場其實只是名單處理完。

## 原因
1. 「花錢的請求」與「標記完成」之間某一步沒有寫入任何東西（例如起訖代碼都空，寫檔迴圈跑 0 次），上層仍無條件標記完成。
2. 計費單位估錯（以頁估算，實際以筆計），預算失準。
3. 只對 429 重試，網路層錯誤（timeout、連線重置）直接放棄。
4. 雙寫遷移期間同一班被掃兩次，重複計費也重複計數。

## 解法
1. 在花錢之前擋掉一定寫不出東西的請求（記到 skipped 清單，0 成本）；寫入零目標時直接 throw，不要靜默。
2. 定期對帳：done 數 vs 實際資料筆數 vs 去重後 ID 數，差異要分類。
3. 重試涵蓋網路層錯誤，並加 circuit breaker（連續 N 次失敗或最近 M 次失敗過半就停），避免把 credit 燒在壞掉的時段。
4. 去重以單一正本檔為準（例如以航班 ID），不要從兩個來源合併計數。
5. 「完整」拆三層驗：查詢涵蓋（時間窗、分頁）、航班取得（有無軌跡、404、空回應）、單班幾何（點數、連續性、起降端）。未驗前不稱「完整一天」。

## 怎麼偵測
- 通用：`done 數 − 實際資料數` 應為 0；不為 0 時列出差額的共同特徵。
- 搜尋（無條件標記完成）：`rg -n -i 'markDone|mark_done|setDone|done\.add' -B5`，看前面是否確認有寫入。
- 搜尋（重試範圍）：`rg -n -i '429|retry|backoff' `，確認也處理 `ECONNRESET|ETIMEDOUT|fetch failed`。
- 搜尋（circuit breaker）：`rg -n -i 'circuit|breaker|consecutive.?fail'`。

## 出處
- 一般付費 API 抓取做法（預檢、對帳、熔斷）。
- 實例：[歷史航跡盤點：「完整」要拆成查詢涵蓋、航班取得、單班幾何三件事](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/historical-flight-trails/inventory-2026-09-18.md)。

