---
id: 06-00
title: 資料格式與處理總表：選格式、PMTiles、快取、瘦身、契約、口徑、向量場、ID、路網、動態圖磚
topic: 06-data-formats
kind: catalog
scope: public
evidence: Observed
stacks: [any]
tags: [總表, 資料格式, PMTiles, 快取, 瘦身, 資料契約, 口徑, 向量場, ID, 路網, MVT, 統計圖層]
---

## 原則
先問資料會不會變、量大不大、要不要依條件查詢，再選格式；靜態只顯示用 PMTiles，會變或要查詢才用動態圖磚。上線後的空白、對不上與口徑問題，先查下表對應的卡。

## 對照表

### 選格式與 PMTiles
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 不知道用 GeoJSON、PMTiles 還是動態查詢 | [06-01](06-01-format-selection-decision.md) | 先答三問（變不變、量多大、要不要查詢），量用 DevTools 實測；不因格式新就選它 |
| GeoJSON 轉 PMTiles | [06-02](06-02-geojson-to-pmtiles-tippecanoe.md) | polygon 加 `--no-tiny-polygon-reduction`，點位用 `--buffer` 控制單磚大小；確認 Range 回 206，轉檔後比對 feature 數 |
| PMTiles 本機正常、上線沒有點 | [06-03](06-03-gzip-breaks-range-requests.md) | PMTiles 路徑關閉 gzip；部署後用 Range 請求確認回 206 才宣告上線 |

### 快取與瘦身
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 設長期快取、部署後仍是舊檔 | [06-04](06-04-cache-immutable-404-and-stale-edge.md) | 只有 URL 對應永不改變內容的檔才設 immutable，內容變就換檔名；部署完成前探測新 URL 加 cache-buster |
| 檔案太大要縮 | [06-05](06-05-shrink-geometry-precision-simplify-columns.md) | 依序：刪欄位 → 截精度 → 傳輸壓縮 → 保拓撲簡化 → 才換格式，每步量大小；換格式的檔案大小起點門檻在這張；簡化後量距離要先 Segmentize |

### 資料契約與口徑
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 0、null、未涵蓋、過期混在一起 | [06-06](06-06-zero-null-stale-data-contract.md) | 五者分開表示，不對觀測值用 0 兜底；匯出的 JSON 必須嚴格合法 |
| 比率、加總、兩來源相加 | [06-07](06-07-ratio-denominator-and-double-counting.md) | 比率寫明分子分母並用官方值抽驗；聚合前確認沒有疊檔、多來源、多層級，指定單一口徑 |
| 輸出是推估或模擬 | [06-08](06-08-label-estimates-and-models.md) | 圖層名、圖例、文字都標「推估」「模擬」，人數寫範圍，至少用替代參數驗證結論 |
| 統計圖層新增或切換指標 | [06-14](06-14-statistics-layer-source-overview-and-comparability.md) | 同一 PR 更新資料來源總覽；切換只配對同期別、同維度選項，找不到顯示「不可用」 |

### 向量場
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 風、海流格點要上圖 | [06-09](06-09-bake-vector-field-to-png.md) | 離線烘成無損 PNG：R＝u、G＝v、alpha＝有效遮罩，min／max 寫進 metadata，前端 CPU 雙線性取樣 |

### 欄位與 ID
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 圖層長期靜默空白 | [06-10](06-10-loader-column-mismatch-silent-blank.md) | 接完圖層一定實際開啟看到點才算完成；catch 不可只 warn，空結果與失敗要分開 |
| join 多縣市、多系統資料 | [06-11](06-11-id-not-unique-across-scopes.md) | 先比 `count(*)` 與 `count(distinct key)`；不唯一改用全域唯一欄位或複合鍵，代碼當字串 |

### 路網記憶體
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|

### 動態圖磚
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|

## 相關主題
- 依數量級與縮放選畫法：[14-02](../14-scale-density/14-02-point-count-thresholds.md)、[14-07](../14-scale-density/14-07-moving-objects-and-trails-at-scale.md)。
- 自託管 PMTiles 底圖與地形：[02-09](../02-basemaps/02-09-self-hosted-pmtiles-basemap.md)、[02-10](../02-basemaps/02-10-dem-terrain-rgb-encoding-and-bathymetry.md)。

## 出處
各項依據見對應卡片。
