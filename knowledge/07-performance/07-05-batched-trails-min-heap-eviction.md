---
id: 07-05
title: 數千條軌跡的批次繪製：一個 draw call、固定 slot、用 min-heap 逐出
topic: 07-performance
kind: pattern
scope: public
evidence: Evaluated
stacks: [mapbox-gl, maplibre, three.js]
tags: [BatchedTrails, draw call, slot, min-heap, 逐出, 軌跡, guard vertex, 部分上傳, 軌跡尾巴]
---

## 原則
數千條軌跡用單一 mesh、固定容量 buffer 與固定大小 slot 批次繪製，draw call 恆為 1；池滿時用二元 min-heap（O(log n)）逐出，不要線性掃描。

## 症狀
- 幾百條軌跡很順，超過兩三千條後掉幀，即使每條都只有幾個點。
- 池子滿了之後 CPU 時間暴增，某個函式佔了九成。
- 壓力下偶爾有軌跡莫名消失，且低物件數時重現不了。

## 原因
- 每條軌跡一個 `Line`＝一個 draw call＋一份物件開銷，成本隨「條數」而非「複雜度」成長。
- 池滿時要逐出一條；用線性掃描找「最快結束的」是 O(容量)，每次取得都掃，量大時佔去整層成本的絕大部分。
- 若 slot 被重新分配而堆裡還留著舊項目，不驗證就逐出會殺掉無關的健康軌跡。

## 解法
1. **單一 mesh、固定容量 buffer、固定大小 slot**：每條軌跡佔一個 slot。容量依峰值同時數量設定，夾在下限與上限之間（上限是記憶體保護）。
2. **guard vertex**：line strip 會把相鄰 slot 連起來，在 slot 兩端各放一個疊在鄰近頂點上、opacity＝0 的頂點；**所有 per-vertex attribute 都要複製**，不只 position。
3. **部分上傳**：每次寫入只標記自己 slot 的範圍，一幀合併成一段上傳；空閒 slot 池永遠先發最小 index，讓使用中的 slot 集中在 buffer 前段，範圍才會小。
4. **預先計算不動的部分**：歷史點只算一次並快取；每幀只對頭和尾做三角函數。
5. **逐出用二元 min-heap**（key＝結束時間）。兩個正確性細節：
   - 每個 slot 有序號（generation）；彈出的堆項目序號對不上就丟棄再彈。這是正確性要求，不是優化。
   - 時間戳常被量化，同值很多，要明確以取得順序打破平手，結果才和線性掃描一致。
   - 失效項目累積過多時重建堆。
6. **壓力測試**：把需求量拉到遠超容量，確認沒有健康軌跡被誤殺。

## 怎麼偵測
- 通用：軌跡數增加時幀時間線性上升；Profiler 顯示 slot 取得／逐出函式佔大宗；Draw call 數隨軌跡數增加。
- 搜尋：`for \(const .* of .*(slots|active)\.(values|entries)\(\)\)` 內比較 `endTime`／`end`；每條軌跡 `new THREE.Line\(`（適用 stack：three.js）。

## 出處
- three.js BufferAttribute 部分更新 API（`addUpdateRange`）。
- 相關卡：[07-04](07-04-update-granularity-setdata-vs-buffer.md)。

