---
id: 00-01
title: 系統四元素：圖層集合不等於系統理解
topic: 00-system-thinking
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [系統思考, 系統四元素, Elements, Interconnections, Function, Purpose, Behavior over time, Meadows, 圖台敘事]
---

## 原則
圖台說明不要只列「整合了哪些資料」；先寫這些圖層共同描述的現象與系統功能，再說明各圖層是哪類元素、彼此如何連動。

## 症狀
圖台上有降雨、河川、感測器、醫院、人口六個圖層，說明文字卻只是「本圖台整合了六類資料」。讀者看得到點和面，看不到它們為什麼應該放在一起、彼此如何連動、整體在做什麼。圖層能一起匯入 GIS，不代表它們描述同一個系統。

## 原因
把「有哪些資料」當成「系統是什麼」。系統不是物件清單，而是由四件事構成的結構：

| 元素 | 問句 | 例（淹水） |
|---|---|---|
| Elements | 有哪些事物、行動者、資源？ | 降雨、河川、排水設施、道路、醫院 |
| Interconnections | 它們如何連動？ | 降雨增加逕流；排水容量限制排除量；積水阻斷道路 |
| Function / Purpose | 這套系統在做什麼？ | 排除雨水、維持移動與醫療可達性 |
| Behavior over time | 受到變化後如何回應？ | 豪雨後積水累積、退去、道路復通 |

提醒：系統「實際的功能」未必等於個別單位自稱的目標；時間行為是觀察結構的切入點，不是第四種「物件」。

## 解法
1. 圖台或分析開頭先寫一句：這些圖層共同描述哪個現象？（沒有答案就是尚未形成系統。）
2. 對每個圖層回答：它是哪一類 Element？與哪個 Element 有哪種關係？（關係寫法見 [00-03](00-03-every-edge-must-mean-something.md)、[00-05](00-05-eight-relationship-types-and-spatial-vs-system-proximity.md)。）
3. 寫出系統的 Function / Purpose，以及資料是否足以觀察 Behavior over time（不足就明講，見 [00-06](00-06-system-changes-over-time-stock-flow.md)）。
4. 好的 System Map 重點不是節點最多，而是能說清楚「為什麼畫這條線」；結構在連線，不在節點。
5. 區分三個相近詞：Systems Thinking 是較廣的思考方式；System Mapping 是表達結構的工具；System Dynamics 是分析系統隨時間行為的建模傳統。

## 怎麼偵測
檢查對象：圖台說明文字、README、system map JSON。
- 通用：說明只列「整合了 N 類資料」，沒有任何關係動詞、沒有一句 purpose；圖層面板是平的清單，沒有關係或分組語意。
- 搜尋（system map JSON）：`system_function` 為空或缺；`edges` 長度為 0 或遠少於 `nodes`；節點全部沒有 edge（孤立點，見 [00-14](00-14-system-map-pre-publish-checklist.md)）。
- 搜尋（文字）：`整合了|匯集了|涵蓋.*類資料` 後面沒有 `因此|用來|目的` 之類的 purpose 句。
- 僅限有寫「系統」「整體」論述的圖台；純資料瀏覽器不適用。

## 出處
- Meadows, D. (2008). Thinking in Systems: A Primer（elements、interconnections、function/purpose）。
- 「圖層集合不等於系統理解」是教學歸納，非原著用語。

