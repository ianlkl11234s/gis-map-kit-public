---
id: 13-01
title: SDK 預設 MapLibre，同時申請 Mapbox token 備用，需要時才換
topic: 13-author-taste
kind: decision
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre]
tags: [MapLibre, Mapbox, token, SDK 選型, 費用, 免費額度, globe]
---

這是作者的設計偏好，不是業界規範；你可以不同，但要說得出理由，偏離時在 README 或 PR 寫一句。

## 原則
新專案預設用 MapLibre，同時申請一組 Mapbox token 備用；只有需要 Mapbox 專屬樣式或功能時才換，並寫下理由。

## 症狀
- 新專案一開始就綁 Mapbox，之後發現流量計費、token 外露或授權問題才想換。
- 或反過來：為了「免費」選 MapLibre，卻需要 Mapbox 專屬的樣式或功能而卡住。

## 原因
兩者 API 相近但不等價：MapLibre 沒有 token 與 map load 計費，可搭自架底圖；Mapbox 有官方樣式與部分專屬功能，但要 token 與計費。

## 解法
1. 預設 MapLibre，底圖優先自架或無 key 來源（見 [02-09](../02-basemaps/02-09-self-hosted-pmtiles-basemap.md)、[02-02](../02-basemaps/02-02-basemap-selection-decision.md)）。
2. 同時申請一組 Mapbox token 備用。個人或課堂用量通常在免費額度內；額度數字請查 Mapbox 官方計價頁，本卡不引用。
3. 需要 Mapbox 專屬樣式或功能時才換，並寫下換的理由。
4. token 一律限制 URL／用途並放環境變數，不進公開 repo，計費與授權見 [02-04](../02-basemaps/02-04-mapbox-billing-token-license.md)，節流與祕密處理見 [01-08](../01-taiwan-apis/01-08-token-secret-throttle-backoff.md)。
5. 與 globe 搭配 custom layer 時，先確認該 SDK 版本是否支援（MapLibre 官方文件有支援說明，Mapbox 的限制請查官方文件，見 [04-13](../04-effects-catalog/04-13-custom-layer-on-globe.md)）。

## 怎麼偵測
- 通用：新專案使用 Mapbox 卻沒寫理由；公開 repo 出現 token；README 沒有備用方案說明。
- 搜尋：`mapbox-gl` 於 package.json、`mapboxgl\.accessToken`、`pk\.[A-Za-z0-9]{20,}`（適用 stack：mapbox-gl）。命中後問：是否需要 Mapbox 專屬樣式或功能？token 是否有 URL 限制？
- 反向：使用 MapLibre 但 style 指向 `mapbox://`，會需要 token 與相容性檢查。

## 出處
- 官方文件：Mapbox 計價與 Terms；MapLibre GL JS 文件。
- 實例：[mini-taiwan-pulse 內嵌地圖的底圖設定（MapLibre＋自架 PMTiles，無 key）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/embed/basemapStyle.ts)。
