# 07-performance 繪製效能與品質

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [07-00](07-00-performance-index.md) | 效能總表：症狀或想做的事 → 該看哪張卡 | 先看 [07-01](07-01-performance-budget-and-measurement.md) 訂預算並… | catalog | Evaluated | any | 總表, 效能, 量測, 大量點, 重繪, 記憶體, 首屏, RPC, 載入狀態, 個資 |
| [07-01](07-01-performance-budget-and-measurement.md) | 先量再改：效能預算與量測方法（推測不等於實測，TypedArray 不在 JS heap） | 花了半天優化，畫面沒有變順。 | pattern | Evaluated | any | 效能預算, 量測, DevTools, performance.now, 閒置, render 次數, 記憶體, backingStorage, DPR, A/B |
| [07-02](07-02-many-points-rendering.md) | 大量點的渲染：縮放分階的點徑與描邊、PMTiles、cluster／heatmap、GPU instancing 怎麼選 | 打開一個幾十萬點的圖層後，筆電風扇狂轉、拖曳卡頓。 | decision | Evaluated | mapbox-gl, maplibre, leaflet, deck.gl, three.js | 大量點, cluster, heatmap, circle, instancing, 描邊, 低 zoom, 發熱, 點徑, symbol |
| [07-03](07-03-hidden-layer-paint-keeps-map-busy.md) | 沒開任何圖層，地圖仍一直重畫：對隱藏圖層 setPaintProperty 會讓 transition 卡住 | 所有圖層關閉、時間軸暫停，`map.on('render')` 仍持續觸發，風扇不停。 | pitfall | Observed | mapbox-gl | 多圖層, 全關, 耗電, setPaintProperty, transition, hasTransitions, idle, 隱藏圖層, visibility none, 重畫, 風扇 |
| [07-04](07-04-update-granularity-setdata-vs-buffer.md) | 更新粒度：每幀別 setData；位置寫 typed array，樣式只更有變的 key，物件組不變就不重建 | 播放時每幀 CPU 很高，`setData` 佔大宗。 | pattern | Implemented | mapbox-gl, maplibre, deck.gl, three.js | setData, typed array, buffer, InstancedMesh, per-instance attribute, dispose, 重建, diff, 閃爍, fast path |
| [07-05](07-05-batched-trails-min-heap-eviction.md) | 數千條軌跡的批次繪製：一個 draw call、固定 slot、用 min-heap 逐出 | 幾百條軌跡很順，超過兩三千條後掉幀，即使每條都只有幾個點。 | pattern | Evaluated | mapbox-gl, maplibre, three.js | BatchedTrails, draw call, slot, min-heap, 逐出, 軌跡, guard vertex, 部分上傳, 軌跡尾巴 |
| [07-06](07-06-float32-timestamp-precision.md) | 絕對時間戳不要存 Float32：1.7e9 秒的精度只有 128 秒，動畫會一格一格跳 | 高倍速播放時軌跡的「已走過／未走過」邊界每隔一段時間才跳一格，而不是平滑前進。 | pitfall | Observed | mapbox-gl, maplibre, deck.gl, three.js | float32, 精度, timestamp, unix, ulp, 相對時間, shader uniform, 階梯, 播放 |
| [07-07](07-07-backend-preaggregate-and-data-path-triage.md) | 後端預先彙總：慢查詢先分流成靜態快照、預彙總表、即時 RPC 三條路 | 時序或大表的查詢動輒數秒到逾時，使用者看到空白或轉圈。 | decision | Evaluated | any | 預彙總, pre-aggregate, matview, RPC, 快照, CDN, cron, advisory lock, OOM, 索引, 併發排隊 |
| [07-08](07-08-public-rpc-timeout-clamp-rowcap.md) | 對外 RPC 的三個守門：逾時有層級、範圍要 clamp、列數上限會靜默截斷 | 大查詢在 3 秒被砍，前端拿到空結果。 | pitfall | Observed | any | statement_timeout, clamp, PostgREST, 20000, 206, content-range, 靜默截斷 |
| [07-09](07-09-bundle-size-lazy-load-on-demand.md) | 首屏要輕：重函式庫與明細按需載入、視窗內才載、主執行緒外解析 | 首屏 JS 達數 MB，行動網路載入很慢。 | pattern | Evaluated | any | bundle, lazy, React.lazy, dynamic import, code splitting, Web Worker, 視窗內載入, 分批, 首屏 JS, 二進位 |
| [07-10](07-10-memory-leaks-listeners-contexts.md) | 記憶體洩漏：切底圖或重建圖層後，listener、WebGLRenderer、場景實例越留越多 | 反覆切換底圖或圖層後，頁面記憶體線性成長，最終變慢或 WebGL context lost。 | pitfall | Evaluated | mapbox-gl, maplibre, deck.gl, three.js | 記憶體洩漏, dispose, listener, webglcontextlost, WebGLRenderer, 切底圖, style.load, cleanup, TypedArray |
| [07-11](07-11-big-response-memory-blowup-streaming.md) | 大回應整包解析會讓記憶體膨脹數倍：串流解析、落地磁碟、重工作放子行程 | 排程資料處理在某幾天把主行程記憶體從 1.5 GB 推到 4 GB，主機 MemAvailable 見底，OOM kil… | pitfall | Evaluated | any | 記憶體, OOM, 串流, ijson, 子行程, oom_score_adj, collector, 解析, JSON, RSS |
| [07-13](07-13-loading-state-and-lint-guard.md) | 載入狀態也是功能：每個非同步請求都要有 loading／error，且用測試守住 | 使用者看著空白地圖，分不出「在載入」還是「沒有資料」。 | pitfall | Implemented | any | loading, error, 載入中, 靜默失敗, 守門測試, ratchet, 豁免, 空白地圖, 使用者感受速度 |
| [07-14](07-14-open-data-pii-column-exclusion.md) | 開放資料本身可能含個資：入庫與上圖前先列欄位，欄位級排除並在建置腳本擋住 | popup 直接顯示個人姓名與電話。 | pitfall | Observed | any | 個資, PII, 開放資料, 姓名, 電話, 欄位排除, popup, 建置腳本, 去識別化, 資安 |
