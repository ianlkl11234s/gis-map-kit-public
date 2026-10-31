---
id: 12-06
title: MMSI 不是可靠的船舶身分：測試碼、無效碼與航標混在船舶資料裡
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Evaluated
stacks: [any]
tags: [AIS, MMSI, MID, AtoN, 身分, 去重, 分類, 船舶]
---

## 原則
不要把 MMSI 當成唯一的船舶身分；寫入層先做格式與黑名單檢查，99 開頭的助航設備路由到獨立分類，並用空間可行性偵測多船共用。

## 症狀
- 一艘「船」的軌跡在島的兩側來回跳，看起來穿越陸地。
- 航標或助航設備被分類成軍艦、漁船。
- 船隻數量統計比預期多出幾個「超級活躍」的 ID。
- 地圖上的誤導：多艘船共用同一 MMSI 時，會被畫成一艘船在幾分鐘內往返兩地；航標被當成艦艇會讓監看圖層誤報。

## 原因
MMSI 是 9 位數，船舶首碼依 ITU 規定為 2–7（MID 國碼）。實際資料流中常見：
- 未設定或測試用的 `000000000`、`111111111`、`999999999` 等，被很多設備共用。
- 99 開頭是助航設備（AtoN）格式，也可能是自主無人載具這類非傳統船舶。
- 尾數多個 0 的海岸電台、非法 MID。
這些雜訊在不同抓取管道都會出現，是原始資料流本身的問題，不是某支解析器的 bug。

## 解法
1. 在寫入層（或分析前）做分級格式檢查：
   - A：`^[0-9]{9}$`（必做）。
   - B：已知測試碼黑名單（`0`、重複數字、`123456789` 等）。
   - C：完整 MID allowlist（維護成本高，視需求）。
2. 99 開頭（AtoN）不要直接丟，路由到獨立分類，並排除在「一個 MMSI＝一艘船」的去重規則外。
3. 身分去重不要只靠 MMSI：同 MMSI 在同時刻出現在相距過遠的兩處，就視為多船共用並拆開或排除。
4. 分類（船種）以軌跡表的實際 ship_type 為準，人工名冊要定期重算。

## 怎麼偵測
- 通用：統計每個 MMSI 的點數與空間範圍；點數極多、範圍橫跨不可能距離的 ID 先查。
- 通用：列出首碼分布，0／1／8／9 開頭都要有說明。
- 搜尋：`rg -n -i 'mmsi' | rg -v -i 'mmsi\s*[!=]~|isValidMmsi|MID'`，找有用 MMSI 當 key 但沒驗證的地方。
- SQL：`select mmsi, count(*) from positions where mmsi !~ '^[2-7][0-9]{8}$' group by 1 order by 2 desc limit 50;`

## 出處
- ITU-R M.585（MMSI 指配與 MID）。
- 實例：[船舶監看改版紀錄](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/vessel-watch/changelog.md)（`999999999` 被判成軍艦，加 MMSI 守門）；[待辦清單](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/vessel-watch/backlog.md)（三級檢查的實測占比，其中 99 開頭有一個是真實的自主無人載具，不可擋）。

