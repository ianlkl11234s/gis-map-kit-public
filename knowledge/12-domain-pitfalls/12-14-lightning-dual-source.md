---
id: 12-14
title: 落雷兩個來源是同一批雷的兩份觀測，相加就重複計算；各來源精度與去重鍵也不同
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Evaluated
stacks: [any]
tags: [lightning, 落雷, 多來源, 重複計算, dedup, source, KML, 302, rolling window, unique index]
---

## 原則
同一現象有多個觀測來源時，資料表與查詢都要帶 `source` 並由使用者選一個，不提供跨來源加總；去重鍵依各來源精度設計。

## 症狀
- 同一張卡片上，主數字（單一來源）和趨勢圖（全部來源）差 1.5–2 倍。
- 新來源接上後，第一版解析出 0 筆且不報錯。
- 手動 curl 測端點拿到 0 bytes，誤判「這個源沒資料」。
- 上游換新 ID 重發同一筆後，整批寫入卡住。
- 地圖上的誤導：加總後的落雷數被讀成「雷暴變多一倍」；兩源座標精度不同，疊在一起像同一處被打兩次。

## 原因
1. 兩個偵測網（例如氣象單位與電力公司）觀測的是同一批閃電，不是互補的兩半；查詢時沒指定來源就被加總。
2. 來源精度不同：一個到奈秒、小數 5 位座標、有電流強度；另一個只到分鐘、座標 2–3 位小數、沒有 ID，只能合成 hash 去重，雷雨密集時可能把不同閃電塌成一筆。
3. 滾動 1 小時視窗的來源，同一筆會被抓到十幾次，靠唯一鍵擋重複；表上若有兩個 unique index，`ON CONFLICT (某欄)` 只保護其中一個，另一個衝突會讓整批失敗。
4. 格式細節：KML 收尾標籤是 `</when >`（多一個空格），regex 寫 `</when>` 解出 0 筆；端點回 302，程式會跟隨、curl 不加 `-L` 不會。

## 解法
1. 多來源觀測同一現象時，資料表加 `source` 欄，查詢與 RPC 必須指定來源；UI 讓使用者選來源，不提供「全部加總」。
2. 快取鍵與彙總都帶 source（例如 `${source}|${date}`）。
3. 去重鍵依來源精度設計，並在文件寫明低精度來源可能少算。
4. 有多個唯一約束時用不指定目標的 `ON CONFLICT DO NOTHING`，或合併成一個約束。
5. 解析 XML／KML 收尾標籤寫成 `</tag\s*>`，或用正式 XML parser；手動測陌生端點一律 `curl -L`。
6. 兩源並行還有一個好處：一邊有、一邊沒有時，立刻看得出單邊停供（見 [12-16](12-16-event-feed-silent-outage.md)）。

## 怎麼偵測
- 通用：同一時段分別查各來源筆數，若加總值出現在任何 UI 上就要問「是否同一現象」。
- SQL：`select source, count(*) from lightning where ts > now() - interval '1 day' group by 1;`
- 搜尋（未指定來源）：`rg -n -i 'lightning' | rg -i 'rpc|select' ` 再看是否帶 `source`／`p_source`。
- 搜尋（脆弱 regex）：`rg -n "</[a-zA-Z]+>" ` 在 XML／KML 解析程式，改成允許空白。
- 搜尋（多個 unique）：`rg -n -i 'create unique index|unique \(' ` 在同一張表的 migration。

## 出處
- 一般多來源觀測資料整合原則（同一現象不可直接相加）。相關卡：[12-16](12-16-event-feed-silent-outage.md)。
- 實例：[前端快取鍵帶 source](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/lightningLoader.ts)；[p_source 為空時兩源加總，前端改固定來源](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/8a8b1daaec1d735f0b3d2e069055b2d95cdad4d0)；[collector：兩源精度比較、滾動視窗去重、302 要 -L](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/collectors/lightning_cwa.py)。
