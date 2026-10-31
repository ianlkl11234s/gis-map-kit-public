---
id: 06-12
title: 全國 OSM 路網分析吃爆記憶體：先找本機 PBF、osmium 預過濾、跑前試算 RAM，分區要重疊
topic: 06-data-formats
kind: pitfall
scope: public
evidence: Observed
stacks: [any]
tags: [OSM, PBF, osmium, pyrosm, osmnx, networkx, Overpass, 路網, 等時圈, isochrone, 可達性, RAM, swap, OOM, 分區, bbox overlap]
---

## 原則
全國級路網分析先找本機 PBF、用 osmium 預過濾道路類型、跑前試算節點邊數與 RAM；分區的 bbox 一定外擴重疊；不要對全國範圍打公開 Overpass。

## 症狀
- 要算全國的等時圈或最近設施距離，腳本跑了幾十分鐘，CPU 只剩個位數百分比，看起來還活著但沒有進度。
- 記憶體與 swap 被吃光，磁碟剩餘空間跟著見底，整台機器變慢。
- 用 Overpass 抓全國路網，請求卡住不回、被拒連或回 403／406，幾小時後才恢復。
- 分區跑完拼回全國，區界附近的設施服務範圍被切斷。

## 原因
- 把整份國家級 PBF（含 residential、footway、path、track）讀進 networkx 這類 Python 物件圖，節點與邊可達數百萬到上千萬，每個物件的額外開銷讓記憶體需求放大到數十 GB。
- 記憶體不足時開始 swap thrash：CPU 很低不代表死鎖，而是在等磁碟。
- 公開 Overpass mirror 對大範圍查詢不可靠：大 bbox 被切成幾十個子查詢序列執行，任一個卡住整支程式就卡住；短時間打太多會被暫時封鎖。
- 分區的 bbox 不重疊時，區界附近起點的搜尋圖只含本區道路，跨區路徑被切斷。

## 解法
1. **先找本機有沒有 PBF**（例如 Geofabrik 的國家檔），有就完全避開 Overpass；沒有就下載一份放在共用資料夾，給所有分析共用。
2. **osmium 預過濾**：`osmium tags-filter` 只留需要的道路類型（開車只留主要幹道到某一級；步行要特別嚴格篩 footway／path／track），檔案和圖都會小很多。
3. **跑前試算**：用過濾後的 PBF 估節點與邊數，對照機器 RAM，並確認磁碟剩餘空間足夠 swap 與中間檔；預估超過就換策略，不要先跑再說。換策略的順序：更嚴格過濾 → 簡化圖（合併度數為 2 的節點）→ 分區跑 → 改用路由引擎（OSRM、Valhalla）或資料庫（pgRouting）算，不在 Python 物件圖裡算。
4. **分區一定要重疊**：每區 bbox 外擴一段（例如 0.1–0.2 度，依最大搜尋半徑定），結果只保留本區內的起點，再拼回全國。
5. **監看行為**：記憶體使用超過一半就停掉；CPU 長時間接近 0 先查 swap 與網路等待。
6. **重跑前對齊設定**：道路篩選條件、bbox、API base URL 寫在一處，重跑前比對上次成功的設定；套件間參數命名不同（例如 `walk`／`walking`、`drive`／`driving`），用一張對照表隔開，不要混用。

## 怎麼偵測
- 通用：分析腳本直接讀整份國家 PBF 或對全國 bbox 打 Overpass；沒有分區重疊參數；沒有跑前 RAM／磁碟檢查。
- 搜尋：`pyrosm\.OSM\(|get_network\(` 讀的檔案沒有經過 `osmium tags-filter`（Python）。
- 搜尋：`graph_from_bbox|graph_from_place` 搭配國家級範圍、且沒有設定 timeout 或 mirror fallback（osmnx）。
- 搜尋：分區程式的 bbox 沒有 buffer／overlap 參數（any）。

## 出處
- osmium-tool `tags-filter` 文件；pyrosm、osmnx 文件；Geofabrik 下載站；Overpass API 使用政策（大量查詢會被限流）。
- 相關卡：[06-01](06-01-format-selection-decision.md)、[07-11](../07-performance/07-11-big-response-memory-blowup-streaming.md)（大回應記憶體爆量）、[10-12](../10-ops/10-12-upstream-ip-block-deploy-env.md)（上游 IP 封鎖）。
- 實例：[mini-taiwan-pulse 事故紀錄（pyrosm 未過濾讀全台路網吃掉數十 GB RAM 造成 swap thrash；Overpass mirror 卡死與封鎖；分區不重疊使區界斷裂）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/memory/INCIDENTS.md)；[跑前檢查清單（mirror 健康度、磁碟與 RAM 門檻）](https://github.com/ianlkl11234s/mini-taiwan-pulse/blob/af703e85417277c83391cfe446f7771c209ad2b8/.claude/skills/accessibility-analysis/references/troubleshooting.md)。
