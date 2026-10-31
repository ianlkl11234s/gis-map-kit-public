---
id: 12-13
title: 颱風路徑多來源、多版本、同時間戳交錯，畫出來回穿越的軌跡
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [typhoon, 颱風, JMA, JTWC, CWA, NCDR, forecast track, advisory, 預報路徑, 風圈, storm_key]
---

## 原則
颱風路徑依「颱風 × 來源」分開畫，每個來源只取最新一版，不跨來源或跨版本連線與平均；抓取失敗要與「目前沒有颱風」分開記錄。

## 症狀
- 一個颱風的路徑在兩個相距上千公里的地點之間來回拉線，3 小時「移動」2,000 多公里。
- 預報路徑被平均成一條不屬於任何機構的線。
- 只有一個颱風時解析器報錯，兩個以上反而正常；颱風風圈不對稱時整輪寫入失敗。
- 抓取失敗被記成「目前沒有颱風」，圖層靜默清空。
- 地圖上的誤導：穿越線看起來像颱風急轉或打轉；平均後的預報路徑會被讀成「官方預報」，實際上沒有任何機構這樣預報。

## 原因
1. 同一個來源的不同段落（熱帶性低氣壓、颱風、分析）可能用同一個時間戳，排序後點位交錯。
2. 多家機構（JMA、JTWC、CWA 等）與多個發布版本對同一 valid time 各有預報；混在一起後按時間連線或取平均，都會產生虛構路徑。
3. 上游 JSON 結構不穩定：只有一個颱風時陣列變成單一物件；非對稱風圈時欄位從物件變字串；跨月時日期時間群組（DTG）需要修正。
4. 不同機構的最大風速平均時間不同（1 分鐘 vs 10 分鐘），直接比較強度會差約一成多。
5. 錯誤處理把「抓取失敗」與「沒有颱風」寫成同一個結果。

## 解法
1. 路徑依 `storm × source` 分開畫；每個來源只取最新一版（最大 advisory 編號），各版帶 `[valid_from, valid_until)`，不要跨版平均。
2. 跨來源配對同一颱風時，用「年份＋英文名」之類的穩定鍵，不要依賴某一家才有的國際編號。
3. 相鄰點距離超過「最快移速（約 120 km/h）× 時間差＋緩衝」就斷開線段；同時刻多點先去重。
4. 解析時同時接受陣列與單一物件、字串與物件；附屬欄位（風圈）解析失敗只把該欄設 NULL，主路徑照寫。
5. 抓取失敗要寫成錯誤狀態，與「確認目前無颱風」分開；上游只保留最新一報的來源，要自己存檔，漏抓無法回補。
6. 圖例註明風速的平均時間與單位（kt 或 m/s）。

## 怎麼偵測
- 通用：對每條路徑算相鄰點的隱含速度，> 150 km/h 的段落就是交錯或配對錯；單一颱風、非對稱風圈要各準備一份測試 fixture。
- 搜尋（平均預報）：`rg -n -i 'avg|mean|centroid' ` 在颱風 loader，確認不是跨來源或跨版本平均。
- 搜尋（結構假設）：`rg -n -i "TropicalCyclone|\['area'\]|\.area\b" `，看是否處理 dict／list、str／object 兩種型別。
- 搜尋（失敗當無資料）：`rg -n -i 'except.*:\s*(return \[\]|pass)'` 在颱風 collector。

## 出處
- JTWC 與 JMA 最大風速定義（1-min vs 10-min sustained wind，兩者差約 12–15%）。
- 實例：[路徑 loader：最快移速加緩衝斷線、同時刻去重](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/typhoonTracksLoader.ts)；[每個 storm×source 只留最新 advisory，各版有效區間](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/typhoon-cwa-ncdr/README.md)；[collector 修正：抓取錯誤被當成無颱風、單一颱風是 dict 而改用 storm_key](https://github.com/ianlkl11234s/gis-data-collectors/commit/9d2e78e691020cc4ed0b89606ce8fb7d96b81be5)。
