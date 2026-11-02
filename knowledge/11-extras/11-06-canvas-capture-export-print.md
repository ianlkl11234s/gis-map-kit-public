---
id: 11-06
title: 截圖、匯出與列印：WebGL 畫布不是隨時讀得到（黑畫面），不要為了截圖整站開 preserveDrawingBuffer
topic: 11-extras
kind: pitfall
scope: public
evidence: Implemented
stacks: [mapbox-gl, maplibre, three.js]
tags: [截圖, preserveDrawingBuffer, toDataURL, 黑畫面, Capture mode, 匯出, CSV, GeoJSON, 列印, 錄影, 逐格, 轉場, 防暈, wipe, 宣傳影片]
---

## 原則
在 `render` 事件的同一個 tick 內同步讀取畫布，不為了截圖整站開 `preserveDrawingBuffer`；錄影一律逐格拍真實畫面。

## 症狀
- `canvas.toDataURL()` 或錄影拿到全黑畫面。
- 為了截圖開了 `preserveDrawingBuffer: true`，整站效能變差。
- 列印出來地圖是空白（canvas 沒轉成圖）。
- 錄的宣傳影片每次重錄都不一樣、掉幀，或觀眾反映轉場看了會暈。
- 匯出的資料沒帶來源、授權、時間，或包含不該外流的欄位。

## 原因
WebGL 預設在畫面合成後清空繪圖緩衝區，畫布內容只保證在 `render` 事件的同一個 tick 內讀得到；`preserveDrawingBuffer` 預設為 false（MapLibre 官方預設值）。

## 解法
**截圖**
1. 程式化取像在 `render` handler 內同步完成：先 `map.triggerRepaint()`，再在 `once('render')` 內讀取。要保留緩衝才明確開 `preserveDrawingBuffer`，並說明代價。
2. 若為了效能把它從 true 改回 false，要接受約零點幾個百分點的像素差異，並重建視覺回歸基準。
3. 提供「拍攝模式」（隱藏所有介面、只留地圖與標題，Esc 離開，遵守 reduced-motion），截圖交給使用者或自動化瀏覽器，比做下載按鈕便宜。
4. 要截某一時刻，配合分享網址的時間參數（[11-04](11-04-share-camera-og-image-saved-scene.md)）。
5. 行動瀏覽器的錄影相容性要實機驗證。

**錄影（宣傳、回顧、前後對比影片）**
1. 逐格拍真實畫面，不要即時錄螢幕、也不要用 HTML 重刻介面：每格用程式把鏡頭跳到插值位置（`jumpTo`，ease-in-out）→ 等地圖 `idle`（設上限）→ 截圖；時間推進也由程式控制。介面動效可用 Web Animations API 暫停後逐格拍。這樣每次重拍結果一致，不受機器卡頓影響。
2. 用正式站與拍攝模式取材，隱藏不該入鏡的控制項；保留底圖與資料署名。
3. 避免頭暈：畫面主體保持穩定，前進感交給時間軸、計數器等框架元素；轉場用細光縫掃過（wipe），前後景位移很小；不要整張橫推、水平動態模糊或白閃頻閃；鏡頭運動方向一致、速度慢（運鏡原則見 [04-12](../04-effects-catalog/04-12-camera-motion.md)）。
4. 前後對比：同一畫面只換介面，用分隔線單程掃過（不淡入、不掃回），第一格就要有畫面與標題。
5. 把抽樣幀拼成縮圖總覽（contact sheet），逐張看過每個轉場中點與固定間隔的抽樣幀再發布。
6. 影片中的數字要能溯源、日期不捏造；入鏡內容先排除個資與點名內容。

**匯出與列印（候選設計）**
- 匯出 CSV／GeoJSON：帶來源、授權、資料時間；排除個資與不能再散布的欄位；大量資料用串流或分段。
- 列印：`@media print` 隱藏控制項；WebGL 畫布列印前先轉成圖片（同截圖規則）。

## 怎麼偵測
- 通用：按截圖／錄影得到黑畫面；列印預覽空白；影片素材是手動滑鼠錄的、轉場整張橫推或頻閃。
- 搜尋：`toDataURL|getImageData|captureStream` 不在 `render` handler 內；`preserveDrawingBuffer:\s*true` 無註解理由；`window\.print|@media print` 零命中而產品需要列印；匯出函式未過濾欄位（適用 stack：mapbox-gl、maplibre、three.js）。

## 出處
- MapLibre MapOptions `canvasContextAttributes.preserveDrawingBuffer`：https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapOptions/ 。匯出與列印部分為一般業界做法，未經實作驗證。
- 相關卡：[04-12](../04-effects-catalog/04-12-camera-motion.md)、[11-04](11-04-share-camera-og-image-saved-scene.md)。
- 實例：[mini-taiwan-pulse 設計規格中的拍攝模式（Capture mode）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/docs/design-system/spec.md)。

