# Reference Guide: 5-presentation-spec.md

> 基於 `0-skill-mode.md` 的推導模式。配合 `templates/5-presentation-spec.template.md` 使用。

## 文件目的

描述 feature 對外呈現方式 — 給前端 / UX 工程師看的「說明書」。視覺細節歸 Design System,這份只寫「**用什麼 component、在什麼 page、走什麼 flow**」。

## 進入這份文件時的開場

```
進入第五份:呈現規格。

這份描述 feature 怎麼對外呈現給使用者 — 不一定是 UI,
也可能是 API only / Background Job / CLI / Notification。

我會先推導,你確認 / 修正。

```

## Claude 推導指南

### Presentation Type 推導

從 §1 + §2 推測類型:
- 使用者有「點按鈕、看畫面」的描述 → GUI
- 純 API 整合 → API Only
- 定時任務 / 系統行為 → Background Job
- 命令列工具 → CLI
- 通知 / email / push → Notification

**判斷基準是「使用者怎麼接觸 feature」,不是 feature 的領域**:
- Notification 類型指投遞通道本身(email / push 的觸發與內容),**不是**「功能跟通知有關」
- 例:站內通知中心有鈴鐺、面板、設定頁 → 主類型是 GUI(Notification 可作次要類型)
- 拿不準時:只要使用者會「看畫面、點東西」,就有 GUI 成分 → §5.4-5.7 要寫

**標 `[需確認]` 讓使用者確認**(可能有多種類型)

### 後續節推導(依 Presentation Type)

| Type | 5.2 | 5.3 | 5.4-5.7 |
|---|---|---|---|
| GUI | User Story | User Flow | 寫 |
| API Only | Consumer Story | Consumer Flow | 跳 |
| Background Job | Trigger Story | Execution Flow | 跳 |
| CLI | Command Story | Command Flow | 跳 |
| Notification | Recipient Story | Trigger Flow | 跳 |

### User Story 推導

從 §1.3 persona + §2.1 FR 推:
- 每個 persona 配對自己會用的 FR
- 用「作為 X,我想要 Y,以便 Z」格式
- 一個 persona 通常 1-3 個 story

### User Flow 推導

從 §4.1 SF 反推「使用者視角」:
- SF 寫「系統做什麼」,UF 寫「使用者看到 / 做什麼」
- 每個 SF 對應 1-N 個 UF
- 用 step by step 描述,不要寫系統內部細節

### Component / Page 推導(僅 GUI)

從 user flow 推:
- 每個 step 涉及的 UI 元素 → component(C-N)
- 每個 step 發生在哪個畫面 → page(P-N)
- 每個 page 的版面結構 → 區塊(T-N)

### 回填 §4

§5.3 寫完 UF 後,**主動回頭把 §4 各 SF 的 "Related UF" 欄位補上對應 UF-N**。

## 前端體驗決策清單(僅 GUI,必跑)

> 這是 §5 的核心詢問清單。結構(有哪些 component / page)由 Claude 推導,
> 但「長什麼樣、怎麼互動、出錯時怎麼辦」是體驗決策 — Claude 推得出建議值,拍板權在使用者。
> 常見失誤:結構推完就走,前端體驗一句都沒問,使用者拿到 spec 才發現跟想像的不同。

確認為 GUI 後,逐一檢視 8 個維度:

| # | 維度 | 生活化問法 | 常見選項 |
|---|---|---|---|
| 1 | 進入點與導覽 | 「使用者要從哪裡進到這個功能?」 | 側欄新項目 / 既有頁面加按鈕 / 既有選單加項目 / 設定頁 |
| 2 | 容器形式 | 「主要操作開獨立頁、彈窗,還是側邊抽屜?」 | 獨立頁 / Modal / Drawer / 就地展開 |
| 3 | 操作模式 | 「資料一頁填完,還是分步驟引導?可以在列表上直接改嗎?」 | 單頁表單 / 分步精靈 / inline 編輯 |
| 4 | 空狀態與首次使用 | 「第一次進來、一筆資料都沒有時,使用者看到什麼?」 | 引導文案 + CTA / 空表格 / 範例資料 |
| 5 | 錯誤與部分成功 | 「操作失敗時使用者看到什麼?能在原地重試嗎?10 筆裡成功 8 筆要怎麼顯示?」 | 整批失敗 + 訊息 / 部分成功 + 結果清單 / 原地重試 |
| 6 | 操作回饋與防呆 | 「成功後怎麼告訴使用者?危險操作(刪除 / 覆蓋)要不要再確認一次?要能反悔嗎?」 | Toast / Banner / 確認 Modal / Undo |
| 7 | 資料量呈現 | 「列表長到幾百筆時怎麼辦?要搜尋、篩選嗎?預設怎麼排?」 | 分頁 / 無限捲動 / 搜尋 + 篩選 / 固定上限 |
| 8 | 裝置與即時性 | 「手機要不要能用?同一筆資料會被別人同時改嗎 — 畫面要自動更新嗎?」 | 桌機 only / RWD;手動刷新 / 輪詢 / 即時推送 |

### 使用方式

1. **先過濾**:判斷哪些維度跟本 feature 相關(例:純展示型功能沒有「操作模式」議題;單人工具沒有「即時性」議題)。不相關的跳過,展示時一句帶過:「維度 X 不適用,因為…」
2. **逐維度推建議值**:從 §1 persona、§2 FR/NFR、§4 EF/EC 推,每個建議值附一句理由
3. **打包拍板**:
   - 非 POC:照 0-skill-mode 的 AskUserQuestion 規則,一輪 2-3 題分批問
   - POC 快速模式:**不是默默套預設值**,而是「一輪確認包」 — 把相關維度的建議值列成清單一次展示:「前端體驗我建議這樣:(清單)。有要改的嗎?都 OK 我就照這個寫」。整包算 1 個硬停
4. **落盤**:拍板結果寫進 §5.7 決策表(不適用的維度寫 N/A + 原因)。影響資料模型或不可逆的(例:部分成功策略牽動 API 設計)升級為 ADR

### 為什麼前端不適用「默默採建議值」

前端是使用者唯一直接「看得到」的部分。後端結構選錯,要讀完文件才會發現;前端體驗選錯,做出來第一眼就會被推翻 — 而那時已經是實作階段。在 §5 多花一輪確認,比實作完重做便宜得多。

## 必要決策點(要問使用者的)

### 必補問題

1. **Presentation Type 確認**:推測類型後讓使用者確認
2. **前端體驗決策清單**(僅 GUI):見上節 — 相關維度逐一給建議值,打包拍板
3. **Component 視覺細節**:若使用者有特殊視覺要求(例:節點卡片必須是 160x140),補問

### 不該問的(結構推導,Claude 自己做)

- ❌ 「User stories 寫什麼?」(從 persona + FR 推)
- ❌ 「有哪些 component?」(從 user flow 推)
- ❌ 「Page 結構是?」(從 user flow 推)

判斷線:「**有哪些**」是結構問題,Claude 自己推;「**長怎樣、怎麼互動、出錯怎麼辦**」是體驗決策,要拿建議值給使用者拍板。

## Open Question 候選

- Presentation Type 不確定(多種類型混合)
- Component 拆法多種合理(一個大的 vs 多個小的)
- Page 配置多種合理(獨立頁 vs Modal vs 抽屜)
- 空狀態 / 部分成功的呈現方式多種合理
- 裝置支援範圍使用者未明說(桌機 only vs RWD)

## 展示給使用者的格式

### 步驟 1:確認 Presentation Type

先快速問:

```
我從前面文件推測這個 feature 主要透過 GUI 呈現給使用者。對嗎?
還是有其他形式(例如後台 cron job)我漏了?
```

### 步驟 2:摘要

```
我推導出:

- Presentation type:{類型}
- User stories:{N 個} (覆蓋 {M} 個 persona)
- User flows:UF-1 ~ UF-{N}
- Components(若 GUI):C-1 ~ C-{N}
- Pages(若 GUI):P-1 ~ P-{N}

需要你拍板:[N 個]
```

### 步驟 3:逐節展開

對 GUI 類:
- 先確認 user stories(快)
- 再 user flows(中等)
- 最後 components + pages(慢,需要視覺確認)

### 步驟 4:問必要決策點(以前端體驗決策清單為主軸)

```
前端體驗有 5 個維度需要你拍板(另外 3 個維度不適用,我列在最後):

1. 進入點:我建議放在模板列表頁的「建立」選單裡,不另開側欄項目。OK 嗎?
2. 容器形式:匯入預覽我建議獨立頁(P-5),不是 Modal。可以嗎?
   (考量:預覽內容多,Modal 會擠;但獨立頁多一次跳轉)
3. 失敗呈現:驗證失敗停在原頁 + 錯誤訊息,不做「部分匯入」。對嗎?

(下一輪再問:操作回饋方式、資料量呈現)
不適用維度:操作模式(無多步驟表單)、即時性(單人編輯)、…
```

有 AskUserQuestion 工具時用它問,一輪 2-3 題。

## 容易卡住的點

### 使用者沒寫過 UI spec

明確說:「我們不寫實作層(props、event handler 等),只寫:這個 component 角色是什麼、有哪些狀態、用在哪些 page。視覺細節歸 Design System。」

### 使用者想直接給 Figma 連結

接受。Reference 寫:「視覺以 Figma 為準([連結]),本 spec 只描述結構 + 互動」。

### 使用者描述 UI 卡在抽象

主動 propose:「我幫你列幾個可能的 component:[列舉]。看哪些符合你想的,哪些不在範圍。」

### 使用者想用設計工具(Fable / Pencil MCP / ui-ux 類 skill)做視覺

§5 只寫結構(C-N / P-N / UF-N),視覺本來就歸實作階段 — 使用者提出要用設計工具是合理走向,不要卡住:

- **先確認分工**:spec 繼續寫結構,還是現在就停下來出 mockup?建議「先把文件寫完,視覺留到實作」 — 版面類決策選可逆的合理預設寫進 spec,並標注「視覺與版面由 {工具} 於實作階段定案」
- 若現在就要 mockup:把 §5 已定的 C-N / P-N / 版面 ASCII 帶給工具當輸入,設計結果回填 §5,保持 spec 與設計一致
- 工具暫時不可用(MCP 斷線等)→ 照常用預設寫完 spec,不要讓流程停在工具上

## 反思檢查(進 §6 前)

- [ ] Presentation type 已確認
- [ ] 每個 user story 對應到至少 1 個 persona + FR
- [ ] 每個 user flow 對應到 SF(GUI 類)
- [ ] §4 各 SF 的 "Related UF" 欄位已回填
- [ ] 每個 page 用到的 component 都在 §5.5 定義(GUI 類)
- [ ] 每個 component 至少出現在 1 個 page(無孤兒)(GUI 類)
- [ ] 前端體驗決策清單 8 個維度都檢視過:相關的已拍板、不相關的已註明 N/A(GUI 類)
- [ ] 拍板結果已寫入 §5.7 決策表,重大決策已升級 ADR(GUI 類)

## 文件結束時的 summary

```
§5 presentation-spec 完成!

- Presentation type:{類型}
- User stories:{N 個}
- User flows:UF-1 ~ UF-{N}
- Components:C-1 ~ C-{N}(若 GUI)
- Pages:P-1 ~ P-{N}(若 GUI)
- 前端體驗決策:{M} 個維度已拍板,{K} 個不適用(§5.7)(若 GUI)
- §4 SF 的 "Related UF" 已回填

接下來進入 §6 interfaces,我會推導對外 API、events、整合點。要進嗎?
```
