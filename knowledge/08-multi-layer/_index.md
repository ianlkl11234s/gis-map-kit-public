# 08-multi-layer 多圖層管理

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [08-00](08-00-multi-layer-index.md) | 多圖層管理總表：登記、守門、狀態、疊放、上限、新增與分享 | 圖層事實只在登記簿定義一次，其餘一律派生；先看 [08-01](08-01-layer-registry-single-… | catalog | Implemented | any | 總表, 多圖層, 登記簿, 開關, 疊放, 分享網址, 搜尋別名, 多國化 |
| [08-01](08-01-layer-registry-single-source.md) | 圖層登記簿單一來源：一筆登記派生 UI、圖例、popup、控制項，別在多處各抄一份 | 新增一個圖層要改多個檔案、多個地方：顏色表、圖示表、圖層面板、資料來源表、圖例表、點擊表……少改一處，畫面就缺一塊（沒圖… | pattern | Implemented | any | 登記簿, manifest, registry, SSOT, 圖層清單, 派生, 單一來源, 漂移, 新增圖層, 面板 |
| [08-02](08-02-registry-completeness-tests-and-ledger.md) | 登記簿的自動守門：完整性測試＋「豁免要登記理由」的雙向 ledger | 新圖層上線後才發現沒有圖例、點了沒 popup、沒有透明度滑桿。 | pattern | Implemented | any | 測試, 完整性, ledger, ratchet, 豁免, null, 圖例, popup, 守門, CI, 契約測試 |
| [08-03](08-03-layer-visibility-store.md) | 圖層開關狀態：細粒度訂閱的 store，預設全關，快照 identity 只在真的變動時換 | 任何一個圖層切換，整個 App 重新渲染；圖層一多，開關就卡。 | pattern | Implemented | any | 圖層開關, visibility, store, useSyncExternalStore, 訂閱, identity, 預設狀態, 全部關閉, 狀態管理 |
| [08-05](08-05-layer-stacking-order.md) | 多圖層疊放順序：登記順序就是 z-order，大面積在底、選取圈在頂，動態重建會跑到最上層 | 打開一張全島 raster（例如熱島、影像）後，其他點圖層全被蓋住。 | pattern | Observed | mapbox-gl, maplibre, leaflet, openlayers, deck.gl | z-order, 疊放, 圖層順序, beforeId, addLayer, 遮蔽, 選取圈, 熱力圖, 底圖標籤, raster, 重建 |
| [08-06](08-06-how-many-layers-at-once.md) | 同時開幾個圖層：上限不要憑感覺，分「每種資源」各自設限 | 同時開十幾個圖層，畫面糊成一片，使用者看不出誰是誰；或兩張面量圖互相蓋住，顏色變成混色。 | decision | Implemented | any | 圖層數量, 上限, 可讀性, 效能, 面量圖, 單一, 可重疊, 同時只開一個, 選取圈, 面板, 脈衝 |
| [08-07](08-07-new-layer-checklist.md) | 新增圖層 checklist：資料驗收、接線、UX、瀏覽器單層驗收，各步驟誰來守 | 新圖層上線後才發現：點數比來源少、popup 欄位全是 undefined、分色全同色、檔案路徑 404、座標落在赤道附… | pattern | Implemented | any | checklist, 新增圖層, 驗收, 上線, onboarding, All Off, 資料驗收, 常漏項, 守門 |
| [08-08](08-08-shareable-layer-state-url.md) | 分享網址記住開了哪些圖層：只寫與預設不同的項目，讀不懂的就丟掉 | 使用者分享的連結打開後是空白預設畫面，或開了不同的圖層。 | pattern | Implemented | any | 分享連結, URL state, query string, deep link, 嵌入, 版本, 靜默降級, 圖層, 白名單, 相機 |
| [08-09](08-09-layer-search-alias-only-for-misses.md) | 圖層搜尋別名只補「名稱命不中」的詞，名稱、說明、主題一律從登記簿派生 | 使用者搜「急診」找不到「醫院」圖層，或搜英文找不到中文名圖層。 | pattern | Implemented | any | 圖層搜尋, 別名, alias, 同義詞, 登記簿, 排序, 單一來源 |
| [08-10](08-10-multi-country-country-selector-no-cross-mix.md) | 多國化：國家當面板主體而不是另開一個入口，視野只提示不自動切，跨國只並列不混算 | 每加一個國家就在側欄多一個入口，外國永遠是次一級；國名寫死在程式的 `if` 裡，加一國要改很多處。 | decision | Implemented | any | 多國, 國家選單, country selector, 國碼, ISO 3166, 分享網址, 視野提示, 全部關閉, 跨國比較, MAUP, 分母, 未涵蓋, registry, 主題識別字 |
