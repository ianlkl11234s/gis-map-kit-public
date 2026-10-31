# 09-design-system 設計系統

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [09-00](09-00-design-system-index.md) | 設計系統總表：token、四鐵則、面板、圖例、popup、控制項、四態、文字、RWD、符號 | 先看 [09-01](09-01-token-ssot-and-ratchet-guard.md) 建立 token 與… | catalog | Implemented | any | 總表, 設計系統, token, 四鐵則, 面板, 圖例, popup, 控制項, RWD, 符號尺寸 |
| [09-01](09-01-token-ssot-and-ratchet-guard.md) | 圖台設計系統骨架：token 單一來源＋規格文件＋只降不升的自動檢查 | 圖台長大後，每個面板的圓角、字級、灰階、陰影都略有不同；有人寫死 hex、有人引入 web font；暗色模式修好了，淡… | pattern | Implemented | any | design system, token, SSOT, lint, ratchet, guard, 暗色, 淡色, 字型 |
| [09-02](09-02-layer-ux-four-iron-rules.md) | 圖層 UX 四鐵則：透明度、圖例、popup、選單，缺一不可 | 新圖層上線後：看不出類別（沒圖例）、點了沒反應（沒 popup）、蓋住別的圖層又不能調（沒透明度）、篩選選項太多用按鈕排… | pattern | Implemented | any | 圖層, 透明度, 圖例, popup, select, 驗收, checklist, 鐵則, 新增圖層 |
| [09-03](09-03-panels-layering-and-portal.md) | 面板、層級與彈出層：停靠位置、z-index 分層、互斥與 portal | 面板、popup、圖例、時間軸互相蓋住；為了壓過別人把 z-index 越寫越大（21、41、9999）。 | pattern | Implemented | any | 面板, panel, z-index, 互斥, portal, 下拉, popover, 停靠, 標頭, 彈出層 |
| [09-04](09-04-legend-spec.md) | 圖例規格：標題、色票型態、與地圖同源、可收合的範圍 | 各圖層圖例長得不一樣：標題大寫英文在前、色票尺寸各寫各的、有的有單位有的沒有、popup 打開時圖例擠掉畫面。 | pattern | Implemented | any | 圖例, legend, 色票, swatch, 漸層, 缺值, 收合, 精簡版, 標題 |
| [09-05](09-05-popup-and-source-footer.md) | popup 與來源 footer：固定結構、null 不渲染、來源缺漏要明講 | 每個圖層的 popup 長得不一樣；欄位出現內部代號（dataset id、layer key）。 | pattern | Implemented | any | popup, 資訊面板, 來源, footer, 授權, null, 內部 id, 選取圈, 停靠 |
| [09-06](09-06-layer-controls-spec-driven.md) | 圖層控制項：用規格自動產生，固定順序與元件種類 | 每個圖層的控制區長得不一樣：滑桿樣式不同、開關有三種尺寸、篩選選單在不同位置、選項太多時用按鈕排滿、期別／指標選單彼此連… | pattern | Implemented | any | 控制項, 滑桿, 開關, 選單, 分段, 篩選, select, filter, opacity, 規格驅動, 連動選單 |
| [09-07](09-07-loading-data-time-and-stale.md) | 載入、錯誤、無資料、過期四態與資料時間標示 | 資料載入時畫面沒反應，使用者以為壞了；或載入提示一閃即逝。 | pattern | Implemented | any | loading, 載入, 錯誤, 過期, stale, 資料時間, 新鮮度, 時間軸, 未涵蓋, skeleton |
| [09-08](09-08-text-hierarchy-dark-basemap.md) | 地圖介面的文字層級與對比：六階文字色、暗淡成對、淡色徽章要混深 | 深色面板上標籤、數值、說明都是同一種灰，看不出主次；換到淡色底圖後，同一組灰又太淡；黃、淺綠這類淺色相的徽章文字在白色面… | pattern | Implemented | any | 文字層級, 對比, 深色, 淡色, 徽章, chip, 字級, 地圖標籤, halo, 淺色相 |
| [09-09](09-09-responsive-and-touch.md) | 圖台 RWD 與觸控最低清單：手機標頭、底部抽屜、hover 替代、safe-area、浮層全開檢查 | 在桌機拉窗測過 RWD，手機一轉橫式就壞；底部面板蓋住版權列或時間軸。 | pattern | Implemented | any | RWD, 手機, 觸控, hover, safe-area, 底部抽屜, bottom sheet, 橫式, 浮層, 斷點 |
| [09-10](09-10-map-symbol-size-tiers.md) | 地圖符號尺寸分三階，切換底圖只換色不改尺寸與透明度 | 同一個圖台裡，A 圖層的點半徑 3、B 圖層 8，線寬從 0.5 到 4 都有，面透明度 0.04 到 0.85；切換暗… | pattern | Implemented | mapbox-gl, maplibre | 點大小, 線寬, 面透明度, 描邊, 熱區, 三階, 密集點, 底圖切換, 尺寸 |
