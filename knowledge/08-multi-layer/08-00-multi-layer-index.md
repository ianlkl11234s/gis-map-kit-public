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
圖層事實只在登記簿定義一次，其餘一律派生；新增圖層走 [08-07](08-07-new-layer-checklist.md) 的清單。

## 對照表


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


## 相關主題
- 四鐵則：[09-02](../09-design-system/09-02-layer-ux-four-iron-rules.md)。
- 圖層疊放與透明度：[14-04](../14-scale-density/14-04-overlap-order-and-opacity.md)。
- 分享鏡頭與時間：[11-04](../11-extras/11-04-share-camera-og-image-saved-scene.md)。

## 出處
各項依據見對應卡片。
