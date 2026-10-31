---
id: 02-06
title: 換底圖後自己的圖層、terrain 消失：setStyle 的 diff 與 style.load
topic: 02-basemaps
kind: pitfall
scope: public
evidence: Observed
stacks: [mapbox-gl, maplibre]
tags: [setStyle, diff, style.load, isStyleLoaded, load, idle, 圖層消失, 底圖切換, terrain, 重建]
---

## 原則
切底圖一律用 `setStyle(url, { diff: false })` 完整重載，並把自管的 source、layer、terrain 全部放在單一 `style.load` handler 重建；不要依賴 `isStyleLoaded()` 或 `once('load')`。

## 症狀
- 切換底圖（暗色→淺色→再切回）後，自己加的 source／layer 全部消失。
- 3D 地形突然變平。
- 自訂圖層永遠沒掛上，畫面空白。

## 原因
- 對**相同的 style URL** 呼叫 `setStyle` 時，SDK 走 diff 增量更新：會拿掉自訂圖層，卻**不觸發 `style.load`**，因此沒有機會重建。
- `isStyleLoaded()`、`once('load')` 不可靠（可能早已觸發或永遠不再觸發）。
- 換底圖會清掉 terrain 設定。

## 解法
1. 切底圖用 `map.setStyle(url, { diff: false })` 強制完整重載。
2. 自管的 source／layer／terrain 統一在 `style.load` 事件重建；全站只放一個 `style.load` handler，避免分散。
3. 加圖層時 try／catch，失敗就等 `idle` 重試，不要依賴 `once('load')`。
4. 驗收項目：有底圖切換功能就測「切換後圖層還在」。

## 怎麼偵測
- 通用：切底圖後圖層消失；重新整理才恢復。
- 搜尋：`setStyle\(`（沒有 `diff:\s*false` 且附近沒有 `style.load` 重建）；`once\(['"]load['"]`（適用 stack：mapbox-gl, maplibre）。

## 出處
- 一般建議：以官方 `style.load` 事件重建自訂圖層；相關卡：[02-05](02-05-style-customization-by-code.md)。
- 實例：[底圖切換與 style.load 重建](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/MapView.tsx)（[commit 41d3416e](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/41d3416e2da0bc24d5e8a9833540a1bc42b66440)）、[load 事件只觸發一次的事故紀錄](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/pitfalls/2026-04-22-mapbox-load-once-fired.md)、[換底圖後 2D 軌道消失的設計規則](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)（[commit ebedc65c](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/ebedc65c250e04544ca323ae7d98467158293340)）。
