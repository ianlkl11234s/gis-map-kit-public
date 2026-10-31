---
id: 00-10
title: System Map 是問題產生器：每個節點長出待驗證的問題
topic: 00-system-thinking
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [system map, 待驗證問題, evidence questions, 資料蒐集藍圖, critical uncertainty]
---

## 原則
畫完 System Map 後，為每個重要節點與每條待驗證的邊寫出具體的待驗證問題與所需的 Evidence、Metric、Dataset，再決定要加什麼資料。

## 症狀
畫完圖就停在「畫好看的關係圖」，沒有下一步；或下一步變成「還可以加什麼圖層」，資料越加越多，卻說不出各自要驗證哪條關係。

## 原因
把 System Map 當成成果而不是工作藍圖。更好的問法不是「還能加什麼」，而是「這個系統怎麼運作」。

## 解法
1. 對每個重要節點與每條 hypothesized／unknown 邊，寫一個待驗證的問題。例：排水容量？淹水深度隨時間？醫院旅行時間改變多少？
2. 每個問題標：需要什麼 Evidence → 要用什麼 Metric → 可能的 Dataset（見 [00-08](00-08-question-evidence-metric-dataset-loop.md)）；找不到資料就記入 critical uncertainty（見 [00-07](00-07-system-boundary-five-criteria.md)）。
3. 問題依「可能改變結論的程度 × 驗證可行性」排序，先做成本最低的檢查。
4. 在 inspector 或匯出文件中保留「待驗證問題」欄位，驗證後回頭更新邊的 evidence_status。

次序是：先知道想驗證哪些關係，再找能支持或反駁的 Evidence，最後才找 Dataset。

## 怎麼偵測
檢查對象：system map JSON、README、圖台 inspector 說明。
- 通用：圖上有大量 hypothesized 或 unknown 邊，卻沒有對應的待驗證問題或資料需求；新增圖層的理由是「資料很多」而非某條關係。
- 搜尋（JSON）：`evidence_status` 為 hypothesized／unknown 的 edge，其 `dataset_ids` 與待驗證問題欄位皆空。
- 搜尋（文字）：只有 `可進一步|未來可|延伸` 等空泛句，沒有具體問題。

## 出處
- Meadows (2008) Thinking in Systems。
- 「System Map 是問題產生器」是教學歸納。

