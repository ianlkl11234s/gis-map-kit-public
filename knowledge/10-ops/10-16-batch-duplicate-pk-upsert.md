---
id: 10-16
title: 同一批次內主鍵重複，UPSERT 整批失敗：寫入前先按 key 去重
topic: 10-ops
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [UPSERT, ON CONFLICT, 主鍵重複, 批次寫入, PostgreSQL, current 表, 去重]
---

## 原則
批次 UPSERT 前先按衝突 key 去重（同 key 只留最新一筆），並把去重寫在共用寫入層。

## 症狀
- 即時資料（公車、車輛、船舶）寫入偶發失敗，錯誤類似 `ON CONFLICT DO UPDATE command cannot affect row a second time`。
- 整批資料都沒寫進去，圖層停更，但單筆測試正常。

## 原因
上游同一次回應裡同一個主鍵出現兩次（例如同一輛公車出現兩筆）。PostgreSQL 的 `INSERT … ON CONFLICT DO UPDATE` 不允許同一個 INSERT 語句更新同一列兩次。

## 解法
1. 寫入前在應用層用 dict 以 key 去重，**同一 key 只保留最後（或時間最新）一筆**。
2. 去重要用實際的衝突 key（可能是複合鍵），key 為 null 的列另行處理。
3. 去重規則寫進共用寫入層（writer），讓所有有 current 表的 collector 一起受惠，不要每支各寫。
4. 去重丟掉多少筆要記 log／指標，異常多代表上游有問題。
5. 失敗要有隔離：一批失敗不應讓整輪作廢（見 [10-17](10-17-all-or-nothing-batch-and-checkpoint.md)）。

## 怎麼偵測
- 通用：log 出現 `cannot affect row a second time`；即時圖層偶發停更。
- 搜尋：`ON CONFLICT .* DO UPDATE` 的批次寫入程式中，值列表建立前沒有按 key 去重的步驟（`dict|seen|drop_duplicates`）（適用 stack：PostgreSQL；其他資料庫的 upsert 規則請另查）。

## 出處
- PostgreSQL 文件〈INSERT … ON CONFLICT〉。相關卡：[10-17](10-17-all-or-nothing-batch-and-checkpoint.md)。
- 實例：[408b594](https://github.com/ianlkl11234s/gis-data-collectors/commit/408b59449e36006ea4e4d26a4195b1b4b55ea7ef)（current 表 UPSERT 前按主鍵去重）、[storage/supabase_writer.py](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/storage/supabase_writer.py)。
