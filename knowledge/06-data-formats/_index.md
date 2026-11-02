# 06-data-formats 資料格式與處理

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [06-00](06-00-data-formats-index.md) | 資料格式與處理總表：選格式、PMTiles、快取、瘦身、契約、口徑、向量場、ID、路網、動態圖磚 | 先問資料會不會變、量大不大、要不要依條件查詢，再選格式；靜態只顯示用 PMTiles，會變或要查詢才用動態圖磚。 | catalog | Observed | any | 總表, 資料格式, PMTiles, 快取, 瘦身, 資料契約, 口徑, 向量場, ID, 路網, MVT, 統計圖層 |
| [06-01](06-01-format-selection-decision.md) | 資料格式怎麼選：先問「會不會變、量大不大、要不要查詢」，再對照格式 | 首屏卡在下載一個幾十 MB 的 GeoJSON。 | decision | Implemented | any | GeoJSON, TopoJSON, MVT, PMTiles, FlatGeobuf, GeoParquet, COG, Arrow, 選型, 格式 |
| [06-02](06-02-geojson-to-pmtiles-tippecanoe.md) | GeoJSON 轉 PMTiles：流程與 tippecanoe 參數的三個坑（polygon 變色塊、tile 過重、圖層沒畫） | polygon 轉 PMTiles 後，低 zoom 變成整片實心色塊，細節消失。 | pattern | Evaluated | any | PMTiles, tippecanoe, coalesce, no-tiny-polygon-reduction, buffer, drop-densest, 低 zoom, 色塊, tile 大小 |
| [06-03](06-03-gzip-breaks-range-requests.md) | PMTiles 本機正常、上線一個點都沒有：伺服器 gzip 讓 Range 請求回 200 而不是 206 | 本機開發完全正常，部署後圖層空白，沒有 JS 錯誤。 | pitfall | Observed | any | PMTiles, Range, 206, gzip, nginx, content-range, CORS, 反向代理, 部署 |
| [06-04](06-04-cache-immutable-404-and-stale-edge.md) | 靜態資產快取三件事：換內容換檔名、部署前探測會種下 404、邊緣仍供舊檔 | 換了新資料檔，使用者（甚至部署後）仍看到舊資料，要等一天。 | pitfall | Observed | any | CDN, Cloudflare, immutable, cache-control, 404, negative cache, cache-buster, 內容雜湊, purge, Range |
| [06-05](06-05-shrink-geometry-precision-simplify-columns.md) | 檔案變小的順序：先刪欄位與多餘精度，再簡化，最後才換格式——簡化要留意拓撲與折返 | 靜態 JSON／GeoJSON 太大，首屏下載慢。 | pattern | Observed | any | 座標精度, 簡化, simplify, Douglas-Peucker, 拓撲, 欄位瘦身, gzip, topojson, 檔案大小, geography, 測地距離, ST_Segmentize |
| [06-06](06-06-zero-null-stale-data-contract.md) | 資料契約：0、null、「未涵蓋」、過期要分開表示，匯出的 JSON 還要是合法 JSON | 地圖上大片格子顯示 0，其實是「未測」或「該區沒有資料」。 | pitfall | Observed | any | null, 0, 缺值, 未測, stale, Infinity, NaN, 兜底, COALESCE, JSON.parse, 資料契約 |
| [06-07](06-07-ratio-denominator-and-double-counting.md) | 口徑誠信（一）：比率的分母要寫清楚，兩個來源描述同一現象不能直接相加 | 同一個指標，圖台算出的數字和官方網站差一大截（例如 12% 對 17%），使用者先懷疑 ID 對錯。 | pitfall | Observed | any | 分母, 比率, 重複加總, 雙來源, 疊檔快照, 口徑, 蓄水率, 落雷, 對帳, 外部基準 |
| [06-08](06-08-label-estimates-and-models.md) | 口徑誠信（二）：推估與模擬的輸出要標示，並用範圍與敏感度取代單一數字 | 圖上寫「現在有 X 人」，其實是模型輸出；換一個假設參數，排名與結論就變。 | pattern | Observed | any | 日夜人口, 推估, 模擬, 估算, 範圍, 敏感度, 圖例, 觀測 vs 推估, 不確定性, 口徑矛盾 |
| [06-09](06-09-bake-vector-field-to-png.md) | 向量場（風、海流）烘成 PNG：R／G 放 u／v，alpha 放有效遮罩 | 要畫風場或海流粒子，原始 NetCDF／GRIB 太大、前端不能直接讀。 | pattern | Implemented | any | 向量場, u/v, PNG, 烘焙, 風場, 海流, alpha, 遮罩, 雙線性取樣, 粒子 |
| [06-10](06-10-loader-column-mismatch-silent-blank.md) | loader 欄位名與資料來源不符：整包查詢失敗、catch 只 warn，圖層長期靜默空白 | 圖層一直是空的，沒有任何錯誤畫面，壞了很久才被發現。 | pitfall | Observed | any | loader, 欄位名, select, PostgREST, 靜默失敗, catch, console.warn, 空白圖層, 資料契約, view |
| [06-11](06-11-id-not-unique-across-scopes.md) | ID 只在某個範圍內唯一：StationID 跨縣市撞號，join 前先驗 key | 公車站牌、軌道車站跨縣市／跨系統合併後，popup 內容張冠李戴，或站名對錯城市。 | pitfall | Observed | any | ID, 主鍵, 撞號, StationID, StationUID, 複合鍵, 前導零, join, count distinct, 重編號 |
| [06-14](06-14-statistics-layer-source-overview-and-comparability.md) | 統計圖層的兩個交付門檻：資料來源總覽要一起更新，切換指標或期別只能配對可比的選項 | 新增或合併了統計圖層，側欄看得到，但「資料來源」頁找不到它，或只找得到合併後的群組名、找不到裡面的原始指標。 | pattern | Implemented | any | 統計圖層, choropleth, 資料來源總覽, 來源卡, 可比性, 跨期比較, selector, 期別, 口徑, 邊界版本, 衍生指標, 圖層登記表, 增量發布 |

