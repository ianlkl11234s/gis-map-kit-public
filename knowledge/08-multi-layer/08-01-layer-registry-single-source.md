---
id: 08-01
title: 圖層登記簿單一來源：一筆登記派生 UI、圖例、popup、控制項，別在多處各抄一份
topic: 08-multi-layer
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [登記簿, manifest, registry, SSOT, 圖層清單, 派生, 單一來源, 漂移, 新增圖層, 面板]
---

## 原則
圖層的名稱、顏色、圖示、主題、資料來源等登記事實只在一處定義，其餘的表、面板、圖例、控制項一律從它派生，不要在多處各抄一份。

## 症狀
- 新增一個圖層要改多個檔案、多個地方：顏色表、圖示表、圖層面板、資料來源表、圖例表、點擊表……少改一處，畫面就缺一塊（沒圖例、點了沒反應、面板沒列出）。
- 同一個圖層的名字、顏色在兩個側欄各抄一份，改了一邊另一邊漂移。
- 型別檢查擋得住「欄位不存在」，擋不住「填了錯的值」。

## 原因
圖層的「登記事實」（叫什麼、什麼色、什麼圖示、屬於哪個主題、資料從哪來、有沒有圖例／popup／控制項）被複製進多張表。複製就會漂移。

## 解法
**把登記事實收成一處，其他表一律從它派生。** 與框架無關的做法：

1. **一個登記檔，每個圖層一筆**，欄位只放「事實與指向」：key、顯示名、顏色、圖示、所屬主題、資料來源、`legend`／`popup`／`params` 的指向宣告。欄位值寫 `null` 要有意義：`legend: null` 代表「有意識地沒有」，需另行登記理由（見 [08-02](08-02-registry-completeness-tests-and-ledger.md)）。
2. **實質邏輯不進登記檔**：loader、hook、paint 表達式、圖例元件、popup 元件各自留在原處。登記檔若什麼都放，就會變成一個巨大且人人都要改的檔案，退回原點。
3. **下游表用函式派生**：`LAYER_COLORS = mapValues(MANIFEST, e => e.color)`；面板的圖層列、圖示、資料來源清單同理。下游禁止反向 import 登記檔以外的東西造成循環（import 方向要單向，登記檔只依賴型別與零相依的常數）。
4. **參數控制項也用宣告式規格**（滑桿／下拉／開關的預設值、範圍、選項、傳給 paint 的編碼）：值的 store、控制項長相、傳給 paint 的編碼三者都從同一筆規格派生，不再有「加 state＋加 case＋加編碼＋加 deps」四五個手寫位置。規格與登記檔分開放，再用契約測試焊在一起（規格派生的控制項數量與種類 = 登記檔宣告）。
5. **所有入口用同一個面板元件**：桌機側欄、手機底部面板、不同國家／主題的入口，定義只有一份、渲染元件只有一個；不准在任何面板另畫一份圖層列或控制項，並用測試擋。
6. 搬遷既有專案時，先用「等價快照」（把舊的各表輸出凍成 fixture，搬完逐位元比對）確認派生結果與原本完全一致，再刪舊表。

```ts
// 登記一筆
export const MANIFEST = {
  riverRpi: { label: "河川污染指數", color: C.rpi, icon: "droplet", theme: "water",
              source: "river-rpi", legend: "riverRpi", popup: "riverRpi", params: { count: 2 } },
  // ...
} as const satisfies Record<LayerKey, Entry>;

// 下游全部派生
export const LAYER_COLORS = mapValues(MANIFEST, (e) => e.color);
export const LAYER_ICONS  = mapValues(MANIFEST, (e) => e.icon);
```

React／Vue／純 JS 都適用：差別只在最後一步「由登記簿渲染面板」是元件還是 DOM 產生函式。

## 怎麼偵測
- 通用：新增一個圖層時，數一數要改幾個檔案；問「顏色／名稱還有沒有第二個定義的地方」。
- 搜尋：
  - 重複登記：同一個圖層 key 字串出現在 3 個以上不同的「表」檔案（`rg -c "'myLayerKey'"` 看分布）（any）。
  - 手寫逃生口：`HANDWRITTEN_|LEGACY_|EXTRA_` 開頭的補充表，型別允許新 key 只登記在那裡（TypeScript）。
  - 入口各畫一份：兩個側欄元件各有自己的圖層列元件、各有自己的 `SECTIONS|THEMES` 常數（React、Vue）。

## 出處
- 一般「single source of truth＋派生」設計；宣告式 UI 規格（schema-driven form）。相關卡：[08-09](08-09-layer-search-alias-only-for-misses.md)（圖層搜尋別名只補名稱命不中的詞，其餘從登記簿派生）。
- 實例：[src/data/layerManifest.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/layerManifest.ts)、[src/data/layerParamsSpec.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/data/layerParamsSpec.ts)、[docs/development-rules.md（新增圖層觸點表）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/development-rules.md)。

