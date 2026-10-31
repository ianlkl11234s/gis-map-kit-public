# 03-dynamics 動態與時間軸

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [03-00](03-00-dynamics-index.md) | 動態與時間軸總表：時間模型、訂閱、三種時間、預載、即時回放、邊界、缺段與常見 bug | 時間是共用的外部狀態：先選時間模型，播放中的時間放在框架外的 store，由各圖層自己訂閱，再依資料粒度挑訂閱方式。 | catalog | Implemented | any | 總表, 動態, 時間軸, 時間訂閱, 節流, 預載, 回放, 缺段, store, 重繪 |
| [03-01](03-01-time-model-global-vs-scoped-clock.md) | 時間模型選型：全站單一時鐘 vs 各圖層／各事件自己的 scoped clock | 把「地震發生後 40 秒」這種事件內時間掛在以日曆時間為單位的全站時間軸上：單位對不上，其他圖層跟著亂跑。 | decision | Implemented | any | 時間軸, 時鐘, scoped clock, 全域時間, 回放, replay, live, 選型, 時間模型 |
| [03-02](03-02-time-in-reactive-state-rerender-storm.md) | 播放中的時間放進框架響應式狀態：每幀整個 App 重繪，圖層越多越卡 | 時間軸回放時，單開一個動態圖層還順，同時開三、四層就掉幀。 | pitfall | Observed | any | React, Vue, Svelte, useState, 響應式, re-render, currentTime, deps, external store, 時間軸, 60fps |
| [03-03](03-03-subscription-granularity-and-throttle.md) | 時間訂閱的粒度：逐幀、節流、只看日期，各依資料粒度選 | 每幀都 `setFilter` 或查表，GPU 沒事但主執行緒被塞滿。 | pattern | Implemented | any | 節流, throttle, debounce, 訂閱, subscribe, 日期, 粒度, setFilter, 預載, trailing edge |
| [03-04](03-04-data-time-vs-playback-time-vs-wall-clock.md) | 三種時間不要混：資料時間、播放時間、掛鐘時間；內部一律 UTC epoch | 回放歷史資料時，畫面角落的「3 分鐘前」「現在 14:32」跟著回放跳，不是真實時間。 | pattern | Implemented | any | 時區, UTC, epoch, 掛鐘, wall clock, 資料時間, 抓取時間, 新鮮度, 日期鍵, 時間戳 |
| [03-05](03-05-time-window-and-prefetch.md) | 時間窗與預載：只載視窗內的日期，並限制同時請求數 | 使用者把時間範圍拉到 7 天、同時開了幾個按日載入的圖層，後端連線池被打爆，畫面一片 LOADING。 | pattern | Observed | any | 預載, prefetch, 時間窗, 並行上限, concurrency, debounce, 載入中, loading, 快取, 資料庫連線池 |
| [03-06](03-06-live-and-replay-share-one-render-path.md) | 即時與回放共用同一條渲染路徑：只換「誰在寫時間」，並依資料的時間型態決定怎麼顯示 | 即時與回放各寫一份繪圖程式，改一邊忘了另一邊，兩邊畫面逐漸不一致。 | pattern | Implemented | any | 即時, live, 回放, replay, 時間型態, track, snapshot, cyclic, event, static, 模式切換 |
| [03-07](03-07-playhead-bounds-no-future.md) | 播放頭的邊界：不播進未來、尾端停住不回跳、分頁切回不暴衝 | 回放播到「今天 23:59」，但現在才下午三點：後半段是空的，卻像在播放。 | pitfall | Implemented | any | 播放頭, 未來, 尾端, clamp, RAF, dt, 分頁切換, 倍速, 邊界, 外推 |
| [03-08](03-08-timeline-gaps-and-data-coverage.md) | 時間軸上的資料缺段：顯示涵蓋範圍、缺的就說缺，不補 0 也不補舊值 | 使用者拖到某個時段，畫面空白，分不出是「那時候沒事」、「資料還在載」還是「那段根本沒收集」。 | decision | Candidate | any | 資料缺段, 涵蓋範圍, 密度條, 無資料, 缺測, null, 時間軸 UI, 多圖層時間範圍, 聯集 |
| [03-09](03-09-store-write-during-render.md) | 在 render 階段寫入被訂閱的 store：警告只在 remount／HMR 時才出現 | Console 出現「Cannot update a component (A) while rendering a d… | pitfall | Observed | any | React, render, useSyncExternalStore, StrictMode, HMR, 副作用, store write, 警告, remount, useEffect |
| [03-10](03-10-throttle-zombie-closure-flicker.md) | 節流的 trailing 計時器會執行舊 closure：關掉的圖層殘影閃一下又消失 | 高倍速播放時，把某一類圖層（分類開關）關掉，殘留的物件「閃一下又消失」。 | pitfall | Observed | any | throttle, trailing, closure, 殭屍, useCallback, 閃爍, listener 洩漏, 訂閱, 穩定性, 更新頻率 |
