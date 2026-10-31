---
id: 04-10
title: 偽 bloom 光暈點：一個 Points draw call + 三段 halo + 加性混合
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, three.js]
tags: [bloom, glow, 光暈, AdditiveBlending, Points, 夜景, 發電廠, renderOrder, 亮色主題]
---

## 原則
夜景式光暈用單一 `THREE.Points` + 三段 halo + `AdditiveBlending` 自繪，不引入後處理 bloom；光暈大小乘 zoom 係數，亮色主題改 Normal blending 並明確設 `renderOrder`。

## 症狀
想要「夜晚城市燈火」感：密集處自然爆白、疏處是柔和光點。用原生 `circle` + 大 blur 做不出疊加爆白；用後處理 bloom（UnrealBloomPass）又要新增依賴、和 Mapbox 共用 GL context 麻煩。

## 原因
爆白需要加性混合（顏色相加），原生 layer 沒有。

## 解法
- 一支 `THREE.Points` + 自訂 `ShaderMaterial`，零新依賴：fragment 疊三段徑向 halo（core／mid／far），`AdditiveBlending`，`depthWrite/depthTest: false`；白心：`col = mix(color, white, core * coreBoost)`，coreBoost 約 0.7。
- 通用輸入：`{lon, lat, colorHex, sizeNorm 0–1}[]`，不綁業務；顏色在餵資料時決定（連續色帶或分類），shader 不管語意。
- 大小：`sqrt(值/max)` 壓縮右偏分布，再乘 `pixelRatio × zoomScale × 使用者倍率`。
- **zoom 自適應**：`gl_PointSize` 永遠是螢幕像素，不隨 zoom 縮；拉遠到全國時每顆光暈會蓋住大片區域。乘 `1.5^(zoom - refZoom)`（下限～上限夾住），不要用 2 的底（會與地理尺度完全同步，光暈失去動感）。
- 線狀物（輸電線）：instanced 四邊形展開成固定像素寬 fat line，fragment 用指數衰減做亮中心 emissive。
- 夜景建物：從視野內 `querySourceFeatures` 取高度大於門檻的建物，去重後取前 N 棟（如 4,096）餵光暈；低 zoom 是城市群聚發亮、高 zoom 是逐棟 beacon。
- **亮色主題陷阱**：暗色用 Additive、亮色必須改 Normal + 深飽和色。Additive 具交換律，疊序錯誤在暗色下看不出來；一到亮色就有 mesh 蓋到不該蓋的。多層（外暈、內暈、白心、閃爍）要設明確的 `renderOrder`（取 0～1 間小數，避開預設 0 的其他 mesh）。
- `depthWrite` 與 `depthTest` 是兩件事：透明物幾乎都該 `depthWrite:false`。
- 想貼 globe 見 [04-13](04-13-custom-layer-on-globe.md)。

## 怎麼偵測
- 通用：縮到全國視野光暈蓋滿；切亮色主題後疊序怪；光點在 globe 背面仍可見。
- 搜尋：`AdditiveBlending` 且檔內沒有 `renderOrder`；`gl_PointSize\s*=` 沒有 zoom 係數（three.js）。

## 出處
- 相關卡：[04-03](04-03-trail-tails.md)、[04-13](04-13-custom-layer-on-globe.md)。
- 實例：[mini-taiwan-pulse GlowPointsScene.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/GlowPointsScene.ts)（發電廠 bloom 原型）、[powerPlantGlowCustomLayer.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/powerPlantGlowCustomLayer.ts)。

