---
id: 01-14
title: 表名不等於內容、欄位與 ID 漂移、IP 封鎖與上游停更
topic: 01-taiwan-apis
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [口徑, 欄位漂移, ID 對應, 停更, 台灣 IP, 疊檔, 分母, row unit, 模擬資料]
---

## 原則
用任何資料表前先確認「一列代表什麼」、時點與層級，加總前先篩單一快照與單一層級；表名不等於內容，上游會改欄位、換 ID、停更或封鎖 IP。

## 症狀
- 資料集名叫「水庫蓄水量」卻沒有蓄水量數值；叫「船舶」卻只是港口名冊。
- 同一份表直接 count 或加總翻倍。
- 人均值離譜。
- 本機能抓，部署到國際雲後逾時或被拒。
- 換年份後 ID 對不上，被誤讀為「消失了」。

## 原因
- 表名與內容不符；多個時點／多層級／多個來源檔疊放在同一張表；有些是模擬或抽樣資料。
- 日夜人口、模擬人口不是戶籍人口，不能當人均分母。
- ID 會重編號（行道樹 TreeID「消失」不等於樹被砍）。
- 部分政府主機只接受台灣 IP，或擋國外雲出口 IP。
- 上游悄悄停更、改欄名或換檔名。

## 解法
1. 用前先看「一列代表什麼」（row unit）與時點、層級；加總前先篩單一快照與單一層級。
2. 人均分母用戶籍人口；日夜／模擬資料標明並禁作分母。
3. 跨期比對用穩定鍵，並把「ID 變了」與「真的消失」分開判斷。
4. 估計量與觀測量分開標示（插值、模擬、推估）。
5. 部署後觀察 24 小時，新環境的第一批請求有無逾時（IP 封鎖見 [10-12](../10-ops/10-12-upstream-ip-block-deploy-env.md)、[12-12](../12-domain-pitfalls/12-12-upstream-blocking-rate-limits.md)）。
6. 對每個來源保留一份「踩雷紀錄」，並做欄位 schema 檢查，欄位消失或型別改變要告警。

## 怎麼偵測
- 通用：count 與官方公布數字差整數倍；人均超出常識；某來源在雲端環境逾時。
- 搜尋：`SUM\(.*population\)` 且表名含 day/night/mock；缺少 `DISTINCT|snapshot` 條件（適用 stack：any）。

## 出處
- 一般建議：資料口徑與 row unit 檢查為通用做法。
- 相關卡：[00-13](../00-system-thinking/00-13-case-method-two-period-change-and-closure-scenario.md)（兩期比對的配對與措辭）、[01-06](01-06-nlsc-ris-boundaries-population.md)、[10-12](../10-ops/10-12-upstream-ip-block-deploy-env.md)、[12-12](../12-domain-pitfalls/12-12-upstream-blocking-rate-limits.md)。
- 實例：[外部 collector 的台灣 IP 限制](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/EXTERNAL_COLLECTORS.md)。

