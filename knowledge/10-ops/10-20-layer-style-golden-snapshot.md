---
id: 10-20
title: 圖層樣式黃金快照：把派生出的 paint／參數／點擊順序凍成 fixture，既有層一行都不該動
topic: 10-ops
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [黃金快照, golden snapshot, snapshot test, fixture, 回歸測試, 樣式, paint, layer registry, 守門, CI, PR 交會, 重構]
---

## 原則
把派生出的圖層樣式、參數與點擊順序凍成 golden fixture，既有層的任何 diff 都視為回歸；重產 fixture 要逐行 review 並獨立 commit。

## 症狀
- 重構登記簿或共用樣式後，測試全綠，上線才發現某幾層顏色、線寬或點擊順序變了。
- 兩個各自 CI 全綠的 PR 合併後，主幹測試紅了。
- 快照一紅就直接重產 fixture 讓它變綠，護欄等於沒有。

## 原因
- 圖層的最終樣式常是「登記簿＋規格＋共用函式」層層派生出來的，單元測試只驗各段，驗不到派生結果有沒有漂移。
- 同一份 fixture 被多個 PR 同時依賴：PR A 新增一層、PR B 改了全站的點描邊規則，各自都對，合在一起時 A 的新層也吃到 B 的規則，fixture 就不一致。
- 重產腳本會覆蓋基準值；沒有逐行 review，就會把真回歸收下。

## 解法
1. **抽取器只寫一份**：測試與重產腳本共用同一個「從登記簿抽出派生結果」的函式，兩邊各寫一份必定漂移。輸出用穩定排序的 JSON，diff 才可讀。
2. **只凍其他測試沒守到的段落**：例如 overlay 的 paint／filter、參數控制項的派生結果、點擊查詢的全域順序。已被逐 key 對帳測試守住的欄位不要再凍第二份（登記簿完整性測試見 [08-02](../08-multi-layer/08-02-registry-completeness-tests-and-ledger.md)）。
3. **驗收規則**：新增圖層只會在 fixture 新增該 key 的幾行；**既有層的任何 diff 都視為回歸**，要有理由才收。
4. **重產要有儀式**：重產腳本檔頭寫明「只在確認變更是有意的時候跑，跑完逐行 review」；重產結果用獨立 commit 並寫明原因。
5. **多個 PR 交會**：依序合併會動樣式的 PR 時，每合一個就看主幹 CI。紅了就在下一個要合的 PR 分支重產 fixture，確認 diff 只是兩個 PR 交會的預期結果，再獨立 commit、等 CI 綠才合。
6. **快照不等於畫面正確**：它只保證沒有非預期的變化，新層仍要在瀏覽器實際驗收。

## 怎麼偵測
- 通用：重構登記簿或共用樣式後，只靠型別與單元測試就合併；多個樣式 PR 平行開發卻沒有共用的派生結果快照；fixture 的變更與功能程式混在同一個 commit。
- 搜尋：測試目錄沒有 `golden|snapshot|__fixtures__` 相關檔，但專案有集中式圖層登記簿（any）。
- 搜尋：`toMatchSnapshot\(\)` 套在整個 style JSON 上、沒有分段（vitest、jest），diff 太大沒人看。
- 搜尋：git log 中 fixture 檔的變更 commit 訊息只寫「update snapshot」（any）。

## 出處
- Vitest／Jest snapshot testing 文件；一般 golden master（characterization test）做法。
- 實例：[docs/development-rules.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/development-rules.md)、[dump-layer-golden.ts（重產腳本）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/scripts/preprocess/dump-layer-golden.ts)、[layerGoldenExtract.ts（測試與腳本共用抽取器）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/__tests__/layerGoldenExtract.ts)、[layer-golden.json](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/__tests__/__fixtures__/layer-golden.json)。
- 相關卡：[08-01](../08-multi-layer/08-01-layer-registry-single-source.md)、[08-02](../08-multi-layer/08-02-registry-completeness-tests-and-ledger.md)、[08-07](../08-multi-layer/08-07-new-layer-checklist.md)。
