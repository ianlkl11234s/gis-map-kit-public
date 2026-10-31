---
id: 00-07
title: 系統邊界五判準：fit for purpose，並保留關鍵不確定性
topic: 00-system-thinking
kind: decision
scope: public
evidence: General
stacks: [any]
tags: [系統邊界, 判準, critical uncertainty, proxy, 敏感度分析, 排除項目, fit for purpose]
---

## 原則
用五個判準決定哪些因素放進系統邊界；影響大但沒資料的因素列為 critical uncertainty，不可默默刪掉，暫不納入的項目也要明列理由。

## 症狀
兩種極端：地圖想包羅萬象，節點多到沒人看得懂；或為了乾淨默默刪掉「沒資料」的因素，結論看起來很穩，其實漏掉最大的變數。

## 原因
沒有明確的邊界準則，也沒有把「暫不納入」和「影響大但缺資料」分開記錄。

## 解法
以五個判準決定要不要把某因素畫進系統：

1. Purpose：這是探索還是實際工程或公共決策？
2. Expected impact：這個因素可能改變結論多少？
3. Data availability / quality：能否衡量？
4. Time / modeling cost：增加精度要多少成本？
5. Consequence of error：判錯有多嚴重？

原則是 fit for purpose，不是追求最大複雜度。探索性研究可用簡化假設；結果若會影響真實工程或公共安全，標準就要提高並要求專家審查。

關鍵規則：影響很大但沒有資料的因素不可默默刪掉。必須列為 critical uncertainty，並說明處理方式：proxy、情境範圍、敏感度分析，或暫緩結論。其餘「暫不納入」的項目也要明列，並寫理由。

## 怎麼偵測
檢查對象：system map JSON、README 的範圍段、圖台「資料說明」。
- 通用：沒有「不包含」或「限制」段；結論語氣確定但資料明顯缺大塊（例如沒有刷卡資料卻講擁擠度）。
- 搜尋（JSON）：`boundaries` 或 `exclusions` 空；`critical_uncertainties` 為空而存在大量 `unknown` 邊或無 dataset 的節點。
- 搜尋（文字）：缺 `限制|不包含|未涵蓋|待確認` 一類字眼；`全面|完整`用在明顯只含部分來源的描述。

## 出處
- Meadows (2008) Thinking in Systems（系統邊界與模型目的）。
- 五判準是依成熟方法整理的教學判準，非單一原著。

