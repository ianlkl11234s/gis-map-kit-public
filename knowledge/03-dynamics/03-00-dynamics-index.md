---
id: 03-00
title: 動態與時間軸總表：時間模型、訂閱、三種時間、預載、即時回放、邊界、缺段與常見 bug
topic: 03-dynamics
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [總表, 動態, 時間軸, 時間訂閱, 節流, 預載, 回放, 缺段, store, 重繪]
---

## 原則
時間是共用的外部狀態：先選時間模型，播放中的時間放在框架外的 store，由各圖層自己訂閱，再依資料粒度挑訂閱方式。時間軸的邊界與缺段要明說，不補值。

## 對照表

### 時間模型與訂閱
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 多圖層要對齊同一個「現在」，還是單一面板自己播 | [03-01](03-01-time-model-global-vs-scoped-clock.md) | 日曆時間用全站單一時鐘、圖層只訂閱；事件內時間用 scoped clock，兩者互不讀寫 |
| 播放時整個 App 每幀重繪、圖層越多越卡 | [03-02](03-02-time-in-reactive-state-rerender-storm.md) | 時間放 external store，不放 useState／ref；圖層 hook 參數不收 currentTime |
| 不知道該逐幀、節流還是只看日期 | [03-03](03-03-subscription-granularity-and-throttle.md) | 依資料更新粒度挑；節流要補 trailing edge，跨日載入要 debounce |
| 時間顯示對不上、時區亂 | [03-04](03-04-data-time-vs-playback-time-vs-wall-clock.md) | 資料時間、播放時間、掛鐘時間分開存放；內部一律 UTC epoch；「更新於」顯示資料時間 |

### 預載
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 播放時請求暴增或卡頓 | [03-05](03-05-time-window-and-prefetch.md) | 只預載視窗內日期鍵，走有並行上限的佇列；前景載入要有可見的載入狀態 |

### 即時與回放
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 同時要做即時與回放 | [03-06](03-06-live-and-replay-share-one-render-path.md) | 渲染層只讀一個時間，模式只決定誰寫時間；顯示規則依資料時間型態統一登記 |

### 邊界與缺段
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 播放頭跑進未來、到尾端回跳、分頁切回暴衝 | [03-07](03-07-playhead-bounds-no-future.md) | 終點取 min(視窗結尾, 現在)，抵達就停住；單幀 dt 夾上限；推進一幀寫成純函式 |
| 時間軸上某段沒資料 | [03-08](03-08-timeline-gaps-and-data-coverage.md) | 資料層保留 null，不補 0 也不沿用前值；畫面明說「此時段無資料」並顯示涵蓋範圍 |

### 常見 bug
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| render 時寫 store，警告只在 remount／HMR 出現 | [03-09](03-09-store-write-during-render.md) | render 階段不寫任何被訂閱的 store，寫入放 effect、事件處理器、async 或 RAF |
| 關掉的圖層殘影閃一下又消失 | [03-10](03-10-throttle-zombie-closure-flicker.md) | 節流回呼讀 ref 並保持 identity 穩定；清理時取消 trailing 計時器，監聽器全進清理函式 |

## 相關主題
- 動態圖層的特效：[04-00](../04-effects-catalog/04-00-effects-index.md)。
- 事件圖層的固定上限凍結：[12-01](../12-domain-pitfalls/12-01-timestamp-timezone-offset.md)。
- 移動物件與軌跡的規模：[14-07](../14-scale-density/14-07-moving-objects-and-trails-at-scale.md)。

## 出處
各項依據見對應卡片。
