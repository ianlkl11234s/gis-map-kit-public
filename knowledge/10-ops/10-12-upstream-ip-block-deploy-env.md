---
id: 10-12
title: 上雲端才連不上：來源封鎖雲端出口 IP；ConnectTimeout 先懷疑被擋，不是網路慢
topic: 10-ops
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [IP 封鎖, ConnectTimeout, 出口 IP, 台灣 IP, 政府 API, collector, 雲端, blackhole]
---

## 原則
部署前從部署環境對每個外部來源實測連線；遇到 ConnectTimeout 先比較本機與部署環境的結果，不要先調逾時時間。

## 症狀
- 本機（台灣 ISP）測試都正常，部署到雲端後某來源持續 ConnectTimeout，資料停更數天。
- 不是 403，而是連線逾時（SYN 沒回應）。
- 部分政府 API 只放行台灣 ISP，國際雲商與邊緣運算平台（如 Workers）都被擋。

## 原因
上游封鎖資料中心 IP 段（防爬蟲或地域限制）；本機與雲端出口 IP 不同。

## 解法
1. 部署前**從部署環境**對每個來源 curl 一次；搬家前也要重測全部來源。
2. 排查：ConnectTimeout 先比較「本機 vs 部署環境」結果，不要先調逾時時間。
3. 對策選項：需要台灣 IP 的 collector 放在台灣 IP 的 VM；改用原始供應者（上游的上游）；本機抓好後上傳靜態檔。
4. 需要台灣 IP 的 VM 若為手動部署，git push 不會自動生效，要在文件寫清楚。
5. 瀏覽器端 403／CORS 與此不同，見 [01-11](../01-taiwan-apis/01-11-cors-and-direct-calls.md)；封鎖與限流整體見 [12-12](../12-domain-pitfalls/12-12-upstream-blocking-rate-limits.md)。

## 怎麼偵測
- 通用：來源在本機可用、部署後逾時；錯誤型態是 timeout 而非 4xx。
- 搜尋：collector 設定缺「需要台灣 IP」標記；沒有從部署環境做連通性測試的 CI／腳本（適用 stack：any）。

## 出處
- 一般網路排查。
- 實例：[celestrak-ip-blocked（來源封鎖雲端出口 IP，衛星資料停更數天）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/.claude/pitfalls/2026-04-14-celestrak-ip-blocked.md)、[EXTERNAL_COLLECTORS.md（只放行台灣 ISP 的來源）](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/EXTERNAL_COLLECTORS.md)。

