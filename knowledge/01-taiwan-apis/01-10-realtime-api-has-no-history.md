---
id: 01-10
title: 即時 API 只給「現在」：要比較時間就得自己存快照，並防靜默斷供
topic: 01-taiwan-apis
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [快照, 歷史, collector, 覆寫, 靜默斷供, stale, 心跳, 新鮮度, 歸檔]
---

## 原則
要看歷史或比較時間，就自己排程存快照；抓取間隔不可長於上游覆寫間隔；畫面標出最後觀測時間，並用「連續空回應」告警區分「無事件」與「上游斷供」。

## 症狀
- 想做「昨天 vs 今天」才發現 API 只有最新值。
- 上游端點仍回 200，內容卻是空的，圖台悄悄變空，一個月後才發現。
- 圖面標示「即時」，實際資料已停在好幾小時前。
- 把抓取間隔設得比來源覆寫週期長，漏掉大部分批次。

## 原因
- 多數即時端點只保留最新一份或僅數小時。
- 監控只看「程序有跑」或「最後成功時間」（只在有寫入資料時更新），無法分辨「合法沒事件」與「上游斷供」。

## 解法
1. 需要歷史就排程抓取並存起來：每筆保存「上游觀測時間」與「收集時間」兩欄，用內容雜湊或事件 id 去重。
2. 熱資料放資料庫，冷資料歸檔到物件儲存。
3. 抓取間隔 ≤ 上游覆寫間隔。
4. 畫面標出「最後觀測時間」；超過約 3 倍更新間隔顯示 stale，不要顯示成正常。
5. 0 筆時分辨「無事件」與「斷供」：連續 N 次空回應告警，或用第二資料源交叉驗證；歸檔檔案大小連續相同也是停供訊號。
6. 新鮮度以資料內的觀測時間判斷，不以 API 的 UpdateTime 或「傳輸 ready」判斷。
7. 學生／原型版：不寫 collector，課前手動存 3–5 個時間點快照，並在畫面標抓取時間。
8. 沒有官方歷史的資料（如逐年覆寫的清單），自己定期存快照；補歷史用網頁封存時要標明。

## 怎麼偵測
- 通用：圖層宣稱即時但沒有時間標示；監控沒有「連續空回應」規則；資料表最新一筆時間遠早於現在。
- 搜尋：`last_success|heartbeat`（只在寫入成功時更新）；沒有 `stale|observed_at|最後更新` 之類欄位（適用 stack：any）。

## 出處
- 一般建議：快照與新鮮度顯示為通用做法。
- 相關卡：[01-02](01-02-cwa-integration.md)、[01-13](01-13-time-zone-and-update-time.md)。
- 實例：[多來源同時斷供、28 天沒人發現](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/pitfalls/2026-08-07-silent-upstream-outage.md)；[collector 架構（短期保留、每日歸檔）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/ARCHITECTURE.md)；[落雷整檔覆寫、每批只存 60 秒](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/config.py)。
