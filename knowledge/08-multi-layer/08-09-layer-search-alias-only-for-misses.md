---
id: 08-09
title: 圖層搜尋別名只補「名稱命不中」的詞，名稱、說明、主題一律從登記簿派生
topic: 08-multi-layer
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [圖層搜尋, 別名, alias, 同義詞, 登記簿, 排序, 單一來源]
---

## 原則
圖層搜尋索引的名稱、說明、主題一律從圖層登記簿派生；另設的別名表只收名稱本身命不中的詞。

## 症狀
- 使用者搜「急診」找不到「醫院」圖層，或搜英文找不到中文名圖層。
- 反過來，搜尋用的別名表越長越大，與圖層登記簿出現兩份名稱，改名後搜尋壞掉。

## 原因
搜尋索引另外維護了一份圖層名稱／說明，與登記簿分叉；或別名表被當成第二個目錄在維護。

## 解法
1. 搜尋索引的名稱、說明、主題、來源一律**從圖層登記簿派生**（見 [08-01](08-01-layer-registry-single-source.md)），不另存一份。
2. 另設一張很小的別名表（圖層 key → 同義詞陣列），**只收名稱本身不會自然命中的詞**（口語稱呼、英文、上位概念）；名稱已能命中的詞不要重複加。
3. 排序規則固定並可測：完整 key／名稱命中 > 別名命中 > 前綴或詞彙命中 > 描述或來源命中；多個關鍵字要全部命中。
4. 別名表的鍵用登記簿的 key 型別約束，刪除圖層時編譯期就會報錯。
5. 測試涵蓋：別名可命中；不同區域（例如國外圖層）共用同一個索引。

## 怎麼偵測
- 通用：改圖層名稱後搜尋結果沒跟著變；別名表裡出現與名稱相同或包含關係的詞；搜尋與登記簿各有一份名稱字串。
- 搜尋：`ALIASES|aliases|synonyms` 常數表中出現與該圖層 title 完全相同的字串；搜尋模組內有手寫的圖層名稱清單而非 import 登記簿（適用 stack：any）。

## 出處
- 一般搜尋索引設計建議（單一事實來源）。相關卡：[08-01](08-01-layer-registry-single-source.md)。
- 實例：[src/lib/layerSearch.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/lib/layerSearch.ts)、[src/lib/__tests__/layerSearch.test.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/lib/__tests__/layerSearch.test.ts)。
