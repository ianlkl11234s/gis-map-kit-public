---
id: 10-04
title: 公開 client token 與真 secret 要分開：VITE_ 前綴的變數一定會進前端 bundle
topic: 10-ops
kind: pitfall
scope: public
evidence: Implemented
stacks: [any]
tags: [token, secret, 金鑰, 環境變數, VITE_, bundle, anon key, RLS, 輪換, 網域限制]
---

## 原則
只有設計給前端用的公開 token 才能進 bundle，真 secret 一律留在後端或 CI；`VITE_` 這類前綴的變數必定內嵌進產出檔。

## 症狀
- 把 service role、API client secret、S3 金鑰放進 `VITE_*` 變數，打包後任何人 view-source 都看得到。
- 以為「放在 `.env` 就安全」。
- 以為「anon key 是公開的＝資料庫全開」，或反過來忽略它其實沒有權限保護。
- 測試網址上底圖 403（token 有網域限制，新網域不在白名單，見 [10-05](10-05-local-vs-production-differences.md)）。

## 原因
前端 bundler 會把特定前綴（如 `VITE_`、`NEXT_PUBLIC_`）的變數內嵌進產出檔。有些「token」本來就是設計給前端用的，保護靠別的機制；真 secret 則絕不能進前端。

## 解法
| | 公開 client token | 真 secret |
|---|---|---|
| 例 | 地圖底圖 public token、資料庫 anon key | service role、API client secret、物件儲存存取金鑰、LLM key |
| 進前端 | 會（build 期注入） | 禁止 |
| 保護 | 網域限制（best-effort）、資料庫權限（RLS／GRANT） | 後端環境變數、CI secrets；外洩就輪換 |

1. 前端能直打的 RPC／函式：先 REVOKE PUBLIC 再明確 GRANT；內部／cron 函式連 anon、authenticated 一起收回；時間範圍等參數在函式內 clamp。對**既有**函式不要直接 REVOKE PUBLIC：先盤點哪些服務角色只靠 PUBLIC 取得權限，再逐一 GRANT 後收回。
2. 託管平台出事（外洩環境變數）時，放在該平台的金鑰全部要換；平時就維護「金鑰名稱清單」（只列名稱，不列值）。金鑰一旦進入對話或 log，視為外洩並輪換；dev server 與 CLI 的外洩路徑見 [10-21](10-21-secrets-in-bundle-and-dev-server.md)。
3. 使用者自填 key（BYOK：存 session 儲存、直連、不經手伺服器）的設計，網站端沒有代付端點，才不會有被刷費用的風險；若要代付，必須經後端代理並限流。
4. 公開 client token 要設網域／URL 限制、只給最小權限；建置後掃描 bundle（搜尋 `sk-`、`service_role` 等金鑰格式），納入 CI。
5. 用 CSP 的 `connect-src` 限制 key 只能送往預期網域；CSP 怎麼部署見 [10-24](10-24-csp-for-map-sites.md)。

## 怎麼偵測
- 通用：build 後在產出檔搜尋 secret 型態的變數名與值樣式；環境變數清單裡 `VITE_` 開頭但名字含 `SECRET|SERVICE|PRIVATE|PASSWORD`。
- 搜尋：`grep -rE "VITE_[A-Z_]*(SECRET|SERVICE|PRIVATE|PASSWORD)" .`；`grep -rE "service_role|sk-[A-Za-z0-9]{20,}" dist/`（只輸出檔名與行號，不要貼出值）（適用 stack：Vite／webpack／Next 等所有會內嵌環境變數的 bundler）。

## 出處
- Vite 文件〈Env Variables and Modes〉：只有 `VITE_` 前綴會暴露給客戶端。Supabase 文件：anon key 設計上可公開，安全依賴 RLS。
- 實例：[CLAUDE.md（service role 金鑰禁止進 bundle）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/CLAUDE.md)、[docs/development-rules.md](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/development-rules.md)。

