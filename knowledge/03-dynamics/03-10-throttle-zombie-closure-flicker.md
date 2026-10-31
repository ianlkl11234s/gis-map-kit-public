---
id: 03-10
title: 節流的 trailing 計時器會執行舊 closure：關掉的圖層殘影閃一下又消失
topic: 03-dynamics
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [throttle, trailing, closure, 殭屍, useCallback, 閃爍, listener 洩漏, 訂閱, 穩定性, 更新頻率]
---

## 原則
節流訂閱的回呼讀 ref 而非 closure 內的狀態，且保持 identity 穩定；清理時取消 pending 的 trailing 計時器，並讓所有地圖監聽器進清理函式。

## 症狀
- 高倍速播放時，把某一類圖層（分類開關）關掉，殘留的物件「閃一下又消失」。
- 關掉的分類，資料又被寫回地圖 source 一次。

## 原因
三層疊加：
1. **殭屍 trailing fire**：節流訂閱（見 [03-03](03-03-subscription-granularity-and-throttle.md)）在節流期間排了 trailing 計時器；框架重新 render 完成前，這個計時器仍可能執行舊版本的回呼 closure，用舊的「哪些分類開著」把資料寫回去。
2. **回呼進依賴陣列且 identity 每次都變**：回呼依賴一個每次 render 都新建的物件字面量，導致回呼與訂閱每次 render 都重綁，放大殭屍視窗。
3. **listener 洩漏**：在「初始化失敗就等 `style.load`／`idle` 再試」的分支裡註冊的監聽器，沒有進清理函式（見 [07-10](../07-performance/07-10-memory-leaks-listeners-contexts.md)）。

## 解法
1. 回呼讀 **ref**（最新的開關狀態、參數），回呼本身用空依賴陣列保持 identity 穩定；訂閱只綁一次。
2. 所有 `map.on(...)` 監聽器都進清理函式。
3. 開關改變時另用一條穩定化的 key（把開關狀態壓成短字串）當依賴，變動就立即強制重算一次，不等下一個節流週期。
4. 清理時一併取消 pending 的 trailing 計時器，或在計時器回呼內先檢查「是否已卸載／已關閉」。
5. **穩定性修好後要顯式設更新頻率**：原本「順暢」可能是每次 render 重綁而額外觸發更新的副產物；修好後畫面可能退化成 1 Hz 跳格。把更新拆成輕量（點與足跡，約 10 Hz）與重量（軌跡，約 1 Hz）兩條，總 CPU 不增加但視覺流暢。

## 怎麼偵測
- 通用：高倍速播放時快速開關分類，看關掉的物件會不會再閃現；長時間操作後 listener 數量上升。
- 搜尋：`useCallback\(.*,\s*\[[^\]]*(visibility|filters|options)` 依賴一個每次 render 新建的物件；`subscribeThrottled|throttle\(` 的回呼讀的是 closure 內的狀態而非 ref；`map\.on\(['"](style\.load|idle)` 出現在條件分支而 cleanup 內沒有對應 `map.off`（適用 stack：React + 任何地圖函式庫；其他框架看「回呼是否捕捉到舊狀態」）。

## 出處
- 一般 React／訂閱生命週期知識（stale closure）。相關卡：[03-03](03-03-subscription-granularity-and-throttle.md)、[07-10](../07-performance/07-10-memory-leaks-listeners-contexts.md)。
- 實例：[mini-taiwan-pulse 事件紀錄](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)（「2026-06-13 衛星 throttle 殭屍 closure 閃爍」：60x 播放下關掉某分類仍殘留閃爍）。
