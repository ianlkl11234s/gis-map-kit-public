---
id: 03-01
title: 時間模型選型：全站單一時鐘 vs 各圖層／各事件自己的 scoped clock
topic: 03-dynamics
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [時間軸, 時鐘, scoped clock, 全域時間, 回放, replay, live, 選型, 時間模型]
---

## 原則
日曆時間（多圖層要對齊同一個「現在」）用一條全站時鐘，圖層只訂閱不自己播放；事件內時間（只在單一面板有意義）用獨立的 scoped clock。兩者互不讀寫，不預先做逐圖層時間軸。

## 症狀
- 把「地震發生後 40 秒」這種事件內時間掛在以日曆時間為單位的全站時間軸上：單位對不上，其他圖層跟著亂跑。
- 每個圖層各自維護一個播放器：同時開三層，進度不同步，使用者看不出「現在是幾點」。
- 時間軸一動，整個 App 都在重算（見 [03-02](03-02-time-in-reactive-state-rerender-storm.md)）。

## 原因
「時間」有兩種尺度，常被混成一個：
1. **日曆尺度**：幾月幾日幾點，單位是 unix 秒，多個圖層應該看到同一個「現在」。
2. **事件尺度**：事件後經過幾秒或幾分鐘，只有一個面板在用，範圍與倍速都跟日曆無關。

## 解法
先回答三個問題再選：

| 問題 | 是 → | 否 → |
|---|---|---|
| 多個圖層要同時對齊到同一個時刻嗎？ | 全站單一時鐘 | 看下一題 |
| 時間單位是日曆時間嗎（unix 秒、日期）？ | 全站單一時鐘 | scoped clock |
| 這個播放只在一個面板或一個事件內有意義嗎？ | scoped clock | 全站單一時鐘 |

1. **全站單一時鐘**：只有一條主時間軸，其餘圖層都訂閱它（見 [03-03](03-03-subscription-granularity-and-throttle.md)），不各自播放。時間模式（回放／即時）也只有一個切換（見 [03-06](03-06-live-and-replay-share-one-render-path.md)）。
2. **scoped clock**：獨立的 external store，自帶範圍、倍速與 RAF，寫入即時、通知節流（約 10 Hz）；視覺寫成時鐘的純函數，scrub 只要 `set(t)`。實作細節見 [04-07](../04-effects-catalog/04-07-event-replay-scoped-clock.md)。
3. **兩者並存**：scoped clock 不寫入全站時鐘，反過來也不讀它。進入事件回放時，掛全站時鐘的圖層維持原狀，或在 UI 上明說「回放期間全站時間不動」。
4. **不要預先做逐圖層獨立時間軸**：一條主軸加模式切換通常就夠；逐圖層播放速度、範圍覆寫等有明確需求再做。
5. 多個圖層共用同一個 scoped clock 時，範圍取聯集、`setRange` 只呼叫一次（見 [04-07](../04-effects-catalog/04-07-event-replay-scoped-clock.md)）。
6. 畫面上同時有兩個時間（全站時間軸與回放面板）時，要讓使用者看得出各自是哪一個，不要只靠 tooltip。

## 怎麼偵測
- 通用：事件回放期間，無關的圖層也跟著動；或同時開多層時每層各有一個播放鍵、進度不一致；或回放總長用日曆秒表示卻從 0 開始。
- 搜尋（any）：同一個專案裡出現兩套以上的 `setInterval|requestAnimationFrame` 播放迴圈，且都在寫「目前時間」；`currentTime|playhead|elapsed` 以多個 state／store 並存。
- React：`useState\((0|Date\.now\(\))\)` 之後在多個元件各自 `setInterval`；Vue：多個元件各自 `ref(0)` 搭配 `setInterval`；純 JS：多個模組各自持有 `let t = 0` 並自行推進。

## 出處
- 一般時間軸 UI 設計慣例（單一播放頭加模式切換）。相關卡：[03-02](03-02-time-in-reactive-state-rerender-storm.md)、[03-03](03-03-subscription-granularity-and-throttle.md)、[03-06](03-06-live-and-replay-share-one-render-path.md)、[04-07](../04-effects-catalog/04-07-event-replay-scoped-clock.md)。
- 實例：[mini-taiwan-pulse 時間軸架構文件](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/TIMELINE_ARCHITECTURE.md)（含「不做什麼」清單）。

