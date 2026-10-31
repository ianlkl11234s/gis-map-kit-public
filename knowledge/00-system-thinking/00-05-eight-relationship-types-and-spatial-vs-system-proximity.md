---
id: 00-05
title: 八種關係型別，以及「空間近不等於系統近」
topic: 00-system-thinking
kind: decision
scope: public
evidence: General
stacks: [any]
tags: [關係型別, Tobler, 距離度量, 拓撲, 路網, 可達性, 流向, 依賴, 替代, 空間近, 地圖畫法]
---

## 原則
先判斷兩者之間是哪一種關係，再選距離度量與畫法；不要因為直線距離近就宣稱有關或有因果。

## 症狀
兩點直線距離很近就被說成「有關」：污染源與學校隔著山，風場不同；兩站直線近但中間有河，實際行車時間很遠；河流兩點直線很遠卻在同一條上下游路徑上。用單一距離（通常是歐氏距離）衡量所有關係。

## 原因
Tobler 地理學第一定律（近的事物傾向更相關）是理解空間自相關的起點，但不是任何情況下都能假設近就有因果。空間近不一定是系統近。要先確認作用機制，再選距離度量。

## 解法
先選關係型別，再選度量與畫法：

| 型別 | 核心問句 | 建議度量 | 建議畫法 |
|---|---|---|---|
| Metric proximity | 有多近？ | 歐氏或大圓距離 | buffer、距離標註；不畫成有向箭頭 |
| Topology | 接壤、交疊、包含？ | intersects／contains／adjacent | 疊合面、高亮交集 |
| Network connectivity | 有路連通嗎？ | 圖連通性（是否同一連通分量） | 實線網路，必要時雙向 |
| Flow direction | 沿什麼方向流？ | 上下游順序、流向 | 有向箭頭，標流動介質 |
| Accessibility | 多快到達？ | 路網旅行時間（非直線） | 等時圈、路徑 |
| Functional dependency | 誰依賴誰？ | 依賴鏈 | 由依賴方指向被依賴方，圖例交代 |
| Substitution / competition | 可替代或爭資源？ | 容量與替代條件 | 標明限定條件與容量 |
| Association / causal hypothesis | 共同出現或可能影響？ | 統計關聯；因果須機制與證據 | 虛線或獨立樣式，不可與因果同樣式 |

補充：
- 距離度量依機制選：歐氏、水文連通、道路網路時間、沿風向傳播。水庫與空氣污染是否有關，要看沉降、集水區等機制，不能只靠距離排除或斷言。
- 警察局與消防局放得近，不代表共享最佳服務位置；要測是否有共同可達性優勢，不能把共址當證據。
- Association 與 causal hypothesis 同一型別但語意不同；宣稱因果時才升級，並寫出機制。

## 怎麼偵測
檢查對象：圖台說明文字、分析方法段落、system map JSON、距離計算程式。
- 通用：結論是「靠近所以影響」，方法只有 buffer；可達性用直線距離；上下游關係用半徑圈起來。
- 搜尋（程式）：`ST_DWithin|buffer|turf\.(distance|buffer)`用在「影響|可達|暴露」論述且沒有路網或水文計算（適用 stack：PostGIS、turf.js）。
- 搜尋（JSON）：`relationship_type` 是 metric proximity 卻出現 `verb_label` 為 `causes|affects`。
- 搜尋（文字）：`附近.{0,6}(影響|導致|造成)`。

## 出處
- Tobler, W. R. (1970), "A Computer Movie Simulating Urban Growth in the Detroit Region", Economic Geography, 46, 234–240。
- Meadows (2008) Thinking in Systems。
- 八型別表是教學整理，非外部標準分類。

