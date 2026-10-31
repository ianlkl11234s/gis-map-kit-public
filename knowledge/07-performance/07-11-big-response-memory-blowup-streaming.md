---
id: 07-11
title: 大回應整包解析會讓記憶體膨脹數倍：串流解析、落地磁碟、重工作放子行程
topic: 07-performance
kind: pitfall
scope: public
evidence: Evaluated
stacks: [any]
tags: [記憶體, OOM, 串流, ijson, 子行程, oom_score_adj, collector, 解析, JSON, RSS]
---

## 原則
可能超過數十 MB 的回應不要整包解析：寫到磁碟後串流逐列處理，尖峰的重工作放進子行程並設高 `oom_score_adj`，不要與常駐服務同行程。

## 症狀
- 排程資料處理在某幾天把主行程記憶體從 1.5 GB 推到 4 GB，主機 MemAvailable 見底，OOM killer 把整個容器內的服務一起殺掉。
- 用完後記憶體也不回落（ratchet 在高位）。

## 原因
- 對大回應同時持有「原始 body、解碼後文字、解析後樹」三份，總量約為 body 的 4–5 倍；資料密集的分片特別多。
- 解析腫起來的記憶體被配置器留在行程內，不還給作業系統。
- 重工作和常駐服務在同一行程，一個尖峰就拖垮全部。

## 解法
1. **串流**：把回應寫到磁碟，用串流 JSON 解析器（如 ijson）逐列處理，記憶體與資料量脫鉤；不支援的形狀回退為舊的整包解析，且「下一頁」之類游標失敗時要 fail closed。
2. **重工作放子行程**：每日發布、轉檔這類尖峰工作 fork 子行程，並設高的 `oom_score_adj`，尖峰時只殺它；結束後記憶體完整還給作業系統。
3. 以合成資料（例如 100 萬列分片）量峰值記憶體差，確認前後輸出位元組相同、速度代價可接受。
4. 部署時監控主機 MemAvailable，不只看容器 RSS。
5. 同一服務盡量單實例，避免兩個實例同時重工作（見 10-ops）。

## 怎麼偵測
- 通用：排程當下 RSS 陡升；主機 OOM 日誌；服務無預警重啟。
- 搜尋：`json\.loads\(.*\.text\)|response\.json\(\)` 對可能超過數十 MB 的回應；`resp\.read\(\)` 全讀（適用 stack：Python requests、Node fetch）。

## 出處
- ijson 文件；Linux `oom_score_adj`。
- 相關卡：[06-12](../06-data-formats/06-12-national-osm-road-network-memory.md)（全國 OSM 路網分析的記憶體與分區）。
- 實例：[gis-data-collectors 修正 commit](https://github.com/ianlkl11234s/gis-data-collectors/commit/79090a4d11fa17a34a83c0aba5e7911dd1587778)（改 ijson 串流加子行程；合成 100 萬列分片，峰值差 1584 MB→2 MB，輸出位元組相同、速度慢約 10%）。
