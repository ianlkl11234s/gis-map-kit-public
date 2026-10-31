---
id: 12-11
title: 衛星位置用過期 TLE 外推會失控；新鮮度要看 TLE epoch，不是抓取時間
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Implemented
stacks: [any]
tags: [satellite, TLE, SGP4, epoch, decay, 衛星, 軌道, ECI, GMST, satellite.js]
---

## 原則
用 TLE 自己的 epoch 判斷新鮮度，超過門檻（常用 30 天）就不畫或標過期，並對傳播結果做健全性檢查；不要拿抓取時間當資料時間。

## 症狀
- 少數衛星出現在幾萬公里外，或位置是 NaN 讓整批渲染壞掉。
- 已墜毀或失聯的衛星還在軌道上轉。
- 面板顯示「資料更新於 5 分鐘前」，但部分衛星的軌道根數其實是一個月前的。
- 分批計算位置時，同一畫面上不同批衛星的時間不一致，相鄰衛星位置錯開。
- 地圖上的誤導：過期 TLE 外推的位置看起來精確，實際上可能偏差數百到上千公里；把「抓取成功」當成「位置新鮮」會讓人相信一顆已不存在的衛星正經過頭頂。

## 原因
1. TLE 是某個 epoch 的軌道根數，SGP4 從 epoch 外推；離 epoch 越久誤差越大，低軌受大氣阻力影響尤其快。已 decay 或失追的物件不會再有新 TLE，但舊 TLE 仍可被外推。
2. 「新鮮度」常用抓取時間代表，但同一次抓取裡每顆衛星的 epoch 不同。
3. 為了效能分批傳播時，每批用的時間點不同，再轉成地理座標時又共用同一個 GMST，造成錯位。

## 解法
1. 解析 TLE 第一行的 epoch（YYDDD.DDDDDDDD；YY < 57 屬 2000 年代），超過門檻（常用 30 天）就不畫或標「過期」。
2. 優先使用附 decay 日期與物件類型（衛星本體、火箭體、碎片）的來源，直接排除已 decay 物件。
3. 對傳播結果做健全性檢查：高度 > 約 50,000 km、< −200 km、速度 > 100 km/s 或非有限數就丟。
4. 分批計算時，用每批的 ECI 速度外插到同一個模擬時間，再用該時間的 GMST 轉換。
5. 面板的「更新時間」顯示最新（或中位數）TLE epoch，而不是抓取時間。

## 怎麼偵測
- 通用：畫「各衛星 TLE 年齡」分布；有長尾而程式沒有門檻就是問題。檢查傳播結果有沒有 NaN 或極端高度。
- 搜尋（有沒有 epoch 門檻）：`rg -n -i 'epoch|maxAgeDays|isTleActive|decay'` 在衛星 loader；`rg -n 'twoline2satrec|propagate\('` 有命中卻沒有 epoch 檢查就是疑點。
- 搜尋（新鮮度來源）：`rg -n -i 'updated|fetched_at|collected_at' ` 在衛星面板，確認不是拿抓取時間當資料時間。

## 出處
- Vallado et al., "Revisiting Spacetrack Report #3"（SGP4 標準實作）。
- CelesTrak／Space-Track GP 資料格式說明（TLE epoch 欄位、DECAY_DATE）。
- 相關卡：[12-07](12-07-ghost-last-known-position.md)、[12-12](12-12-upstream-blocking-rate-limits.md)。
- 實例：[解析 TLE epoch 與過期判斷](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/satelliteSGP4.ts)；[面板新鮮度改為最新 TLE epoch](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/71e3d5d2a4dea580d8438067670d15dbdd374f6a)、[後續調整](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/f052b8e3cd6558830413d7bd32a644880e60c213)。

