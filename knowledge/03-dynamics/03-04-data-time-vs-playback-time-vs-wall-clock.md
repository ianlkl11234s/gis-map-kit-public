---
id: 03-04
title: 三種時間不要混：資料時間、播放時間、掛鐘時間；內部一律 UTC epoch
topic: 03-dynamics
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [時區, UTC, epoch, 掛鐘, wall clock, 資料時間, 抓取時間, 新鮮度, 日期鍵, 時間戳]
---

## 原則
播放時間、資料時間、掛鐘時間分開存放、分開顯示；內部一律用 UTC unix epoch，只在顯示層轉當地時區。「更新於」顯示資料本身的時間，不顯示抓取時間。

## 症狀
- 回放歷史資料時，畫面角落的「3 分鐘前」「現在 14:32」跟著回放跳，不是真實時間。
- 「更新於」顯示的是瀏覽器收到資料的時間，來源其實已停更好幾天，畫面看起來卻很新鮮。
- 圖層整批資料偏移 8 小時（時間戳沒帶時區，被當成 UTC 存），或切日時日期差一天。

## 原因
一個畫面裡同時有三種時間，卻共用一個變數：

| 時間 | 是什麼 | 誰改變它 |
|---|---|---|
| **播放時間** | 時間軸游標，回放時是歷史時刻、即時模式等於現在 | 播放控制器 |
| **資料時間** | 這筆資料本身代表的時刻（觀測、發布、報表日） | 資料來源 |
| **掛鐘時間** | 使用者此刻真實的時間 | 時鐘 |

另外，時間戳的格式與時區若沒有約定，資料管線與前端各自解讀。

## 解法
1. **播放時間**放在時間 store（見 [03-02](03-02-time-in-reactive-state-rerender-storm.md)）；**掛鐘**另開一個獨立的小 store 或訂閱，專供「現在」「N 分鐘前」這類 UI。掛鐘訂閱共用同一個計時器（依毫秒分桶），訂閱數歸零自動清掉；不要在元件裡自己 `setInterval`。
2. **資料時間**由資料帶進來，UI 顯示它而不是抓取時間；拿不到就顯示「無資料時間」，不要假裝即時。新鮮度依來源的預期更新週期判定（見 [09-07](../09-design-system/09-07-loading-data-time-and-stale.md)）。
3. **內部一律真實 UTC unix epoch**（秒或毫秒，全專案統一一種），資料庫與 API 也輸出 epoch；只有顯示層轉成當地時區。
4. **日期鍵**（`YYYY-MM-DD`）用於分日載入與快取時，明確指定時區計算，例如 `toLocaleDateString("sv-SE", { timeZone: "Asia/Taipei" })`；一天的起點是「當地午夜對應的 UTC 秒」，不是 `Date.UTC(y, m, d)`。
5. **來源沒帶時區的時間戳**：進管線時就判斷並轉成 UTC，驗收時抽 1–2 筆與來源網站對照；不要留到前端猜。
6. 時間軸上顯示時區（例如「UTC+8」），跨時區使用者才不會誤讀。

## 怎麼偵測
- 通用：回放時畫面上的「現在」跟著動；船／車資料整批比預期早或晚 N 小時出現；跨午夜時圖層短暫空白或日期重複。
- 搜尋：
  - 掛鐘誤用：UI 元件內 `Date\.now\(\)` 搭配 `setInterval` 顯示「前」或時鐘（any）。
  - 時區：`new Date\("\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(:\d{2})?"\)`（沒有 Z／偏移，依瀏覽器所在時區解讀）、`Date\.UTC\(` 直接拿來當當地日起點、`toISOString\(\)\.slice\(0, ?10\)` 當當地日期（any）。
  - 更新時間來源：`updatedAt|lastUpdated` 被賦值為 `Date\.now\(\)` 或 `new Date\(\)` 而非資料欄位（any）。

## 出處
- 一般時間處理慣例（儲存用 UTC、顯示轉當地）。相關卡：[01-13](../01-taiwan-apis/01-13-time-zone-and-update-time.md)、[03-02](03-02-time-in-reactive-state-rerender-storm.md)、[09-07](../09-design-system/09-07-loading-data-time-and-stale.md)、[12-01](../12-domain-pitfalls/12-01-timestamp-timezone-offset.md)（船舶時間戳 +8 小時事件）。
- 實例：[mini-taiwan-pulse 時間 store](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/state/timeStore.ts)（掛鐘與資料時間軸分離，註解明寫「不是資料時間軸」）。

