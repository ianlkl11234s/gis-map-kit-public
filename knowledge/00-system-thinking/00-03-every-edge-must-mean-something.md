---
id: 00-03
title: 每條線都要有意義：關係類別、方向、動詞、證據狀態
topic: 00-system-thinking
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [system map, edge, 關係, 動詞, 證據狀態, observed, source_supported, hypothesized, simulated, unknown, 因果, 共現]
---

## 原則
System Map 的每條線都要標關係類別、方向、動詞與證據狀態；共現與因果用不同線型，沒有證據的線不得畫成因果。

## 症狀
圖上全是同一種灰線：「降雨—河川—淹水」。讀者無法分辨哪條是因果、哪條是路網連通、哪條只是兩者碰巧出現在同一區。共現被畫成實線箭頭，讀起來就是因果。

## 原因
連線沒有語意。因果、連通、流向、共現是不同種類的關係，不能混成同一種箭頭；一旦混用，圖就在暗示它沒有證據支持的結論。

## 解法
每條 edge 至少標四件事：

1. 關係類別（八種型別見 [00-05](00-05-eight-relationship-types-and-spatial-vs-system-proximity.md)）。
2. 方向（有向或明確的無向語意）。
3. 簡短動詞（increases runoff、depends on、drains to、blocks）。
4. 證據狀態：

| 狀態 | 意義 |
|---|---|
| observed | 有實際觀測或紀錄 |
| source_supported | 有來源（文獻、官方文件）支持 |
| hypothesized | 合理但待驗證的假說 |
| simulated | 模型或情境推演的結果 |
| unknown | 關係存在與否、強度都未知 |

補充規則：
- 只有宣稱因果的線才能當因果連結；因果箭頭需說明機制，必要時標極性（+/-）與延遲。共址、相鄰本身不能推斷共享機制。
- 圖例要交代方向規則（例：依賴關係由依賴方指向被依賴方）。
- 共現／關聯用虛線或其他線型，視覺上不能與因果線相同。
- 證據狀態的詳細欄位定義見 [00-09](00-09-system-map-data-model-and-checklist.md)。

## 怎麼偵測
檢查對象：system map JSON、圖台圖例與說明文字。
- 通用：圖上只有一種線型；點開線看不到動詞或證據狀態；圖例沒有區分關係類別。
- 搜尋（JSON）：edge 缺 `verb_label`、`relationship_type`、`evidence_status`；`relationship_type` 為 association／co-location 卻用實線箭頭樣式（`directed: true` 且 style 與 causal 相同）。
- 搜尋（文字）：`影響|導致|造成` 出現在只有空間重疊或相關係數的段落（需人工複核）。
- 適用 stack：any（圖形庫可用 React Flow、Cytoscape、Mermaid 等，檢查的是資料欄位與樣式對應）。

## 出處
- Meadows (2008) Thinking in Systems；System Dynamics Glossary (2019)（因果箭頭、極性、延遲的定義）。
- 證據狀態五分法是本卡的設計，不是外部標準。

