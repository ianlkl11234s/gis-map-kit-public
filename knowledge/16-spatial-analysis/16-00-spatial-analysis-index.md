---
id: 16-00
title: 空間分析總表：想回答什麼問題 → 方法與口徑 → 卡片
topic: 16-spatial-analysis
kind: catalog
scope: public
evidence: Evaluated
stacks: [any]
tags: [空間分析, 總表, 熱點, 區位商數, MAUP, 可達性, 地理編碼, 件數口徑, 偏態, 幾何健檢]
---

## 原則
空間分析先定「想回答的問題」，再選方法，並把分析單元、分母、類別定義與檢定寫進回答；這些都是口徑，不是細節。算之前先做幾何健檢（[16-08](16-08-geometry-quality-flags-before-analysis.md)），算完對照資料的限制（件數口徑、極端值）再下結論。

## 對照表

| 想回答的問題 | 方法或要先確認的口徑 | 卡片 | 一句重點 |
|---|---|---|---|
| 哪裡是熱點、是否群聚、點是不是擠在一起 | 全域 Moran、Gi*、LISA、最近鄰 | [16-01](16-01-hotspot-clustering-methods.md) | 各自回答不同問題；寫明單元、鄰接與檢定口徑；多單元同時檢定做 FDR 校正；做成確定性工具 |
| 某地某類比別處特別多嗎、占比多少 | 區位商數 LQ 與比例指標 | [16-02](16-02-location-quotient-and-ratio-metrics.md) | 分母與類別定義是口徑，預設寫進工具；樣本小於門檻標「樣本太少」、不給值；排名附件數 |
| 換個尺度（村里、鄉鎮、網格）還成立嗎 | 跨尺度相關（MAUP） | [16-03](16-03-cross-scale-maup.md) | 同一組相關至少兩個尺度各算一次，並列單元數與顯著性；主係數用 Spearman；相關不當因果 |
| 到最近服務多遠、服務範圍有多大、哪裡是服務沙漠 | 路網可達性與等時圈 | [16-04](16-04-accessibility-isochrones.md) | 用路網距離不用直線 buffer；全部站一次 dissolve、環差分級；未連通、缺座標分開表示、不填 0 |
| 地址變座標，精度夠不夠 | 地理編碼 | [16-05](16-05-geocoding-precision-and-routing.md) | 存來源與精度欄位；分析預設排除粗略點；依量級選服務；送第三方前先取得同意 |
| 件數多代表發生多嗎，趨勢是上升嗎 | 通報與登錄口徑 | [16-06](16-06-reported-counts-not-occurrence.md) | 件數只代表被記錄的件數；解讀差異先看通報管道，解讀趨勢先看登錄完整度；先確定一列代表什麼 |
| 金額、面積、長度的總和與平均可信嗎 | 偏態與極端值 | [16-07](16-07-skewed-sums-extreme-values.md) | 先列前幾大值與占總和比例；總和搭中位數或件數；轉換方式先講明；回答點名極端值 |
| 分析前資料幾何可用嗎 | 逐列品質旗標、落區對照 | [16-08](16-08-geometry-quality-flags-before-analysis.md) | 距離、環域、落區、熱點前先標旗標；點落區對照宣稱的縣市；缺幾何的件數要回報；依縣市計數用縣市欄 |

## 相關主題
- 比例指標的分母與重複計算：[06-07](../06-data-formats/06-07-ratio-denominator-and-double-counting.md)；標示推估與模型值：[06-08](../06-data-formats/06-08-label-estimates-and-models.md)。
- 給 AI agent 的分析工具如何設計、口徑如何傳遞：[17-04](../17-ai-agent/17-04-agent-tool-design-semantics.md)。
- 資料新鮮度與零值、缺值契約：[06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)。
- 圖上未涵蓋與空格的畫法：[14-05](../14-scale-density/14-05-honest-aggregation.md)。

## 出處
各項依據見對應卡片。
