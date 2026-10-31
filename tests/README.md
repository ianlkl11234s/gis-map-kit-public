# 回歸測試（手動）

跑法（prompt 一定要走 stdin，`--allowedTools` 後面直接接 prompt 會被吃掉；sed 拿掉開頭括號裡給人看的執行位置說明。05 要接在 04 後面，用 `claude -p --continue`）：

```bash
cd <測試資料夾> && sed 's/^（[^）]*）//' <本 repo>/tests/prompts/<題目>.txt | claude -p --plugin-dir <本 repo> \
  --allowedTools "Read,Grep,Glob,Agent,Skill,WebFetch,WebSearch,Write,Edit,Bash(python3:*),Bash(curl:*)" \
  --output-format stream-json --verbose > trace.jsonl
```

| 題目 | 驗收 |
|---|---|
| 01 review | `fixture-map` 埋了 12 個問題，全部要抓到：前端寫死 key、缺值 `\|\| 0`、attributionControl:false、無 loading／錯誤、mouseenter popup、user-scalable=no、手寫圖例、無資料時間、重複 addSource、未檢查 res.ok、座標未驗證、limit 寫死 |
| 02 advisor | 要觸發 gis-advisor 並引用卡片（05-04、05-08），不是只憑模型知識 |
| 03 start | 要引用卡片；架構不可讓前端直連帶 secret 的 API |
| 04 system | `python3 tests/grade_system.py system/`：邊欄位 0 問題；data.gov.tw ID 全部存在；分開 6377（環境部）與 25787（水利署）兩套保護區；污染源相關邊不可是已驗證因果。另跑 `skills/gis-system/scripts/check_system.py system/` 要 0 錯誤 |
| 05 execute | 瀏覽器打開圖台（等 15 秒以上再截圖）：底圖＋保護區面可見；popup 有來源、資料時間、取得時間、授權 |
| 06 flood | 要指出臺北幾乎沒有開放的實測積水資料；市府積水模擬與水利署淹水潛勢不可混用 |
| 07 aqi | check_system 0 錯誤；有涵蓋矩陣與「找不到」紀錄；有 is_proxy 節點；P1 不可有只看過標題的資料集 |
| 08 taste | 要引用 13-00；未指定時照作者品味給預設（MapLibre、深色單色底圖、系統字型、時間軸不自動播放），並說明這是作者偏好、可依需求改 |
| 09 scale | 要引用 14 主題的卡（14-00、14-02）；縮小用熱區或密度格網、z12 起才畫單點；30 萬點不整包載入 GeoJSON（改向量圖磚或 PMTiles）；點徑以固定三階為主 |
| 10 workshop change | 觸發 gis-workshop；兩期資料同一來源、同一行政區單位（不能一年用 A 來源一年用 B 來源而不說明）；色階門檻兩期固定；切換後地圖顏色真的改變（瀏覽器實測、截圖）；README 有來源、授權、資料時間；QA.md 分 Pass／Fail／待人工驗證；不強加播放動畫 |
| 11 workshop flow | 觸發 gis-workshop；斷訊那段切段不連線、不插出中間位置（引用 12-04）；時間軸只在有資料的範圍內動；說明 13:00–15:30 怎麼標「無資料」 |
| 12 workshop no-history | 觸發 gis-workshop；明講即時 API 不能做過去一週回放（引用 01-10），給「先存快照」與「改用有歷史的來源／講師備援資料」兩個選擇；拒絕把 secret 寫進網頁（10-04）；假資料要標 synthetic-demo、不算完成 |
| 13 workshop routing | 五題各自觸發箭頭後的 skill；重點是第 1 題不能被 gis-workshop 搶走、第 2 題不能落到 gis-start |

每題用 Opus 約 US$4.5–5.7、3–11 分鐘。

13 routing 每行一題，拿掉箭頭與後面的預期答案再送出，只需看 trace 裡第一個 `Skill` 工具呼叫的 skill 名稱，可加 `--max-turns 3` 省費用：

```bash
sed -n '2,$p' <本 repo>/tests/prompts/13-workshop-routing.txt | while IFS= read -r line; do
  q=$(printf '%s' "$line" | sed -E 's/^[0-9]+\. //; s/ → .*$//')
  printf '%s' "$q" | claude -p --plugin-dir <本 repo> --max-turns 3 --output-format stream-json --verbose \
    | grep -o '"skill":"[^"]*"' | head -1
done
```

**學生乾淨環境**：10–13 要在沒有個人 CLAUDE.md、沒有自己裝的 skill、沒有存過 token 的新資料夾跑，才能代表學生的狀況。維護者自己的電腦做不到完全乾淨（使用者層的 CLAUDE.md 與 skill 仍會載入），結果要註明「部分乾淨」與實際載入了哪些東西；真正的學生環境要另用一個新帳號或新電腦試。

