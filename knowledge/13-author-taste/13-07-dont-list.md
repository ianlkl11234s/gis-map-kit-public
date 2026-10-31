---
id: 13-07
title: 作者的反面清單：明確不要的做法與偵測條件
topic: 13-author-taste
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [不要, 反面清單, 假進度條, 缺值, 大寫, 假動態, gis-review]
---

這是作者的設計偏好，不是業界規範；你可以不同，但要說得出理由，偏離時在 README 或 PR 寫一句。

## 原則
下表的做法一律不做；gis-review 命中時，要求補一句偏離理由，不是一律判錯。

## 症狀
畫面看起來精緻，但有些做法會誤導讀者或讓維護變難。

## 原因
這些是作者反覆踩過或明文禁止的做法，集中成一份供 gis-review 使用。

## 解法
| 不要 | 怎麼做 | 偵測 |
|---|---|---|
| 載 web font／引用未載入的字族 | 系統字（[13-04](13-04-ui-one-ruleset.md)） | `fonts.googleapis`、`@font-face` |
| 圓角 > 8 | 圓角 ≤8 | `border-radius:\s*(9\|[1-9][0-9]+)px` |
| 預設衛星底圖卻無地表實況需求 | 深色單色（[13-02](13-02-basemap-dark-mono-default.md)） | style URL 含 satellite |
| 時間軸或動畫預設自動播放 | 預設不播（[13-05](13-05-motion-data-driven.md)） | `playing:\s*true`、`autoplay\s*[:=]\s*true` |
| 用 transition 冒充平滑 | 資料插值 | transition duration 非 0 且宣稱平滑 |
| 為動畫而動畫、無限循環明暗閃動 | 動態代表資料 | 無資料來源的 `@keyframes infinite` |
| 靜態資料加光暈 | 光只給進行中 | additive／blur 用在靜態層 |
| 缺值顯示成 0 | 顯示「未涵蓋」或無資料色 | `?? 0`、`\|\| 0` 於資料欄位 |
| 假進度條、開站畫面放假即時數字 | 真實載入狀態 | 固定時間跑完的進度條 |
| 沒有功能的占位按鈕 | 做不到就不放 | 空的 onClick |
| 英文大寫 eyebrow、「LEGEND」 | 中文標題在前 | `uppercase` |
| 圖例憑空發明分類；類別色用紅、循環 | 類別對應資料 | 圖例與資料欄位不一致 |
| 為了 3D 而 3D | 立體要有理由（[13-06](13-06-camera-and-3d.md)） | 無高度意義的 extrusion |
| 低縮放爆點、一次塞滿整條路網 | 設 minzoom 或聚合 | 無 minzoom 的大量點圖層 |
| 寫死 hex、字級、圓角 | 取 token（[09-01](../09-design-system/09-01-token-ssot-and-ratchet-guard.md)） | 元件內 `#[0-9a-fA-F]{6}` |

## 怎麼偵測
見上表最後一欄；命中後要求補偏離理由，不是一律判錯。

## 出處
- 見 [13-02](13-02-basemap-dark-mono-default.md)～[13-06](13-06-camera-and-3d.md)、[05-04](../05-color/05-04-null-is-not-zero-color.md)、[04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)。
- 實例：[mini-taiwan-pulse 設計規格的禁止清單](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)。
