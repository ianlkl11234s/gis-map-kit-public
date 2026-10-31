---
id: 02-07
title: 底圖與資料的 attribution：要顯示什麼、窄螢幕怎麼辦
topic: 02-basemaps
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [attribution, 版權, logo, Mapbox, OSM, CARTO, ODbL, 顯名標示, 手機, 收合]
---

## 原則
底圖版權與資料來源分開標示，版權列永遠留在最上層、窄螢幕也看得到；不要為了畫面乾淨隱藏 attribution。

## 症狀
為了畫面乾淨隱藏了版權列；窄螢幕上被其他控件蓋住；只標了底圖沒標資料來源；收合後找不到授權資訊。

## 原因
底圖與資料各有標示義務，且彼此獨立：
- Mapbox：logo 與文字（© Mapbox、© OpenStreetMap、Improve this map）一定要顯示；文字可調色與字級但須可讀，logo 不能改樣式。
- OSM 內容：ODbL 須可見可讀的標示；收合時仍須能找到授權資訊。
- CARTO：須標 OSM 與 CARTO，且要「顯眼」。
- 政府開放資料：須顯名標示提供機關（見 [01-05](../01-taiwan-apis/01-05-data-gov-tw-and-license.md)）。。

## 解法
1. 底圖版權與資料來源分開兩處：底圖版權用 SDK 的 attribution 控件（可關預設控件、改自訂 compact 版），資料來源放獨立的來源列或每個圖層的 popup／圖例 footer。
2. 版權列永遠在最上層，不被圖例、面板、時間軸遮住；Mapbox wordmark 與文字永遠留在收合列上。
3. 在窄螢幕實測仍可見（手機底部面板打開時尤其要確認）。
4. 每個即時來源標機關與授權；授權「未載明」就照實標未載明。
5. 底圖換成其他服務時，同步換 attribution 字串。

## 怎麼偵測
- 通用：畫面看不到版權文字；手機版被底部面板蓋住；popup 沒有來源。
- 搜尋：`attributionControl:\s*false`（沒有自訂補上）；`display:\s*none.*attribution`（適用 stack：mapbox-gl, maplibre, leaflet）。

## 出處
- 官方：docs.mapbox.com/help/getting-started/attribution/、osmfoundation.org/wiki/Licence/Attribution_Guidelines、carto.com/legal/basemap-terms/。
- 相關卡：[01-05](../01-taiwan-apis/01-05-data-gov-tw-and-license.md)。
- 實例：[版權列元件](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/components/AttributionBar.tsx)（[commit ad3ad820](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/ad3ad82094b6171bc7a4d30addbf6d2659577ae0)）、[設計規格](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)。
