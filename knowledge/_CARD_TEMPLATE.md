---
id: <主題碼>-<兩位數>          # 例：12-03（12-domain-pitfalls 第 3 張）
title: <一句話講問題或做法>
topic: <資料夾名，例：12-domain-pitfalls>
kind: pitfall | pattern | decision | catalog   # 踩坑／做法／選型決策／清單或總表
scope: public | private        # private＝整張卡只進課程版（見下方「scope」）
evidence: Evaluated | Implemented | Observed | Candidate | General
#   Evaluated   有量測或比對結果
#   Implemented 有程式實作
#   Observed    有事件或修正紀錄，但沒正式量測
#   Candidate   做過研究、還沒實作
#   General     一般業界建議，不是自己的經驗（不可寫成「我們遇過」）
stacks: [any]                  # SDK 無關寫 [any]；只適用特定 SDK 就列出，順序 mapbox-gl, maplibre, leaflet, openlayers, deck.gl, three.js；any 不和其他值混用
tags: [關鍵字, 給 INDEX 與 advisor 搜尋用]
---

## 原則
一到兩句，agent 照著做就不會踩坑的規則（祈使句，例如「切底圖一律完整重載，並在 style.load 重建自己的圖層」）。後面各段是這條原則的依據與做法。

## 症狀
2–4 條。使用者或開發者看得到的現象（畫面、錯誤訊息、數字不對）。第一條會被索引當成「什麼情況看這張」，要能單獨讀懂。

## 原因
1–3 條。造成症狀的機制，不寫發現經過。

## 解法
編號步驟，最多 6 步，用祈使句寫給 agent 照做。需要取捨時列選項＋建議。

## 怎麼偵測
給 gis-review 用：
- 通用：<看什麼畫面／什麼行為>
- 搜尋：`<regex>`（適用 stack：…）
- 若只適用特定架構，明寫「僅限 <架構>」。

## 出處
- 官方文件或一般文獻；相關卡：xx-yy。
- 公開 repo 的實例可以留在這裡，用釘 commit 的 GitHub 連結。


---

# 寫法規則（所有卡片一致）

**讀者是 agent**：卡片是讓 agent 照著做、避開已知的坑。先寫原則，再寫「遇到什麼 → 為什麼 → 怎麼做 → 怎麼查」。原則要能單獨成立；解法是原則的展開，遇到例外時寫「什麼情況可以調整」。

**要刪掉或改寫的**
- 寫給作者自己看的：發現經過、複驗紀錄（「以 grep 複驗」「先前查無是因為本機落後」）、誰在哪天拍板、A 級／B 級這類內部評等。
- 專案內部名稱：元件名、檔名、store 名（例如 layerManifest、timeStore）改成通用說法（「圖層登記表」「共用的時間 store」）。真的需要時放進 private 實例。
- 專案自己的數量與規模（「59 層」「831 站」）。只保留能拿來當門檻或判斷依據的數字（「單層超過 5 MB 改用 PMTiles」）。
- 行號與冗長的 commit 考古。

**長度**
- 公開正文（不含程式碼區塊）：pitfall、pattern 不超過 2,000 字；decision、catalog 不超過 2,800 字。超過就拆成兩張，或刪掉不影響做法的細節。
- private 段不超過 400 字，只留 1–2 條可追溯的實例指標。總表（kind: catalog）例外：private 卡的清單列只能包進 private 段，不受此限。

**scope**
- 設 `private` 的條件：整張卡只對本人專案有意義，或屬於後端排程／維運、作者個人偏好、AI agent 設計等對初學做地圖的學生太進階的內容。
- 公開卡不可在正文引用 private 卡的編號：總表或「相關卡」清單裡的項目移進 private 段；正文句子改寫成不依賴該卡。

**出處**
- 公開 repo（mini-taiwan-pulse、gis-data-collectors）：用 `https://github.com/ianlkl11234s/<repo>/blob/<commit>/<path>` 連結，可以放在公開段。
- 私人 repo（其他所有 repo）：只放在 private 段，寫「repo 名／相對檔名（年-月，一句話）」。
- 不寫絕對路徑、行號、金鑰、私人端點。

**例外**：00 系統思考、13 作者品味是方法論與偏好卡，不強制五段；kind 是 catalog 的總表也不強制五段。

**總表**：每個主題的 `xx-00` 是總表（kind: catalog），該主題每張卡至少出現一次，卡片編號一律是連結。
