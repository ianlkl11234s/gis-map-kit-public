---
id: 10-11
title: 保留期要有註冊表、歸檔刪本地前先驗證遠端：上游滾動視窗今天不存就沒了
topic: 10-ops
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [retention, 保留期, 歸檔, 冷備份, S3, lifecycle, 原始回應, 分區表, 容量]
---

## 原則
每張表的保留期登記在一份註冊表，歸檔先把遠端讀回驗證才刪本地；依賴上游滾動視窗的資料，每次都存原始回應。

## 症狀
- 資料庫一路長到幾十 GB，原因是新增的分區表沒人登記清理。
- 清理函式只刪「正好等於今天減 N 天」那一天，漏跑一次就永遠清不回來。
- 歸檔任務靜默失敗一個月，沒人發現。
- 想回補歷史才發現當時沒存原始回應，上游只給最近 N 則。

## 原因
「先存起來再說」沒有設計保留期；清理清單寫死在函式裡，新表會漏；歸檔上傳「成功」不等於遠端內容完整。

## 解法
1. **保留期註冊表是唯一正本**：新表只要 INSERT 一列；永久保留要明寫 NULL（表示刻意）。保留天數下限＝前端實際回看窗口再加 margin。
2. 清理用範圍條件（`< now() - N days`），不是等值。
3. 提供覆蓋率檢查函式，但「0 缺口」不代表全部有登記；DELETE 不會把磁碟還給 OS，要另外 VACUUM／回收。
4. **冷歸檔**：每天把前一天的本地檔打包上傳物件儲存；**刪本地前把遠端讀回驗證並寫 receipt**；物件儲存不設 expiration，用 lifecycle 轉冷層；每天打包成一個檔（物件數比容量貴）。日報加歸檔心跳與 retention 覆蓋區塊。
5. **依賴上游滾動視窗的資料，今天不存就永久少一天**：每次抓即時 API 都存原始回應（`raw/YYYY-MM-DD_HHmm.json`），加工結果另存。

## 怎麼偵測
- 通用：資料庫大小持續成長；新表上線 PR 沒有 retention 變更；歸檔腳本沒有「驗證後才刪」的步驟。
- 搜尋：清理函式內寫死表名清單；`DELETE .* WHERE .* = ` 等值日期條件；歸檔腳本中 `rm|unlink|os.remove` 出現在上傳之後但沒有 verify（適用 stack：any）。

## 出處
- AWS S3 storage classes／lifecycle 文件（用前查）。
- 實例：[operations.md（歸檔任務與保留期運維）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/handbook/operations.md)、[README.md（每日打包上傳與生命週期設定）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/README.md)。

