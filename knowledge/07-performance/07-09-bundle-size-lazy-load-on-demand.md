---
id: 07-09
title: 首屏要輕：重函式庫與明細按需載入、視窗內才載、主執行緒外解析
topic: 07-performance
kind: pattern
scope: public
evidence: Evaluated
stacks: [any]
tags: [bundle, lazy, React.lazy, dynamic import, code splitting, Web Worker, 視窗內載入, 分批, 首屏 JS, 二進位]
---

## 原則
首屏只載入必要的程式與資料：重函式庫與明細用動態 `import()` 延後，資料在圖層開啟且進入視窗才抓，重解析放到 Web Worker。

## 症狀
- 首屏 JS 達數 MB，行動網路載入很慢。
- 載入一個大 JSON 時主執行緒長任務，畫面凍結。
- 使用者沒開的圖層，資料早就下載完了。

## 原因
- 重函式庫（3D、六角格、統計）被靜態 import，進了主 bundle，即使多數使用者不用。
- 明細資料與首屏資料綁在一起。
- 大量 JSON 在主執行緒 parse。

## 解法
1. **量 bundle**：每次發版記錄首屏 JS 大小；用 bundle analyzer 找前幾大依賴。
2. **動態 `import()`**：3D 引擎、六角格庫、統計明細、圖例面板等「點了才用」的模組延後載入（`React.lazy`＋Suspense）。
3. **資料按需**：圖層關閉就不抓、不建；換主題時跳過隱藏圖層的建置；PMTiles／MVT 只下載視窗內圖磚，檔案總大小只影響儲存，不影響使用者載入量。
4. **分批**：大集合依區域或時間分片，優先載入視野內的；背景預取要可取消，並標註在 loading 豁免名單。
5. **主執行緒外**：重 parse 或空間索引放 Web Worker；大陣列用 `postMessage` 的 transferable 避免拷貝。把 JSONL 改為欄式二進位（header＋typed array＋offsets），解析成本趨近記憶體複製（見 [06-01](../06-data-formats/06-01-format-selection-decision.md)）。
6. **取捨**：lazy 會增加首次互動延遲，需要預載（hover／idle 時預取）；Worker 增加維護成本，只在量到長任務時才用。每次調整後用 [07-01](07-01-performance-budget-and-measurement.md) 的預算對照。

## 怎麼偵測
- 通用：首屏 Network 的 JS 超過預算；Performance 面板主執行緒長任務；沒開圖層仍在下載其資料。
- 搜尋：`^import .* from ['"](three|h3-js|d3|@turf/turf)` 在入口檔；頂層 `await fetch` 載入非首屏資料；`JSON\.parse\(` 對大字串（適用 stack：vite、webpack、React）。

## 出處
- React.lazy、Vite 動態 import、MDN Web Workers。
- 相關卡：[06-01](../06-data-formats/06-01-format-selection-decision.md)、[07-01](07-01-performance-budget-and-measurement.md)。
- 實例：[mini-taiwan-pulse 效能稽核](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/audit/perf-audit-2026-09-30.md)（three、h3、統計明細改按需後，首屏 JS 約 8.6→6.2 MB）。

