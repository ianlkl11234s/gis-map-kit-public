---
id: 10-23
title: 前端帶公開金鑰時，資料庫的表、欄位、函式、schema 都要當成對全世界開放來盤點
topic: 10-ops
kind: pitfall
scope: public
evidence: Implemented
stacks: [any]
tags: [Supabase, PostgREST, anon, authenticated, RLS, GRANT, REVOKE, PUBLIC, default privileges, SECURITY DEFINER, search_path, exposed schemas, 欄位權限, 個資]
---

## 原則
公開金鑰放在前端 bundle 是設計如此，真正的防線是資料庫權限。開放註冊時「已登入」也幾乎等於任何人，所以匿名與已登入角色可碰到的 schema、表、欄位、函式，都要明確盤點並只給必要的。

## 症狀
- 匿名使用者能呼叫內部的清理、refresh 函式，拖慢或改動共用資料庫。
- 某張表含姓名、電話的欄位，可被 REST 直接讀出。
- 新建的函式沒有人授權，卻已對匿名開放。
- 收回權限後，背景服務或排程突然失效。

## 原因
1. REST 層可同時開放多個 schema；只要角色有權限，物件就能被請求，不管前端有沒有用到。
2. 新物件的預設權限依「建立者的角色」與預設權限設定而不同（例如 Supabase 上由平台管理角色建立的物件可能自動授權匿名，由一般資料庫角色建立的不一定）；這會隨版本變動，要實際查，不要憑印象。
3. PostgreSQL 函式建立後，EXECUTE 預設授予 PUBLIC（所有角色，含之後才建立的）；函式也不受 RLS 管，只能靠 EXECUTE 權限。
4. 不少服務角色（唯讀帳號、排程、報表）是靠 PUBLIC 取得權限，沒有明確的 GRANT；對 PUBLIC 直接收回就會讓它們失權。

## 解法
1. **REST 只開放前端真的需要的 schema**。即時或內部 schema 不開放，前端只經公開 RPC 讀。
2. **表**：開 RLS，只給 SELECT；含個資的欄位不給（用 view、欄位層級 GRANT，或入庫時就拿掉，見 [07-14](../07-performance/07-14-open-data-pii-column-exclusion.md)）。
3. **新函式**：先 `REVOKE ... FROM PUBLIC, anon, authenticated`，再只 GRANT 給需要的角色。cron、refresh、cleanup 等內部函式一律收回。`SECURITY DEFINER` 函式一律 `SET search_path`。
4. **既有函式**不能直接 `REVOKE FROM PUBLIC`：先盤點只靠 PUBLIC 的服務角色，明確 GRANT 給它們，在交易裡測試後再收回；也可用 `ALTER DEFAULT PRIVILEGES` 讓之後新建的函式不再預設授予 PUBLIC。
5. **寫入路徑**：匿名唯讀；寫入要求登入再加站主檢查（RLS policy 或函式內檢查）。
6. **service role／secret key 永不進前端**（見 [10-04](10-04-public-token-vs-secret.md)、[10-21](10-21-secrets-in-bundle-and-dev-server.md)）。
7. **定期跑稽核查詢**（下節），並把結果與上一次比較。對外函式要在函式內限制逾時、範圍與筆數。

## 怎麼偵測
以下 SQL 適用 Supabase／PostgREST；其他框架概念通用（列出公開角色可碰到的東西）。

```sql
-- 匿名角色可執行的函式（排除系統 schema）
SELECT n.nspname, p.proname
FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE n.nspname NOT IN ('pg_catalog','information_schema')
  AND has_function_privilege('anon', p.oid, 'EXECUTE')
ORDER BY 1, 2 LIMIT 200;

-- 開放 schema 中沒開 RLS 的表（把 'public' 換成實際開放的 schema）
SELECT n.nspname, c.relname
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r' AND NOT c.relrowsecurity
  AND n.nspname IN ('public')
ORDER BY 1, 2 LIMIT 200;
```

- 搜尋：migration 裡 `CREATE (OR REPLACE )?FUNCTION` 之後 20 行內沒有 `REVOKE`，判紅（any）。
- 通用：匿名金鑰直接 `GET` 含個資欄位的表；`SECURITY DEFINER` 函式沒有 `SET search_path`。

## 出處
- PostgreSQL 文件：GRANT（PUBLIC 為所有角色的隱含群組，含之後建立者）https://www.postgresql.org/docs/current/sql-grant.html ；函式預設 EXECUTE 給 PUBLIC 見 Privileges 一節 https://www.postgresql.org/docs/current/ddl-priv.html ；ALTER DEFAULT PRIVILEGES https://www.postgresql.org/docs/current/sql-alterdefaultprivileges.html 。
- Supabase 文件〈Securing your API〉（對所有經 Data API 公開的表開 RLS；RLS 不適用函式，只對需要的角色授 execute；撤銷 PUBLIC 的 execute 會影響其他 schema 的函式）https://supabase.com/docs/guides/api/securing-your-api ；API keys 與 Row Level Security 說明同站。
- 相關卡：[07-14](../07-performance/07-14-open-data-pii-column-exclusion.md)、[10-04](10-04-public-token-vs-secret.md)、[10-21](10-21-secrets-in-bundle-and-dev-server.md)。

