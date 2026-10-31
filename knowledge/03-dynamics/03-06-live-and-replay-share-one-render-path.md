---
id: 03-06
title: 即時與回放共用同一條渲染路徑：只換「誰在寫時間」，並依資料的時間型態決定怎麼顯示
topic: 03-dynamics
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [即時, live, 回放, replay, 時間型態, track, snapshot, cyclic, event, static, 模式切換]
---

## 原則
渲染層只讀一個時間，不知道現在是即時還是回放；模式只決定誰寫時間。顯示規則依資料的時間型態（軌跡、快照、週期、事件、靜態）統一登記，不散在各圖層。

## 症狀
- 即時與回放各寫一份繪圖程式，改一邊忘了另一邊，兩邊畫面逐漸不一致。
- 切到即時模式後，沒有即時來源的圖層仍在畫舊資料，使用者以為是現在的。
- 在即時與歷史大模式間切換後，時間軸回不到原本的位置。

## 原因
即時只是「播放時間 = 現在」的特例。若繪圖程式接收的是「模式」而不是「時間」，就必須為每個模式寫分支。

## 解法
1. **渲染層只讀一個時間**（見 [03-02](03-02-time-in-reactive-state-rerender-storm.md) 的 `getTime()`）。
2. **模式只決定誰寫時間：**
   - 回放：RAF 依倍速推進，寫入時間 store。
   - 即時：每秒（對齊整秒）寫一次 `Date.now()`。即時資料本身是秒到分鐘級更新，高頻寫入只會讓所有圖層白白重算。
   - 即時時暫停播放，隱藏回放用的滑桿或改成「回看」。
3. **依資料的時間型態決定顯示規則**，登記在資料來源描述裡：

| 型態 | 例子 | 顯示規則 |
|---|---|---|
| track（軌跡） | 船、飛機 | 只在有資料的時段顯示，其他時間消失 |
| snapshot（快照） | 站點即時量、壅塞 | 顯示最接近目前時間的快照 |
| cyclic（週期） | 時刻表 | 只取「時刻」部分循環 |
| event（事件） | 新聞、警報 | 顯示目前時間往前 N 小時內的事件 |
| static（靜態） | 站、路網 | 永遠顯示 |

4. **即時模式下沒有即時來源的 track 類，就隱藏或灰化並標示**，不要拿舊資料冒充現在（見 [04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)）。
5. **大模式切換要能還原**：切換前存下時間軸快照（選定日期、視窗、目前時間），切回時用「跳到精確時刻」的函式還原，並同時還原視窗日期鍵，否則預載會對不上。
6. 進入即時模式時，選定日期跟著「今天」；離開時不要把「今天」寫成回放的起點，除非使用者要。

## 怎麼偵測
- 通用：即時模式與回放模式下同一時刻（把回放拖到「現在」）畫面應該相同；不同就有分支重複。
- 搜尋：
  - 渲染程式內以模式分支：`if \(.*(mode|isLive|isReplay).*\)` 出現在繪圖或圖層更新函式（any）。
  - 即時模式用高頻寫入：`setInterval\([^,]+, ?(16|33|50|100)\)` 搭配寫時間（any）。
  - 沒有型態描述：資料來源登記沒有 `timeType|temporalKind` 之類欄位，各圖層自己判斷（any）。

## 出處
- 一般時間序列視覺化慣例（live／replay 共用資料流）。相關卡：[03-02](03-02-time-in-reactive-state-rerender-storm.md)、[03-05](03-05-time-window-and-prefetch.md)、[03-07](03-07-playhead-bounds-no-future.md)、[04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)。
- 實例：[mini-taiwan-pulse 時間軸 hook](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/hooks/useTimeline.ts)（即時 1 Hz 對齊整秒寫入、回放 RAF 寫入、模式切換快照還原）、[時間軸架構文件](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/TIMELINE_ARCHITECTURE.md)（五種時間型態的設計稿；實際只有部分來源註冊型態，其餘圖層各自判斷）。
