---
id: 12-12
title: 即時源的封鎖與限流：瀏覽器 403、雲端 IP 被黑洞、全域 429 與 401 連鎖
topic: 12-domain-pitfalls
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [CelesTrak, Space-Track, TDX, 429, 401, 403, CORS, IP block, rate limit, ASN, collector, proxy]
---

## 原則
前端不直接打第三方即時源；部署前從部署環境實測每個來源；同一把金鑰共用一個全域限流器，token 失敗要 backoff，401、403、429、connect timeout 分開處理。

## 症狀
- 本機 curl 正常，部署後的瀏覽器整天 0 顆衛星、console 出現 403。
- 搬到新主機後，某些來源全部 connect timeout（不是 403、不是 404），其他來源正常。
- 擴充到更多城市後，大部分城市同時回 429，連帶其他用同一把金鑰的 collector 也 429。
- 429 怎麼降頻都不好，因為根本原因是 token 端點的 401。
- 地圖上的誤導：被擋的來源在地圖上通常就是「0 筆」，看起來像「現在沒有衛星／沒有公車」，而不是「抓不到」。

## 原因
1. 部分公開資料站對瀏覽器 UA 加 CORS preflight 或高頻請求回 403；也有對雲端 PaaS、特定 ASN 的 IP 段直接丟包（SYN 無回應），本機測不出來。
2. 政府或地方 API 常對海外雲端 IP 段做 geo/ASN 封鎖，換機房就斷。
3. 平台限流以「金鑰」為單位，取 token 的請求也算在配額內；多支 collector 各自限流等於沒限。
4. token 取得失敗時不 cache、不 backoff，每一輪每一支都重打 token 端點，形成 retry storm，副作用才是 429。

## 解法
1. 前端不直接打第三方即時源：由後端排程抓好存成表或快照，前端讀自己的端點。
2. connect timeout（而非 4xx）時先懷疑 IP 層封鎖：排查順序與對策（從部署環境實測、選機房前先測候選主機、改接原始供應者）見 [10-12](../10-ops/10-12-upstream-ip-block-deploy-env.md)。
3. 同一把金鑰的所有請求（含 token 請求）走同一個全域限流器，速率低於官方上限；排程避免整分鐘 burst，錯開起跑時間。
4. token 端點失敗要有指數 backoff 並遵守 `Retry-After`；看到「token 401＋業務 429」同時出現，先查認證。
5. 狀態碼分開處理與告警：401（認證）、403（權限／地區）、429（頻率，指數退避加抖動）、connect timeout（網路層封鎖）各有各的對策；告警依連續失敗次數倍增，避免告警風暴。
6. 每個來源保留一份限速與封鎖的踩雷紀錄。

## 怎麼偵測
- 通用：從部署環境（不是本機）跑一次請求並記錄狀態碼與耗時；比較本機與容器的結果。
- 通用：圖層 0 筆時，先看最近一次抓取的 HTTP 狀態，再決定是不是「真的沒有」。
- 搜尋（前端直打第三方）：`rg -n "fetch\(['\"\`]https?://(?!localhost)" --pcre2 src/`
- 搜尋（限流器是否共用）：`rg -n -i 'ratelimit|RateLimiter|throttle|sleep\(' ` 在 collector，確認是全域單例而非每支各自建立。
- 搜尋（token 重試）：`rg -n -i 'get_?token|access_token|Retry-After|backoff'`。

## 出處
- MDN：CORS preflight 與 403 的差異。
- 各平台官方配額說明（例如 TDX 每金鑰每秒請求上限）。
- 實例：[雲端出口 IP 被丟包、停更 5 天，改接 Space-Track GP](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/.claude/pitfalls/2026-04-14-celestrak-ip-blocked.md)；[TDX 擴到 22 縣市後的 429 與全域限流器](https://github.com/ianlkl11234s/gis-data-collectors/blob/e0beb720e2abd9fc35b674ef33e83d62df5d665b/docs/TDX_RATE_LIMITING.md)；[瀏覽器 403 改讀後端同步的 view](https://github.com/ianlkl11234s/mini-taiwan-pulse/commit/3fb4d4b49108b0378205b25a4ecc8cbed41f3b83)。

