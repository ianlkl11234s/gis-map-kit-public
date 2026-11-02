# 定案表（全 plugin 唯一的預設值來源）

skill、README、卡片提到下列項目時，**數值與說法以本表為準，不另寫一份**；需要時寫「照 DEFAULTS.md」。要改預設，先改本表，再跑一致性檢查找出所有舊說法。

| 項目 | 定案 | 備註 |
|---|---|---|
| 地圖 SDK | MapLibre GL JS | 免 key；需要 Mapbox 專屬功能時才換 |
| 預設底圖 | OpenFreeMap **dark**：`https://tiles.openfreemap.org/styles/dark` | 免 key；attribution 由樣式自動帶出（OpenFreeMap、OpenMapTiles、OpenStreetMap），不要關掉。條款與限制見 02-02 |
| 淺色底圖（需要時） | OpenFreeMap positron：`https://tiles.openfreemap.org/styles/positron` | 同上 |
| 不要用 | 沒帶 key 的 CARTO 圖磚 | 會整片蓋上「API KEY REQUIRED」浮水印 |
| 備援底圖 | MapLibre demotiles | 只在 OpenFreeMap 連不上時用；臺北街道尺度幾乎只剩海陸 |
| 本機開網頁 | 在專案資料夾跑 `python3 -m http.server`，用瀏覽器開 | 直接雙擊 HTML 會讀不到資料檔 |
| 資料格式起點 | GeoJSON；大到載入變慢再換 PMTiles | 門檻見 06-05 |
| 點數門檻 | 1 千／1 萬／10 萬三條線（數值只寫在 14-02） | 其他卡只引用 14-02，不重寫數字 |
| 缺資料 | 顯示成「無資料」，不補 0、不造座標 | 圖例要有獨立的「無資料」項。初學骨架用色階沒用到的中性灰；進階面圖層用透明底＋斜線（見 05-04） |
| 每份資料要記 | 來源機關、網址、授權、資料時間（觀測時間）、抓取時間 | 資料時間與抓取時間分開寫 |

## 課堂工作坊（對齊 Week 09 簡報）

| 項目 | 定案 |
|---|---|
| 完成標準 | 靜態版是**里程碑**，可以交；加一項讓地圖內容改變的操作是**完整目標** |
| 學生進度五站 | 選題 → 資料 → 地圖 → 動態 → 驗收 |
| 六階段 Demo | Basemap & Skeleton／Data to Layer／Style & Legend／Make It Dynamic／Interaction & Playback／Trustworthy & Reproducible |
| QA 狀態用詞 | Pass／Fail／未驗證 |
| 驗收四題 | 見 skills/gis-workshop/references/qa-checklist.md；「這個結果不能說明什麼？」必答 |
| 資料取得 | 先自己從公開來源下載；做不到時用講師提供的下載連結或本機資料 |
| 北科大 Week 09 備援資料 | https://ntut-urban-data-course.itsmigu.com/downloads/week09-data.zip （64 KB）：`flow-bus/` 臺北市公車 2026-10-28 07:00–09:00 每 5 分鐘位置（299 路點位與已切好的段、四條路線點位）；`change-population/` 臺北市 12 區界線＋2015、2025 戶籍人口。每個資料夾附 SOURCES.md（來源、授權、資料時間、欄位） |
