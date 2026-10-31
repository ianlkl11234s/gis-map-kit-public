---
id: 10-18
title: 有些任務只能單一實例跑：搬家與擴展時，先停舊的再開新的，並帶走尚未上傳的本地狀態
topic: 10-ops
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [單一實例, 雙寫, manifest, 緩衝, spool, 搬遷, 擴展, 鎖, 互斥]
---

## 原則
搬家或擴展前先盤點「只能單一實例的任務」與「尚未上傳的本地狀態」；先停舊的、搬狀態、再開新的，並在設定載入時檢查互斥旗標。

## 症狀
- 新舊兩台同時跑，共用的 manifest 被寫壞、append-only 表雙寫。
- 搬家後少了一段資料，因為本地緩衝（尚未上傳的批次、狀態檔）沒帶走。

## 原因
平常只有一台，沒人去想「新舊兩邊同時跑」；任務的互斥性只存在人的腦中，沒有寫進設定。

## 解法
1. 盤點兩份清單：**只能單一實例的任務**（會寫共用 manifest、發布單一產物、append-only 寫入）、**尚未上傳的本地狀態**（buffer、狀態檔、spool）。
2. 切換順序：舊的先停（含確認舊處的旗標設為關閉）→ 搬狀態 → 新的再開。已搬走的任務在舊處維持停用。
3. **程式端守門**：設定載入時檢查互斥旗標（新舊兩種發布不得同時開啟），衝突就啟動失敗。
4. 寫不進資料庫時資料先進 buffer 再重放；但會讓舊值蓋過新值的寫入不進 buffer。

## 怎麼偵測
- 通用：搬遷文件缺「單一實例清單」與「本地狀態清單」。
- 搜尋：環境旗標（`*_ENABLED`）互斥關係沒有在 config 載入時驗證；volume 內有 `buffer|spool|state.json` 但未列入備份或搬遷清單（適用 stack：any）。

## 出處
- 一般分散式任務互斥實務。相關卡：[10-13](10-13-migration-and-domain-cutover.md)。
- 實例：[config.py（新舊兩種發布旗標不得同時開啟，載入時檢查）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/config.py)。

