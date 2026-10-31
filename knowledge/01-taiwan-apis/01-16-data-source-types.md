---
id: 01-16
title: 資料來源六類：直接取得三類、加工產生三類，各自要先確認什麼
topic: 01-taiwan-apis
kind: catalog
scope: public
evidence: Implemented
stacks: [any]
tags: [資料來源, 開放資料, 縣市拼接, OSM, collector, API 收集, 行政區統計, choropleth, 衛星影像, 航照, 影像辨識, YOLO, 都市熱島, 地表溫度, Landsat]
---

## 原則
拿到一份資料先判斷它屬於哪一類，再照那一類的檢查項驗證。直接取得的資料要驗來源、授權、時間；加工產生的資料還要寫出方法、參數與限制，不能畫成實測。

## 症狀
- 不知道某個主題該去哪裡找資料，或找到之後不知道該先檢查什麼。
- 各縣市拼成全國的圖層，有的縣市點位飄到海上，有的縣市整片空白。
- 即時 API 接上了，卻做不出「過去一週」的回放。
- 衛星或模型算出來的圖層被讀成實測值，或拿去跟其他地區直接比。

## 原因
- 六類資料的取得方式、授權、時間語意與誤差來源都不同，一套檢查項無法涵蓋。
- 加工產生的資料，結果取決於方法與參數；沒寫出來，讀者就無從判斷能不能比較。

## 解法
先分類，再照該類的檢查項做。

**一、可以直接取得的資料**

| 類別 | 從哪裡拿 | 先確認 | 相關卡 |
|---|---|---|---|
| 1a 開放資料：全國一份 | data.gov.tw、部會平台（TDX、氣象署、環境部、水利署、國土測繪中心） | 授權、資料時間、座標系、欄位定義 | [01-00](01-00-platforms-overview.md)、[01-05](01-05-data-gov-tw-and-license.md)、[01-12](01-12-coordinates-crs-and-column-names.md)、[01-13](01-13-time-zone-and-update-time.md) |
| 1a 開放資料：各縣市分開、要拼成全國 | 縣市開放資料平台，逐縣市下載後合併 | 各縣市座標系（TWD97／WGS84 混用）、編碼（cp950）、欄名與代碼、更新時間不同；ID 跨縣市撞號；缺的縣市標「未涵蓋」 | [01-07](01-07-local-and-other-platforms.md)、[01-12](01-12-coordinates-crs-and-column-names.md)、[06-11](../06-data-formats/06-11-id-not-unique-across-scopes.md)、[16-08](../16-spatial-analysis/16-08-geometry-quality-flags-before-analysis.md) |
| 1b OSM | Geofabrik 區域 PBF（記快照日期）、Overpass（查一次存檔，不要每次載入頁面都打） | ODbL 標示「© OpenStreetMap contributors」；完整度不均，沒畫上去不代表不存在；不要跟官方名冊直接合併 | [02-03](../02-basemaps/02-03-osm-data-license-vs-tile-policy.md)、[02-07](../02-basemaps/02-07-attribution.md)、[06-12](../06-data-formats/06-12-national-osm-road-network-memory.md) |
| 1c 要打 API 持續收集 | 即時 API（例如 TDX 公車、AIS），用常駐收集程式定時存檔 | 即時 API 沒有歷史，回放要靠自己存的快照；配額與限流；保存期與歸檔；上游靜默斷供 | [01-08](01-08-token-secret-throttle-backoff.md)、[01-10](01-10-realtime-api-has-no-history.md)、[01-14](01-14-semantics-drift-and-upstream-loss.md)、[12-12](../12-domain-pitfalls/12-12-upstream-blocking-rate-limits.md) |

**二、需要進一步分析才產生的資料**

| 類別 | 怎麼產生 | 先確認 | 相關卡 |
|---|---|---|---|
| 2a 以行政區為單位的統計 | 點位或名冊依行政區彙總，或直接取用官方的鄉鎮、村里統計 | 分子、分母、年份寫清楚；縣市值不可複製到鄉鎮；行政區改制前後的代碼要對照；換尺度結論可能翻轉 | [06-07](../06-data-formats/06-07-ratio-denominator-and-double-counting.md)、[06-14](../06-data-formats/06-14-statistics-layer-source-overview-and-comparability.md)、[16-02](../16-spatial-analysis/16-02-location-quotient-and-ratio-metrics.md)、[16-03](../16-spatial-analysis/16-03-cross-scale-maup.md)、[16-07](../16-spatial-analysis/16-07-skewed-sums-extreme-values.md) |
| 2b 衛星／航照／CCTV 影像跑模型辨識，甚至重建路口 | 物件偵測模型（YOLO、RF-DETR、Grounding DINO 等）辨識車輛、建物；再從正射影像畫車道、停止線重建路口（路口重建為作者實作中，尚無精度結果） | 模型授權（YOLO 系列為 AGPL-3.0，商用要改用 Apache 2.0 的模型）；正俯視與夜間畫面的召回率可能極低，要先用人工標註抽樣量精度；影像本身的授權與敏感區遮蔽 | [06-01](../06-data-formats/06-01-format-selection-decision.md)（影像格式）、[16-06](../16-spatial-analysis/16-06-reported-counts-not-occurrence.md) |
| 2c 都市熱島 | 衛星熱紅外波段反演地表溫度（例如 Landsat 8/9 Collection 2 Level-2），做雲遮罩、扣掉郊區背景，再跨多景取中位數 | 地表溫度不是氣溫；過境時間固定（Landsat 約上午 10 點半），不是全天；多雲山區的空白不代表沒有熱島；含海拔訊號，不能跨海拔直接比較 | [05-11](../05-color/05-11-raster-value-encoding-color-mix-pixel-sampling.md)、[05-12](../05-color/05-12-raster-value-pixel-sampling-and-nodata.md)、[08-05](../08-multi-layer/08-05-layer-stacking-order.md) |

做法：
1. 在 README 或來源摘要寫出這份資料屬於哪一類。
2. 直接取得類（1a–1c）：照表上的檢查項確認後，記錄機關、網址、授權、資料時間、座標系。
3. 加工產生類（2a–2c）：另外寫出方法、參數、時間範圍與已知限制；圖例或 popup 要標「推估」「模型辨識」等字樣。
4. 同一個圖層混用多類來源時（例如官方名冊加 OSM 補點），在欄位或圖例裡分開標示來源，不要合併成一個數字。
5. 2b、2c 若沒有自己量過精度，只能當探索用，不要拿來做排名或結論。

## 怎麼偵測
- 通用：README 只寫「資料來源：政府開放資料」而沒有分類與時間；拼接圖層沒寫涵蓋哪些縣市；模型或衛星推估的圖層沒有方法說明。
- 搜尋：`openstreetmap|overpass|geofabrik`，有命中但畫面上沒有 OSM 標示（適用 stack：any）。

## 出處
- TDX 服務條款：ptx.transportdata.tw/PTX/APIs/Terms；OSM 授權：osmfoundation.org/wiki/Licence；Landsat Collection 2 Level-2 地表溫度：USGS Landsat 產品說明。
- 實例：[統計圖層規則（分子、分母、年份）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/fa15f1672254164fed58398a921c01a1ddcd109a/docs/statistics-layer-guidelines.md)、[都市熱島圖層說明](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/fa15f1672254164fed58398a921c01a1ddcd109a/docs/features/urban-heat-lst/README.md)。

