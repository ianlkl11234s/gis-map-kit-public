# 12-domain-pitfalls 領域踩坑（海流、風場、航班、船舶、衛星…）

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [12-00](12-00-domain-index.md) | 特定領域圖層踩坑索引：領域 → 卡片 | 做海流、風場、航班、船舶、衛星、事件型即時資料時，不知道該先檢查哪些坑。本索引依領域列出卡片；每張卡的 `## 症狀` … | catalog | General | any | index, catalog, 海流, 風場, 航班, AIS, 衛星, 落雷, 地震, 颱風, 即時車輛 |
| [12-01](12-01-timestamp-timezone-offset.md) | 即時軌跡的時間戳差 ±8 小時：naive datetime、UTC 日界與上游時區錯 | 時間軸回放載入上萬筆，畫面卻是 0 艘船；或「今天」出現比現在晚 8 小時的資料。 | pitfall | Evaluated | any | timezone, UTC, naive-datetime, 時區, 日界, AIS, flight, earthquake, collector, backfill |
| [12-02](12-02-flight-altitude-units.md) | 航班高度英呎與公尺混用，再被前端 heuristic 二次轉換，3D 軌跡壓扁 | 大範圍（全國、全球）視角下 3D 航跡貼地壓扁，放大到單一機場又看似正常。 | pitfall | Evaluated | any | altitude, feet, meters, ADS-B, FR24, 單位, heuristic, 3D 軌跡, LOD |
| [12-03](12-03-antimeridian-split.md) | 衛星地面軌跡、跨太平洋航班與全球連線在 ±180° 換日線被畫成橫跨全圖的線 | 衛星地面軌跡每繞一圈就有一條水平線從地圖右緣拉到左緣。 | pitfall | Implemented | mapbox-gl, maplibre, leaflet, openlayers, deck.gl, three.js | antimeridian, dateline, 換日線, longitude unwrap, satellite ground track, 跨太平洋, fitBounds |
| [12-04](12-04-track-gap-segmentation.md) | 船舶 AIS 與航班軌跡斷訊後被直接連線，畫出跨海峽、穿越陸地的虛構航跡 | 船的軌跡出現一條筆直、橫跨海峽或穿越島嶼的線。 | decision | Evaluated | mapbox-gl, maplibre, leaflet, openlayers, deck.gl, three.js | AIS, gap, 斷訊, 切段, trips layer, flight track, great circle, 虛線, 推測航段 |
| [12-05](12-05-ais-position-jumps.md) | AIS 座標亂碼造成瞬移跳點：用相對前一保留點的速度門檻過濾 | 軌跡中間突然出現一個遠在幾十公里外的尖刺，然後又回到原處。 | pitfall | Implemented | any | AIS, GPS jump, 跳點, outlier, speed filter, knots, SOG |
| [12-06](12-06-mmsi-not-unique-identity.md) | MMSI 不是可靠的船舶身分：測試碼、無效碼與航標混在船舶資料裡 | 一艘「船」的軌跡在島的兩側來回跳，看起來穿越陸地。 | pitfall | Evaluated | any | AIS, MMSI, MID, AtoN, 身分, 去重, 分類, 船舶 |
| [12-07](12-07-ghost-last-known-position.md) | 「最後已知位置」變幽靈點：停泊船、失聯衛星與 UPSERT-only 的 current 表 | 船停在港內好幾天，地圖上始終有一個看起來「在線」的點；回放時一整串點疊在碼頭。 | pitfall | Implemented | any | ghost, stale, current table, UPSERT, 停泊, SOG, 港口, last known position, 即時位置 |
| [12-08](12-08-vehicle-interpolation-fake-motion.md) | 即時車輛插值製造假動態：曲線 overshoot 倒退、GPS 直線切街廓、跨趟次倒飛 | 時刻表動畫裡的車在某些站「先往回退一點再前進」。 | pattern | Implemented | any | interpolation, lerp, Catmull-Rom, overshoot, snap to route, progress, 公車, 火車, 即時車輛, 回放, frame rate |
| [12-09](12-09-vector-field-conventions.md) | 風場與海流的三個慣例：風向是「來向」流向是「去向」、經度 0–360、粒子跨世界邊界 | popup 的風向和氣象局公布的差 180°。 | pattern | Implemented | any | wind, ocean current, u/v, 風向, 流向, from/to, 0-360, GFS, GRIB, NetCDF, particle, wrap |
| [12-10](12-10-gridded-forecast-time-axis.md) | 格點場（風、海流、沙塵）時間軸：預報值冒充實況、最近幀沒有容差、抓取沒限時間範圍 | 時間軸拉到任何一天，風場都顯示同一張圖（「換日期不會變」）。 | pitfall | Evaluated | any | GFS, CMEMS, forecast, analysis, lead time, valid time, frame, tolerance, NetCDF, subset, 海流, 風場 |
| [12-12](12-12-upstream-blocking-rate-limits.md) | 即時源的封鎖與限流：瀏覽器 403、雲端 IP 被黑洞、全域 429 與 401 連鎖 | 本機 curl 正常，部署後的瀏覽器整天 0 顆衛星、console 出現 403。 | pitfall | Observed | any | CelesTrak, Space-Track, TDX, 429, 401, 403, CORS, IP block, rate limit, ASN, collector, proxy |
| [12-13](12-13-typhoon-multi-source-tracks.md) | 颱風路徑多來源、多版本、同時間戳交錯，畫出來回穿越的軌跡 | 一個颱風的路徑在兩個相距上千公里的地點之間來回拉線，3 小時「移動」2,000 多公里。 | pitfall | Observed | any | typhoon, 颱風, JMA, JTWC, CWA, NCDR, forecast track, advisory, 預報路徑, 風圈, storm_key |
| [12-14](12-14-lightning-dual-source.md) | 落雷兩個來源是同一批雷的兩份觀測，相加就重複計算；各來源精度與去重鍵也不同 | 同一張卡片上，主數字（單一來源）和趨勢圖（全部來源）差 1.5–2 倍。 | pitfall | Evaluated | any | lightning, 落雷, 多來源, 重複計算, dedup, source, KML, 302, rolling window, unique index |
| [12-15](12-15-earthquake-report-types.md) | 同一場地震有多份報告：正式目錄、顯著報告、地方報告與初報修訂不能混算或等值 join | 地震件數比官方多，排名第一的「最大地震」其實是同一場地震的另一份報告。 | pitfall | Evaluated | any | earthquake, 地震, catalog, report type, 初報, 修訂, join, dedup, event_id, 震度, USGS |
| [12-16](12-16-event-feed-silent-outage.md) | 事件型即時資料「0 筆是合法結果」，上游靜默斷供時沒人發現：0、沒資料與過期要分開 | 落雷、地震、颱風、事件型圖層連續幾週沒有點，但 collector 每分鐘都在跑、HTTP 200、沒有錯誤。 | pitfall | Observed | any | silent outage, stale, freshness, heartbeat, ledger, 0 vs null, 落雷, 地震, 颱風, 共機, 新鮮度, monitoring |

