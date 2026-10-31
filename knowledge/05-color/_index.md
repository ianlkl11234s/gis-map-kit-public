# 05-color 色票

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [05-00](05-00-color-index.md) | 色票總表：依問題找卡（色階類型、缺值、深淺底圖、類別、色盲、透明度、圖例、門檻、raster） | 色票主題的入口：先依資料型態定色階類型，再處理灰色 0、缺值、底圖方向、圖例同源與跨期門檻。 | catalog | Implemented | any | 總表, 色票, 色階, 缺值, 深淺底圖, 類別色, 色盲, 透明度, 圖例, 分級門檻, raster |
| [05-01](05-01-color-ramp-decision-table.md) | 資料型態 → 色階類型 → 建議色階的決策表 | 用彩虹色表示人口、用紅綠表示好壞、類別圖層用了連續色階，讀者看不出高低或看錯語意。 | decision | Implemented | any | 色階, choropleth, sequential, diverging, categorical, 決策表, ColorBrewer, viridis, magma |
| [05-02](05-02-gray-zero-and-outline-collision.md) | 灰色「0 級」與最淺／最亮級撞色，白描邊點與淺色撞 | 圖上有一級「0」或「無」用灰色畫，另一端最高級是米黃或淡黃；地圖一縮放，最高級的點／線和灰色 0 級分不出來。 | pitfall | Observed | any | 色階, 撞色, 描邊, 零值, 對比, 深底圖 |
| [05-03](05-03-dark-light-ramp-direction.md) | 暗底圖與淡底圖的序列色階方向相反，兩邊都要過對比檢查 | 同一個熱區色階在暗底圖很漂亮，換到淡底圖後最密的地方幾乎看不見（淡黃對白底）。 | pattern | Evaluated | any | 色階, 暗色底圖, 淡色底圖, 對比, 熱區, 驗證, 底圖切換 |
| [05-04](05-04-null-is-not-zero-color.md) | 缺值（null）要有獨立畫法，不能畫成 0 級或最淺色 | 行政區沒有資料的地方被畫成最淺色或灰色，讀者把它當成「0」或「很低」。 | pitfall | Implemented | any | 缺值, null, 斜線, hatch, 未涵蓋, 遮蔽, 零值, 圖例 |
| [05-05](05-05-categorical-count-and-semantic-colors.md) | 類別色不要太多、不要循環，狀態與警報色不要挪給資料分類 | 一張圖有十幾個類別，圖例像調色盤，使用者無法把色塊對回地圖。 | pitfall | Implemented | any | 類別色, categorical, 語意色, 警報, 紅綠, 色相, 類別過多, 其他 |
| [05-06](05-06-colorblind-and-similar-ramps.md) | 色盲模擬與「太像」的色階：只靠色相區分的設計會失效 | 色覺異常（約 8% 男性有紅綠色弱）的使用者無法分辨兩個類別或兩個等級。 | pitfall | Evaluated | any | 色盲, protan, deutan, tritan, ΔE, OKLab, 色盤, 太像, 換色 |
| [05-07](05-07-alpha-stacking-and-fill-opacity.md) | 透明度疊加會變色與糊掉：單層 alpha 要依疊加層數回推 | 疊加很多半透明面／線（例如上百天的活動範圍、多層覆蓋面）後，整塊變成不透明，密度差異全部看不見。 | pitfall | Observed | any | 透明度, alpha, 疊圖, 熱區, fill-opacity, 底圖透色, 疊加 |
| [05-08](05-08-legend-key-mismatch.md) | 圖例與地圖顏色對不上：色票必須與渲染同源，且只描述畫面 | 圖例色票的色號和地圖實際顏色差一點，肉眼比對總覺得「怪怪的」。 | pitfall | Observed | any | 圖例, legend, 同源, 色票, 分類, 漏寫, 門檻, breaks |
| [05-09](05-09-fixed-breaks-across-time.md) | 分級門檻要跨期固定，不要隨當次資料重算 quantile | 拖動時間滑桿或切換年份後，同一個顏色在不同年份代表的數值不同；使用者以為某區域「變深＝變多」，其實只是當年門檻重算了。 | pattern | Implemented | any | 分級, breaks, quantile, 跨期比較, choropleth, 門檻, 時間序列, 顏色語意漂移 |
| [05-10](05-10-colorramps-used-catalog.md) | 用過的色階清單與語意對照（序列、發散、類別、官方色） | 選色階前先查本表：同主題沿用既有色系，再依資料型態選類型（[05-01](05-01-color-ramp-decisi… | catalog | Implemented | any | 色階清單, ColorBrewer, viridis, magma, YlOrRd, PuOr, RdBu, 官方色, 色盤庫 |
| [05-11](05-11-raster-value-encoding-color-mix-pixel-sampling.md) | 值編碼 raster 用 raster-color-mix 上色：係數作用在 0–1 取樣值上，漏乘 255 整層單色 | 把物理值（樹高、地表溫度、雨量）編進 PNG 像素，用 `raster-color` 上色，結果整層變成單一顏色、看不到… | pitfall | Evaluated | mapbox-gl | raster-color, raster-color-mix, raster-value, raster-color-range, 值編碼, 像素取樣, nodata, alpha, shader, 驗收 |
| [05-12](05-12-raster-value-pixel-sampling-and-nodata.md) | 值編碼 raster 的驗收：一律用畫面像素取樣，nodata 靠來源 alpha 而不是透明 stop | nodata 區域被塗上色階最低色，蓋住底圖。 | pitfall | Evaluated | mapbox-gl | raster-color, raster-color-mix, raster-value, raster-color-range, 值編碼, 像素取樣, nodata, alpha, shader, 驗收 |
