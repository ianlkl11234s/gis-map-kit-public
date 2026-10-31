---
id: 04-09
title: 強調類效果：脈衝、光柱、旋轉燈塔、閃爍、選取圈——每一種都要有語意
topic: 04-effects-catalog
kind: pattern
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, three.js]
tags: [脈衝, 光柱, beam, 燈塔, 旋轉, 閃爍, 選取圈, 警示, InstancedMesh, 階級]
---

## 原則
強調效果先寫出語意句再選效果，疊在原生圖層上而非取代它；同時持續動的元素要少，答不出「拿掉會少看懂什麼」就不要做。

## 症狀
想讓某類點「被看見」，結果全圖都在閃，使用者不知道哪個重要；或四個階級只靠顏色看不出差別。

## 原因
強調效果是在花使用者的注意力。沒有語意的動畫是雜訊。

## 解法
先填語意句：「每個物件是［主體］，正在［動作／狀態］，影響［範圍］」，再選效果：

| 語意 | 效果 | 做法 |
|---|---|---|
| 週期性運作的裝置（燈塔、雷達） | 旋轉光束／掃描扇形 | 半透明錐 + 旋轉角度（暫停時凍結角度）；每座起始相位錯開 |
| 階級／重要度 | 光柱高度與半徑依階級 + 頂端光球 | `InstancedMesh`（柱／帽／漣漪三個 instance 組）per-instance 顏色與縮放；疊在原生 circle 上，circle 負責俯視可見與 popup |
| 警示／異常 | 閃爍 | 低頻、只在異常態啟動；shader 內算，不用 JS 逐物件 |
| 剛發生的事件 | ripple | 見 [04-06](04-06-ripple-and-wavefront.md)，用「剛發生」時間窗限制 |
| 目前選取的物件 | 呼吸圈 | 全站單一元件，位置來自單一「最後點擊」記錄；超過 10 秒的點擊不再代表目前面板 |
| 設施的「性格」（焚化爐火苗煙、轉運站雷達、醫療偶發閃電） | 小型戲劇化 scene | 量少（數十處）才值得；一個 layer 內多 sub-scene 各自開關 |
| 飄浮粒子（音符飄起） | GPU billboard `Points` | 環形 buffer 重用 slot、`uTime - aSpawnTime` 在 vertex shader 算位置與大小 |

通則：
- 同一時間畫面上持續動的元素要少；純裝飾動畫在時間軸暫停時也不該拖累效能（見 [04-15](04-15-animation-repaint-budget.md)）。
- 疊在原生圖層上而非取代它：保留 popup、點擊、俯視可見性。
- 光柱／3D 元件預設 ≤ 數百處；超過千點改用密度表達（h3、heatmap）。
- 「拿掉這個效果，使用者會少看懂什麼？」答不出來就不要做。

## 怎麼偵測
- 通用：全圖多處同時閃爍；動畫元素超過數百仍各自一個 mesh；選取圈殘留在已關閉的面板。
- 搜尋：`new THREE\.Mesh` 在迴圈內且數量 > 100（three.js）；`@keyframes` 套在大量 marker DOM 上（any）。

## 出處
- 相關卡：[04-06](04-06-ripple-and-wavefront.md)、[04-15](04-15-animation-repaint-budget.md)。
- 實例：[mini-taiwan-pulse FireStationScene.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/FireStationScene.ts)（依階級分柱高）、[LighthouseScene.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/three/LighthouseScene.ts)（旋轉光束、暫停凍結）、[selectionRing.ts](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/src/map/selectionRing.ts)（單一選取圈）。
