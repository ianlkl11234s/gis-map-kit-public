---
id: 10-02
title: 資料更新不等於重建前端：換內容就換檔名，快取政策跟著版本化
topic: 10-ops
kind: pattern
scope: public
evidence: Observed
stacks: [any]
tags: [快取, cache-control, immutable, 版本化, 指標檔, manifest, CDN, 404 快取, purge, 退版]
---

## 原則
資料內容更新時換檔名（日期或內容 hash）或改指標檔，不要覆寫同名檔；快取政策跟著版本化配套，發布流程要包含資料資產。

## 症狀
- 資料補上了，使用者（或自己）仍看到舊檔。
- 補檔後線上仍 404，或設了長效 immutable 的檔更新後舊訪客一直拿舊檔（快取機制見 [06-04](../06-data-formats/06-04-cache-immutable-404-and-stale-edge.md)）。
- 資料路徑寫死在程式裡，想退回上一版沒辦法。

## 原因
- 靜態資料檔路徑寫死且沒有版本，換內容只能覆寫；CDN／瀏覽器快取不知道內容已變。
- 資料路徑沒有版本，發布流程又只寫程式、沒寫資料資產。

## 解法
1. **換內容就換檔名**（`trees_20261029.geojson` 或內容 hash）：最笨但最不會被快取騙；舊檔名保持不變即可退版。
2. **指標檔模式**（進階，不想重部署時）：資料檔 append-only、不覆寫；發布順序「資料檔 → manifest → `current.json`」，前端只讀 `current.json`；改指標就生效、改回舊指標就退版。
3. **快取政策與版本化配套**（機制與理由見 [06-04](../06-data-formats/06-04-cache-immutable-404-and-stale-edge.md)）：
   - 會變的指標檔（`*manifest*.json`、`*_current.*`）→ 短 TTL（如 5 分鐘）＋must-revalidate；
   - 檔名含日期或 hash → 長效 immutable；
   - 其餘未版本化資料 → 短到中等（如 1 天，可加 stale-while-revalidate）。
4. 補檔後仍 404 或看到舊檔：依 [06-04](../06-data-formats/06-04-cache-immutable-404-and-stale-edge.md) 排查（404 負向快取、邊緣舊檔、CDN 規則範圍與 purge）。
5. 大檔若由 entrypoint／啟動腳本從物件儲存同步到容器，注意「容器重啟才拉」，部署順序要寫在發布步驟裡（先上傳大檔，再合併程式）。
6. 發布文件要包含「資料資產」步驟，不能只寫程式發布。

## 怎麼偵測
- 通用：改了資料後，用無痕視窗與 `curl -I` 看快取標頭是否還是舊的（細節見 [06-04](../06-data-formats/06-04-cache-immutable-404-and-stale-edge.md)）。
- 搜尋：程式中寫死 `/data/xxx.geojson` 而無版本（適用 stack：any，設定檔位置依託管而異）。

## 出處
- 一般 HTTP 快取實務（RFC 9111 Cache-Control、immutable 指令）。
- 相關卡：[06-04](../06-data-formats/06-04-cache-immutable-404-and-stale-edge.md)（快取機制：immutable、404 負向快取、邊緣供舊檔、CDN 規則）。
- 實例：[nginx.conf（指標檔短 TTL、版本化檔長效、其餘 1 天）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/nginx.conf)、[src/data/layerAssetIndex.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/layerAssetIndex.ts)（靜態資產版本化試點）。

