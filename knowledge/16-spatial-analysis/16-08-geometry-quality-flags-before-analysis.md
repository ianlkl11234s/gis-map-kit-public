---
id: 16-08
title: 分析前的幾何健檢：逐列留座標品質旗標，用落區對照宣稱的縣市，缺幾何的件數要回報
topic: 16-spatial-analysis
kind: pattern
scope: public
evidence: Evaluated
stacks: [any]
tags: [幾何品質, 座標品質, coord flag, 落區, point in polygon, 縣市不符, 重複座標, 離群點, 東沙, 南海, 缺幾何, 環域, 距離, 健檢]
---

## 原則
做距離、環域、落區或熱點之前，先對每列幾何標品質旗標，並用「點落在哪個行政區」對照資料自己寫的縣市；有問題的點排除並回報件數，依縣市計數時改用縣市欄，不用座標落點。

## 症狀
- 外島的服務據點算出「離島沒有服務站」，因為那幾站的座標全落在台北同一點。
- 依縣市統計件數，用座標落點算出來比資料本身的縣市欄少了近一成。
- 全台範圍的外接框被拉到南海，地圖初始鏡頭縮得很遠。
- 環域統計說某半徑內 0 筆，其實那些事件沒有座標。

## 原因
1. 載入時的範圍檢查（[01-12](../01-taiwan-apis/01-12-coordinates-crs-and-column-names.md)）只擋「明顯落在台灣外」的點；落在台灣內但位置錯的點（例如誤用總部座標、地址推算到別縣）照樣通過。
2. 合法的遠離點（東沙、太平島）和錯值混在一起，一刀切會誤刪或誤留。
3. 缺幾何的列在空間查詢裡靜默消失，結果看起來完整。

## 解法
1. **逐列標品質旗標**，至少分：正常、缺座標、超出範圍（經緯度填反、度分秒、離譜值）、零點 (0,0)（[06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)）、離群但合法（例：南海島礁）、與宣稱縣市不符。旗標存在表裡，不在分析時臨場判斷。
2. **落區對照**：把點與行政區界做空間 join，和資料自己的縣市欄比對；不符的列標旗標，不自動改座標。
3. **重複座標**：`count(distinct geom)` 明顯少於列數、或多個不同名稱的據點共用同一座標時，視為位置不可靠（地址推算共用座標的情況見 [16-05](16-05-geocoding-precision-and-routing.md)）；這些點不用於距離與離島涵蓋分析。
4. **整批偏移與座標系不符**：幾何欄宣稱經緯度、值卻是數十萬的公尺座標時，先確認座標系再算距離（[01-12](../01-taiwan-apis/01-12-coordinates-crs-and-column-names.md)）。某縣市的點整批落在另一縣市（例：離島點經度整批偏約 2 度，常是投影分帶用錯）時，這個縣市的點只能做計數，不做空間分析，並回報上游（[01-12](../01-taiwan-apis/01-12-coordinates-crs-and-column-names.md)）。
5. **回報缺幾何**：回答寫明「共 N 件，有座標 M 件」；依縣市計數用縣市欄（全部列都有），依距離、環域分析才用有座標的列。
6. **外接框與鏡頭**：計算全區範圍時排除「離群但合法」的點，或另外處理，不讓少數遠點決定預設鏡頭。

## 怎麼偵測
- 通用：離島或偏遠縣市的結果異常少；多個據點在地圖上疊成一點；外接框大得不合理。
- SQL：`SELECT count(*), count(geom), count(DISTINCT geom) FROM t` 三個數字一起看。
- SQL：`SELECT county, min(ST_X(geom)), max(ST_X(geom)), min(ST_Y(geom)), max(ST_Y(geom)) FROM t GROUP BY 1`，看是否有縣市整批落在別處。
- SQL：`SELECT t.county, b.county, count(*) FROM t JOIN admin b ON ST_Within(t.geom, b.geom) WHERE t.county <> b.county GROUP BY 1,2`。
- SQL：`SELECT geom, count(*) FROM t GROUP BY geom HAVING count(*) > 1 ORDER BY 2 DESC`。
- 搜尋：環域、距離計算（`ST_DWithin|ST_Distance|turf\.distance`）前沒有品質旗標或 `geom IS NOT NULL` 的條件（適用 stack：any）。

## 出處
- PostGIS 文件：`ST_Within`、`ST_Extent`。
- 相關卡：[01-12](../01-taiwan-apis/01-12-coordinates-crs-and-column-names.md)（載入時的座標系與範圍檢查）、[01-01](../01-taiwan-apis/01-01-tdx-integration.md) 與 [06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)（(0,0) 與魔術值）、[16-05](16-05-geocoding-precision-and-routing.md)（地理編碼精度與共用座標）。

