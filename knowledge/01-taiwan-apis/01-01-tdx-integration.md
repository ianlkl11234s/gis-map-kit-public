---
id: 01-01
title: TDX 接法：OAuth token、全域節流、站牌 ID 與更新時間的坑
topic: 01-taiwan-apis
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [TDX, 公車, YouBike, 台鐵, 國道, OAuth2, 429, StationUID, LastUpdateTime, 節流]
---

## 原則
同一把 TDX 金鑰的所有呼叫（含取 token）走同一個全域節流器；token 與 secret 只放後端；跨縣市 join 用 `StationUID`／`RouteUID`；新鮮度看資料本身的觀測時間，不看 `LastUpdateTime`。

## 症狀
- 多個城市／多支程式同時呼叫後大量 429，甚至 401 與 429 一起出現。
- 公車站牌用 `StationID` join，不同縣市的站撞在一起。
- 用 `LastUpdateTime` 判斷「事件有沒有變」，結果多數是假刷新。
- 資料裡出現 (0,0) 座標的點。

## 原因
- TDX 限流以「金鑰」為單位；取 token 的請求也算次數，token 端點本身另有每 IP 每分鐘上限（官方 SampleCode 說明）。多個程式共用同一把金鑰又各自節流，等於沒有節流；整分鐘同時 burst 更容易爆。
- `StationID` 只在單一城市內唯一；跨縣市要用 `StationUID`。
- `LastUpdateTime` 是 API 快取刷新時間，不是事件實際變動時間。

## 解法
1. 先到 tdx.transportdata.tw 註冊會員、經管理員審核，取得 Client Id／Secret 換 token；不帶 key 呼叫會回 401「Valid API Key Required」（2026-11-02 實測）。審核時間官方未寫，課堂使用要提前辦。後端取得 token 並快取到期前重用；前端永遠不碰 client secret（見 [01-08](01-08-token-secret-throttle-backoff.md)）。
2. 同一把金鑰的所有呼叫走同一個全域節流器（例如每秒 4 次），429／401 分開處理，做法見 [12-12](../12-domain-pitfalls/12-12-upstream-blocking-rate-limits.md)。
3. 站牌、路線 join 用 `StationUID`／`RouteUID`，不要用城市內才唯一的 ID。
4. 新鮮度看資料本身的觀測時間，不看 API 的 UpdateTime。
5. 座標做範圍檢查，丟掉 (0,0)。
6. 官方每秒／每日額度與免費方案數字官方原文未取得（官方說法是「依訂閱方案而定」），不要自己補數字。

## 怎麼偵測
- 通用：日誌連續 429；多支排程各自 `sleep`；跨城市 join 後筆數暴增；站點有 (0,0)。
- 搜尋：`StationID`（且附近沒有 `StationUID|city`）、`LastUpdateTime|UpdateTime`（被用來判斷新鮮度）、`client_secret` 出現在前端目錄（適用 stack：any）。

## 出處
- 官方：github.com/tdxmotc/SampleCode（呼叫限制說明）。
- 相關卡：[01-08](01-08-token-secret-throttle-backoff.md)、[12-12](../12-domain-pitfalls/12-12-upstream-blocking-rate-limits.md)。
- 實例：[TDX 限流事故紀錄](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/TDX_RATE_LIMITING.md)、[修正 commit（全域節流器）](https://github.com/ianlkl11234s/gis-data-collectors/commit/15bd11ee16ad20d887a9939aa88edf978c0c0b1f)；[公車夜間暫停](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/BUS_NIGHT_PAUSE.md)；[StationID 跨城市撞號](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/simulation/PLAN.md)。

