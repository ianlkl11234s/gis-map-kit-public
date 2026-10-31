---
id: 00-08
title: Question → Evidence → Metric → Dataset 迴圈，以及「資料還不是證據」
topic: 00-system-thinking
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [研究問題, evidence, metric, dataset, question-first, data-first, exploration-first, 鄰近, 暴露, 因果, 水源, proxy]
---

## 原則
結論的強度不得超過證據：依 Question → Evidence → Metric → Dataset 迴圈推進，並區分鄰近、連通、暴露、污染與因果，每一階都要有新的證據。

## 症狀
把資料疊上地圖就宣稱「污染已影響取水口」；用一個數字（工廠數）當作風險；探索時看到的 pattern 直接寫成結論；或反過來，堅持必須一開始就有完美問題才能看資料。

## 原因
混淆了四個層次，也混淆了幾種遞進的強度。

| 層次 | 在問什麼 | 水源例（示範） |
|---|---|---|
| Question | 想回答什麼？ | 哪些取水口的上游值得優先調查？ |
| Evidence | 哪些事實支持或否定？ | 上游可連通污染源、申報排放、水質測站變化 |
| Metric | 如何量測？ | 上游潛在污染源數、申報負荷、水質時序、網路旅行時間 |
| Dataset | 用哪些原始紀錄？ | 保護區圖、排放許可申報、水質監測、取水口與河網 |

Evidence 不一定是數值（文獻、現勘、制度也算），Metric 也不自動等於 Evidence。

## 解法
兩個入口，同一個迴圈：
- Question-first：已知問題 → Evidence → Metric → Dataset。
- Exploration-first（data-first）：有大方向 → 看資料 → 發現 pattern → 細化 Question。
- 迴圈：Question ↔ Evidence ↔ Metric ↔ Dataset ↔ Visualization ↔ Refined Question。資料先行也要回到一個方向，持續更新提問；簡單的描述性問題是有效起點。

兩條不能跨越的階梯（每一階都需要新的證據）：
- Nearby ≠ Connected ≠ Causal：直線近、水文或路網上真的連通、有時序與污染物證據支持影響，是三個不同強度。
- Presence ≠ Exposure ≠ Contamination ≠ Causation：有污染源，不等於暴露；暴露不等於已發生污染；已發生也不等於由該來源造成。

配套要求：
- 標明每項 Metric 是 observed、reported（申報值，不等於獨立實測）、proxy、estimated 或 unknown。
- 污染源數量只是「潛在壓力」的粗略 proxy，不代表水質較差。
- 資料日期、空間尺度、更新頻率要對齊，不把月採樣說成即時。
- 探索分析不等於治理級風險判定。非預期結果是問題，不是立即的發現：先檢查資料品質、join、時間差、定義與尺度，再解釋。
- 不能只憑標題認定資料可用；查不到的欄位或資料集標「待確認」。

## 怎麼偵測
檢查對象：圖台說明、分析 README、system map JSON、AI 產出的研究計畫。
- 通用：結論句比證據強一階以上（只有 buffer 卻說影響）；沒有說明 Metric 是申報值、proxy 還是實測；探索 pattern 寫成確定因果。
- 搜尋（文字）：`影響了|污染了|造成.{0,8}(污染|淹水)` 旁沒有 evidence 欄位；`1\s*(km|公里)內.{0,10}(污染|風險)` 只有半徑沒有上下游判斷。
- 搜尋（JSON）：edge 的 `evidence_status` 為 observed，但來源類型是申報資料或僅空間疊合；`dataset_ids` 為空的 observed 邊。
- 搜尋（AI 輸出）：資料集、欄位或 URL 沒有「待確認」或查核標記。

## 出處
- US EPA, Source Water Assessments（界定保護範圍、盤點污染源、評估 susceptibility；可作為成熟框架參考，不等於已完成風險評估）。
- Meadows (2008) Thinking in Systems。
- 本卡的迴圈與階梯是教學整理。
- 相關卡：[00-02](00-02-start-from-phenomenon-why-and-so-what.md)（先從現象往前與往後拆出待驗證假說，再進本卡找證據）、[00-11](00-11-visualization-as-thinking-explore-explain.md)（視覺化即思考）、[00-12](00-12-pattern-to-insight-confounding-claim-check.md)（從 pattern 到 insight）。

