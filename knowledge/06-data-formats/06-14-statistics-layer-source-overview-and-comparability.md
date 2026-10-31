---
id: 06-14
title: 統計圖層的兩個交付門檻：資料來源總覽要一起更新，切換指標或期別只能配對可比的選項
topic: 06-data-formats
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [統計圖層, choropleth, 資料來源總覽, 來源卡, 可比性, 跨期比較, selector, 期別, 口徑, 邊界版本, 衍生指標, 圖層登記表, 增量發布]
---

## 原則
新增或改動統計圖層時，同一個 PR 更新資料來源總覽；切換指標或口徑時只配對同期別、同維度的選項，找不到就顯示「不可用」，不靜默換年份。

## 症狀
- 新增或合併了統計圖層，側欄看得到，但「資料來源」頁找不到它，或只找得到合併後的群組名、找不到裡面的原始指標。
- 從「人數」切到「每萬人口」時，期別悄悄從 2024 跳成 2022，畫面看起來在比較，其實不同年。
- 兩個名稱相近的指標被當成可互換（例如「登錄人次」與「不重複人數」），或縣市值被複製到底下每個鄉鎮。
- 增量發布新指標後，舊的指標從線上消失。

## 原因
- 來源資訊常被當成附屬文件，只在側欄補一個名稱；整合或改名時，原始指標的出處就斷掉了。
- 統計值的身分不只是「指標名稱」，而是來源資料集、指標、發布期別、維度（類別、季度、母體）的完整組合。只比名稱，就會配錯。
- 參考邊界的版本不一定等於統計當年的原生界線。
- 用一份只含新指標的小清單覆蓋線上的全量清單，舊的就不見了。

## 解法
1. **來源總覽同步**：新增、改名、合併圖層，或增加指標、口徑選項時，同一個 PR 更新資料來源總覽；總覽涵蓋原始與衍生選項，搜尋要找得到群組裡的每個選項。
2. **來源卡內容**：中文名稱、原始或衍生、來源資料集與指標、觀察期間、單位、地理層級、來源連結，以及衍生方法與限制。機關、網址、授權不明時寫「未知」，不要捏造；CDN 只是傳輸位置，不是資料生產機關，平台自己的「已驗證」也不是官方認證。
3. **selector 與配對**：每個值用完整 selector（資料集＋指標＋期別＋維度）定位，不用名稱比對；切換口徑時只配對同期別、同共用維度的選項，沒有相同期別就顯示「不可用」並說明。
4. **比率與層級**：人均、密度、占比要寫明分子、分母、倍率、年份與母體（分母細節見 [06-07](06-07-ratio-denominator-and-double-counting.md)）；縣市與鄉鎮切換只用該層級的來源或有證據的彙總，不把上層值複製到下層，也不用「部分已知縣市的合計」冒充全國分母；記錄參考邊界的版本與定義。
5. **分級與缺值**：分級門檻屬於比較契約，不隨當次資料重算（見 [05-09](../05-color/05-09-fixed-breaks-across-time.md)）；缺值、遮蔽、部分涵蓋要原樣保留（見 [05-04](../05-color/05-04-null-is-not-zero-color.md)、[06-06](06-06-zero-null-stale-data-contract.md)）。
6. **發布**：統計值走不可變的檔案＋指標檔（manifest）＋目前版本指標；SHA、大小、selector 驗證失敗就報錯，不退回其他來源讀值。增量資料要合進全量 manifest、保留既有 selector，不可用交付包的小 manifest 覆蓋全量。

## 怎麼偵測
- 通用：在資料來源頁搜尋剛上線的指標名稱找不到；切換口徑前後，說明欄的期別不同卻沒有提示；同一指標縣市與鄉鎮的值完全相同。
- 搜尋：新增統計 recipe／指標的 PR 沒有同時改動來源總覽相關檔（any，看 PR diff）。
- 搜尋：切換指標的程式在找不到同期別時 fallback 到 `latest|periods\[0\]|max\(` 這類任意年份（any）。
- 搜尋：發布腳本直接 `put` 或覆寫 `current|manifest` 檔，沒有先讀線上全量合併（any）。

## 出處
- ColorBrewer、Matplotlib colormap 文件（數值色階方法）。
- 相關卡：[05-04](../05-color/05-04-null-is-not-zero-color.md)、[05-09](../05-color/05-09-fixed-breaks-across-time.md)、[06-06](06-06-zero-null-stale-data-contract.md)、[06-07](06-07-ratio-denominator-and-double-counting.md)、[10-02](../10-ops/10-02-data-update-vs-redeploy-and-cache.md)。
- 實例：[mini-taiwan-pulse 統計圖層規則（資料意義先於外觀、口徑切換維持可配對期別、資料來源總覽為必要交付、不可變 artifact 加指標檔）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/statistics-layer-guidelines.md)；[統計可比性實作紀錄（增量發布保留既有 selector、只配對同期別與共用維度）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/statistics-comparability/README.md)。
