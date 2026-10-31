# 14-scale-density 尺度與密度權衡（資料分類 × 數量級 × 縮放）

> 由腳本自動產生，不要手改。

| id | 標題 | 什麼情況看這張 | 類型 | 證據 | stacks | tags |
|---|---|---|---|---|---|---|
| [14-00](14-00-scale-density-decision-table.md) | 尺度與密度決策總表：資料分類 × 數量級 × 縮放尺度 → 預設畫法 | 每加一個圖層都重新決定「要不要聚合、要不要熱區、幾級開始出點」，結果每層做法不一樣。 | catalog | Implemented | any | 決策表, 數量級, 縮放, 熱區, 網格, cluster, PMTiles, 點, 線, 面, 移動物件, 總表 |
| [14-01](14-01-default-by-data-type.md) | 先看資料是什麼，再決定畫法：點、線、面、網格、行政區統計、軌跡、移動物件、事件各自的預設 | 行政區統計被畫成一堆點；軌跡被當成獨立點畫；事件和設施用同一種點，看不出哪個在「發生中」。 | decision | Implemented | any | 資料分類, 點, 線, 面, 網格, H3, 行政區, 統計, 軌跡, 移動物件, 事件, 預設畫法 |
| [14-02](14-02-point-count-thresholds.md) | 點的數量級門檻：1 千、1 萬、10 萬三條線，分別調透明度、低縮放換熱區、延後出點 | 一份幾十萬點的資料在全國視角糊成一整片，看不出哪裡密。 | decision | Implemented | any | 數量級, 門檻, 熱區, heatmap, cluster, 出點縮放, minzoom, 透明度, 密集點, 10k, 100k |
| [14-03](14-03-zoom-handoff-pitfalls.md) | 隨縮放換畫法的交界坑：熱區提早消失、透明圖層仍攔截點擊、切換點來回閃 | 熱區設 `maxzoom: 12`、點設 `minzoom: 12`，結果在 z11.5–12 之間兩者都不見，畫面空白… | pitfall | Observed | any | minzoom, maxzoom, 縮放切換, 熱區, 格網, H3, 解析度, 遲滯, hysteresis, 標籤密度, queryRenderedFeatures, 尺度接力 |
| [14-04](14-04-overlap-order-and-opacity.md) | 重疊與遮蔽：誰畫在上面要有規則——泡泡大的先畫、分級線高值在上，多層熱區要降透明 | 大泡泡蓋住小泡泡，小值的點完全看不到、點不到。 | pattern | Implemented | any | 重疊, 遮蔽, sort-key, circle-sort-key, line-sort-key, 繪製順序, 透明度, 熱區疊加, 高值在上, 泡泡 |
| [14-05](14-05-honest-aggregation.md) | 聚合後要誠實：篩選時不能顯示未篩選的總量、抽稀不能冒充全部、空格與未涵蓋不是 0 | 使用者勾選「只看製造業」，拉遠後的密度格網仍是全部公司的量。 | pitfall | Implemented | any | 聚合, 格網, 熱區, 抽稀, drop-densest, 篩選, 未涵蓋, 空格, 計數, 小樣本, 誠實表示 |
| [14-06](14-06-small-data-no-overpackaging.md) | 資料少時不要過度包裝：數百點以內直接畫，個位數到數十點用大一階的點加名稱 | 全圖只有數百個測站，卻套了 cluster，使用者看到一堆「12」「37」的圓圈，要點好幾下才看到站。 | decision | Implemented | any | 少量資料, cluster, 熱區, 過度包裝, 點大小, 標籤, 個位數, 數百點 |
| [14-07](14-07-moving-objects-and-trails-at-scale.md) | 移動物件與軌跡的規模：容量先定上限、軌跡依鏡頭範圍換抽稀層、粒子拉遠反而要加 | 船舶或航班一多，軌跡頂點爆量，記憶體一路漲。 | pattern | Implemented | any | 移動物件, 軌跡, LOD, 抽稀, Douglas-Peucker, 容量上限, instancing, 粒子, 自適應, 方向箭頭, 遲滯 |
