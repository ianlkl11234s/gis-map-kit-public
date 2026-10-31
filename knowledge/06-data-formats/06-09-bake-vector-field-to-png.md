---
id: 06-09
title: 向量場（風、海流）烘成 PNG：R／G 放 u／v，alpha 放有效遮罩
topic: 06-data-formats
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [向量場, u/v, PNG, 烘焙, 風場, 海流, alpha, 遮罩, 雙線性取樣, 粒子]
---

## 原則
格點向量場離線烘成無損 PNG：R＝u、G＝v、alpha＝有效遮罩，每通道的 min／max 寫進 metadata；前端讀回像素後在 CPU 雙線性取樣再還原單位。

## 症狀
- 要畫風場或海流粒子，原始 NetCDF／GRIB 太大、前端不能直接讀。
- 粒子在海岸線附近跑到陸地上。
- 解碼後的風速與原值對不上。

## 原因
格點場是規則網格，不需要向量格式。用影像儲存最省事：瀏覽器原生可解碼、可 HTTP 快取，取樣就是讀像素。

## 解法
1. **預處理（後端或離線）**：把 u、v 各自線性映射到 0–255。**R＝u、G＝v**；同時把每個通道的 `[min, max]` 寫進旁邊的 metadata（JSON），解碼時才能還原。
2. **有效遮罩放 alpha，不放 B**：`alpha ≥ 128` 視為有效格；海流類可把遮罩向內侵蝕幾像素，避免粒子畫到海岸線上。B 通道可保留空白。
3. **PNG 必須無損、不預乘 alpha**：用 canvas 讀回時要確認沒有 premultiplied 造成低 alpha 像素的 RGB 失真（讀回後遮罩外像素不要使用）。
4. 前端把 `<img>` 畫到離屏 canvas，讀回 `Uint8ClampedArray`，**在 CPU 對四個相鄰像素做雙線性混合**後再還原成 u/v 單位。
5. 經度排序（0–360 或 −180–180）與緯度方向（上北下南）要在烘焙時統一，寫進 metadata（見 [12-09](../12-domain-pitfalls/12-09-vector-field-conventions.md) 的風向與流向慣例）。
6. 8 位元解析度有量化誤差：極值範圍太大時改用 16 位元（R＋G 組成高低位元）或兩張圖。圖檔名含時間與內容雜湊，方便快取（見 [06-04](06-04-cache-immutable-404-and-stale-edge.md)）。

## 怎麼偵測
- 通用：粒子越過海岸；解碼風速超出物理合理範圍；改了色表後風速錯誤。
- 搜尋：`getImageData\(` 後直接 `data\[i\]` 當 u/v 卻沒有對照 `min|max` metadata；遮罩通道使用 `data\[i\s*\+\s*3\]`（alpha）的讀取程式（適用 stack：any 前端）。

## 出處
- 一般建議：格點場影像編碼為常見做法（如 windy 系列的 PNG 風場）；8 位元量化與 premultiplied alpha 的提醒也屬一般建議。
- 相關卡：[06-04](06-04-cache-immutable-404-and-stale-edge.md)、[12-09](../12-domain-pitfalls/12-09-vector-field-conventions.md)。

