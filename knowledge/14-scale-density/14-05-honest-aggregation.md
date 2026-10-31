---
id: 14-05
title: 聚合後要誠實：篩選時不能顯示未篩選的總量、抽稀不能冒充全部、空格與未涵蓋不是 0
topic: 14-scale-density
kind: pitfall
scope: public
evidence: Implemented
stacks: [any]
tags: [聚合, 格網, 熱區, 抽稀, drop-densest, 篩選, 未涵蓋, 空格, 計數, 小樣本, 誠實表示]
---

## 原則
聚合層（格網、熱區、圖磚內被抽稀的點）要和明細同步：篩選時隱藏或同步篩選聚合層，不抽稀點資料，空格與未涵蓋不畫成 0，小樣本不上色。

## 症狀
- 使用者勾選「只看製造業」，拉遠後的密度格網仍是全部公司的量。
- 向量圖磚在低 zoom 自動丟掉部分點，熱區看起來比實際稀疏，但圖例沒有說。
- 沒有資料的格子畫成最淺色，被讀成「很少」。
- 只有 2 班車的路段算出 100% 超載，被畫成最紅。

## 原因
聚合是另一份資料（預先算好的格網、圖磚內被抽稀的點），它和明細不一定同步。前端常常只篩了明細，聚合層沒跟著篩，畫面就說了錯的數字。

## 解法
1. **聚合層沒套用篩選時，篩選一開就隱藏聚合層**，並在圖例說明「拉近看篩選後的點」；不要顯示未篩選的總量。
2. **熱區與點共用同一個 filter**；點若用透明度做篩選，熱區改用 `weight` 0／1 同步。
3. **點資料預設不抽稀**：建置向量圖磚時宣告「不抽樣」，並在建置驗證擋掉 `drop-densest`、`drop-fraction`、`cluster-distance` 類參數。真的抽稀了，就不要在上面再疊熱區（熱區會反映被抽掉後的密度），並在圖例寫明。
4. **空格不畫**：網格只畫有觀測的格；來源明確計數 0 才能畫成 0 級，缺值、未涵蓋、遮蔽各自表示（[05-04](../05-color/05-04-null-is-not-zero-color.md)、[06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)）。
5. **小樣本不上色**：比率類指標設最小樣本門檻（例：班次 < 5 不畫），低於門檻是「不足以判斷」，不是 0。
6. **計數寫法**：≥ 1 萬寫「1.2 萬」、< 1 萬用千分位；聚合單位（格網大小、層級）寫進圖例。
7. 推估或模擬的聚合（例：人口推估格網）要標示是推估（[06-08](../06-data-formats/06-08-label-estimates-and-models.md)）。

## 怎麼偵測
- 通用：開任何篩選後拉到最遠，看聚合層的數字或顏色有沒有跟著變；不變就是說謊。
- 搜尋：tippecanoe 參數含 `--drop-densest-as-needed|--drop-fraction-as-needed|--cluster-distance|-r[0-9]`，而同層又有 heatmap 或宣稱完整（any）；格網 `fill-color` 的 fallback 是色階第一級而不是透明（適用 stack：mapbox-gl、maplibre）；聚合層的 `layout.visibility` 沒有依篩選狀態切換。
- 比率圖層沒有最小樣本門檻（找 `ratio|rate|share` 欄位卻沒有 `n|count|trips` 的下限判斷）。

## 出處
- 一般統計製圖慣例：小樣本比率不穩定；缺值與零值要可區分。
- 缺值畫法 [05-04](../05-color/05-04-null-is-not-zero-color.md)；資料契約 [06-06](../06-data-formats/06-06-zero-null-stale-data-contract.md)；推估標示 [06-08](../06-data-formats/06-08-label-estimates-and-models.md)；抽稀被否決的背景 [07-02](../07-performance/07-02-many-points-rendering.md)。
- 實例：[mini-taiwan-pulse 格網在篩選時隱藏](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/overlayRegistry.ts)。
- 實例：[熱區 weight 同步篩選](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/mapStyleScale.ts)。
- 實例：[建置驗證擋抽稀參數](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/scripts/preprocess/verify-public-life-assets.py)。
