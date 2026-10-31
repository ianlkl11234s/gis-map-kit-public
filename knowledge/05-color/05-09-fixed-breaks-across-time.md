---
id: 05-09
title: 分級門檻要跨期固定，不要隨當次資料重算 quantile
topic: 05-color
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [分級, breaks, quantile, 跨期比較, choropleth, 門檻, 時間序列, 顏色語意漂移]
---

## 原則
同一指標在所有期別使用同一組人工決定的門檻，把門檻當成跨期、跨圖的比較契約；只有單一時間點、無跨期需求的圖層才可用資料自適應門檻。

## 症狀
- 拖動時間滑桿或切換年份後，同一個顏色在不同年份代表的數值不同；使用者以為某區域「變深＝變多」，其實只是當年門檻重算了。
- 不同指標、不同期別之間無法比較。

## 原因
每次載入資料都用 quantile／自然斷點重新切級。好處是每張圖都五顏六色，代價是顏色失去跨期、跨圖的語意。

## 解法
1. 門檻是比較契約：同一指標所有期別用同一組門檻，圖例分界數字也固定。
2. 門檻由人決定（取整、貼近人類可理解的量級），並記錄依據（例如參考分位數 p75、p95、max）。
3. 某年資料超出範圍時，用最後一級承接（「> N」），不要自動再切一級。
4. 真正需要改門檻（資料分布改變）時，視為 breaking change：寫理由、評估對跨期比較的影響、更新所有受影響圖層與歷史快照。
5. 單一時間點且無跨期需求（例如一次性分析結果）才可用 quantile 或自然斷點，並在圖例標明方法。
6. 發散色階的門檻必須對稱於基準（例如 [-a, -b, 0, b, a]），0 是邊界而不是一級顏色。
7. 色票數至少是門檻數 + 1，重複門檻合併後地圖與圖例同步（見 [05-08](05-08-legend-key-mismatch.md)）。

## 怎麼偵測
- 通用：時間序列圖層在不同年份看圖例，分界數字是否變動；圖例沒有分界數字。
- 搜尋：`quantile|percentile|ckmeans|jenks|d3.scaleQuantile|simple-statistics` 出現在載入資料後的 hook 或 loader（適用 stack：any）；Mapbox expression 的 `step` 門檻由 runtime 計算而不是常數表。

## 出處
- 製圖學標準做法：跨圖比較要用相同分級（等距、固定門檻）；分位數分級只適合單張圖的內部比較。
- 相關卡：[05-08](05-08-legend-key-mismatch.md)、[06-14](../06-data-formats/06-14-statistics-layer-source-overview-and-comparability.md)。
- 實例：[統計圖層規則 §4（分級門檻屬比較契約）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/statistics-layer-guidelines.md)、[日本人口網格（7 級跨年份固定）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/jpPopulationMeshModes.ts)、[都市形態網格（依 p75／p95／max 取整的固定門檻）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/urbanFormGridTypes.ts)。
