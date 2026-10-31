---
id: 06-10
title: loader 欄位名與資料來源不符：整包查詢失敗、catch 只 warn，圖層長期靜默空白
topic: 06-data-formats
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [loader, 欄位名, select, PostgREST, 靜默失敗, catch, console.warn, 空白圖層, 資料契約, view]
---

## 原則
接完資料圖層一定實際開啟看到點才算完成；loader 的 catch 不可只 warn，錯誤要進入載入狀態；空結果與失敗要分開。

## 症狀
- 圖層一直是空的，沒有任何錯誤畫面，壞了很久才被發現。
- Console 只有一行 warning；Network 的那個請求其實是 4xx 或回錯誤 JSON。

## 原因
- 前端用 `.select("a,b")` 或固定欄位清單取資料，欄位名與資料庫 view／API 實際欄位不同（例如少了單位後綴）。查詢**整包**失敗，不是只缺一欄。
- 錯誤被 `catch` 吞掉只印 warning，圖層「不建立」而不是顯示錯誤。
- 本機資料來源與正式不同，或沒有人實際打開過這個圖層。

## 解法
1. 接完資料圖層後，**一定實際開啟圖層看畫面**；把「開圖層、有點出現」當驗收項目。
2. loader 的欄位清單與來源 schema 由同一份型別或契約產生，或加契約測試（讀 view 欄位 vs 程式欄位）。
3. catch 不可只 warn：要讓錯誤進入載入狀態（顯示「載入失敗・圖層名」），見 [07-13](../07-performance/07-13-loading-state-and-lint-guard.md)。
4. 空結果與失敗要分開：回 0 筆是「沒資料」，4xx 是「失敗」。
5. 欄位改名／加單位後綴時，用 grep 找所有 loader；上游 view 改版要通知前端。
6. 欄位語意漂移是相似變體（見 [01-14](../01-taiwan-apis/01-14-semantics-drift-and-upstream-loss.md)），處理方式相同：契約測試加實際開圖層。

## 怎麼偵測
- 通用：圖層常駐空白但沒有紅字；DevTools Network 有 400；資料表有資料而圖層沒點。
- 搜尋：`catch\s*\(.*\)\s*\{\s*console\.warn` 且後面沒有 rethrow／錯誤狀態；`\.select\(["'][^"']+["']\)` 的欄位對照 view 定義（適用 stack：supabase-js／PostgREST 或任何 REST loader）。

## 出處
- 一般建議：以契約測試與驗收開圖層守住前後端欄位對應。
- 相關卡：[07-13](../07-performance/07-13-loading-state-and-lint-guard.md)、[01-14](../01-taiwan-apis/01-14-semantics-drift-and-upstream-loss.md)。
- 實例：[mini-taiwan-pulse 事故紀錄（颱風軌跡 loader 的欄位名缺單位後綴，PostgREST 整包報錯、catch 只 warn，圖層長期空白）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)。
