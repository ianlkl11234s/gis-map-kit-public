---
id: 00-09
title: System Map 資料模型的最低欄位
topic: 00-system-thinking
kind: pattern
scope: public
evidence: General
stacks: [any]
tags: [system map, 資料模型, schema, System, Node, Edge, Source, Dataset, relationship_type, verb_label, evidence_status]
---

## 原則
System Map 輸出前先定固定欄位（System、Node、Edge、Source、Dataset），讓每條邊都能檢查動詞、證據狀態與來源；欄位名稱一律沿用本卡。

## 症狀
System Map 只存節點和連線，沒有來源、證據狀態與對應資料；匯出後分不出哪條邊是假說、哪條有資料支持；AI 產生的圖只有名詞加亂連線，無從檢查。

## 原因
沒有先定最低可用 schema。欄位固定，圖才能被檢查，其他工具才能共用同一組欄位名稱。

## 解法
最低可用欄位（`?` 表示可選）：

**System**
- id, title, central_question, purpose, region, time_scope, system_function
- boundaries, exclusions[], critical_uncertainties[], status, version

**Node**
- id, label, type（phenomenon／condition／driver／trigger／stock／flow／state／asset／population／intervention／...）
- definition, spatial_context?, temporal_context?, importance, evidence_status
- source_ids[], dataset_ids[], position
- 擴充：is_proxy?（代理資料為 true，不可標 observed）

**Edge**
- id, from_node_id, to_node_id, relationship_type
- verb_label（例：increases runoff／depends on／drains to）
- directed（boolean）, polarity?（+/-，僅因果模型）, delay?, mechanism?
- evidence_status（observed／source_supported／hypothesized／simulated／unknown）
- confidence_basis（文字理由，不強製無根據的機率值）, source_ids[], dataset_ids[]
- 必填：relationship_type、verb_label、directed、evidence_status、confidence_basis

**Source**
- id, title, url, publisher, retrieved_at, source_type, supports_claim_ids[]

**Dataset**
- id, title, landing_url, api_url?, owner, license, spatial_coverage, spatial_resolution
- temporal_coverage, update_frequency, fields[], geometry_type, quality_notes, access_status
- 擴充：verification_level（title／metadata／sample／fit：只看過標題／讀過 metadata／抓過樣本／確認能算指標）、data_nature（observed／reported／estimated／simulated：觀測、申報、推估、模擬）

需要版本追溯時另加 Version／Audit Event。檢查清單見 [00-14](00-14-system-map-pre-publish-checklist.md)。

## 怎麼偵測
檢查對象：system map JSON、匯出的 Markdown、圖台 inspector 顯示內容。
- 通用：點開邊，看不到動詞、證據狀態或來源。
- 搜尋：缺動詞、缺證據狀態、共現帶極性、孤立點、observed 卻沒有來源的 jq 查法見 [00-14](00-14-system-map-pre-publish-checklist.md)。

## 出處
- 欄位是此模板的約定，非外部標準；概念依據：Meadows (2008) Thinking in Systems；System Dynamics Glossary (2019)（polarity、delay）。
- 相關卡：[00-03](00-03-every-edge-must-mean-something.md)（邊的語意與證據狀態）、[00-14](00-14-system-map-pre-publish-checklist.md)（檢查清單）。

