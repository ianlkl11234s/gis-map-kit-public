---
id: 00-12
title: 從 Pattern 到 Insight：觀察、推論、假說、驗證分層寫，混淆變數要講準，發布前問五題
topic: 00-system-thinking
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [insight, pattern, association, causation, 相關不等於因果, confounding, 混淆變數, 替代解釋, 主張證據, 發布前檢查, 敘事]
---

## 原則
把 pattern 寫成 insight 時，依觀察、推論、假說、驗證分層，混淆變數要講準，宣稱因果前先答三問，發布前自問五題。

## 症狀
- 兩個圖層疊在一起看起來錯開或重疊，報告就寫「A 造成 B」「飛機在躲雷」。
- 把任何沒放進分析的因素都叫「混淆變數」，或反過來完全不考慮第三因素。
- 只有「最高層級的因果結論才算 insight」，於是描述性發現被硬拉成因果；或什麼都不敢說。
- 對外文章的結論強度和手上證據不相稱，被讀者追問時答不出來。

## 原因
- 一個 pattern 從被看見到能支持行動，中間要經過觀察、推論、假說、驗證四層；省略中間層，主張就比證據強。
- 第三因素可能同時影響 A 與 B，使兩者看起來相關。但嚴格的混淆變數必須同時與暴露（A）和結果（B）有關，而且不是 A 造成的中介結果；第三變數也可能是中介、結果或平行原因。
- insight 有不同深度，該走多深由目的決定；調查行動的門檻可以低於責任認定的門檻。

## 解法
1. **四層分開寫**（同一個案例每層一句）：
   | 層次 | 例：航跡 × 雷擊 |
   |---|---|
   | Observation 觀察 | 某時段航跡與雷擊密集區出現空間錯開 |
   | Interpretation 推論 | 可能與對流天氣或空域運作有關 |
   | Hypothesis 假說 | 某些時段航班可能因強對流而繞行 |
   | Validation 驗證 | 比對時間、天氣雷達、既定航路與航管資訊 |
2. **insight 的深度依目的**：Describe（盤點、比對）→ Relate（縮小範圍）→ Hypothesize（提出監測或查核假設）→ Validate & Act（相稱的行動）。每一層都可能有價值，不要畫成只有最高層才算的排行。
3. **混淆變數講準**：畫出「第三因素 → A、第三因素 → B」的示意，問「控制或分組比較這個因素後，原本的關係還在嗎？」。若第三因素只影響 B、不影響 A，它是另一個解釋，不是混淆變數。示意圖要標「假設情境」。
4. **宣稱因果前三問**：
   - 有沒有其他因素也能解釋結果？
   - 時間先後與物理傳播路徑合理嗎？
   - 有沒有獨立證據支持或推翻？
   答不出來就寫「這是值得驗證的假設」，不寫「已證明」。
5. **主張越強，證據越多**：從「有潛在來源」到「某來源造成某次事件」，每往上一階都要補新證據；最後一階不能只靠疊圖。階梯的寫法見 [00-08](00-08-question-evidence-metric-dataset-loop.md)。
6. **發布前五問**：我觀察到什麼？我在推論什麼？還有什麼能解釋？缺哪些證據？現在能正當採取什麼行動？把「已知、推論、未知」分開寫。
7. 「設施位在保護區內」不等於違法，「有列管」不等於實際造成污染；地點層級的主張要檢查資料時效、空間精度、連通性與監測。

## 怎麼偵測
檢查對象：分析報告、文章草稿、AI 產出的結論段落。
- 通用：結論段沒有「替代解釋」或「限制」；示意性的因果圖沒標「假設」；一張疊圖支撐了「造成」「導致」的句子。
- 搜尋（文字）：`造成|導致|證明|因為.{0,10}所以` 出現在只有疊圖或相關係數的段落；`混淆` 指稱的變數沒有說明它如何同時影響兩邊。

## 出處
- CDC Field Epidemiology Manual, Analyzing and Interpreting Data（confounding、偏誤、關聯與因果）。https://www.cdc.gov/field-epi-manual/php/chapters/analyze-interpret-data.html
- NIST/SEMATECH e-Handbook, Experiments and Experimental Design（correlation 與 causality）。
- Penn State STAT 100, Relationships Between Measurement Variables（替代解釋、離群值）。
- US EPA Source Water Assessments、Determine Susceptibility to Contaminant Sources（成熟的風險評估構面，不等於已完成評估）。
- 相關卡：[00-03](00-03-every-edge-must-mean-something.md)（關聯與因果線型不同）、[00-08](00-08-question-evidence-metric-dataset-loop.md)（主張階梯）、[00-11](00-11-visualization-as-thinking-explore-explain.md)（觀察清單）。

