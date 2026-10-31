---
id: 17-04
title: 給 agent 的分析工具怎麼設計：口徑寫進資料使用須知、常見分析做成確定性工具、不相容的比較直接擋下
topic: 17-ai-agent
kind: decision
scope: public
evidence: Implemented
stacks: [any]
tags: [AI agent, MCP, 工具設計, 資料使用須知, 口徑, 確定性工具, 相容性檢查, 跨國比較, 並列不混算, must state, 配方 SQL]
---

## 原則
口徑知識放進工具回傳與資料使用須知，不靠 agent 記憶；常見分析做成確定性工具；來源口徑不相容時由工具直接擋下或附限制句；跨國只並列不混算。

## 症狀
- agent 每次自己寫 SQL 算熱點或集中度，同一題答出不同數字。
- 資料表有已知陷阱（疊了兩個快照、一列是一個當事人而不是一件事故），agent 不知道，直接加總。
- agent 把台灣的站點數和日本的人口相除，算出一個看似合理但毫無意義的比例。

## 原因
agent 只看得到工具說明和工具回傳的內容。口徑知識若只在人的腦袋或內部文件裡，agent 就會自選口徑；複雜計算若只給「配方」讓它照抄，抄錯就算錯，而且每次都可能不一樣。

## 解法
1. **資料使用須知跟著資料走**：每個有陷阱的資料集寫一段白話須知（一列代表什麼、要先取哪個快照、哪些欄位是粗略定位、預設要排除什麼），在 agent 查到這個資料集時由工具回傳，而不是寫在 agent 不一定會讀的文件裡。
2. **口徑有多種合理定義時，定一個預設，並要求回答寫明**：例如「製造業」有兩種界定時，工具回傳用了哪一種、還可以換哪幾種，並附一句必須寫進回答的句子。
3. **常見分析做成確定性工具**（熱點、群聚、集中度、跨尺度相關、等時圈）：同樣輸入每次同樣輸出，門檻與檢定方式寫死在工具裡（[16-01](../16-spatial-analysis/16-01-hotspot-clustering-methods.md)、[16-02](../16-spatial-analysis/16-02-location-quotient-and-ratio-metrics.md)、[16-03](../16-spatial-analysis/16-03-cross-scale-maup.md)），agent 只選參數。
4. **計算前先做口徑相容性檢查**：兩個來源的時間範圍、空間範圍、計數單位、是否為推估值不一致時：
   - 嚴重不相容 → 預設拒算，回傳原因與替代做法；
   - 輕微不相容 → 照算，但附一句必須寫進回答的提醒；
   - 使用者明確要求照算時才放行，回答仍要帶限制句。
5. **跨國或跨資料體系只並列、不混算**：不同國家的統計定義、行政層級、人口分母不同，各自在自己的單元上算，再並排呈現；工具直接拒絕把兩國來源放進同一個相關或比率，且不可被放行。缺邊界或人口分母的國家回「未涵蓋＋缺什麼」，不回 0。
6. **工具回傳附建議樣式與摘要**，讓上圖與回答都有固定格式；大結果只內嵌前幾十列，其餘分頁取。
7. **候選分類可以交給模型，權限、資料健康與執行由確定性程式決定**。
8. **把規則放在工具回傳與 server 指示，而不只在 skill**（[17-01](17-01-agent-map-control-rules.md)）；改了工具就跑回歸題庫（[17-02](17-02-agent-evaluation-regression-bank.md)）。

## 怎麼偵測
- 通用：同一題重跑數字不同；agent 的 SQL 每次寫法不同；回答沒有說明用了哪種定義；跨國比較出現單一合併數字。
- 搜尋：工具回傳中沒有 `notes|caveats|mustState|usage` 類的欄位；分析類功能只有「SQL 範本」文件、沒有對應的工具實作；比較或相關函式沒有檢查兩個來源的 `country|period|unit`（適用 stack：MCP server、any）。

## 出處
- 一般軟體設計原則：把領域規則放在程式與資料契約裡，而不是靠使用者（或 agent）記住。
- 相關卡：[16-01](../16-spatial-analysis/16-01-hotspot-clustering-methods.md)（熱點）、[16-02](../16-spatial-analysis/16-02-location-quotient-and-ratio-metrics.md)（集中度）、[16-03](../16-spatial-analysis/16-03-cross-scale-maup.md)（跨尺度）、[06-07](../06-data-formats/06-07-ratio-denominator-and-double-counting.md)（分母與疊檔）、[01-14](../01-taiwan-apis/01-14-semantics-drift-and-upstream-loss.md)（資料語意漂移）、[08-10](../08-multi-layer/08-10-multi-country-country-selector-no-cross-mix.md)（多國化）。
- 實例：[mini-taiwan-pulse 經驗總集](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/LESSONS.md)。

