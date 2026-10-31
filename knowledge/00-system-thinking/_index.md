# 00-system-thinking 系統思考（先建立系統，再找資料）

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [00-00](00-00-system-thinking-index.md) | 系統思考總表：從議題到 System Map、發布檢查與 Insight 的使用順序 | 依使用順序走：先定議題與邊界，再建 System Map，接著從問題走到資料，發布前逐項檢查，最後把 pattern 寫… | catalog | General | any | 總表, 系統思考, System Map, 使用順序, 因果, 共現, 邊界, 發布前檢查 |
| [00-01](00-01-four-elements-layers-are-not-a-system.md) | 系統四元素：圖層集合不等於系統理解 | 圖台上有降雨、河川、感測器、醫院、人口六個圖層，說明文字卻只是「本圖台整合了六類資料」。讀者看得到點和面，看不到它們為什… | pattern | General | any | 系統思考, 系統四元素, Elements, Interconnections, Function, Purpose, Behavior over time, Meadows, 圖台敘事 |
| [00-02](00-02-start-from-phenomenon-why-and-so-what.md) | 從現象出發：往前找條件與觸發（WHY），往後找暴露與影響（SO WHAT） | 分析從「手上有什麼資料格式」開始，拼出一堆圖層；或者從現象直接跳到單一原因（「淹水＝下雨」），忽略同樣一場雨為何有些街區… | pattern | General | any | 系統思考, 現象, WHY, SO WHAT, 初步拆解, 假說, 因果 |
| [00-03](00-03-every-edge-must-mean-something.md) | 每條線都要有意義：關係類別、方向、動詞、證據狀態 | 圖上全是同一種灰線：「降雨—河川—淹水」。讀者無法分辨哪條是因果、哪條是路網連通、哪條只是兩者碰巧出現在同一區。共現被畫… | pattern | General | any | system map, edge, 關係, 動詞, 證據狀態, observed, source_supported, hypothesized, simulated, unknown, 因果, 共現 |
| [00-04](00-04-six-layer-analysis-template.md) | 六層分析模板：從基線到介入的完整現象拆解（教學整理的框架） | 地圖只回答「哪裡淹水」，或把潛在淹水圖、感測器點、人口、道路各自成圖，沒有一條從條件到影響到決策的主線。也可能把某個教學… | pattern | General | any | 六層, 分析模板, hazard, exposure, vulnerability, capacity, UNDRR, 淹水, 連鎖影響, 介入, 回饋 |
| [00-05](00-05-eight-relationship-types-and-spatial-vs-system-proximity.md) | 八種關係型別，以及「空間近不等於系統近」 | 兩點直線距離很近就被說成「有關」：污染源與學校隔著山，風場不同；兩站直線近但中間有河，實際行車時間很遠；河流兩點直線很遠… | decision | General | any | 關係型別, Tobler, 距離度量, 拓撲, 路網, 可達性, 流向, 依賴, 替代, 空間近, 地圖畫法 |
| [00-06](00-06-system-changes-over-time-stock-flow.md) | 系統隨時間變化：Stock、Flow、State、Trigger、Delay、Feedback、Threshold | 動態圖台只是把靜態資料做成時間滑桿；或在沒有證據的地方畫出「因為塞車所以改道又回頭加重塞車」的迴圈；或把容量瓶頸造成的非… | pattern | General | any | System Dynamics, stock, flow, state, trigger, delay, feedback, threshold, 動態圖台, 時間 |
| [00-07](00-07-system-boundary-five-criteria.md) | 系統邊界五判準：fit for purpose，並保留關鍵不確定性 | 兩種極端：地圖想包羅萬象，節點多到沒人看得懂；或為了乾淨默默刪掉「沒資料」的因素，結論看起來很穩，其實漏掉最大的變數。 | decision | General | any | 系統邊界, 判準, critical uncertainty, proxy, 敏感度分析, 排除項目, fit for purpose |
| [00-08](00-08-question-evidence-metric-dataset-loop.md) | Question → Evidence → Metric → Dataset 迴圈，以及「資料還不是證據」 | 把資料疊上地圖就宣稱「污染已影響取水口」；用一個數字（工廠數）當作風險；探索時看到的 pattern 直接寫成結論；或反… | pattern | General | any | 研究問題, evidence, metric, dataset, question-first, data-first, exploration-first, 鄰近, 暴露, 因果, 水源, proxy |
| [00-09](00-09-system-map-data-model-and-checklist.md) | System Map 資料模型的最低欄位 | System Map 只存節點和連線，沒有來源、證據狀態與對應資料；匯出後分不出哪條邊是假說、哪條有資料支持；AI 產生… | pattern | General | any | system map, 資料模型, schema, System, Node, Edge, Source, Dataset, relationship_type, verb_label, evidence_status |
| [00-10](00-10-system-map-as-question-generator.md) | System Map 是問題產生器：每個節點長出待驗證的問題 | 畫完圖就停在「畫好看的關係圖」，沒有下一步；或下一步變成「還可以加什麼圖層」，資料越加越多，卻說不出各自要驗證哪條關係。 | pattern | General | any | system map, 待驗證問題, evidence questions, 資料蒐集藍圖, critical uncertainty |
| [00-11](00-11-visualization-as-thinking-explore-explain.md) | 視覺化即思考：探索和說明分開、先看全貌、數字要有比較基準、空白也是問題 | 圖層一放上去就盯著熱區下結論，沒看全台分布，也沒點開單筆確認資料本身。 | pattern | General | any | 視覺化即思考, Exploratory, Explanatory, Overview first, Shneiderman, EDA, 八項觀察, Count ≠ Risk, 比較基準, 分母, No data ≠ No service, 資料空白, data artifact |
| [00-12](00-12-pattern-to-insight-confounding-claim-check.md) | 從 Pattern 到 Insight：觀察、推論、假說、驗證分層寫，混淆變數要講準，發布前問五題 | 兩個圖層疊在一起看起來錯開或重疊，報告就寫「A 造成 B」「飛機在躲雷」。 | pattern | General | any | insight, pattern, association, causation, 相關不等於因果, confounding, 混淆變數, 替代解釋, 主張證據, 發布前檢查, 敘事 |
| [00-13](00-13-case-method-two-period-change-and-closure-scenario.md) | 案例方法：兩期比對要先做實體配對（資料裡消失不等於被移除），移除連結的情境分析要標明是模型 | 拿兩年份的行道樹（或店家、設施）名冊相減，就發文說「今年砍了 X 棵樹」。 | pattern | General | any | change detection, 兩期比對, 名冊, record linkage, entity resolution, 配對, 不再收錄, 情境分析, scenario, 封橋, 網路重要性, 依賴, 替代性, 措辭 |
| [00-14](00-14-system-map-pre-publish-checklist.md) | System Map 發布前檢查清單：孤立點、未解釋箭頭、因果與共現混用 | 匯出的圖有沒有任何連線的孤立節點、點開看不出意思的箭頭、只有空間重疊卻被畫成因果的線；AI 產生的圖尤其容易出現，卻沒有… | pattern | General | any | system map, 檢查清單, 孤立點, 未解釋箭頭, evidence_status, verb_label, 發布前檢查 |
