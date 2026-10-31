---
id: 03-03
title: 時間訂閱的粒度：逐幀、節流、只看日期，各依資料粒度選
topic: 03-dynamics
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [節流, throttle, debounce, 訂閱, subscribe, 日期, 粒度, setFilter, 預載, trailing edge]
---

## 原則
時間 store 提供逐幀、節流、只看日期三種訂閱，依資料本身的更新粒度挑；節流一定要補送 trailing edge，跨日載入一定要 debounce。

## 症狀
- 每幀都 `setFilter` 或查表，GPU 沒事但主執行緒被塞滿。
- 節流太狠：拖曳進度條停下來之後，畫面停在倒數第二個狀態（少了最後一次更新）。
- 快速拖過好幾天，十幾個圖層同時為「中間日期」各打一波請求。

## 原因
同一個時間來源有三種截然不同的消費需求（動畫要逐幀、篩選約每 0.2–1 秒、載入只在換日時），卻只提供一種訂閱方式。

## 解法
| 需求 | 訂閱方式 | 要點 |
|---|---|---|
| 動畫迴圈每幀要位置 | 直接 `getTime()` 同步讀（在 RAF／render 內） | 不訂閱、不經框架 |
| 每次都要反應但不在迴圈內 | `subscribe(cb)` | 高頻，只給輕量的事 |
| 篩選、查表、UI 時間文字 | `subscribeThrottled(ms, cb)` | **trailing edge**：節流期間的最後一次必須補送，否則停下來時畫面是舊的 |
| 跨日載入資料 | `subscribeDate(cb)` | 只在日期鍵變化時通知；加 leading＋trailing debounce |

**節流毫秒依資料粒度，不憑感覺：**
- UI 時間數字約 250 ms。
- 事件過濾 200–500 ms；10 分鐘粒度的快照 1000 ms 就夠。
- 分鐘級資料用「分鐘鍵」判斷是否換格，沒換就不動。

**日期通知的 leading＋trailing debounce：**
- 距上次通知已安靜超過 quietMs（例如 300 ms）：立即通知，單次切日零延遲。
- 安靜期內又變化：暫存，等連續 quietMs 沒有新變化才送「最後一個日期」，中間日期全部略過。
- 通知前比對是否與上次相同，相同就不送。

**把節流器做成可注入時鐘與計時器**（`now`、`schedule`、`cancel` 當參數），單元測試才能不靠真實等待。

```ts
// trailing edge 的最小形狀
function scheduleThrottled(e: { ms: number; last: number; pending: boolean; cb: (t: number) => void }) {
  const elapsed = performance.now() - e.last;
  if (elapsed >= e.ms) { e.last = performance.now(); e.cb(store.getTime()); }
  else if (!e.pending) {
    e.pending = true;
    setTimeout(() => { e.pending = false; e.last = performance.now(); e.cb(store.getTime()); }, e.ms - elapsed);
  }
}
```

## 怎麼偵測
- 通用：拖曳進度條放開後畫面不是最終狀態；快速拖過多天，Network 面板瞬間出現一串中間日期的請求；播放時主執行緒長期滿載。
- 搜尋：
  - 逐幀裡做重事：RAF 回呼內有 `setFilter|setData|fetch|querySourceFeatures`（mapbox-gl、maplibre）。
  - 節流缺 trailing：自寫 throttle 函式內只有 `if (now - last < ms) return;` 而沒有 `setTimeout` 補最後一次（any）。
  - 日期載入沒做 debounce：`subscribeDate|onDateChange|watch\(.*date` 的回呼直接 `fetch`（any）。

## 出處
- lodash 文件：throttle／debounce 的 leading／trailing 語意。
- 相關卡：[03-02](03-02-time-in-reactive-state-rerender-storm.md)、[03-05](03-05-time-window-and-prefetch.md)、[03-10](03-10-throttle-zombie-closure-flicker.md)（trailing 計時器執行舊 closure）。
- 實例：[mini-taiwan-pulse 時間 store](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/state/timeStore.ts)（節流訂閱含 trailing edge）、[日期通知器](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/state/dateNotifier.ts)（quietMs=300，註解說明快速 scrub 時多個 hook 同時打 RPC 的原因）。
