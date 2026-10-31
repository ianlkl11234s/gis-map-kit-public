---
id: 03-07
title: 播放頭的邊界：不播進未來、尾端停住不回跳、分頁切回不暴衝
topic: 03-dynamics
kind: pitfall
scope: public
evidence: Implemented
stacks: [any]
tags: [播放頭, 未來, 尾端, clamp, RAF, dt, 分頁切換, 倍速, 邊界, 外推]
---

## 原則
播放終點取 min(視窗結尾, 現在)；抵達或超過終點就原地停住、不回跳；單幀 dt 夾上限。把「推進一幀」寫成可單元測試的純函式。

## 症狀
- 回放播到「今天 23:59」，但現在才下午三點：後半段是空的，卻像在播放。
- 播到尾端又自動回到起點，或使用者把游標拖到未來後按播放，畫面往回跳。
- 切到別的分頁再切回來，倍速 960x 的回放瞬間跳過大半天。

## 原因
- 播放終點用「視窗結尾」，沒有與「現在」取較早者。
- 尾端的處理只考慮「抵達」，沒有處理「已經在尾端之後」的狀態。
- 瀏覽器會凍結背景分頁的 RAF，切回的第一幀 dt 可能是好幾秒，乘上倍速就暴衝。

## 解法
1. **播放終點 = min(視窗結尾, 現在)**。資料的尾端若小於現在，就在資料尾端停。
2. **尾端停住**：抵達終點時設 `playing=false` 並停在終點；若目前時間已在終點之後（使用者拖進未來），原地停住，不往回跳。回放預設不 loop，只有展示用嵌入頁明確設定區間時才 loop。
3. **單幀 dt 夾上限**（例如 0.25 秒）：分頁切走再切回時，寧可慢一點也不要暴衝。
4. **游標落在無資料區**時顯示「尚無資料」（見 [03-08](03-08-timeline-gaps-and-data-coverage.md)），不外推、不補值。
5. **記住使用者主動暫停**：資料重載完成後的自動播放，若使用者暫停過就不要重新啟動；只有使用者按播放才清除這個旗標。
6. 把「推進一幀」寫成純函式 `advance(current, elapsed, speed, end) → { time, reachedEnd }`，邊界情況（已超過終點、剛好抵達）都能寫單元測試。

```ts
function advance(cur: number, dt: number, speed: number, end: number) {
  if (cur >= end) return { time: cur, reachedEnd: true };   // 已在尾端之後：原地停
  const next = cur + Math.min(dt, 0.25) * speed;             // dt 夾上限
  return next >= end ? { time: end, reachedEnd: true } : { time: next, reachedEnd: false };
}
const playbackEnd = (windowEnd: number, nowSec: number) => Math.min(windowEnd, nowSec);
```

## 怎麼偵測
- 通用：把時間軸拖到未來再按播放；播到最後看是否回跳；切走分頁 10 秒再切回，看第一幀的跳躍量。
- 搜尋：
  - 終點：`windowEnd|rangeEnd|endTime` 直接被當播放終點，附近沒有 `Date\.now|now\(\)` 的 `Math\.min`（any）。
  - dt：RAF 回呼內 `(now - last) / 1000` 之後直接乘倍速，沒有 `Math\.min`／clamp（any）。
  - 回跳：到達終點的分支內有 `setTime\(.*start|currentTime = .*start`（any）。

## 出處
- 一般動畫迴圈做法（dt clamp，見遊戲迴圈文獻）。相關卡：[03-08](03-08-timeline-gaps-and-data-coverage.md)、[09-07](../09-design-system/09-07-loading-data-time-and-stale.md)（介面面向的「顯示資料時間」）。
- 實例：[mini-taiwan-pulse 時間軸 hook](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/hooks/useTimeline.ts)（終點取較早者、使用者暫停旗標）、[嵌入頁回放時鐘](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/embed/replayClock.ts)（dt 上限 0.25 秒，註解說明約 960x 倍速下的暴衝情境）。
