---
id: 05-08
title: 圖例與地圖顏色對不上：色票必須與渲染同源，且只描述畫面
topic: 05-color
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [圖例, legend, 同源, 色票, 分類, 漏寫, 門檻, breaks]
---

## 原則
圖例的顏色、門檻、標籤必須和地圖渲染 import 同一份常數，圖例只描述畫面真正有的差異；每個以顏色或大小編碼資料的圖層都要有圖例。

## 症狀
- 圖例色票的色號和地圖實際顏色差一點，肉眼比對總覺得「怪怪的」。
- 暗淡底圖切換後，地圖換了色，圖例沒換。
- 圖例列出了地圖上分不出來的類別，或一個語意根本不存在的分類（因為「多色看起來比較專業」）。
- 新增類別／色階時只改了地圖，漏改圖例；或分類 ≥ 2 的圖層完全沒有圖例。
- 色階有 n 個門檻，圖例卻少一色或多一色。

## 原因
地圖的 paint expression、popup 的色點、圖例的色票各自手抄一份色號。圖例被當成「宣稱資料」而不是「描述畫面」。

## 解法
1. 單一資料源：顏色、門檻、標籤抽成一份常數，地圖的 paint、圖例、popup 色點都 import 同一個常數；禁止在圖例檔案手寫色號。
2. 暗淡底圖不同色時，圖例依目前主題取同一邊的常數。
3. 色票至少要有 `breaks.length + 1` 色；重複門檻合併後，地圖與圖例使用同一份合併結果。
4. 圖例只描述畫面真正有的差異：渲染端沒有這個語意（例如單純輪替配色）就不要編造分類；條件限定的編碼（只在某模式出現）要帶顯示條件。
5. 所有「顏色或大小有編碼資料」的圖層都必須有圖例；單色圖層可省略，但要明確登記豁免理由，不能用 null 靜默跳過。可用測試守門：圖層登記表的每個條目都宣告圖例，並與圖例登記比對。
6. 圖例的結構、色票型態與收合規則（色階、分界、單位不可收）見 [09-04](../09-design-system/09-04-legend-spec.md)。
7. 缺值與遮蔽必須有圖例項（見 [05-04](05-04-null-is-not-zero-color.md)）。

## 怎麼偵測
- 通用：把圖例色票吸色與地圖同一級的色塊比對；切換底圖看圖例是否跟著變。
- 搜尋：圖例檔案內出現 `#[0-9a-fA-F]{6}` 字面值而不是 import 的常數；`legend: null`／`NO_LEGEND` 清單；paint 裡的 `match|step` 與圖例是兩份獨立陣列（適用 stack：any，程式結構問題）。

## 出處
- 地圖製圖慣例：圖例應完整描述地圖符號。
- 相關卡：[05-04](05-04-null-is-not-zero-color.md)、[09-04](../09-design-system/09-04-legend-spec.md)（圖例元件規格）、[05-09](05-09-fixed-breaks-across-time.md)。
- 實例：[圖層樣式規範 §4.3（圖例與圖層樣式不一致的盤點與對齊）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/map-layers.md)、[專案原則「圖例不憑空發明分類」](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/PRINCIPLES.md)、[開發規則 §4a（圖例鐵則）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/development-rules.md)。
