---
id: 07-13
title: 載入狀態也是功能：每個非同步請求都要有 loading／error，且用測試守住
topic: 07-performance
kind: pitfall
scope: public
evidence: Implemented
stacks: [any]
tags: [loading, error, 載入中, 靜默失敗, 守門測試, ratchet, 豁免, 空白地圖, 使用者感受速度]
---

## 原則
每個非同步資料請求都要註冊 loading 與 error 狀態，並寫一個會紅燈的守門測試；規則只寫在文件裡等於沒有。

## 症狀
- 使用者看著空白地圖，分不出「在載入」還是「沒有資料」。
- 資料請求失敗，畫面毫無反應。
- 規則寫在文件裡三個月，仍有新的 fetch 沒有 loading。

## 原因
資料最後多半會出來，「載入中」看起來只是裝飾；漏接的後果不是壞掉，而是信任默默流失，永遠不會有人回報。規則沒有守門機制就會被遺漏。

## 解法
載入註冊表、三態（載入中／失敗＋重試）與顯示節奏的做法見 [09-07](../09-design-system/09-07-loading-data-time-and-stale.md)。本卡只留守門：
1. **守門測試**：掃描所有 loader／RPC 呼叫，檢查前後幾行有沒有 loading 包裝；例外（背景預取、popup 內小圖）登記在豁免清單並寫理由。
2. 同類守門（lint 基準只降不升、圖層登記表完整性）見 [09-01](../09-design-system/09-01-token-ssot-and-ratchet-guard.md)；規則要變成會紅燈的測試才會被遵守。

## 怎麼偵測
- 通用：切換圖層／日期時畫面無任何提示；故意把網路斷線看是否有失敗訊息。
- 搜尋：`\.rpc\(|fetch\(` 的呼叫前後 10 行沒有 `withLoading|setLoading|isLoading`（適用 stack：任何前端）。

## 出處
- Nielsen 的系統狀態可見性原則。
- 相關卡：[09-01](../09-design-system/09-01-token-ssot-and-ratchet-guard.md)、[09-07](../09-design-system/09-07-loading-data-time-and-stale.md)。
- 實例：[mini-taiwan-pulse 載入守門測試](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/__tests__/loadingRegistryContract.test.ts)、[載入狀態登記](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/lib/loadingRegistry.ts)、[開發規則](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/development-rules.md)。
