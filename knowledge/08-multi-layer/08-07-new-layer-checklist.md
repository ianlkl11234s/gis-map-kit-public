---
id: 08-07
title: 新增圖層 checklist：資料驗收、接線、UX、瀏覽器單層驗收，各步驟誰來守
topic: 08-multi-layer
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [checklist, 新增圖層, 驗收, 上線, onboarding, All Off, 資料驗收, 常漏項, 守門]
---

## 原則
新增圖層時照固定清單逐項驗收，並標明每項由自動測試還是人工把關；資料落地驗收先於接線，瀏覽器單層驗收要先全部關閉再只開新圖層。

## 症狀
新圖層上線後才發現：點數比來源少、popup 欄位全是 undefined、分色全同色、檔案路徑 404、座標落在赤道附近、圖層只在開發機看得到。這些問題每個新圖層都可能重來一次。

## 原因
驗收項目散在不同人的腦袋裡；有些有自動測試守、有些沒有，卻沒有標出哪些是哪些。

## 解法
把流程固定成有順序的清單，每一項標明「誰守」：**自動**（測試會紅）或**人工**（要親手做）。

**1. 資料落地驗收（最常漏，先於接線）——人工**
- 筆數對得上來源（`jq '.features | length'`、tile 解碼抽樣）。
- 屬性欄位齊全：popup 與分色要用的欄位都在（向量圖磚常因為建置參數沒列全而漏欄位）。
- 座標系統正確（數值超過 ±180／±90 多半是投影座標）、經緯度順序沒顛倒。
- 缺值是 null 不是 0；JSON 不含 `NaN`／`Infinity`（見 [06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)）。
- 已發布的資產 URL 視為契約，不隨意搬動；新資產路徑要同步反向代理與部署腳本。

**2. 接線——大部分自動**
- 登記一筆；型別強制補齊的由編譯器擋，空殼值由完整性測試擋。
- loader 包載入狀態登記（切換圖層、切日都要有可見的載入提示）。
- 動態圖層：遵守時間訂閱規則（[03-02](../03-dynamics/03-02-time-in-reactive-state-rerender-storm.md)、[03-03](../03-dynamics/03-03-subscription-granularity-and-throttle.md)），參數不收 `currentTime`。
- 疊放位置有決定（[08-05](08-05-layer-stacking-order.md)）。

**3. UX 準入——部分自動**
- 透明度、圖例、popup、選單（[09-02](../09-design-system/09-02-layer-ux-four-iron-rules.md)）；哪些由測試守、哪些要人工點，要分開標明。
- 點層的半徑、透明度、是否 cluster 依資料密度決定（見 [14-00](../14-scale-density/14-00-scale-density-decision-table.md)），不憑感覺。

**4. 瀏覽器單層驗收——人工**
- 先按「全部關閉」，**只開新圖層**，避免被別的圖層干擾判斷。
- 看邊界縮放（最小／最大 zoom）、時間軸兩端、點一次 popup、拉兩端透明度、切到另一個國家／面板再回來。
- 動態圖層：全關＋暫停，確認 render 次數 = 0（[07-03](../07-performance/07-03-hidden-layer-paint-keeps-map-busy.md)）。

**5. 跨 repo／資料契約對齊——人工（資料與前端分屬不同 repo 時才需要）**
- 上游資料產生端的交接文件、下游反向引用、有破壞性變更先開決策紀錄。
- 順序：上游先動、下游後動，反過來會讓前端硬依賴不存在的欄位。

**6. 收尾**
- 更新變更紀錄、待辦清單；踩到新坑寫成一則紀錄，學到通則補進規則文件。

做成 PR 範本裡的勾選清單；新圖層用腳手架指令一次產出骨架，免得漏步驟。

## 怎麼偵測
- 通用：隨機抽一個新圖層，逐項對照；或看最近三個圖層的 PR 是否漏了同一項。
- 搜尋：沒有 PR 範本或 `CONTRIBUTING`／skill 檔案列出清單（any）；`npm test`／CI 沒有圖層完整性測試（any）；`rg "kind: .*TODO|FIXME"` 在登記檔留下空殼。

## 出處
- 一般新功能上線 checklist 做法。
- 實例：[layer-onboarding SKILL.md（逐步驗收與 UX 基準表）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/skills/layer-onboarding/SKILL.md)、[layer-integration-common-misses（常漏項）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/pitfalls/2026-07-01-layer-integration-common-misses.md)、[development-rules.md（新增圖層觸點表）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/development-rules.md)。
