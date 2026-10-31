---
id: 14-07
title: 移動物件與軌跡的規模：容量先定上限、軌跡依鏡頭範圍換抽稀層、粒子拉遠反而要加
topic: 14-scale-density
kind: pattern
scope: public
evidence: Implemented
stacks: [any]
tags: [移動物件, 軌跡, LOD, 抽稀, Douglas-Peucker, 容量上限, instancing, 粒子, 自適應, 方向箭頭, 遲滯]
---

## 原則
移動物件先定容量上限並用 GPU 一次畫完；軌跡可抽稀、點資料不可；拉近換方向箭頭，粒子數隨縮放自適應。

## 症狀
- 船舶或航班一多，軌跡頂點爆量，記憶體一路漲。
- 世界視角載入全解析度航跡，下載數十 MB 卻看不出差別。
- 風場粒子在近景剛好，拉遠就稀到看不見流向。
- 車輛點全台視角擠成一團，拉近又看不出往哪走。

## 原因
移動物件的成本是「物件數 × 每個物件的頂點 × 更新頻率」，三者都會隨資料成長。鏡頭越遠，每個像素涵蓋的距離越大，細節沒必要；但流場類的視覺要維持「螢幕上的密度」，拉遠反而要更多粒子。

## 解法
1. **先定容量上限**：每種場景的物件數與軌跡頂點數寫成常數（例：軌跡 3 萬–20 萬頂點、發光點 4,096），超過就逐出最舊（[07-05](../07-performance/07-05-batched-trails-min-heap-eviction.md)），不要無上限成長。
2. **GPU 一次畫完**：數千以上的移動物件用 instancing 或單一 Points draw call，位置寫 typed array（[07-04](../07-performance/07-04-update-granularity-setdata-vs-buffer.md)）。
3. **軌跡依鏡頭範圍選檔**：
   - 世界／區域：抽稀檔，Douglas-Peucker 誤差小於一個像素涵蓋的距離（例：區域視角 2–3 km／px 時用 2 km），每條再設點數硬上限（例：40），超過就放大誤差重算。
   - 中間縮放：中階抽稀（例：50 m、250 m）。
   - 單一場站：全解析度。
   - 高度有意義的軌跡（航跡）抽稀時把高度一起算（3D 距離，可放大高度權重），避免爬升折點被抹平。
   - 兩種策略（依鏡頭範圍換抽稀層、單一固定抽稀檔）都可用，依用途選（作者偏好）：資料量大、要跨尺度瀏覽用前者；單一尺度或小資料用後者。
4. **點資料不抽稀，軌跡可以抽稀**：抽掉軌跡的中間點不改變「有這筆資料」；抽掉點就是少了資料（[14-05](14-05-honest-aggregation.md)）。
5. **拉近換表現**：平面點拉近（約 z12）換方向箭頭；3D 場景依相機距離切換光點與模型，用進出兩個門檻防閃爍（[14-03](14-03-zoom-handoff-pitfalls.md)）。
6. **粒子數隨縮放自適應**：近景用設定值；每拉遠一級乘一個倍率並設上限，數量量化到固定倍數，避免每幀重配置陣列。
7. **流向線太多就簡化表現**：例如 ≥ 30 條流線或使用者開啟減少動態時，退回靜態弧線。
8. 時間插值與「只在資料窗內動」見 [04-02](../04-effects-catalog/04-02-moving-objects-interpolation.md)；不要用插值假造動態（[04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)、[12-08](../12-domain-pitfalls/12-08-vehicle-interpolation-fake-motion.md)）。

## 怎麼偵測
- 通用：開移動物件圖層放著跑 10 分鐘，看記憶體與頂點數是否持續成長；世界視角看 Network 是否下載全解析度軌跡。
- 搜尋：`push\(` 進軌跡陣列且沒有上限常數（`MAX_|CAPACITY`）；`new THREE.Mesh` 或 `new mapboxgl.Marker` 出現在逐物件迴圈；粒子數是常數、與 zoom 無關（three.js、mapbox-gl custom layer、deck.gl）。
- 軌跡檔只有一種解析度且單檔 > 10 MB。

## 出處
- 一般演算法：Douglas-Peucker 線簡化；LOD（level of detail）與遲滯切換。
- 相關卡：[07-04](../07-performance/07-04-update-granularity-setdata-vs-buffer.md)、[07-05](../07-performance/07-05-batched-trails-min-heap-eviction.md)、[04-02](../04-effects-catalog/04-02-moving-objects-interpolation.md)、[04-03](../04-effects-catalog/04-03-trail-tails.md)、[04-04](../04-effects-catalog/04-04-flow-particle-field.md)、[04-16](../04-effects-catalog/04-16-dont-fake-dynamics.md)、[12-04](../12-domain-pitfalls/12-04-track-gap-segmentation.md)、[12-08](../12-domain-pitfalls/12-08-vehicle-interpolation-fake-motion.md)。
- 實例：[mini-taiwan-pulse 船舶軌跡容量上限](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/ShipScene.ts)。
- 實例：[發光點容量](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/GlowPointsScene.ts)。
- 實例：[方向箭頭縮放門檻](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/flatMovingLayers.ts)。
- 實例：[粒子數隨縮放自適應](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/climateParticleLineLayer.ts)。

