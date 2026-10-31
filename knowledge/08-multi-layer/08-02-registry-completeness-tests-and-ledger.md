---
id: 08-02
title: 登記簿的自動守門：完整性測試＋「豁免要登記理由」的雙向 ledger
topic: 08-multi-layer
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [測試, 完整性, ledger, ratchet, 豁免, null, 圖例, popup, 守門, CI, 契約測試]
---

## 原則
為圖層登記簿寫完整性測試與「對帳測試」，所有 `null` 豁免都要登記在雙向 ledger；測試測不到的項目要明講並留人工步驟。

## 症狀
- 新圖層上線後才發現沒有圖例、點了沒 popup、沒有透明度滑桿。
- 為了讓測試過，新圖層直接抄一個 `legend: null`，悄悄豁免掉規則；沒有人知道這是有意的還是漏的。
- 豁免清單只增不減：已經補好的圖層還留在豁免名單裡。

## 原因
型別檢查只能擋「欄位不存在」，擋不住「欄位是空字串／空陣列／null」；而「可以是 null」本身不會痛。

## 解法
測試分兩層，分工不重疊：

**A. 對帳測試（宣告 vs 現況）**——宣告錯就紅：
- 登記的 `legend` 指向 ⇔ 圖例註冊表實際有覆蓋。
- 登記的 `popup` ⇔ 點擊註冊表實際有條目（注意：這個測試通常只能驗「已存在條目是否真的存在」，驗不出「新圖層漏加」，見 [08-07](08-07-new-layer-checklist.md) 的人工步驟）。
- 登記的 `params` 數量與種類 ⇔ 實際派生出的控制項。
- 每筆控制規格都有透明度滑桿（UX 準入見 [09-02](../09-design-system/09-02-layer-ux-four-iron-rules.md)）。
- 登記的 `section` ⇔ 面板實際位置。

**B. 完整性測試（登記簿本身）**——三件事：
1. **key 空間完整**：型別裡的每個圖層 key 都有登記；也不能有型別外的幽靈 key。
2. **必要欄有真值**：逐欄檢查非空字串、非空陣列、血緣不是空殼；失敗時**點名缺什麼**。
3. **豁免必須顯式登記（雙向 ledger）**：
   - 登記簿寫 `null` 的圖層 ⇔ 豁免清單裡的圖層，**兩邊集合必須相等**。
   - 新層寫了 `null` 卻不在清單 → 紅（逼你寫理由）。
   - 已經補好線、卻還留在清單 → 紅（ratchet：只進不退，清單只會縮小）。
   - 現有的歷史豁免在引入時一次凍結，不重新審查；但新增的一定會被問「為什麼沒有」。

**不要用掃描原始碼的方式找接線**：用正則掃 `case "key"` 之類，連註解都會掃到、豁免集又與登記簿各記一份；改守登記簿本身的完整性更穩。

**測試測不到的，要明講並留人工步驟：**滑桿是否真的作用於全部子圖層、圖例色是否與地圖一致、點擊註冊表是否漏加、圖層在瀏覽器裡是否真的畫得出來。這些放進新增圖層 checklist（[08-07](08-07-new-layer-checklist.md)）。

```ts
// ledger 雙向相等的最小形狀
const declaredNull = Object.keys(MANIFEST).filter((k) => MANIFEST[k].legend === null).sort();
expect(declaredNull).toEqual([...NO_LEGEND_LEDGER].sort());
```

## 怎麼偵測
- 通用：搜尋專案裡是否有「圖層準入規則」卻沒有對應的自動測試；或測試只掃檔案文字。
- 搜尋：`legend: ?null|popup: ?null|params: ?null`（TS）、`legend:\s*None`（Python）出現在登記檔，且找不到對應的豁免清單或理由；豁免清單以 `Set\(\[|=\s*\[` 宣告卻沒有註解理由（any）。
- 適用：任何有集中式圖層登記的架構（React／Vue／純 JS 皆可，測試框架不限）。

## 出處
- ratchet 測試的一般做法（只准降不准升的基準）。
- 相關卡：[10-20](../10-ops/10-20-layer-style-golden-snapshot.md)（派生樣式的黃金快照）。
- 實例：[src/components/sidebar/__tests__/layerConsistency.test.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/sidebar/__tests__/layerConsistency.test.ts)（完整性與 ledger）、[src/data/__tests__/layerManifest.test.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/__tests__/layerManifest.test.ts)（對帳）。
