---
id: 00-14
title: System Map 發布前檢查清單：孤立點、未解釋箭頭、因果與共現混用
topic: 00-system-thinking
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [system map, 檢查清單, 孤立點, 未解釋箭頭, evidence_status, verb_label, 發布前檢查]
---

## 原則
System Map 發布前逐項跑檢查清單：沒有動詞、關係類別或證據狀態的邊不得發布，沒有來源的邊不得標 observed 或 source_supported，共現不得輸出成因果。

## 症狀
匯出的圖有沒有任何連線的孤立節點、點開看不出意思的箭頭、只有空間重疊卻被畫成因果的線；AI 產生的圖尤其容易出現，卻沒有人逐項檢查。

## 原因
圖的欄位沒有固定（見 [00-09](00-09-system-map-data-model-and-checklist.md)），也沒有發布前的檢查步驟，錯誤直接流到圖台與報告。

## 解法
發布前逐項檢查：
1. 孤立點：沒有任何 edge 的 node。
2. 未解釋箭頭：缺 `verb_label`、`relationship_type` 或 `evidence_status` 的 edge。無 `verb_label` 的 edge 不得發布。
3. 因果與共現混用：只有 proximity 或 co-location 的資料，不得輸出為 causal influence；沒有來源的邊不得標 observed 或 source_supported。
4. 邊界不明：`boundaries`／`exclusions`／`critical_uncertainties` 全空（見 [00-07](00-07-system-boundary-five-criteria.md)）。
5. 來源：`url` 取不到時標 inaccessible，不虛構出處；simulated 結果不得被當成 observed。
6. Feedback 或 polarity 沒有時序證據就不應標成迴圈（見 [00-06](00-06-system-changes-over-time-stock-flow.md)）。
7. 標 observed／source_supported 的節點與邊，要連到來源或 verification_level 至少 metadata 的資料集；is_proxy 的節點不可標 observed。
8. 一個節點的定義不可混入沒有資料支持的部分（例：有集水區範圍、沒有河網流向，就要拆成兩個節點）。

項目 1、2、3、7 可寫成腳本自動檢查；其餘需人工判斷。

## 怎麼偵測
檢查對象：system map JSON、匯出的 Markdown、圖台 inspector 顯示內容。
- 通用：點開任一條邊，看不到動詞、證據狀態、來源其中之一。
- 搜尋（JSON，以 jq 或腳本）：`edges[] | select(.verb_label == null or .verb_label == "")`；`select(.evidence_status == null)`；`select(.relationship_type | test("association|co-?location")) | select(.polarity != null)`（共現卻帶因果極性）；`nodes[] | select(id 不出現在任何 edge 的 from_node_id／to_node_id)`。
- 搜尋（來源）：`evidence_status` 為 observed 但 `source_ids`、`dataset_ids` 皆空。
- 適用 stack：any。

## 出處
- 檢查項目依 [00-03](00-03-every-edge-must-mean-something.md)、[00-06](00-06-system-changes-over-time-stock-flow.md)、[00-07](00-07-system-boundary-five-criteria.md) 的規則整理。
- 概念依據：Meadows (2008) Thinking in Systems。
- 相關卡：[00-03](00-03-every-edge-must-mean-something.md)、[00-06](00-06-system-changes-over-time-stock-flow.md)、[00-07](00-07-system-boundary-five-criteria.md)、[00-09](00-09-system-map-data-model-and-checklist.md)。

