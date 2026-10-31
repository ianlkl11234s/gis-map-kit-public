---
id: 12-07
title: 「最後已知位置」變幽靈點：停泊船、失聯衛星與 UPSERT-only 的 current 表
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Implemented
stacks: [any]
tags: [ghost, stale, current table, UPSERT, 停泊, SOG, 港口, last known position, 即時位置]
---

## 原則
「最後已知位置」一律帶回報時間：current 表要定期清除過期列，畫面依新舊淡化或不畫，停泊判定要切段，不要讓舊點冒充現況。

## 症狀
- 船停在港內好幾天，地圖上始終有一個看起來「在線」的點；回放時一整串點疊在碼頭。
- 即時圖層的船、車、衛星數量只增不減，跟實際活躍數對不上。
- 已經失聯或任務結束的物件還顯示在上次的位置。
- 地圖上的誤導：使用者把「三天前最後一次出現在這裡」讀成「現在在這裡」，港口或海域看起來比實際擁擠；監看用途會誤報「某船仍在某海域徘徊」。

## 原因
1. 「current」表只做 UPSERT（有新資料才更新），物件不再廣播時就停在最後一筆，永遠不被移除。
2. 停泊的船持續送低速或靜止的點，若不判定為停泊，軌跡會在碼頭累積成一團，且被當成「活躍」。
3. 畫面上沒有區分「最後回報時間」的新舊，所有點用同一種樣式。

## 解法
1. current 表每次寫入後依 `collected_at` 刪除超過保留時間的列（prune），或查詢時加時間條件。
2. 停泊判定：在港口圍欄內（例如半徑 1.5 km、大港 3 km）且 SOG < 0.5 節持續超過約 1 小時，就切段並只保留進出港的邊界點；落在陸地上的點另外排除。
3. 視覺上分層：最後回報超過門檻（例如 3 小時）的點淡化並在 popup 寫「最後回報 X 小時前」；更久的直接不畫。淡化門檻要比軌跡斷線門檻寬，否則整層都會是淡的（見 [12-04](12-04-track-gap-segmentation.md)）。
4. 衛星這類有明確失效時間的物件，用資料本身的 epoch／decay 欄位判斷（見 [12-11](12-11-tle-staleness-sgp4.md)）。

## 怎麼偵測
- 通用：比較「current 表筆數」與「最近 N 分鐘有回報的物件數」；差距持續擴大就是累積幽靈資料。
- 通用：在港口放大看有沒有大團重疊點，或 popup 的最後回報時間是否遠早於現在。
- 搜尋（只 upsert 沒刪除）：`rg -n -i 'on conflict.*do update|upsert' ` 再對照同一張表有無 `delete .* where .*(collected_at|updated_at) <`。
- 搜尋（前端有沒有用回報時間）：`rg -n -i 'stale|lastSeen|last_seen|ageSec|STALE'` 在即時位置圖層。

## 出處
- 一般即時位置資料做法。相關卡：[12-04](12-04-track-gap-segmentation.md)、[12-11](12-11-tle-staleness-sgp4.md)。
- 實例：[船舶監看的淡化（3 小時）與斷線（1 小時）門檻，兩者用途不同](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/vesselWatchLoader.ts)；[衛星 current 表加 prune 設定的連帶變更](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/.claude/pitfalls/2026-04-14-celestrak-ip-blocked.md)（否則 UPSERT 會累積過期資料）。

