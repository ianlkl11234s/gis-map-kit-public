---
id: 12-00
title: 特定領域圖層踩坑索引：領域 → 卡片
topic: 12-domain-pitfalls
kind: catalog
scope: public
evidence: General
stacks: [any]
tags: [index, catalog, 海流, 風場, 航班, AIS, 衛星, 落雷, 地震, 颱風, 即時車輛]
---

## 原則
做海流、風場、航班、船舶、衛星、事件型即時資料的圖層前，先依領域查下表，把對應卡片的「怎麼偵測」搜尋式跑一次；不要憑通用經驗假設資料乾淨。

## 症狀
做海流、風場、航班、船舶、衛星、事件型即時資料時，不知道該先檢查哪些坑。本索引依領域列出卡片；每張卡的 `## 症狀` 最後一條是「地圖上的誤導」，可直接搜尋這個字串。

## 原因
這些領域的資料有共同特性：時間戳多來源、取樣不連續、座標跨全球、事件稀疏、上游格式不穩。同一個坑會在不同領域重複出現，所以下表一張卡可能列在多個領域。

## 解法
| 領域 | 卡片 |
|---|---|
| 海流（CMEMS 等） | [12-09](12-09-vector-field-conventions.md) 向量場慣例、[12-10](12-10-gridded-forecast-time-axis.md) 格點時間軸與抓取範圍 |
| 風場（GFS 等） | [12-09](12-09-vector-field-conventions.md) 向量場慣例、[12-10](12-10-gridded-forecast-time-axis.md) 預報冒充實況與最近幀容差 |
| 航班軌跡（ADS-B、商業航跡 API） | [12-01](12-01-timestamp-timezone-offset.md) 時區與日界、[12-02](12-02-flight-altitude-units.md) 高度單位、[12-03](12-03-antimeridian-split.md) 換日線、[12-04](12-04-track-gap-segmentation.md) 斷訊切段、[12-18](12-18-paid-flight-api-ledger.md) 付費 API 對帳 |
| 船舶 AIS | [12-01](12-01-timestamp-timezone-offset.md) 時區、[12-04](12-04-track-gap-segmentation.md) 斷訊切段、[12-05](12-05-ais-position-jumps.md) 跳點過濾、[12-06](12-06-mmsi-not-unique-identity.md) MMSI 身分、[12-07](12-07-ghost-last-known-position.md) 幽靈點與停泊 |
| 衛星軌道（TLE／SGP4） | [12-03](12-03-antimeridian-split.md) 換日線、[12-07](12-07-ghost-last-known-position.md) current 表幽靈資料、[12-11](12-11-tle-staleness-sgp4.md) TLE 過期與 epoch 新鮮度、[12-12](12-12-upstream-blocking-rate-limits.md) 封鎖與限流 |
| 落雷 | [12-14](12-14-lightning-dual-source.md) 雙來源重複計算、[12-16](12-16-event-feed-silent-outage.md) 靜默斷供 |
| 地震 | [12-01](12-01-timestamp-timezone-offset.md) 時區、[12-15](12-15-earthquake-report-types.md) 多報告類型與 join、[12-16](12-16-event-feed-silent-outage.md) 靜默斷供、[12-17](12-17-event-layer-fixed-limit-freeze.md) 固定上限凍結 |
| 颱風 | [12-13](12-13-typhoon-multi-source-tracks.md) 多來源多版本路徑、[12-17](12-17-event-layer-fixed-limit-freeze.md) 固定上限凍結、[12-16](12-16-event-feed-silent-outage.md) 靜默斷供 |
| 即時車輛（公車、火車） | [12-08](12-08-vehicle-interpolation-fake-motion.md) 插值假動態、[12-12](12-12-upstream-blocking-rate-limits.md) 限流（TDX 429／401）、[12-07](12-07-ghost-last-known-position.md) 幽靈點 |
| 全域／跨領域 | [12-03](12-03-antimeridian-split.md) 換日線（全球事件連線）、[12-12](12-12-upstream-blocking-rate-limits.md) 雲端 IP 封鎖、[12-16](12-16-event-feed-silent-outage.md) 0／無資料／過期分開 |

依症狀找：
- 時間差 ±8 小時、某日只抓到一部分 → [12-01](12-01-timestamp-timezone-offset.md)
- 3D 軌跡壓扁 → [12-02](12-02-flight-altitude-units.md)
- 橫跨全圖的水平線 → [12-03](12-03-antimeridian-split.md)
- 跨海、穿陸的直線 → [12-04](12-04-track-gap-segmentation.md)；單點尖刺 → [12-05](12-05-ais-position-jumps.md)；一艘船兩地跳 → [12-06](12-06-mmsi-not-unique-identity.md)
- 港口一團點、數量只增不減 → [12-07](12-07-ghost-last-known-position.md)
- 車倒退、切街角、倒飛 → [12-08](12-08-vehicle-interpolation-fake-motion.md)
- 風向差 180°、半個地球錯位 → [12-09](12-09-vector-field-conventions.md)
- 換日期圖不變、實況其實是預報 → [12-10](12-10-gridded-forecast-time-axis.md)
- 衛星在幾萬公里外 → [12-11](12-11-tle-staleness-sgp4.md)
- curl 可以、部署不行、大量 429 → [12-12](12-12-upstream-blocking-rate-limits.md)
- 颱風路徑來回穿越 → [12-13](12-13-typhoon-multi-source-tracks.md)
- 數字差 1.5–2 倍 → [12-14](12-14-lightning-dual-source.md)
- 地震件數過多、join 後消失 → [12-15](12-15-earthquake-report-types.md)
- 圖層連續幾週沒點、監控卻正常 → [12-16](12-16-event-feed-silent-outage.md)
- 圖層只顯示最早或最近一小段 → [12-17](12-17-event-layer-fixed-limit-freeze.md)
- 完成數與資料數對不上 → [12-18](12-18-paid-flight-api-ledger.md)

## 怎麼偵測
- 通用：先依領域找卡，再照各卡「怎麼偵測」的搜尋式跑一次。
- 尚無專卡的一般風險：ADS-B 越洋覆蓋缺口、風場粒子高緯變形、AIS 時間戳亂序、經度 0／181／91 的無效值。

## 出處
- 各卡出處段。
