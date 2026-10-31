---
id: 03-08
title: 時間軸上的資料缺段：顯示涵蓋範圍、缺的就說缺，不補 0 也不補舊值
topic: 03-dynamics
kind: decision
scope: public
evidence: Candidate
stacks: [any]
tags: [資料缺段, 涵蓋範圍, 密度條, 無資料, 缺測, null, 時間軸 UI, 多圖層時間範圍, 聯集]
---

## 原則
缺值在資料層保留 null，不補 0、不沿用前一格；畫面對缺段明說「此時段無資料」，並讓使用者看得出每個圖層的涵蓋範圍。

## 症狀
- 使用者拖到某個時段，畫面空白，分不出是「那時候沒事」、「資料還在載」還是「那段根本沒收集」。
- 某一天整批資料缺失，圖表或面量圖看起來像「全部歸零」。
- 多個圖層的資料涵蓋時段不同，時間軸範圍不是太長（都是空白）就是太短（有些資料看不到）。

## 原因
時間軸只有一條游標，沒有告訴使用者「哪裡有資料」；缺段與零值在畫面上長得一樣。

## 解法
資料層的語意規則是已驗證的做法；涵蓋時段的視覺化（第 4、5 步）只是設計建議，尚未有實作驗證。

1. **語意先於畫面**：缺值與零在資料層分開，缺值保留 null（見 [06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)）。
2. **畫面上缺段要說「無資料」**：游標落在沒有資料的時段，圖層顯示「此時段無資料」，不外推、不沿用前一格的值（見 [03-07](03-07-playhead-bounds-no-future.md)、[04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)）。
3. **時間軸範圍 = 已開啟且有時間維度的圖層之涵蓋時段聯集**；static 與 cyclic 型態不參與計算（見 [03-06](03-06-live-and-replay-share-one-render-path.md)）；無資料時退回預設範圍。
4. **涵蓋時段可視化（建議）**：在時間軸下方用半透明色塊疊出各資料源的涵蓋區間（資料密度條）；長空白可考慮壓縮，但壓縮會讓時間比例失真，要標示。
5. **逐圖層標示涵蓋範圍（建議）**：圖層列下方一行淡色小字，例如「2/18–2/20」，週期型寫「每日」，即時型寫「即時」。
6. 「無資料」不要與「載入中」「載入失敗」共用同一個空畫面（見 [09-07](../09-design-system/09-07-loading-data-time-and-stale.md)）。

## 怎麼偵測
- 通用：把游標拖到各圖層資料範圍之外，看畫面是空白、舊資料還是明確標示；關掉某天的資料來源，看圖表是否歸零。
- 搜尋：
  - 補 0：`\?\? ?0|\|\| ?0|COALESCE\(.*, ?0\)|fillna\(0\)` 出現在時間序列取值處（any；SQL／TS／Python）。
  - 前值沿用：`lastKnown|prevValue|lastGood` 在游標超出範圍時被回傳（any）。
  - 沒有涵蓋範圍：圖層登記沒有 `timeRange|coverage` 欄位（any）。

## 出處
- 一般時間序列視覺化的缺值處理建議。相關卡：[03-06](03-06-live-and-replay-share-one-render-path.md)、[03-07](03-07-playhead-bounds-no-future.md)、[06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)、[09-07](../09-design-system/09-07-loading-data-time-and-stale.md)。
- 實例：[mini-taiwan-pulse 時間軸架構文件](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/TIMELINE_ARCHITECTURE.md)（附錄設計稿：資料密度條與非線性壓縮，實作狀態標「未做」）。

