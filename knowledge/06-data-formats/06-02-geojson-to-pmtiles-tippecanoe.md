---
id: 06-02
title: GeoJSON 轉 PMTiles：流程與 tippecanoe 參數的三個坑（polygon 變色塊、tile 過重、圖層沒畫）
topic: 06-data-formats
kind: pattern
scope: public
evidence: Evaluated
stacks: [any]
tags: [PMTiles, tippecanoe, coalesce, no-tiny-polygon-reduction, buffer, drop-densest, 低 zoom, 色塊, tile 大小]
---

## 原則
polygon 轉 PMTiles 一律加 `--no-tiny-polygon-reduction`，點位用 `--buffer` 控制單磚大小而非抽稀；上線前確認 Range 請求回 206，轉檔後與原始比對 feature 數。

## 症狀
- polygon 轉 PMTiles 後，低 zoom 變成整片實心色塊，細節消失。
- 檔案很大，或低 zoom 單一圖磚下載、解壓特別重，拖曳卡頓、風扇狂轉。
- 圖層開了但完全沒畫，Network 沒有明顯錯誤。

## 原因
- tippecanoe 對 polygon 預設會合併相鄰面（coalesce），並把小於 1 像素的 polygon 換成占位方塊。
- 圖磚的 buffer 預設較大：低 zoom 時每個 tile 會帶入鄰近大量重複的點，單 tile 可大到數 MB 以上。
- 圖層「沒畫」常是後續 Range 請求沒有發生（見 [06-03](06-03-gzip-breaks-range-requests.md)），不是樣式問題。

## 解法
1. 流程：GeoJSON → tippecanoe → `.pmtiles` → 放到支援 HTTP Range 的儲存 → 前端註冊 pmtiles protocol → 圖層指向該檔。
2. **polygon**：加 `--no-tiny-polygon-reduction`；不要使用 `--coalesce-densest-as-needed`（它只適合 line）。
3. **點位且「不可抽稀」**：不要靠 `--drop-densest-as-needed`；改調 `--buffer`（只要 ≥ 最大點半徑所需的像素），同樣點數可大幅縮檔。
4. **大面積覆蓋面（等時圈、土地利用）**：一開始就走 PMTiles，不要先走 GeoJSON 簡化；簡化後邊界鋸齒、不簡化 pan 卡，兩頭不討好。必要時先 dissolve／concave 再切。
5. 純 line／fill 仍用 GeoJSON source 時，可調 source 的 `tolerance`、`buffer` 當折衷。
6. 上線前驗證：(a) `curl -r 0-16383` 回 206；(b) 看 access log 有 header 之後的 range 請求；(c) 低 zoom 單 tile 解壓大小。
7. 轉檔結果要和原始比對（feature 數、各 zoom 點數），確認沒被默默抽稀。

## 怎麼偵測
- 通用：低 zoom 出現整島色塊；縮到最小仍載入數 MB 的單一 tile；PMTiles 檔大小遠超原 GeoJSON。
- 搜尋：`tippecanoe.*(-Z|-z)` 的指令列（腳本或 Makefile）沒有 `no-tiny-polygon-reduction` 而來源是 polygon；同一行出現 `coalesce-densest-as-needed` 且來源是 polygon（適用 stack：mapbox-gl、maplibre）。

## 出處
- 官方：tippecanoe README（參數說明）。
- 相關卡：[06-03](06-03-gzip-breaks-range-requests.md)、[06-01](06-01-format-selection-decision.md)。
- 實例：[mini-taiwan-pulse 事故紀錄（polygon 低 zoom 變整島色塊；大面積等時圈 GeoJSON 的兩難）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)；[效能盤點（點位檔 `--buffer=64→8`，三檔 124／103／128 MB 降到 70／57／72 MB，點數不變）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/audit/perf-audit-2026-09-30.md)。

