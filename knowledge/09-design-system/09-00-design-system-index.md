---
id: 09-00
title: 設計系統總表：token、四鐵則、面板、圖例、popup、控制項、四態、文字、RWD、符號
topic: 09-design-system
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [總表, 設計系統, token, 四鐵則, 面板, 圖例, popup, 控制項, RWD, 符號尺寸]
---

## 原則
先看 [09-01](09-01-token-ssot-and-ratchet-guard.md) 建立 token 與自動檢查，再用 [09-02](09-02-layer-ux-four-iron-rules.md) 的四鐵則驗收每個圖層；各介面元件依下表選卡。

## 對照表

### 骨架與驗收
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 樣式值散落各處、舊違規無法一次清 | [09-01](09-01-token-ssot-and-ratchet-guard.md) | token 單一來源，可機器判斷的禁止項寫成 lint，用只降不升的基準管理 |
| 新圖層要驗收 UX | [09-02](09-02-layer-ux-four-iron-rules.md) | 透明度、圖例、popup、選單缺一不可，缺口不得用 null 靜默豁免 |

### 面板與彈出層
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 浮層互相遮擋、z-index 越調越大 | [09-03](09-03-panels-layering-and-portal.md) | 先決定語意層級，用層級表；左側面板同時只開一個，彈出層 portal 到 body |

### 圖例與 popup
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 設計圖例 | [09-04](09-04-legend-spec.md) | 共用元件組成，色票與地圖 paint 共用顏色常數，色階與單位不可收合 |
| 設計 popup 與來源 | [09-05](09-05-popup-and-source-footer.md) | 固定結構，空值整列不渲染，來源缺漏明講「來源待補」 |

### 控制項
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 新圖層要加參數控制 | [09-06](09-06-layer-controls-spec-driven.md) | 由宣告式規格自動產生；選項 4 個以上用下拉，2～3 個互斥才用分段 |

### 四態與文字
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 載入、失敗、無資料、過期怎麼呈現 | [09-07](09-07-loading-data-time-and-stale.md) | 三態註冊到共用登記，失敗、無資料、過期分開呈現，資料時間看得見，缺值不補 0 |
| 深色介面或底圖上文字看不清、徽章對比不足 | [09-08](09-08-text-hierarchy-dark-basemap.md) | 六階文字色各有暗淡值，淡色徽章字色要與深色混色 |

### RWD 與符號尺寸
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 手機版與觸控 | [09-09](09-09-responsive-and-touch.md) | 共用資料面板只換外殼，hover 資訊要有觸控替代，在全部浮層展開下驗收 |
| 點線面尺寸與切底圖 | [09-10](09-10-map-symbol-size-tiers.md) | 尺寸與透明度只用少數固定階，切底圖只換色 |

## 相關主題
- 靜態表現形式總表：[04-20](../04-effects-catalog/04-20-static-forms-catalog.md)。
- 色彩：[05-00](../05-color/05-00-color-index.md)。
- 作者品味與偏好：[13-00](../13-author-taste/13-00-taste-overview.md)。
- 點密度與縮放畫法：[14-00](../14-scale-density/14-00-scale-density-decision-table.md)。

## 出處
各項依據見對應卡片。
