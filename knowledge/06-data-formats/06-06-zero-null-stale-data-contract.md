---
id: 06-06
title: 資料契約：0、null、「未涵蓋」、過期要分開表示，匯出的 JSON 還要是合法 JSON
topic: 06-data-formats
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [null, 0, 缺值, 未測, stale, Infinity, NaN, 兜底, COALESCE, JSON.parse, 資料契約]
---

## 原則
有值、真的 0、null／未測、未涵蓋、過期要分開表示；不對觀測值用 0 兜底；匯出的 JSON 必須是嚴格合法的 JSON。

## 症狀
- 地圖上大片格子顯示 0，其實是「未測」或「該區沒有資料」。
- 「地震 M0.0」「機場 0 人」這類卡片，實際是來源停更。
- 整個圖層的點全部消失，沒有報錯。
- 時序圖在缺測時段掉到 0，看起來像現象消失。

## 原因
- 上游用 0（或 -99、(0,0)）代表缺值，loader 與 SQL 又習慣用 `?? 0`、`COALESCE(x, 0)` 兜底，缺值就變成真實的 0。
- 傳輸狀態「成功」不代表資料新鮮：只看請求成功，不看資料內的觀測時間。
- 上游除以 0 得到 `Infinity`／`NaN`，部分語言（Python）照樣寫出非標準 JSON，瀏覽器 `JSON.parse` 失敗，整層消失。

## 解法
1. 資料契約至少區分四種狀態：**有值**、**0（真的是零）**、**null／未測**、**未涵蓋（這個區域根本沒資料來源）**；再加上時間維度的 **stale（過期）**。
2. 每個上游值域先看分布，列出代表缺值的魔術值（0、-99、(0,0)），在匯入層轉成 null 並記錄在文件；禁止對**觀測值**做 `?? 0`／`COALESCE(…,0)` 兜底，需要時註明理由。
3. 顯示層：null、未涵蓋、stale 各有獨立視覺（灰色「無資料」、斜線、「更新於 …」徽章，見 [05-04](../05-color/05-04-null-is-not-zero-color.md)）。請求失敗、逾時、無回應也不是 0 或空資料：要顯示失敗並可重試（載入／失敗／無資料／過期四態見 [09-07](../09-design-system/09-07-loading-data-time-and-stale.md)）。時間序列缺段、動畫缺測保留 null（斷線或標「此時段無資料」），不補 0、不補舊值、不外推（見 [03-08](../03-dynamics/03-08-timeline-gaps-and-data-coverage.md)、[04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)）。
4. 「更新時間」讀資料本身的觀測時間，不是抓取時間、不是 HTTP Last-Modified。每個即時圖層依來源的更新週期設過期門檻，分級（即時／延遲／過期／停更）與顯示見 [09-07](../09-design-system/09-07-loading-data-time-and-stale.md)。
5. 匯出 JSON 時關閉非標準值（Python：`json.dump(..., allow_nan=False)`），並用嚴格 parser 驗證：`node -e "JSON.parse(require('fs').readFileSync(f,'utf8'))"`。
6. 比值分色（A／B）先擋分母 0，避免 Infinity 進入色階表達式。

## 怎麼偵測
- 通用：地圖有大片 0 值格；「最新時間」停在好幾天前仍顯示為即時；匯出檔 `JSON.parse` 失敗。
- 搜尋：`\?\?\s*0\b|\|\|\s*0\b|COALESCE\([^)]*,\s*0\)`（觀測值兜底）；`json\.dump\(` 沒有 `allow_nan=False`；`Infinity|NaN` 出現在輸出檔（適用 stack：any）。

## 出處
- 規格：RFC 8259 JSON 不允許 NaN／Infinity。
- 相關卡：[05-04](../05-color/05-04-null-is-not-zero-color.md)、[09-07](../09-design-system/09-07-loading-data-time-and-stale.md)、[03-08](../03-dynamics/03-08-timeline-gaps-and-data-coverage.md)、[04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)。
- 實例：[mini-taiwan-pulse 事故紀錄（土壤欄位 0 其實是未測，改畫灰色「無資料」；上游 Infinity 寫出非標準 JSON 使整層點位消失，修法 `allow_nan=False`；監看卡只有部分格子會判斷過期）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)。

