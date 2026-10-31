---
id: 00-00
title: 系統思考總表：從議題到 System Map、發布檢查與 Insight 的使用順序
topic: 00-system-thinking
kind: catalog
scope: public
evidence: General
stacks: [any]
tags: [總表, 系統思考, System Map, 使用順序, 因果, 共現, 邊界, 發布前檢查]
---

## 原則
依使用順序走：先定議題與邊界，再建 System Map，接著從問題走到資料，發布前逐項檢查，最後把 pattern 寫成 insight。圖台要講的是現象與系統功能，不是圖層清單；證據不夠時結論就降級，不補畫因果。

## 對照表

### 1. 定議題與邊界
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 圖台說明只列「整合了哪些資料」 | [00-01](00-01-four-elements-layers-are-not-a-system.md) | 先寫圖層共同描述的現象與系統功能，再說各圖層是哪類元素 |
| 不知道分析從哪裡開始 | [00-02](00-02-start-from-phenomenon-why-and-so-what.md) | 從現象出發，向前列條件與觸發（WHY），向後列暴露與影響（SO WHAT），原因都標待驗證 |
| 需要完整拆解一個現象 | [00-04](00-04-six-layer-analysis-template.md) | 用六層模板組織探索，每層對應資料或標為缺口，不稱為官方標準 |
| 決定哪些因素放進系統 | [00-07](00-07-system-boundary-five-criteria.md) | 用五判準決定邊界；影響大但沒資料的列為 critical uncertainty，不默默刪掉 |
| 現象會隨時間變化 | [00-06](00-06-system-changes-over-time-stock-flow.md) | 先找出變化的是哪個量；沒有時序證據就不畫迴圈、不補動畫 |

### 2. 建 System Map
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 兩個東西「看起來有關」 | [00-05](00-05-eight-relationship-types-and-spatial-vs-system-proximity.md) | 先判斷是哪一種關係再選距離與畫法；空間近不等於系統近 |
| 要在圖上畫連線 | [00-03](00-03-every-edge-must-mean-something.md) | 每條線都標關係類別、方向、動詞、證據狀態；共現與因果用不同線型 |
| 要定輸出欄位 | [00-09](00-09-system-map-data-model-and-checklist.md) | 固定 System、Node、Edge、Source、Dataset 欄位，欄位名稱沿用此卡 |

### 3. 從問題到資料
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 地圖畫完不知道還缺什麼資料 | [00-10](00-10-system-map-as-question-generator.md) | 為每個重要節點與待驗證的邊寫出問題，再列所需 Evidence、Metric、Dataset |
| 手上有資料就想下結論 | [00-08](00-08-question-evidence-metric-dataset-loop.md) | 結論強度不得超過證據；鄰近、連通、暴露、污染與因果要分開，每階都要有新證據 |
| 要決定探索還是說明、怎麼看空白 | [00-11](00-11-visualization-as-thinking-explore-explain.md) | 探索與說明分開，先看全貌；數字附比較基準；空白先分資料缺口與服務缺口 |

### 4. 發布前
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| System Map 要對外發布 | [00-14](00-14-system-map-pre-publish-checklist.md) | 沒有動詞、類別、證據狀態的邊不發布；無來源不標 observed；共現不輸出成因果 |
| 兩期資料比對、或做移除連結的情境 | [00-13](00-13-case-method-two-period-change-and-closure-scenario.md) | 先做實體配對，未配對的稱「不再收錄」；情境分析標明是模型，無容量資料不宣稱壅塞 |

### 5. 從 Pattern 到 Insight
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 把觀察寫成結論 | [00-12](00-12-pattern-to-insight-confounding-claim-check.md) | 依觀察、推論、假說、驗證分層寫；混淆變數講準；宣稱因果前先答三問，發布前自問五題 |

## 相關主題
- 動態與時間變化的呈現：[03-00](../03-dynamics/03-00-dynamics-index.md)。
- 資料口徑與推估標示：[06-07](../06-data-formats/06-07-ratio-denominator-and-double-counting.md)、[06-08](../06-data-formats/06-08-label-estimates-and-models.md)。

## 出處
各項依據見對應卡片。
