---
id: 06-04
title: 靜態資產快取三件事：換內容換檔名、部署前探測會種下 404、邊緣仍供舊檔
topic: 06-data-formats
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [CDN, Cloudflare, immutable, cache-control, 404, negative cache, cache-buster, 內容雜湊, purge, Range]
---

## 原則
只有「URL 唯一對應一份永不改變的內容」的檔才設長期 immutable，內容一變就換檔名；部署完成前探測新 URL 一律加 cache-buster。

## 症狀
- 換了新資料檔，使用者（甚至部署後）仍看到舊資料，要等一天。
- 部署還沒完成就 curl 新檔名確認，之後新檔上線了卻持續回 404。
- 原站已經是新檔，CDN 邊緣還在供舊檔；PMTiles 的 Range 請求也從舊快取切片，`content-range` 總大小是舊檔大小。
- 剛部署完，大檔短時間內回 404 的 HTML，數分鐘後才變 206。

## 原因
1. **URL 是契約**：固定檔名加長 TTL，內容變了 URL 沒變，快取不會失效。
2. **負向快取（negative cache）**：CDN 預設就會把某些副檔名的 404 快取數小時；在部署落地前去探測不存在的 URL，等於親手把 404 種進邊緣。
3. **固定 TTL 規則會連 404／5xx 一起快取**，罩住整個父路徑還會凍住指標檔；CDN 規則會覆寫原站的 cache-control。
4. 檔案同步（如物件儲存鏡像到站台）需要時間，同步完成前檔案不存在。

## 解法
1. **只有「URL 唯一對應一份永不改變的內容」的檔才能設長期 immutable**：檔名含日期，或含內容雜湊。其他一律短 TTL。
2. 內容雜湊要真冪等：雜湊算在實際寫出的位元組上；內容裡不放時間戳（時間戳只進 manifest）；gzip 寫入固定 mtime，否則同內容每次位元組不同。
3. 部署完成前若要探測新 URL，一律加 cache-buster（`?cb=<時間戳>`）。
4. 剛部署的大檔回 404 時先等幾分鐘再重測，不要當成缺檔去重傳。
5. CDN 固定 TTL 規則只貼在不可變前綴（檔名含日期或雜湊的目錄），指標檔路徑不套；同時設定 404／5xx 不快取；改完用公開網址回讀 `cache-control`，不是看儲存端 HEAD。事先備好只清單一 URL 或前綴的 purge，避免整站清除。

指標檔、部署順序、版本化流程見 [10-02](../10-ops/10-02-data-update-vs-redeploy-and-cache.md)。

## 怎麼偵測
- 通用：更新後使用者回報看到舊資料；`curl -I` 的 `cf-cache-status`／`age` 顯示 HIT 且 `content-length` 是舊值；404 一直不消失。
- 搜尋：`immutable` 或 `max-age=31536000` 套在檔名不含日期或雜湊的路徑；部署腳本中先 `curl` 新檔名再上傳（適用 stack：任何 CDN 前置的靜態資產）。

## 出處
- 官方：HTTP caching（RFC 9111）；各 CDN 的預設快取副檔名與 404 TTL 說明。
- 相關卡：[06-03](06-03-gzip-breaks-range-requests.md)、[10-02](../10-ops/10-02-data-update-vs-redeploy-and-cache.md)。
- 實例：[mini-taiwan-pulse 設計原則（immutable 只給含日期或內容雜湊的檔；部署前探測加 cache-buster）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/PRINCIPLES.md)；[事故紀錄（廣泛的快取規則凍結指標檔；原站已更新而邊緣仍供舊 PMTiles）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)。

