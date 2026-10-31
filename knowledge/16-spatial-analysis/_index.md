# 16-spatial-analysis 空間分析、可達性與地理編碼

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [16-00](16-00-spatial-analysis-index.md) | 空間分析總表：想回答什麼問題 → 方法與口徑 → 卡片 | 空間分析先定「想回答的問題」，再選方法，並把分析單元、分母、類別定義與檢定寫進回答；這些都是口徑，不是細節。 | catalog | Evaluated | any | 空間分析, 總表, 熱點, 區位商數, MAUP, 可達性, 地理編碼, 件數口徑, 偏態, 幾何健檢 |
| [16-01](16-01-hotspot-clustering-methods.md) | 熱點與群聚：Gi*、LISA、全域 Moran、最近鄰各回答不同問題，口徑（單元、鄰接、檢定）要寫明 | 被問「事故熱點在哪」，直接把密度最高的格子塗紅，說是「熱點」。 | decision | Evaluated | any | 熱點, 群聚, Getis-Ord, Gi*, Moran's I, LISA, 最近鄰, ANN, Clark-Evans, 鄰接, queen, FDR, 置換檢定, PySAL, 空間統計 |
| [16-02](16-02-location-quotient-and-ratio-metrics.md) | 區位商數 LQ 與比例指標：分母與類別定義都是口徑，小樣本不給值 | 被問「哪個區的製造業特別集中」，算出一個只有 3 家公司、其中 2 家是製造業的里，LQ 排第一。 | pitfall | Implemented | any | 區位商數, LQ, location quotient, 集中度, 比例, 占比, 分母, 人口分母, 類別定義, 最小樣本, 樣本太少, 口徑 |
| [16-03](16-03-cross-scale-maup.md) | 換尺度還成立嗎（MAUP）：同一組相關要在村里、鄉鎮、網格各算一次，並列樣本數與顯著性 | 「人口越密的地方老人越多嗎？」用鄉鎮算是中等正相關，換成村里卻幾乎無關，不知道該報哪一個。 | pattern | Evaluated | any | MAUP, 可變面積單元問題, 跨尺度, 相關, Spearman, 雙變量 Moran, 生態謬誤, 網格, 行政區, 樣本數, 補 0, 尺度翻轉 |
| [16-04](16-04-accessibility-isochrones.md) | 可達性與等時圈：路網距離不是直線距離；等時圈用 concave＋全域 dissolve＋環差分級，缺口狀態不能填 0 | 用 5 公里 buffer 回答「到最近醫院多遠」，但河對岸沒有橋，實際要繞 20 分鐘。 | pattern | Observed | any | 可達性, 等時圈, isochrone, 服務範圍, 路網距離, 直線距離, OSRM, Valhalla, osmnx, PBF, concave hull, dissolve, 環差, 服務沙漠, coverage |
| [16-05](16-05-geocoding-precision-and-routing.md) | 地理編碼：地址內插點不是門牌位置，精度欄位要留下；依量級選服務，送外部前先取得同意 | 手上只有地址清單，不知道該用哪個服務轉座標，一口氣打了幾萬筆付費 API。 | pattern | Observed | any | 地理編碼, geocoding, 地址, 門牌, 內插, 精度, geocode_precision, TGOS, Nominatim, Google Geocoding, 批次, 同意, 隱私, 量級 |
| [16-06](16-06-reported-counts-not-occurrence.md) | 事件件數是「通報、登錄的件數」：分布反映通報管道、趨勢反映登錄完整度，一列也不一定是一起事件 | 擱淺、污染、熱線案件依縣市排名，結論寫成「這裡的海龜最多」「這裡最髒」，其實是那裡通報管道多、巡查密。 | pitfall | Evaluated | any | 通報, 登錄, 件數, 趨勢, 跨年比較, 同期, 不完整年度, 列單位, 隻數, 重複通報, 擱淺, 混獲, 熱線, 報案, 口徑 |
| [16-07](16-07-skewed-sums-extreme-values.md) | 偏態加總：單一極端值主宰總和與平均，先看前幾大與占比，總和配中位數，轉換方式是口徑決定 | 「哪一區資本額最高」的第一名，其實只是一家超大公司登記在那裡；拿掉它，排名完全不同。 | pitfall | Evaluated | any | 極端值, 離群值, 偏態, 長尾, 加總, 平均, 中位數, 對數, 排名, 資本額, 格網, 不可加總, 口徑, 敏感度 |
| [16-08](16-08-geometry-quality-flags-before-analysis.md) | 分析前的幾何健檢：逐列留座標品質旗標，用落區對照宣稱的縣市，缺幾何的件數要回報 | 外島的服務據點算出「離島沒有服務站」，因為那幾站的座標全落在台北同一點。 | pattern | Evaluated | any | 幾何品質, 座標品質, coord flag, 落區, point in polygon, 縣市不符, 重複座標, 離群點, 東沙, 南海, 缺幾何, 環域, 距離, 健檢 |
