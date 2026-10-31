---
id: 08-00
title: 多圖層管理總表：登記、守門、狀態、疊放、上限、新增與分享
topic: 08-multi-layer
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [總表, 多圖層, 登記簿, 開關, 疊放, 分享網址, 搜尋別名, 多國化]
---

## 原則
圖層事實只在登記簿定義一次，其餘一律派生；先看 [08-01](08-01-layer-registry-single-source.md) 定骨架，再用 [08-02](08-02-registry-completeness-tests-and-ledger.md) 守門，新增圖層走 [08-07](08-07-new-layer-checklist.md) 的清單。

## 對照表

### 登記與守門
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 名稱、顏色、圖示等在多處各抄一份 | [08-01](08-01-layer-registry-single-source.md) | 登記事實只在一處定義，面板、圖例、控制項一律派生 |
| 怕新圖層漏接、豁免被亂用 | [08-02](08-02-registry-completeness-tests-and-ledger.md) | 完整性測試加雙向 ledger，null 豁免要登記理由，測不到的要留人工步驟 |

### 狀態與疊放
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 圖層開關狀態放哪、元件為何重繪過多 | [08-03](08-03-layer-visibility-store.md) | 模組級 store 支援 per-key 訂閱，snapshot identity 只在真的變動時換，預設全關 |
| 圖層蓋到別人、重建後跑到最上層 | [08-05](08-05-layer-stacking-order.md) | 有序登記陣列決定 z-order，自訂圖層在底圖標籤之下，動態重建後重排 |
| 該限制同時開幾層 | [08-06](08-06-how-many-layers-at-once.md) | 依資源分別設限，上限來自量測 |

### 新增圖層
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 要新增一個圖層 | [08-07](08-07-new-layer-checklist.md) | 資料驗收先於接線，標明自動或人工把關，單層驗收先全關再只開新層 |

### 分享與搜尋
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 網址要記住開了哪些圖層 | [08-08](08-08-shareable-layer-state-url.md) | 只序列化與預設不同的項目並帶版本號，讀不懂的值靜默丟掉 |
| 圖層搜尋命不中某些詞 | [08-09](08-09-layer-search-alias-only-for-misses.md) | 名稱、說明、主題從登記簿派生，別名表只收名稱命不中的詞 |

### 多國化
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 加入第二個國家的圖層 | [08-10](08-10-multi-country-country-selector-no-cross-mix.md) | 國家是整個介面共用的維度，只在使用者選擇時切換，跨國各算再並列 |

## 相關主題
- 四鐵則：[09-02](../09-design-system/09-02-layer-ux-four-iron-rules.md)。
- 圖層疊放與透明度：[14-04](../14-scale-density/14-04-overlap-order-and-opacity.md)。
- 分享鏡頭與時間：[11-04](../11-extras/11-04-share-camera-og-image-saved-scene.md)。
- 圖層樣式黃金快照：[10-20](../10-ops/10-20-layer-style-golden-snapshot.md)。

## 出處
各項依據見對應卡片。
