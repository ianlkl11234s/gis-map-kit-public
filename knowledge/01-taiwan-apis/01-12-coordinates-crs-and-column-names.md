---
id: 01-12
title: 座標系與欄名不可信：TWD97/WGS84、經緯度互換、單位錯誤
topic: 01-taiwan-apis
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [座標系, TWD97, EPSG:3826, WGS84, 經緯度互換, bbox, 單位, 英呎, prj, 編碼, BOM, cp950]
---

## 原則
載入政府資料後一律先算全部點的 bbox，落在台灣範圍外就停下回報，不自動交換欄位；前端只用 WGS84，轉換在預處理階段完成。

## 症狀
- 點全掉到海裡、赤道附近、或別的國家。
- 離島資料整批偏移約 2 度。
- 高度、胸徑等數值整個被壓扁或放大。
- CSV 讀進來亂碼，或第一個欄名多了看不見的字元。

## 原因
- 欄名騙人：寫 TWD97 的其實是 WGS84，寫 WGS84 的其實是公尺；經緯度兩欄互換；公尺值誤填進經緯度欄。
- 政府資料常是 EPSG:3826，`|X| > 1000` 就是公尺座標。
- SHP 沒有 .prj；GML 沒標 CRS。
- 單位混用（英呎／公尺）。
- 編碼：cp950（Big5）、UTF-8 BOM。

## 解法
1. 載入後算全部點的 bbox，台灣本島約經度 119–122、緯度 21–26；落在外面就停下回報，不自動交換欄位。
2. 判斷規則：值為數十萬以上＝公尺（TWD97）；經緯度互換＝落在別的國家。
3. 前端一律使用 WGS84（EPSG:4326），轉換在預處理階段完成。
4. 無 .prj 時用面積或已知地標交叉驗證投影。
5. 單位在落地時無條件轉換並留 marker，避免遷移不冪等。
6. 編碼：以 `utf-8-sig` 讀 BOM；cp950 檔名要明確指定。
7. 非台灣資料不要假設有 TWD97 欄位。

## 怎麼偵測
- 通用：圖層在海上或空白；點數少於資料列數（parse 失敗被丟）。
- 搜尋：`twd97|3826|EPSG:3826`（旁邊沒有轉換）；`parseFloat.*(lon|lat)` 沒有範圍檢查（適用 stack：any）。

## 出處
- 官方：EPSG:3826（TWD97 / TM2）、EPSG:4326（WGS84）為標準定義。
- 相關卡：[01-03](01-03-moenv-integration.md)、[01-06](01-06-nlsc-ris-boundaries-population.md)。
- 實例：[圖層接線常見遺漏（座標系統沒轉）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/pitfalls/2026-07-01-layer-integration-common-misses.md)。

