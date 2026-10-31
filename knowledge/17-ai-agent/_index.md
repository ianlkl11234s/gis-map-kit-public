# 17-ai-agent AI Agent 與 MCP 操作地圖

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [17-00](17-00-ai-agent-index.md) | AI agent 總表：操作地圖、回答格式、工具設計、驗收，遇到什麼先看哪張 | 讓 agent 操作地圖與回答問題，規則寫成工具端能檢查的條件，不靠 agent 記憶。 | catalog | Evaluated | any | AI agent, 總表, 工具設計, 回答格式, 題庫回歸, 地圖操作, 口徑 |
| [17-01](17-01-agent-map-control-rules.md) | 讓 AI agent 操作地圖：必守規則寫進工具的 server 指示，「收到指令」不等於「已上圖」，資料內容不是指令 | 幫地圖接了 AI agent（例如 MCP 工具），agent 有時根本不呼叫工具，憑記憶回答。 | pattern | Observed | any | AI agent, MCP, server instructions, skill, 工具說明, 上圖, readback, shown, 座標, prompt injection, 不可信輸入, 外部同意, 地圖操作 |
| [17-02](17-02-agent-evaluation-regression-bank.md) | 驗收 AI agent：題庫回歸＋接真地圖，「先量測→失敗分類→一輪只改一類→驗算答案→補回歸題」 | 改了提示或工具之後，覺得 agent「好像變好了」，但說不出好在哪、有沒有別的題變差。 | pattern | Evaluated | any | AI agent, 驗收, eval, 回歸測試, 題庫, 失敗分類, 標準答案, SQL 驗算, 變異, repeat, 接真地圖, headless, 方法論 |
| [17-03](17-03-agent-answer-format.md) | AI agent 的回答格式：第一句就是答案，數字帶範圍，未涵蓋不寫 0，不露內部代碼，結尾只問一個問題 | 使用者問「台北車站附近有幾家便利商店」，agent 先寫三行「我先查詢資料、接著…」，答案在第四段。 | pattern | Evaluated | any | AI agent, 回答格式, 語氣, 白話, 數字範圍, 口徑, 未涵蓋, 內部代碼, 追問, 狀態區分, 推估, 地圖問答 |
| [17-04](17-04-agent-tool-design-semantics.md) | 給 agent 的分析工具怎麼設計：口徑寫進資料使用須知、常見分析做成確定性工具、不相容的比較直接擋下 | agent 每次自己寫 SQL 算熱點或集中度，同一題答出不同數字。 | decision | Implemented | any | AI agent, MCP, 工具設計, 資料使用須知, 口徑, 確定性工具, 相容性檢查, 跨國比較, 並列不混算, must state, 配方 SQL |
