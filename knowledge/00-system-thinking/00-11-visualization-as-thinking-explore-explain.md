---
id: 00-11
title: 視覺化即思考：探索和說明分開、先看全貌、數字要有比較基準、空白也是問題
topic: 00-system-thinking
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [視覺化即思考, Exploratory, Explanatory, Overview first, Shneiderman, EDA, 八項觀察, Count ≠ Risk, 比較基準, 分母, No data ≠ No service, 資料空白, data artifact]
---

## 原則
探索與說明分開做，先看全貌再看細節；數字要附比較基準，資料空白先分成資料缺口與服務缺口，不直接下結論。

## 症狀
- 圖層一放上去就盯著熱區下結論，沒看全台分布，也沒點開單筆確認資料本身。
- 給別人看的成果圖還是探索時那張十幾個圖層疊滿的畫面；或反過來，探索時就花時間修飾版面。
- 「A 區有 500 件事故」直接寫成「A 區最危險」。
- 地圖上某區沒有醫院點位，就寫成「當地沒有醫療服務」。

## 原因
- 探索（Exploratory）與說明（Explanatory）的目的不同：前者要產生問題，後者要讓讀者看懂一個有證據的發現。混在一起，探索畫面拿去說明會讓人看不懂，說明標準拿來探索會拖慢試錯。
- 沒有先看全貌就進細節，容易把局部特例當成整體現象。
- 數量（count）只描述規模；要談異常或風險，需要時間長度、暴露量（人流、車流）、同類地區或適當空間尺度當比較基準。
- 資料空白可能是現實沒有，也可能是漏登、收錄範圍不同或資料過期。

## 解法
1. **探索與說明分開做**：
   - 探索：多圖層、多篩選、不修飾，目標是快速換尺度、加資料、試假設，輸出更多問題。資料的基本檢查仍要做。
   - 說明：只留支撐一個發現所需的圖層，簡化底圖、加註解、寫出限制與下一步。說明不一定要有因果結論，誠實傳達描述性發現與不確定性也可以。
   - 說明時發現證據不夠，就回去探索。
2. **Overview → Zoom & Filter → Details on Demand**：先看全貌（分布在哪），再縮範圍（哪個區域、類別、時間值得看），最後點單筆看屬性、來源與時間。這是互動視覺化的設計原則，不是所有分析都只能照這個順序。
3. **用一張觀察清單掃圖**（教學整理的八項，不是固定分類）：分布、集中、空白、離群、沿線或邊界排列、組成差異、換分母或尺度後是否仍成立、隨時間是否改變。每看到一個 pattern 都問：這是現實世界的現象，還是資料蒐集、分類或更新造成的？
4. **Count ≠ Risk**：數字旁邊補比較基準——時間（一年還一個月）、暴露量、同類地區、空間尺度。沒有可靠分母時不要宣稱算得出率（分母細節見 [06-07](../06-data-formats/06-07-ratio-denominator-and-double-counting.md)）。行政區聚合會遮蔽路口尺度的差異。
5. **No data ≠ No service**：空白先分成 data gap（漏登、範圍、過期）與 service gap（真的沒有或到不了）。驗證順序：第二來源 → 抽樣核對 → 結合人口與可達性。商業地圖可當交叉檢查，不是官方真值。
6. 兩個不同主題的圖層疊在一起出現 pattern 時，先記成「觀察」，下一步是什麼要依 [00-12](00-12-pattern-to-insight-confounding-claim-check.md) 的分層處理，不要直接宣布原因。

## 怎麼偵測
檢查對象：圖台說明、分析報告、對外貼文與截圖。
- 通用：對外圖片疊了五層以上卻只講一個結論；報告第一張圖就是單一城市的熱區；排名只有件數沒有分母或期間；文字出現「沒有」「缺乏」但沒說是哪份資料的涵蓋範圍。
- 搜尋（文字）：`最多|最危險|最高` 附近只有件數、沒有 `每|率|人口|期間`；`沒有.{0,6}(醫院|設施|服務)` 沒有交代資料來源範圍。

## 出處
- Shneiderman, B. (1996). The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations. IEEE VL. https://doi.org/10.1109/VL.1996.545307
- NIST/SEMATECH e-Handbook of Statistical Methods, EDA 章節（找結構、離群、檢查假設）。
- 相關卡：[00-08](00-08-question-evidence-metric-dataset-loop.md)（資料還不是證據）、[00-12](00-12-pattern-to-insight-confounding-claim-check.md)（從 pattern 到 insight）、[06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)（零、null、過期的資料契約）、[06-07](../06-data-formats/06-07-ratio-denominator-and-double-counting.md)（分母）。

