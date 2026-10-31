---
id: 03-05
title: 時間窗與預載：只載視窗內的日期，並限制同時請求數
topic: 03-dynamics
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [預載, prefetch, 時間窗, 並行上限, concurrency, debounce, 載入中, loading, 快取, 資料庫連線池]
---

## 原則
預載只認「視窗內的日期鍵清單」，視窗外不請求；所有預載走有並行上限的佇列，失敗只警告；前景載入一定要有可見的載入狀態。

## 症狀
- 使用者把時間範圍拉到 7 天、同時開了幾個按日載入的圖層，後端連線池被打爆，畫面一片 LOADING。
- 預載了畫面看不到的前後幾天，浪費流量，載入面板被灌滿。
- 預載失敗就把主流程打斷，或預載的請求也跳出載入提示。

## 原因
「按日分檔」的動態資料，每個圖層各自預載、各自併發，請求數是「圖層數 × 天數」；預載邏輯若以「目前日期往外推 N 天」計算，會超出使用者真正看得到的範圍。

## 解法
1. **視窗是唯一真相**：時間 store 維護「視窗內的日期鍵清單」（選定日期起算 N 天），預載只認這份，視窗外不請求，不往外多推。
2. **中心日 foreground、其餘日背景**：目前日用正常載入（有載入提示）；其餘日走靜默預載，與前景共用同一份快取，但不顯示載入面板。
3. **全域並行上限**：所有輕量預載走同一個佇列，同時最多 2 個（依後端能承受的連線數調整），另加約 500 ms 的 debounce，避免視窗連續變動時反覆排隊。大型 payload（影像之類）另外排程，不混進輕量佇列。
4. **預載失敗只警告**：不拋、不影響前景；之後真的切到那天時再走前景載入。
5. **前景載入一定要有可見的載入狀態**：切日、第一次開圖層、改會重抓資料的參數，都註冊到共用的載入狀態登記，禁止靜默 `fetch().then()`。資料畫上地圖之後，載入狀態要延續到地圖真的 idle，不要在請求回來時就關掉。
6. 換日通知要 debounce（見 [03-03](03-03-subscription-granularity-and-throttle.md)），避免快速 scrub 時對中間日期發請求。

```ts
// 並行上限佇列的最小形狀
const MAX = 2; let inflight = 0; const queue: Array<() => Promise<unknown>> = [];
function pump() {
  while (inflight < MAX && queue.length) {
    const task = queue.shift()!; inflight++;
    task().finally(() => { inflight--; pump(); });
  }
}
```

## 怎麼偵測
- 通用：把時間範圍調到最大、同時開所有按日載入的圖層，看 Network 面板的同時請求數與後端連線數；看有沒有請求落在視窗之外的日期。
- 搜尋：
  - 外推：`for \(let i = ?-?\d+; i <= ?\d+; i\+\+\).*(addDays|date)` 之類往前後各推 N 天的迴圈（any）。
  - 沒有並行限制：`Promise\.all\(.*(dates|days|keys)\.map\(` 直接對全部日期併發（any）。
  - 靜默載入：`\.rpc\(.*\)\.then\(|fetch\(.*\)\.then\(` 的呼叫端沒有登記載入狀態（React、Vue、純 JS 皆適用）。

## 出處
- 一般前端請求排程做法（有界併發佇列、debounce）。相關卡：[03-03](03-03-subscription-granularity-and-throttle.md)。
- 實例：[mini-taiwan-pulse 預載佇列](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/lib/dayPrefetch.ts)（並行上限 2、debounce 500 ms；註解記錄範圍 7 天時兩個圖層各排 6 個背景日）、[開發規則 §2](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/development-rules.md)（載入狀態登記）。

