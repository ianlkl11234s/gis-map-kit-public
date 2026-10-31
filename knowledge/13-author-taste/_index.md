# 13-author-taste 作者品味與設計偏好（非業界規範）

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [13-00](13-00-taste-overview.md) | 作者的地圖設計品味總表：每項偏好一句理由，對應到細卡 | 新專案每次都重新決定 SDK、底圖、字型、圓角、動態預設，每個作品長得不一樣。 | catalog | Implemented | any | 設計品味, 偏好, 預設值, 總表, 深色底圖, MapLibre, 系統字 |
| [13-01](13-01-sdk-maplibre-default.md) | SDK 預設 MapLibre，同時申請 Mapbox token 備用，需要時才換 | 新專案一開始就綁 Mapbox，之後發現流量計費、token 外露或授權問題才想換。 | decision | Implemented | mapbox-gl, maplibre | MapLibre, Mapbox, token, SDK 選型, 費用, 免費額度, globe |
| [13-02](13-02-basemap-dark-mono-default.md) | 底圖預設深色單色，衛星只在要看地表實況時用，淡色不是預設 | 底圖顏色太多、道路與地名太搶，資料色被吃掉。 | decision | Implemented | any | 底圖, 深色, 單色, 衛星, 淡色, 標籤, 對比 |
| [13-03](13-03-color-dark-accent-glow.md) | 色彩：近黑底加單一強調色，發光只給進行中的東西 | 畫面彩度過高、每個圖層搶焦點；到處都在發光，看不出什麼是即時的。 | pattern | Implemented | any | 色彩, 強調色, 發光, additive blending, 色階, bloom |
| [13-04](13-04-ui-one-ruleset.md) | UI 統一一套規則：系統字、不載 web font、圓角 8 以內、資訊密度適中 | 同一個人的作品，字型與圓角各自為政；載入 web font 造成首屏變慢與跳字。 | decision | Implemented | any | UI, 字型, web font, 圓角, 玻璃面板, 圖例, popup, design token |
| [13-05](13-05-motion-data-driven.md) | 動態要由資料驅動，用插值平滑，時間軸預設不播放 | 打開頁面就自己播放，使用者還沒看懂就跑掉了。 | pattern | Implemented | any | 動態, lerp, 插值, autoplay, reduced-motion, 時間軸, 假動態 |
| [13-06](13-06-camera-and-3d.md) | 鏡頭總覽俯視、場景才傾斜；立體要有理由，預設平面且每層可開 | 一打開地圖就是傾斜視角，總覽時比較面積與位置會失真。 | pattern | Implemented | any | 鏡頭, pitch, bearing, 3D, 立體, 總覽, 傾斜 |
| [13-07](13-07-dont-list.md) | 作者的反面清單：明確不要的做法與偵測條件 | 畫面看起來精緻，但有些做法會誤導讀者或讓維護變難。 | catalog | Implemented | any | 不要, 反面清單, 假進度條, 缺值, 大寫, 假動態, gis-review |
