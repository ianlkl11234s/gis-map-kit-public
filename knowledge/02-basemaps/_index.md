# 02-basemaps 底圖

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [02-00](02-00-basemaps-index.md) | 底圖總表：選型、授權計費、客製、切換、attribution、深淺色、自託管與地形 | 先把地圖拆成地理資料、底圖服務、渲染 SDK、格式儲存四層，先定 SDK 與計費授權，再選底圖；流量不可控的頁面預設自託… | catalog | Implemented | any | 總表, 底圖, 選型, 授權, 計費, attribution, setStyle, PMTiles, 地形, 深淺色 |
| [02-01](02-01-four-layers-data-tiles-sdk-format.md) | 「地圖」是四層：地理資料、底圖服務、渲染 SDK、格式與儲存，不要混成一張廠商比較表 | 選型討論變成「Mapbox 還是 OSM 還是 Leaflet」，雞同鴨講；換了圖磚來源卻發現帳單沒變；換 SDK 後 … | decision | Implemented | any | 底圖, OSM, Mapbox, MapLibre, Leaflet, deck.gl, PMTiles, Style JSON, 向量圖磚, 分層 |
| [02-02](02-02-basemap-selection-decision.md) | 底圖選型：Mapbox、MapLibre＋自架 PMTiles、OpenFreeMap、CARTO、OSM 圖磚、NLSC 的費用／授權／離線取捨 | 不確定該用哪個底圖；流量變大後帳單暴增；被服務商封鎖；離線展示或嵌入頁出問題；中文地名或國界不符預期。 | decision | Evaluated | any | 底圖選型, Mapbox, MapLibre, PMTiles, Protomaps, OpenFreeMap, CARTO, OSM, NLSC, 通用版電子地圖, 離線, 費用, 國界, 地名 |
| [02-03](02-03-osm-data-license-vs-tile-policy.md) | OSM 的「資料授權」不等於「圖磚伺服器使用政策」 | 因為「OSM 資料可以自由使用」，就把 `tile.openstreetmap.org` 寫進正式站、離線版，或做批量預… | pitfall | General | any | OSM, ODbL, tile.openstreetmap.org, 使用政策, 預抓, 離線, User-Agent, 封鎖, 標示 |
| [02-04](02-04-mapbox-billing-token-license.md) | Mapbox 注意事項：以 Map 初始化計費、token 分兩種、v2 起非開源 | 以為「換成自己的圖磚就不用付 Mapbox 費用」，帳單沒變。 | decision | Evaluated | mapbox-gl | Mapbox, map load, 計費, token, public token, secret token, URL restriction, 授權, TOS, 嵌入 |
| [02-05](02-05-style-customization-by-code.md) | 底圖客製化：用程式覆寫官方 style（paint／layout、beforeId、地名、語言、字型、地形） | 想讓底圖變暗、隱藏地名、切換語言卻不想重寫 style；資料層蓋住地名；換底圖後地形異常。 | pattern | Implemented | mapbox-gl, maplibre | style, setPaintProperty, setLayoutProperty, beforeId, 地名, language, setLanguage, localIdeographFontFamily, terrain, globe, Standard, lightPreset, Mapbox Studio |
| [02-06](02-06-setstyle-wipes-custom-layers.md) | 換底圖後自己的圖層、terrain 消失：setStyle 的 diff 與 style.load | 切換底圖（暗色→淺色→再切回）後，自己加的 source／layer 全部消失。 | pitfall | Observed | mapbox-gl, maplibre | setStyle, diff, style.load, isStyleLoaded, load, idle, 圖層消失, 底圖切換, terrain, 重建 |
| [02-07](02-07-attribution.md) | 底圖與資料的 attribution：要顯示什麼、窄螢幕怎麼辦 | 為了畫面乾淨隱藏了版權列；窄螢幕上被其他控件蓋住；只標了底圖沒標資料來源；收合後找不到授權資訊。 | pattern | Implemented | any | attribution, 版權, logo, Mapbox, OSM, CARTO, ODbL, 顯名標示, 手機, 收合 |
| [02-08](02-08-dark-light-basemap-vs-data-contrast.md) | 深淺色底圖與資料層對比：底圖要「退後」，動態物件才看得清 | 同一組色階在深色底圖上清楚，換淺色底圖後某些級距消失；動態物件被街道與地名淹沒；衛星底圖上資料像貼紙。 | pattern | Implemented | any | 深色底圖, 淺色底圖, 對比, Pure Black, 暗色主題, 色階, 衛星, 資料層, 透明度 |
| [02-09](02-09-self-hosted-pmtiles-basemap.md) | 自託管 PMTiles 底圖：MapLibre＋Protomaps，與 Mapbox 的接法差異 | 想要免 key、無 per-load 費用、可離線的底圖；或同一份 PMTiles 在 Mapbox GL 與 MapL… | pattern | Implemented | mapbox-gl, maplibre, leaflet | PMTiles, Protomaps, MapLibre, addProtocol, HTTP Range, R2, 自託管, glyphs, sprite, 離線, mapbox-pmtiles |
| [02-10](02-10-dem-terrain-rgb-encoding-and-bathymetry.md) | DEM 轉 terrain-RGB 圖磚：解碼哨兵值、缺磚處理、陸海合成與垂直誇張 | 自烘高程圖磚後，海岸或離島出現黑坑、黑三角，或水下全被壓成同一個淺色。 | pattern | Implemented | any | DEM, terrain-RGB, terrarium, raster-dem, 高程編碼, 海底地形, GEBCO, bathymetry, exaggeration, 垂直誇張, 烘焙, nodata, 缺磚 |
| [02-11](02-11-hillshade-slope-aspect-isobath-forms.md) | 山體陰影、坡度坡向、等深線要選哪種形態：預烤影像、即時 raster、還是分級向量 | 想讓使用者點地圖查「這裡坡度幾級」，但坡度圖是一張 PNG，點下去什麼都拿不到。 | decision | Implemented | any | hillshade, 山體陰影, 坡度, 坡向, slope, aspect, 等深線, isobath, GEBCO, 深度分帶, DEM, polygonize, PMTiles, feature-state, 地形 |
