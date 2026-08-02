# 5. Presentation Specification

## 5.1 Presentation Type

**Selected type**: GUI

**Description**: 本 feature 主要透過模板列表頁與流程編輯器的 GUI 操作。使用者透過「⋯」選單觸發匯入 / 匯出，透過匯入預覽頁確認後寫入。AI 生成入口走流程編輯器既有路徑。Seed 模板載入屬於系統行為，無使用者直接觸發。

## 5.2 User Stories

**作為 PM / 流程設計者**：
- 我想要把已建立好的模板匯出為檔案，以便分享給其他工作區的同事使用
- 我想要匯入別人提供的模板檔案，以便快速開始工作而不用從零建立
- 我想要在匯入前看到模板的預覽，以便確認是不是我要的東西
- 我想要在工作區已有同名模板時收到提示，以便決定要覆蓋還是建新的
- 我想要看到結構警告（如孤兒節點），以便決定是否要修正後再使用

**作為 AI 生成功能使用者**：
- 我想要 AI 產出的模板能直接套用到編輯器，以便不用手動轉換或重建

**作為系統管理員 / RD**：
- 我想要把官方範本放進系統 seed 資料夾，以便新工作區能直接使用內建模板
- 我想要在 seed 載入失敗時收到 log，以便排查問題

## 5.3 User Flows

### UF-1: 使用者匯入模板檔案

**Persona**: PM / 流程設計者
**Related FR**: FR-2, FR-3, FR-4, FR-5, FR-6
**Preconditions**: 使用者已登入並進入模板列表頁 (P-1)

**Steps**:
1. 點擊「建立 Automation 模板」展開選單
2. 選擇「匯入模板」
3. 在檔案選擇對話框中選一個 `.json` 檔案
4. 系統執行驗證
5. 驗證通過後跳轉至匯入預覽頁 (P-5)
6. 預覽頁顯示：模板資訊、流程縮圖、待對應 placeholder 清單、結構警告（若有）
7. 點擊「確認匯入」
8. 若同名模板存在，跳出選擇 Modal（覆蓋 / 建立新的 / 取消）
9. 使用者選擇後，系統寫入資料庫
10. 跳轉至流程編輯器 (P-2)
11. 顯示 Toast「模板已匯入，可繼續編輯」

**Expected outcome**: 模板進入草稿狀態，使用者可繼續編輯。需主動點擊「啟用」才生效。

---

### UF-2: 從流程編輯器匯入模板（覆蓋當前編輯）

**Persona**: PM / 流程設計者
**Related FR**: FR-2
**Preconditions**: 使用者已在流程編輯器中編輯某模板

**Steps**:
1. 點擊頂部工具列「⋯」選單
2. 選擇「匯入模板」
3. 系統提示：覆蓋當前編輯內容前需確認
4. 使用者確認後，後續流程同 UF-1 step 3 開始

**Expected outcome**: 同 UF-1。當前編輯內容被新匯入內容覆蓋。

---

### UF-3: 使用者匯出模板

**Persona**: PM / 流程設計者
**Related FR**: FR-1
**Preconditions**: 使用者已在流程編輯器中編輯某模板，且模板有至少 1 個節點

**Steps**:
1. 點擊頂部工具列「⋯」選單
2. 選擇「匯出模板」
3. 系統將當前最新版本序列化為 JSON
4. Browser 觸發下載，檔名為 `{template_name}_{YYYYMMDD}.json`
5. 顯示 Toast「模板已匯出」

**Expected outcome**: 使用者本地獲得 .json 檔案，可分享給其他工作區。

---

### UF-4: 使用者套用 AI 生成的模板

**Persona**: AI 生成功能使用者
**Related FR**: FR-7
**Preconditions**: 使用者已透過 AI 生成功能產出模板（沿用既有 AI 生成 PRD 5.7 章流程）

**Steps**:
1. AI 生成完成，顯示既有「AI 生成結果預覽頁」(P-3)
2. 使用者點擊「套用至流程編輯器」
3. 系統走匯入機制（跳過檔案上傳步驟）
4. 系統執行 schema 驗證
5. 驗證通過後寫入資料庫
6. 跳轉至流程編輯器 (P-2)

**Expected outcome**: AI 生成的模板成為草稿狀態的模板，使用者可繼續編輯。

---

### UF-5: 使用者啟用匯入後的模板（含 placeholder 軟提示）

**Persona**: PM / 流程設計者
**Related FR**: FR-6
**Preconditions**: 使用者已匯入模板，狀態為 Draft

**Steps**:
1. 使用者在流程編輯器中完成必要設定（含對應執行人 placeholder）
2. 點擊「啟用」
3. 若仍有未對應的 placeholder，系統跳出軟提示 Modal：
   - 標題：`啟用前確認`
   - 內容：`有 {N} 個執行人 placeholder 尚未指派，啟用後相關節點觸發時將無法派發 task`
   - 按鈕：「取消」/「仍要啟用」
4. 使用者選擇後，系統更新模板狀態為 Active

**Expected outcome**: 模板狀態變為 Active，相關 task 可被觸發派發。

---

### UF-6: 系統載入 Seed 模板

**Trigger**: System startup
**Related FR**: FR-8

**Steps**:
1. Scheduler / boot sequence 觸發 Seed Loader
2. Seed Loader 掃描 `/seeds/automation-templates/` 資料夾
3. 對每份 `.json` 檔案執行 schema 驗證
4. 驗證通過的檔案載入為系統內建模板（標記為 system flag）
5. 驗證失敗的檔案 skip 並輸出 log
6. 載入完成後系統繼續啟動流程

**Expected outcome**: 系統內建模板出現在「選擇模板」面板供使用者套用。

## 5.4 User Journey（使用者旅程）

> 把 §5.3 的 UF 抽高一層 — PM 從拿到外部模板到讓它在自己工作區生效的完整歷程。
> 卡點欄對齊 §4 的 EF / EC。

**主要旅程：PM / 流程設計者 — 把外部模板變成可用的流程**

| 階段 | 使用者想完成 | 觸及點（UF / Page） | 可能卡點（EF / EC） | 體驗重點 |
|---|---|---|---|---|
| 1. 取得與決定匯入 | 拿到同事匯出的 `.json`，想匯入自己的工作區 | UF-1 / P-1（建立選單） | — | 匯入入口要好找，不被埋在深層選單 |
| 2. 匯入與預覽 | 確認這個檔案是不是我要的、結構有沒有問題 | UF-1, UF-2 / P-5（匯入預覽頁） | EF-1 schema 驗證失敗；EC-3 孤兒節點警告 | 失敗訊息要看得懂；預覽要能一眼判斷要不要 |
| 3. 確認寫入 | 把模板寫進工作區，不要誤覆蓋既有的 | UF-1 / P-5 + C-7（同名 Modal） | EC-1 同名衝突 | 同名時清楚知道「覆蓋 vs 建新」的後果 |
| 4. 調整與啟用 | 補上執行人 placeholder，啟用模板 | UF-5 / P-2（編輯器）+ C-8（啟用前確認） | EC-2 未對應 placeholder 軟提示 | 啟用前知道風險，但不被硬擋（軟提示） |
| 5. 使用 | 模板生效，相關 task 能被觸發派發 | P-2 | — | 確認真的 Active 了 |

> AI 生成入口（UF-4）走相同的「預覽 → 寫入 → 啟用」後段，差別只在來源不是檔案；Seed 載入（UF-6）是系統行為，不在使用者旅程內。

## 5.5 Design System 依賴

**既有 Design System 狀態**:
- [x] **已有** — 沿用既有後台 Design System
- [ ] 沒有

**來源**: 既有後台 Design System（status indicator / chip / graph component）

**本 feature 需要、但既有 Design System 還沒有的**:
- 畫布需要一個可與節點卡片明確區分的底層表面 —— 既有 token 沒有涵蓋「可平移縮放的工作區背景」
- 連線需要能表達方向與可選條件標籤；既有 graph component 有線條但無條件標籤形式
- 節點狀態需要三個級距的表現（設定完整 / 尚未指派 / 條件衝突），沿用既有 status indicator 的三級即可

## 5.6 Component Inventory

### C-1: 節點卡片 (Node Card)

**Used in**: P-2 (流程編輯器)
**Role**: 在主畫布上代表流程中的一個節點，可拖曳、點擊選取、編輯

**Must carry**:
- 節點名稱
- 節點狀態指示（三種意義，見下）
- 欄位名稱清單；超過可顯示數量時要能收起並告知還有幾個
- 執行人 placeholder 標籤，形式為 `@角色名稱`
- 上游連入與下游連出各一個連接點

**States**: idle / selected / dragging

**Status 的三種意義**（呈現方式由 Design System 決定）:
- 設定完整
- 欄位或執行人尚未指派
- 觸發條件衝突或邏輯錯誤

---

### C-2: 連線 (Connection)

**Used in**: P-2
**Role**: 連接兩個節點，表達觸發關係，可帶條件標籤

**Must carry**:
- 來源到目標的方向，必須一眼看得出來
- 觸發條件摘要標籤（例：`金額 ≥ 10000`），沒有條件時不顯示

**States**: idle / selected

**Special interactions**:
- 線段中段可插入新節點

---

### C-3: 節點設定側邊面板 (Node Setting Panel)

**Used in**: P-2
**Role**: 選取節點時顯示，編輯該節點的欄位、執行人、觸發條件

**Must carry**:
- 節點名稱，可就地編輯
- 欄位 / 執行人 / 觸發條件三個分頁，一次顯示一個
- 刪除節點
- 關閉面板

**States**: collapsed / expanded

---

### C-4: 頂部工具列 (Top Toolbar)

**Used in**: P-2
**Role**: 流程編輯器頂部操作區

**Must carry**:
- 返回模板列表頁
- 模板名稱，可就地編輯
- 版本狀態（例：`v1.0 啟用中`）
- 模擬測試
- 工作站
- 發布（本列的主要操作）
- 更多選單：匯入模板 / 匯出模板 / 版本管理 / 複製模板 / 刪除模板

---

### C-5: 「建立 Automation 模板」選單 (Create Template Menu)

**Used in**: P-1 (模板列表頁)
**Role**: 提供 4 種建立模板的入口

**Must carry**:
- 自行建立
- AI 生成
- 選擇模板
- **匯入模板**（本 feature 新增）

**States**: collapsed / expanded

---

### C-6: 匯入預覽卡 (Import Preview Card)

**Used in**: P-5 (匯入預覽頁)
**Role**: 顯示待匯入模板的資訊與唯讀縮圖

**Must carry**:
- 模板資訊區塊：名稱、描述、節點數、連線數
- 流程縮圖：唯讀的流程預覽（節點 + 連線），不可編輯
- 待對應項目區塊：列出所有 placeholder
- 結構警告區塊（條件出現）：列出 §4.3 偵測到的所有警告，逐條可讀，且與一般資訊區分得開

**States**: idle

---

### C-7: 同名模板選擇 Modal (Duplicate Name Modal)

**Used in**: 由 UF-1 step 8 觸發，覆蓋於 P-5
**Role**: 當偵測到同名模板時，讓使用者選擇處理方式

**Must carry**:
- 標題：`已存在同名模板`
- 內容：`工作區已有名為「{name}」的模板，您想要：`
- 三個出口：「覆蓋既有」/「建立新的」/「取消」

**States**: hidden / visible

---

### C-8: 啟用前確認 Modal (Activation Confirmation Modal)

**Used in**: 由 UF-5 step 3 觸發，覆蓋於 P-2
**Role**: 啟用前發現未對應 placeholder 時的軟提示

**Must carry**:
- 標題：`啟用前確認`
- 內容：`有 {N} 個執行人 placeholder 尚未指派，啟用後相關節點觸發時將無法派發 task`
- 兩個出口：「取消」/「仍要啟用」

**States**: hidden / visible

**Note**: 此為軟提示，不阻擋啟用

---

### C-9: Toast 訊息 (Toast)

**Used in**: P-1, P-2, P-5
**Role**: 短暫顯示操作結果訊息

**States**: visible / hidden（3 秒後自動消失）

**Variants**: success / error / info

## 5.7 Page / Screen 結構

> （P-4 已於設計過程中併入 P-3，編號保留不重用）

### P-1: 模板列表頁

**Entry from**: 全域導航；UF-3 結束（匯出後留在此頁）
**Responsibility**: 讓使用者總覽工作區既有模板，並從這裡開始建立新的

**區塊責任**:
- **T-1 頁面標題列**：使用 C-5（建立 Automation 模板選單）。提供 4 種建立入口
- **T-2 模板清單**：列出該工作區的所有模板，點擊進入 P-2 編輯

**Key states**: 無模板時 T-2 顯示空狀態引導（文案 + 指向 C-5 的 CTA）；載入中顯示載入佔位

---

### P-2: 流程編輯器

**Entry from**: UF-1 step 10, UF-2, UF-4 step 6, UF-5; P-1 點擊既有模板
**Responsibility**: 讓使用者編輯流程結構，並從這裡匯入 / 匯出

**區塊責任**:
- **T-1 頂部工具列**：使用 C-4。提供匯入 / 匯出入口（更多選單）
- **T-2 主畫布**：使用 C-1（節點卡片）+ C-2（連線）。支援平移、縮放（25% – 200%）、節點拖曳、連線繪製
- **T-3 節點設定側邊面板**：使用 C-3。未選取節點時收合，選取節點時出現

**版面約束**:
- T-3 出現時 T-2 必須仍可見且可操作 —— 因為使用者要邊看流程邊改設定，設定面板蓋掉正在編輯的節點就等於要來回切換

**Canvas 行為**:
- 平移：空白處按住拖曳
- 縮放：滾輪 + Ctrl/Cmd，或畫布右下角縮放按鈕
- 點擊空白：取消選取，側邊面板收合
- 拖曳節點：移動位置，連線即時重繪
- 點擊連線中段「+」：插入新節點，原連線分為兩段

**空畫布提示**: 中央顯示「拖曳或點擊以建立第一張流程卡片」

---

### P-3: AI 生成結果預覽頁

**Entry from**: AI 生成完成
**Responsibility**: 沿用既有 AI 生成模組定義

> 本 feature 不重新定義 P-3，只說明它如何銜接到匯入機制。
> 點擊「套用至流程編輯器」會走 UF-4 流程。

---

### P-5: 匯入預覽頁

**Entry from**: UF-1 step 4（驗證通過後）, UF-2
**Responsibility**: 讓使用者在寫入前看清楚要匯入什麼，並決定是否繼續

**區塊責任**:
- **T-1 頁面標題列**：標題 + 返回（回到 P-1）
- **T-2 匯入預覽卡**：使用 C-6。展示模板內容（唯讀）
- **T-3 操作按鈕列**：「取消」回 P-1；「確認匯入」觸發寫入流程，可能跳出 C-7（同名 Modal）

**Key states**: 寫入進行中「確認匯入」按鈕轉 loading 並 disable；寫入失敗停留本頁 + error Toast（C-9）

---

> ## POC 階段省略項目（前端 UI 部分）
>
> 下列功能 POC 不做，但設計時版面預留位置：
> - 小地圖 (minimap)
> - 自動排版 (auto-layout)
> - 撤銷 / 重做 (undo/redo) 與鍵盤快速鍵
> - 多選節點批次操作
> - 節點分組 / 子流程
> - 連線分支條件的視覺化區分

## 5.8 Interaction Decisions（互動體驗決策）

> 前端體驗決策清單的拍板結果。不適用的維度寫「N/A — 原因」。

| 維度 | 決定 | 理由（一句話） | Related ADR |
|---|---|---|---|
| 進入點與導覽 | P-1「建立 Automation 模板」選單新增「匯入模板」；編輯器「⋯」選單提供匯入 / 匯出 | 沿用既有建立入口，不增加新導覽項 | — |
| 容器形式 | 匯入預覽用獨立頁（P-5），不用 Modal | 預覽內容多（縮圖 + placeholder + 警告），Modal 會擠 | — |
| 操作模式 | 單線流程：選檔 → 預覽 → 確認，不做分步精靈 | 步驟少，精靈反而拖慢 | — |
| 空狀態與首次使用 | P-1 無模板時顯示引導空狀態；P-2 空畫布顯示建卡提示 | 引導使用者完成第一步操作 | — |
| 錯誤與部分成功 | 驗證失敗停留原頁 + error Toast；匯入全做或全不做，無部分成功 | 對齊 §4 EF；匯入是原子操作 | D-0005 |
| 操作回饋與防呆 | 成功用 Toast（C-9）；覆蓋既有模板需經同名 Modal（C-7）；啟用前軟提示（C-8）；匯入後一律為草稿需主動啟用 | 高風險操作攔截，低風險輕回饋 | D-0004, D-0008 |
| 資料量呈現 | P-1 卡片網格不分頁、不搜尋（POC 假設模板數 < 50） | POC 範圍取捨，預留升級空間 | — |
| 裝置與即時性 | 桌機 only；手動刷新，無即時同步 | 流程編輯器不適合行動裝置；POC 為單人編輯情境 | — |

## 5.9 Design Handoff（前端設計交接）

**Design System 來源**:
- 沿用既有後台 Design System（status indicator / chip / graph component token 既有）。本 feature 僅新增 `--node-canvas-bg`、`--connection-line` 兩個 token，已列於 §5.5。無前置條件缺口。

**Mockup / 視覺稿**:
- 產出方式：實作階段由前端依既有 Design System 定案；節點卡片、連線等特殊視覺已於 §5.6 給尺寸與狀態規範
- 餵給實作 / 設計工具的輸入：§5.6 component（角色 + 狀態 + 尺寸）、§5.7 page（版面 ASCII + Key states）、§5.8 互動決策
- 視覺以既有 Design System 為準；新增 component（節點卡片 C-1、連線 C-2）的視覺於實作階段定案後，回頭同步 §5.6

**前端開工前的前置清單**:
- [x] Design System / tokens 就緒（沿用既有 + 2 個新 token）
- [x] 視覺參照備妥（既有後台元件庫）
- [x] 響應式斷點確認（桌機 only，無需斷點，對齊 §5.8）
- [ ] 文案 / microcopy 來源 — 錯誤訊息、空狀態、軟提示文案散見 §5.3 / §5.6（C-8 啟用前確認文案已定），實作前由 PM 收斂為一份文案表

> 本 feature 無「尚無 Design System」的前置缺口，故 §7 不需額外 OQ。

## 文件結束 — 回填 §4

> 已將 §4 各 SF 的 "Related UF" 對應補全：
> - SF-1 → UF-1, UF-2
> - SF-2 → UF-3
> - SF-3 → UF-4
> - SF-4 → UF-6
