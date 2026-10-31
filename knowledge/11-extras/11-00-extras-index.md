---
id: 11-00
title: 發布與分享總表：被找到、分享嵌入、截圖、定位、PWA、無障礙、隱私、多語、敘事
topic: 11-extras
kind: catalog
scope: public
evidence: Observed
stacks: [any]
tags: [總表, 發布, SEO, llms.txt, 分享, 嵌入, 截圖, 定位, PWA, 無障礙, 隱私, 多語系, 敘事頁]
---

## 原則
站上線後，依「要讓誰用到什麼」選卡：被找到看 SEO 與宣傳組，被轉貼與嵌入看分享組，其餘按功能對應。

## 對照表

### 讓人找到與知道
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 搜尋引擎看不到內容 | [11-01](11-01-spa-empty-html-seo-prerender.md) | 原始 HTML 放靜態說明、meta、結構化資料，結論一篇一個網址 |
| robots、sitemap、canonical | [11-02](11-02-robots-sitemap-soft404-canonical.md) | 放真實檔案，不存在的路徑回 404，多語版 canonical 指向各自 |
| llms.txt 與 AI 爬蟲 | [11-03](11-03-llms-txt-and-ai-crawler-policy.md) | 當低成本實驗，用各 bot 的 User-Agent 實測回應碼，不一致回報站主 |
| 想讓人轉貼 | [11-15](11-15-promote-your-map-video-and-before-after.md) | 影片與前後對比動畫與搜尋是兩條獨立管道，素材用真實畫面 |

### 分享與嵌入
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 分享網址要還原畫面 | [11-04](11-04-share-camera-og-image-saved-scene.md) | 帶鏡頭與時間，預覽圖自己做，持久化場景帶版本號 |
| 開放嵌入 | [11-05](11-05-embed-page-security-billing-gestures.md) | 只有嵌入路徑開放 frame-ancestors，嵌入版只載不產生後端流量的圖層 |
| 嵌入頁的互動 | [11-14](11-14-embed-clock-frozen-time-cooperative-gestures.md) | 時間凍結、時鐘自己持有，開協作手勢不攔截捲動 |

### 截圖與匯出
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 截圖得到黑畫面 | [11-06](11-06-canvas-capture-export-print.md) | 在 render 事件的同一 tick 同步讀取，不整站開 preserveDrawingBuffer |

### 定位與量測
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 「我的位置」 | [11-07](11-07-geolocation-my-location-permissions.md) | 只在 HTTPS 提供，處理授權、拒絕、逾時三路徑，被拒時有退路 |
| 量距離面積、前後比較 | [11-08](11-08-measure-draw-and-compare-maps.md) | 用測地函式量測，比較優先同圖疊色，手機要有單一視圖替代 |

### PWA 與無障礙
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 要不要做 PWA 或離線 | [11-09](11-09-pwa-offline.md) | 先分清可安裝或離線可用，離線是資料策略與底圖授權問題 |
| 鍵盤、螢幕閱讀、中文輸入 | [11-10](11-10-accessibility-keyboard-ime.md) | 判斷 IME 組字狀態，自訂控制項可純鍵盤操作，通知用 aria-live |

### 出處與隱私
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| attribution 與隱私頁 | [11-11](11-11-attribution-and-privacy-disclosure.md) | 任何模式不得隱藏 attribution，隱私頁的第三方以 Network 面板實際網域為準 |

### 多語系
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 加英日文等語系 | [11-12](11-12-i18n-display-layer-lookup-and-fallback.md) | 只在顯示層查表，查不到退回原文，地名用官方英譯 |

### 敘事頁
| 遇到什麼／想做什麼 | 卡片 | 一句重點 |
|---|---|---|
| 寫資料敘事文章 | [11-13](11-13-scrollytelling-story-and-number-ledger.md) | 嵌入地圖而不重畫，正文每個數字在台帳有出處 |

## 相關主題
- 網址序列化總原則：[08-08](../08-multi-layer/08-08-shareable-layer-state-url.md)。
- 部署與 CSP：[10-24](../10-ops/10-24-csp-for-map-sites.md)。
- 隱私與個資：[07-14](../07-performance/07-14-open-data-pii-column-exclusion.md)。

## 出處
各項依據見對應卡片。
