---
id: 07-00
title: 效能總表：症狀或想做的事 → 該看哪張卡
topic: 07-performance
kind: catalog
scope: public
evidence: Evaluated
stacks: [any]
tags: [總表, 效能, 量測, 大量點, 重繪, 記憶體, 首屏, RPC, 載入狀態, 個資]
---

## 原則
先看 [07-01](07-01-performance-budget-and-measurement.md) 訂預算並量測，再依症狀選卡；沒有前後數字的優化不算數。本主題也收了載入狀態與開放資料個資兩張非純效能卡，分在最後一張小表。

## 對照表

### 量測
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 覺得「很慢」、要開始優化 | [07-01](07-01-performance-budget-and-measurement.md) | 先訂可自動量的預算，優化前後用同一套量測對照 |

### 點與軌跡渲染
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 一個圖層點數很多、縮放時卡 | [07-02](07-02-many-points-rendering.md) | 數量級門檻照 [14-02](../14-scale-density/14-02-point-count-thresholds.md)（低縮放換熱區、延後出點）；要動畫或 3D 用 GPU instancing；點徑隨縮放只限該卡定義的特例 |
| 軌跡動畫一格一格跳 | [07-06](07-06-float32-timestamp-precision.md) | 時間戳存相對值，不把 unix 絕對秒放進 Float32 |

### 重繪與更新粒度
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 沒開任何圖層地圖仍持續重畫 | [07-03](07-03-hidden-layer-paint-keeps-map-busy.md) | 不對隱藏圖層呼叫 setPaintProperty，隱藏時暫存樣式 |
| 動畫或即時資料每幀更新 | [07-04](07-04-update-granularity-setdata-vs-buffer.md) | 每幀只改變動的部分，位置寫 typed array，setData 留給真正換集合時 |

### 後端彙總與 RPC 守門
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 查詢慢、資料量大 | [07-07](07-07-backend-preaggregate-and-data-path-triage.md) | 先分流成靜態快照、預彙總表、即時 RPC，改之前用 EXPLAIN 量 |

### 首屏與記憶體
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 首屏太重 | [07-09](07-09-bundle-size-lazy-load-on-demand.md) | 重函式庫與明細動態 import，進入視窗才載資料，重解析放 Worker |
| 切底圖或重建圖層後越用越慢 | [07-10](07-10-memory-leaks-listeners-contexts.md) | 每個 listener 與 GPU 資源都要對應釋放，重複操作 N 次量斜率 |

### 非純效能：載入狀態與個資
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 非同步請求沒有 loading 或 error | [07-13](07-13-loading-state-and-lint-guard.md) | 每個請求都註冊狀態，並用會紅燈的測試守住 |
| 新開放資料要入庫或上圖 | [07-14](07-14-open-data-pii-column-exclusion.md) | 先列全部欄位，疑似個資在建置腳本排除，不只事後清理 |

## 相關主題
- 點數量級與縮放畫法：[14-00](../14-scale-density/14-00-scale-density-decision-table.md)。
- 對外 RPC 的權限面：[10-23](../10-ops/10-23-database-public-exposure-tables-functions.md)。
- 載入、錯誤、無資料、過期四態的呈現：[09-07](../09-design-system/09-07-loading-data-time-and-stale.md)。

## 出處
各項依據見對應卡片。
