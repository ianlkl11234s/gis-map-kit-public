---
id: 08-08
title: 分享網址記住開了哪些圖層：只寫與預設不同的項目，讀不懂的就丟掉
topic: 08-multi-layer
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [分享連結, URL state, query string, deep link, 嵌入, 版本, 靜默降級, 圖層, 白名單, 相機]
---

## 原則
分享網址只序列化與預設不同的項目、人類可讀並帶版本號；解析時未知或不合法的值一律靜默丟掉，不要 throw 或白屏。

## 症狀
- 使用者分享的連結打開後是空白預設畫面，或開了不同的圖層。
- 連結被改壞（手動編輯、舊版連結、貼文被截斷）就白屏。
- 新增圖層、改名圖層後，舊的嵌入碼整批失效。
- 連結很長，沒法手寫或手改。

## 原因
把狀態序列化進網址時沒有訂出規則：寫哪些、怎麼容錯、何時升版。

## 解法
1. **只序列化與預設不同的項目（diff-based），且人類可讀**：預設全關時，`layers=` 就是「要開的清單」，例如 `?v=1&lng=121.5&lat=25&z=11&layers=a,b`；不做 base64 壓縮，寫文章要能手打手改。
2. **版本化**：`v=1`。缺版本或版本不符一律回空物件（用預設畫面），避免舊連結被新解析器誤讀。新增**選填**欄位不升版；同一個 key 的語意變了、或必要欄位變了才升版。語意微調但升版代價（所有舊嵌入碼作廢）更大時可不升版，但要在文件記錄差異。
3. **靜默降級，絕不 throw**：未知的圖層 key、越界數值、被鎖住／未釋出的圖層一律丟掉，寧可少一層也不要白屏；解析失敗的欄位只影響它自己。圖層 key 的白名單（存在於登記簿、非鎖定）放在 parse 階段，消費端看到的永遠是「未指定」或「至少一個合法值」，不會是空陣列。數值只收有限數字，範圍外回 undefined 而不是夾取；相機的經度、緯度、zoom 缺一就整組不用。
4. **哪些狀態該進網址**：相機、開啟的圖層、凍結的日期與小時、底圖、語系、國家／區域、顯示模式（單一／可重疊，見 [08-06](08-06-how-many-layers-at-once.md)）。**不該進**：使用者私有狀態、暫時 UI 狀態。部分參數（如各圖層控制值）可限定只給嵌入頁讀、主站忽略。
5. **反向也要測**：`buildUrl(parseUrl(u)) ≈ u`，並用壞網址、舊版網址、未知 key 做快速測試。
6. 分享連結載入時，圖層仍要走正常的載入狀態與資料權限，不因為網址帶了 key 就繞過。

```ts
// 解析：未知 key 丟掉、全部不合法 → undefined，不是 []
const layers = q.get("layers")?.split(",").filter((k) => ALLOWED.has(k));
return { layers: layers?.length ? layers : undefined };
```

## 怎麼偵測
- 通用：把連結末端截斷、改一個圖層 key 成亂碼、移除 `v=`，看頁面是否仍能打開；新增圖層後用舊連結載入。
- 搜尋：
  - 會 throw：`JSON\.parse\(.*searchParams|atob\(.*get\(` 沒有 try/catch；`layers\.split\(.*\)\.map\(.*\[` 直接以 key 取登記簿而不先檢查存在。
  - 序列化全部狀態：`buildUrl` 或 `history\.(push|replace)State` 寫入的鍵與預設值比較缺失。
  - React Router／Vue Router／History API 皆適用，差別只在讀寫 query 的 API。

## 出處
- URL 作為狀態容器的一般做法（深連結、可分享狀態）。
- 實例：[src/lib/urlState.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/lib/urlState.ts)（diff-based、版本化、靜默降級）、[embeddable-map README（嵌入碼參數）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/features/embeddable-map/README.md)。
