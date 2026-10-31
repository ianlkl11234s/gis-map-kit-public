---
id: 01-06
title: 行政界與人口：NLSC／TGOS 邊界、戶政司 RIS 人口的代碼與層級陷阱
topic: 01-taiwan-apis
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [NLSC, TGOS, 國土測繪, 行政區, 村里, VILLCODE, RIS, 戶政司, 人口, choropleth, 分母, 通用版電子地圖]
---

## 原則
行政區代碼一律以字串讀取並補零、以代碼 join；人口加總前先篩單一層級與單一時點；面積用投影後的幾何計算，不用 bbox；人均分母只用戶籍人口。

## 症狀
- 村里 join 後少了一些列，或對不上（代碼前導零不見）。
- 人口加總是實際的 3 倍；人均值離譜。
- 用縣市 bbox 算面積，結果包含遠方離島。
- 「縣市界 GML」疊上去偏移。

## 原因
- 代碼被當數字讀，前導零掉了；村里名稱不唯一，不能當 key。
- 戶政司人口資料把多個行政層級（縣市／鄉鎮／村里）放同一表；不篩層級加總會重複。
- 縣市 bbox 含東沙、南沙。
- 縣市界 GML 沒標 CRS，實際是 4326；其他來源可能是 EPSG:3826。
- 「未編定村里」不是真村里。
- 日夜人口、模擬人口不是人均分母（見 [01-14](01-14-semantics-drift-and-upstream-loss.md)）。

## 解法
1. 代碼欄一律以字串讀取並補零；join 前驗長度。
2. 村里用代碼為鍵，不用名稱。
3. 人口先篩層級與單一時點再加總；人均分母用戶籍人口。
4. 面積用幾何投影到 EPSG:3826 後計算，不用 bbox。
5. 通用版電子地圖／正射影像（NLSC WMTS）可作底圖候選，授權與前端直連條件官方原文未取得，使用前先確認（見 [02-02](../02-basemaps/02-02-basemap-selection-decision.md)）。
6. TGOS 主題 API 的 Apikey 綁 IP 白名單，帶 header 也繞不過，不適合前端直連。
7. 戶政司 RIS 的授權欄值僅為代碼，官方原文未取得；確認前不要寫成特定授權。

## 怎麼偵測
- 通用：choropleth 缺色塊；人口總和遠超過全台約 2,300 萬；邊界與底圖錯位。
- 搜尋：`VILLCODE|TOWNCODE`（被當 number 讀）、`bbox.*area`（適用 stack：any）。

## 出處
- 官方入口：nlsc.gov.tw、ris.gov.tw/rs-opendata。
- 相關卡：[01-12](01-12-coordinates-crs-and-column-names.md)、[01-14](01-14-semantics-drift-and-upstream-loss.md)、[02-02](../02-basemaps/02-02-basemap-selection-decision.md)。

