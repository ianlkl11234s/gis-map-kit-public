---
id: 11-12
title: 地圖站多語系：只在顯示層查表、查不到退回原文，地名用官方英譯，外文長字要先決定截斷或換行
topic: 11-extras
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [i18n, 多語系, 翻譯, t(), fallback, 退回原文, 顯示層, 識別字, 地名英譯, 羅馬拼音, 外文欄位, 機器翻譯, setLanguage, 底圖地名, 長字, ellipsis]
---

## 原則
只在顯示層翻譯，資料與設定裡的中文保持為識別字；查不到翻譯就退回原文；地名用官方英譯；上游外文欄位先抽查再採用。

## 症狀
- 圖層 key、URL 參數或給 AI 讀的字串被一起翻掉，分享連結和搜尋壞掉。
- 翻到一半合併上線，沒翻到的地方顯示空白或 key 名稱。
- 縣市、車站、港口的英文名各處寫法不一，或用了上游資料裡錯配的英文名。
- 切成英文後側欄圖層名稱太長，把面板撐寬。
- 介面是中文，底圖地名卻是英文（或反過來）。

## 原因
- 中文字串同時是「顯示文字」和「識別字」（圖層名、主題名、選項值）；在來源處改掉，相依的網址、搜尋與測試跟著壞。
- 沒有統一的退回規則，缺翻譯的 key 就顯示成空白或 key 本身。
- 上游資料集的英文欄位品質不一，有些依縣市硬湊、對錯對象。
- 英文名通常比中文長數倍；底圖樣式的語言設定與介面語系是兩條線。

## 解法
1. 只在顯示層翻譯：介面文字一律用 `t("key")`；資料與設定裡的中文保持為正本與識別字，顯示時以中文原文查對照表取外文。URL 參數、元件狀態值、AI 讀的字串不翻。
2. 查不到就退回原文：順序為「該語系翻譯 → 資料既有外文欄位 → 中文原文」，翻譯可分批上線。
3. 只翻不太會變的內容（站名、線名、機場港口、行政區名、機關名、授權類別）；新聞、警報、即時事件內文不翻或標示「原文」。要機器翻譯就在資料收集端做並標示。
4. 地名用官方來源以腳本產生對照表（政府公布的英譯或羅馬拼音檔；代碼、名稱、連寫三種 key）；升格改名、缺代碼、缺筆的地方在腳本內補正並註明，重產時不要拿掉。
5. 上游外文欄位先抽查再用，只採用可信的子集。
6. 長字版面先定規則：中文主名不換行、不縮；外文副標空間不夠時只省略外文（`text-overflow: ellipsis`）；會切換長度的按鈕給固定或最小寬度。右到左語言要另外處理 `dir="rtl"` 與版面鏡像，成本高，真的需要再做。
7. 語言偵測順序：`?lang=` → 使用者上次選擇 → `navigator.languages` → 預設語言；分享網址只在非預設語言時帶 `lang=`（canonical 與 hreflang 見 [11-02](11-02-robots-sitemap-soft404-canonical.md)）。
8. 底圖地名跟著語言：Mapbox 樣式用 `language` 選項與 `setLanguage`（只重抓圖磚、不重載樣式）；MapLibre 搭 OpenFreeMap 等向量樣式，改樣式的 `text-field` 用對應語言欄位（[02-05](../02-basemaps/02-05-style-customization-by-code.md)）。

## 怎麼偵測
- 通用：切成 `?lang=en` 後，側欄或 popup 還有中文；某些地方顯示 key 名稱；分享英文頁的連結打開變中文；長英文名把面板撐寬；底圖地名語言與介面不一致。
- 搜尋：`t\(` 的參數是變數且該變數也用在 URL 或 store key（any）。
- 搜尋：JSX 內直接寫中文字面值 `>[一-鿿]` 出現在已宣稱翻完的元件（React）。
- 搜尋：`new (mapboxgl|maplibregl)\.Map\(` 沒有 `language`／沒有對 `text-field` 做語系切換，而站有多語介面（mapbox-gl、maplibre）。
- 搜尋：外文欄位直接取 `name_en` 顯示，沒有退回中文（any）。

## 出處
- i18next 等函式庫的 fallback 機制文件；Mapbox GL JS `language` 選項與 `setLanguage`；MDN `navigator.languages`、`text-overflow`；政府公布的地名英譯／羅馬拼音資料（台灣為內政部）。
- 相關卡：[02-05](../02-basemaps/02-05-style-customization-by-code.md)、[09-08](../09-design-system/09-08-text-hierarchy-dark-basemap.md)、[11-02](11-02-robots-sitemap-soft404-canonical.md)。
- 實例（mini-taiwan-pulse）：[多語系路線圖](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/i18n/ROADMAP.md)、[地名對照表產生腳本](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/scripts/i18n/gen-place-names.ts)。

