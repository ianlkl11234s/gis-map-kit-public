---
id: 04-08
title: 隨時間變化的面量圖／點／影像：改 feature-state、filter 或 uniform，不要重新 setData
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, deck.gl, three.js]
tags: [時間軸, choropleth, feature-state, setFilter, fade, uniform, 壅塞, 影像序列, 雷達回波, cross-fade]
---

## 原則
時間軸驅動的變化依「時間語意」改 filter、feature-state 或 GPU uniform，不要每幀 `setData`；兩期以上的色階級距用全部期別合併決定。

## 症狀
拖曳／播放時間軸時：面量圖或上萬點每幀卡頓；切期別後顏色級距跟著重算導致兩期不可比；影像序列閃爍。

## 原因
`setData` 與逐 feature 重算 data-driven 表達式都是 O(feature) 每幀；GPU buffer 重灌。

## 解法
按「時間語意」選手段：

| 想表達 | 手法 | 成本 |
|---|---|---|
| 累積顯示（到目前為止發生過的） | `setFilter(["<=", ["get","ts"], t])`，節流 200–1000ms | 每次一次 |
| 每個 feature 的狀態隨時間換色（壅塞、格網溫度） | `setFeatureState`，**只在等級改變時**寫；source 首次 loaded 後才可靠 | 只改變的 feature |
| 海量點隨時間淡入淡出（數十萬點） | 一次性上傳 GPU buffer + `uCursorTs` uniform，fade 在 shader 算；buffer 內存相對起點的差值 | 每幀固定 |
| 兩期／情境切換 | select + 換欄位或 filter；**色階級距用所有期別合併決定**，切換時不重算 | 一次 |
| 影像序列（雷達回波、衛星雲圖） | image source `updateImage`／換 URL；（一般建議）預載下一張避免閃爍 | 每張一次 |
| 熱力／密度隨時間 | 雙 slot 疊兩層 heatmap 做 cross-fade | 兩層 |
| 溫度曲面等連續場 | 相鄰兩 frame 的頂點高度逐幀 lerp | 每幀固定 |

細節：
- `float32` 精度：unix 時間戳（~1.7e9）超出尾數，shader buffer 要存「相對起點的差值」。
- 時間語意先判斷：track（只在資料時段顯示）／cyclic（只取時刻循環）／snapshot（顯示最近一張）／event（顯示 N 小時內）。
- 跨站比較的指標（水位）用「當日變化量」而不是絕對值，否則拖時間軸數字幾乎不動。
- 只有兩期資料時不補中間年份、不做播放動畫。
- 動態指標缺測畫「無資料」灰，不是 0。

## 怎麼偵測
- 通用：播放時 FPS 低；每幀 Network／CPU 有大量 JSON 序列化；暫停後仍在重繪。
- 搜尋：`setData\(` 在 `subscribe|requestAnimationFrame|setInterval` callback 內；`currentTime` 出現在 `useEffect|useMemo` deps（mapbox-gl、maplibre）。

## 出處
- 相關卡：[04-16](04-16-dont-fake-dynamics.md)、[07-06](../07-performance/07-06-float32-timestamp-precision.md)。
- 實例：[mini-taiwan-pulse RealEstatePointsScene.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/RealEstatePointsScene.ts)（大量點改 GPU uniform 淡入淡出）；[useRoadCongestionLayer.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/hooks/useRoadCongestionLayer.ts)；[temperatureGridLayerFactory.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/temperatureGridLayerFactory.ts)；[cwaImageryLayer.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/cwaImageryLayer.ts)（影像序列）。

