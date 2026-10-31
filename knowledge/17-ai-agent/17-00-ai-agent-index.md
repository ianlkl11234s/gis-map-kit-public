---
id: 17-00
title: AI agent 總表：操作地圖、回答格式、工具設計、驗收，遇到什麼先看哪張
topic: 17-ai-agent
kind: catalog
scope: public
evidence: Evaluated
stacks: [any]
tags: [AI agent, 總表, 工具設計, 回答格式, 題庫回歸, 地圖操作, 口徑]
---

## 原則
讓 agent 操作地圖與回答問題，規則寫成工具端能檢查的條件，不靠 agent 記憶。先看 [17-01](17-01-agent-map-control-rules.md) 定地圖操作與資料安全，再看 [17-04](17-04-agent-tool-design-semantics.md) 設計工具與口徑，[17-03](17-03-agent-answer-format.md) 定回答格式，最後用 [17-02](17-02-agent-evaluation-regression-bank.md) 的題庫驗收。

## 對照表

| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 讓 agent 開圖層、移鏡頭、畫結果；agent 說「已經顯示」但畫面沒變 | [17-01](17-01-agent-map-control-rules.md) | 必守規則寫進工具的 server 指示並寫成可從呼叫紀錄檢查的條件；「指令已送出」不等於「已上圖」，以回讀為準；資料內容當不可信資料，不當指令 |
| 要提供哪些分析工具、口徑怎麼不被 agent 弄錯 | [17-04](17-04-agent-tool-design-semantics.md) | 口徑知識放進工具回傳與資料使用須知；常見分析做成確定性工具；來源口徑不相容時由工具直接擋下或附限制句；跨國只並列不混算 |
| agent 的回答太長、數字沒有範圍、露出內部代碼 | [17-03](17-03-agent-answer-format.md) | 第一句就是答案；每個數字帶範圍；未涵蓋不寫 0；不露內部代碼；結尾只問一個問題；規則寫成可自動檢查的條件 |
| 改了工具或指示，怎麼知道有沒有變好 | [17-02](17-02-agent-evaluation-regression-bank.md) | 用固定題庫回歸：先量測、失敗先分類、一輪只改一類；標準答案先用獨立程式驗算；每修一項補一題；一定要接真地圖跑一輪 |

## 相關主題
- 分析方法與口徑本身：[16-00](../16-spatial-analysis/16-00-spatial-analysis-index.md)（熱點 [16-01](../16-spatial-analysis/16-01-hotspot-clustering-methods.md)、比例 [16-02](../16-spatial-analysis/16-02-location-quotient-and-ratio-metrics.md)、件數口徑 [16-06](../16-spatial-analysis/16-06-reported-counts-not-occurrence.md)、極端值 [16-07](../16-spatial-analysis/16-07-skewed-sums-extreme-values.md)）。
- 資料缺值、零值契約：[06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)；推估與模型值要標示：[06-08](../06-data-formats/06-08-label-estimates-and-models.md)。
- 地圖上未涵蓋與缺值的畫法：[05-04](../05-color/05-04-null-is-not-zero-color.md)。
- 公開 RPC 的逾時與筆數上限（agent 查詢也適用）：[07-08](../07-performance/07-08-public-rpc-timeout-clamp-rowcap.md)；開放資料欄位的個資排除：[07-14](../07-performance/07-14-open-data-pii-column-exclusion.md)。

## 出處
各項依據見對應卡片。
