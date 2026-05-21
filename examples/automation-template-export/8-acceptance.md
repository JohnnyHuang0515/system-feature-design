# 8. Acceptance Criteria

## 8.1 AC for Functional Requirements

### FR-1: Export template as JSON file

#### AC-1.1: 成功匯出含節點的模板

**Given** 使用者在流程編輯器中編輯一個含至少 1 個節點的模板
**When** 點擊「⋯」選單 → 「匯出模板」
**Then**
- Browser 觸發檔案下載
- 檔名格式為 `{template_name}_{YYYYMMDD}.json`
- 檔案內容符合 §3.2 的完整 JSON Schema
- 檔案 metadata.exported_at 為當前時間
- 不包含真實 user_id、workspace_id、DB 內部 ID
- Assignees 為 placeholder 格式
- 顯示 Toast「模板已匯出」

#### AC-1.2: 匯出無節點模板應失敗

**Given** Template 存在但無任何 Node
**When** 點擊「匯出模板」
**Then**
- 回傳 422 EMPTY_TEMPLATE
- 顯示錯誤訊息「模板尚未建立任何節點，無法匯出」
- 不觸發檔案下載

---

### FR-2: Import template from JSON file

#### AC-2.1: 成功匯入合法檔案（無同名）

**Given** 使用者已登入並進入模板列表頁，workspace 內無同名模板
**When** 透過「建立 Automation 模板」→「匯入模板」上傳合法 JSON 檔案，並確認匯入
**Then**
- 回傳 201
- DB 建立新 Template，status = Draft
- Template 的 Nodes 與 Connections 已建立
- 所有 ID 重新分配為 DB UUID（檔案內的 local_id 不出現在 DB）
- 跳轉至流程編輯器顯示新模板
- 顯示 Toast「模板已匯入，可繼續編輯」
- 發出 TemplateImported 事件（source = file）

#### AC-2.2: 匯入觸發預覽頁

**Given** 上傳合法 JSON 檔案
**When** 系統完成驗證
**Then**
- 跳轉至匯入預覽頁 (P-5)
- 預覽頁顯示模板資訊（名稱、描述、節點數、連線數）
- 預覽頁顯示流程縮圖（唯讀）
- 預覽頁列出所有 assignee placeholder

#### AC-2.3: 未授權匯入

**Given** 使用者未登入
**When** 嘗試呼叫 POST /api/templates/import
**Then**
- 回傳 401 UNAUTHORIZED
- 不建立任何資料

---

### FR-3: Schema validation on import

#### AC-3.1: Schema 不合法應拒絕

**Given** 上傳的檔案缺少必填欄位（例：缺 metadata.name）
**When** 觸發匯入
**Then**
- 回傳 400 INVALID_SCHEMA
- Response.error.details.path 指出具體錯誤位置（例：`/metadata/name`）
- 不跳轉至預覽頁
- 不建立任何資料

#### AC-3.2: 節點自連應拒絕

**Given** 上傳檔案中存在 connection 的 source_node_id == target_node_id
**When** 觸發匯入
**Then**
- 回傳 400 INVALID_STRUCTURE
- Error message 指明違規的 node_id
- 不建立任何資料

#### AC-3.3: Connection 引用不存在的 field 應拒絕

**Given** 上傳檔案中 condition.field_key 在 source 節點的 fields 中不存在
**When** 觸發匯入
**Then**
- 回傳 400 INVALID_STRUCTURE
- Error message 指明違規的 field_key
- 不建立任何資料

---

### FR-4: Import preview page

#### AC-4.1: 預覽頁顯示警告區塊

**Given** 檔案合法但含結構警告（例：孤兒節點）
**When** 進入預覽頁
**Then**
- 預覽頁顯示警告區塊，列出所有警告（每項一行，黃色警告 icon）
- 警告不阻擋「確認匯入」按鈕
- API response 的 warnings 陣列包含這些警告

---

### FR-5: Duplicate name handling

#### AC-5.1: 同名偵測跳出 Modal

**Given** Workspace 已有名為「訂單流程」的 Template，使用者匯入同名檔案
**When** 點擊預覽頁「確認匯入」
**Then**
- 跳出 Modal「已存在同名模板」
- Modal 提供 3 個按鈕：「覆蓋既有」/「建立新的」/「取消」
- 不直接寫入任何資料

#### AC-5.2: 「覆蓋既有」儲存為新版本

**Given** Modal 出現，使用者選「覆蓋既有」
**When** 確認後
**Then**
- 既有模板新增一個版本（v1 → v2）
- 原版本內容保留（版本歷史不丟）
- 新版本狀態為 Draft，需手動啟用
- 既有版本若為 Active 且有執行中 task：執行中 task 繼續跑舊版完成

#### AC-5.3: 「建立新的」加 suffix

**Given** Modal 出現，使用者選「建立新的」
**When** 確認後
**Then**
- 建立全新 Template，名稱自動加 suffix（例：「訂單流程 (2)」）
- 不影響原模板
- 新 Template 狀態為 Draft

#### AC-5.4: 同名但未提供 action

**Given** 預覽階段偵測到同名，使用者直接呼叫 /confirm 未帶 duplicate_name_action
**When** 系統處理
**Then**
- 回傳 409 DUPLICATE_NAME_UNRESOLVED
- 不建立資料

---

### FR-6: Imported templates as Draft

#### AC-6.1: 匯入後預設為 Draft

**Given** 任何匯入路徑（檔案 / AI / Seed 除外）
**When** 寫入完成
**Then**
- Template.status = Draft
- 模板不被 Automation 引擎觸發

#### AC-6.2: 啟用前 placeholder 軟提示

**Given** Template Draft 狀態，至少有 1 個未對應的 assignee placeholder
**When** 使用者點擊「啟用」
**Then**
- 跳出軟提示 Modal「啟用前確認」
- Modal 內容包含未對應 placeholder 數量
- 按鈕：「取消」/「仍要啟用」
- 「仍要啟用」可繼續啟用流程（軟提示不阻擋）

---

### FR-7: AI-generated content import path

#### AC-7.1: AI 生成走匯入機制

**Given** AI 生成功能產出合法 JSON 結構
**When** 使用者點擊「套用至流程編輯器」
**Then**
- 系統走 POST /api/templates/import（source = "ai"）
- 跳過檔案上傳步驟
- 沿用既有 AI 生成結果預覽頁
- 驗證通過後寫入 DB，sources = ai

#### AC-7.2: AI 生成不合法應走 AI 失敗流程

**Given** AI 生成的 JSON 結構不符合 schema
**When** 觸發匯入
**Then**
- 不寫入 DB
- 視為「AI 生成失敗」走既有失敗流程
- 扣點規則依既有 AI 模組決定（不在本 feature 範圍）

---

### FR-8: Seed templates loading

#### AC-8.1: Seed 載入成功

**Given** `/seeds/automation-templates/` 內有合法 .json 檔案
**When** 系統啟動
**Then**
- 每份合法檔案載入為系統內建模板
- 模板帶 system flag
- 出現在「選擇模板」面板供使用者套用

#### AC-8.2: Seed 載入失敗 skip

**Given** Seed 資料夾內有不合法檔案（schema 違規）
**When** 系統啟動
**Then**
- 該檔案 skip 不載入
- 輸出 log 含 file_path + error
- 發出 SeedTemplateLoadFailed 事件
- 系統繼續啟動（不阻擋其他檔案載入或系統運作）

---

### FR-9: Structural warnings (non-blocking)

#### AC-9.1: 孤兒節點警告

**Given** 模板含未連線節點且總節點數 > 1
**When** 匯入
**Then**
- 允許匯入，不擋
- API response 的 warnings 包含 `{ type: "orphan_node", message: "..." }`
- 預覽頁顯示警告

#### AC-9.2: 多重連線警告

**Given** 同兩節點間有 ≥ 2 條 connection
**When** 匯入
**Then**
- 允許匯入，不擋
- API response 的 warnings 包含 `{ type: "duplicate_connection", message: "..." }`
- 預覽頁顯示警告

#### AC-9.3: 環狀連線不警告

**Given** 模板有 A → B → C → A 環狀連線
**When** 匯入
**Then**
- 允許匯入，不擋
- 不出現任何警告（既不擋亦不警告）

## 8.2 AC for State Transitions

### Template State Transitions

#### AC-S.1: 匯入後進入 Draft（合法）

**Given** 通過匯入流程完成寫入
**When** 寫入成功
**Then**
- Template.status = Draft
- 不發出 TemplateActivated 事件

#### AC-S.2: Draft → Active（合法）

**Given** Template 處於 Draft 狀態，至少有 1 個 Node
**When** 呼叫 activate()
**Then**
- Template.status = Active
- 發出 TemplateActivated 事件

#### AC-S.3: 空 Template 不可 Activate（違規）

**Given** Template Draft 但 Nodes 為空
**When** 嘗試 activate()
**Then**
- 回傳 422 BUSINESS_RULE_VIOLATION
- Template.status 保持 Draft
- 不發出事件

#### AC-S.4: Active → Archived（合法）

**Given** Template 處於 Active 狀態
**When** 呼叫 archive()
**Then**
- Template.status = Archived
- 已執行中的 task instance 繼續跑完
- 發出 TemplateArchived 事件

#### AC-S.99: 所有未列出的狀態轉換皆應被拒絕

**Given** Template 處於任何狀態
**When** 嘗試執行該狀態不允許的轉換（參照 §3.3）
**Then**
- 回傳 409 INVALID_STATE_TRANSITION
- 狀態不改變
- 不觸發 side effect

## 8.3 AC for Business Rules

### BR-1: Template name unique in workspace

#### AC-BR.1

**Given** Workspace 已有名為「訂單流程」的 Template
**When** 嘗試直接建立同名 Template（不走匯入）
**Then**
- 回傳 409 DUPLICATE_NAME（DB constraint 觸發）
- 不建立新 Template

> 註：匯入路徑的同名處理見 AC-5.1 ~ AC-5.4，那是預期行為（提供使用者選擇），非錯誤。

### BR-2: Schema version supported

（參見 AC-3.1）

### BR-3: Assignees use placeholders only

#### AC-BR.3

**Given** 匯出 Template
**When** 序列化為 JSON
**Then**
- 所有 assignees 欄位的 placeholder_type 為 role 或 variable
- 不出現任何 user_id 或 user-specific 標識

### BR-4: No self-connection

（參見 AC-3.2）

### BR-5: Connection references valid field

（參見 AC-3.3）

### BR-6: File size ≤ 5 MB

#### AC-BR.6

**Given** 上傳檔案 > 5 MB
**When** POST /api/templates/import
**Then**
- 回傳 400 FILE_TOO_LARGE
- 不執行 schema 驗證（短路）

### BR-7: Imports start as Draft

（參見 AC-6.1）

### BR-8: Import atomicity

#### AC-BR.8

**Given** 匯入過程中發生 DB 寫入失敗（模擬 connection drop）
**When** Transaction commit 階段
**Then**
- Transaction rollback
- DB 不留下任何半成品（無 Template / Node / Connection 記錄）
- 回傳 500 INTERNAL_ERROR

## 8.4 AC for Error & Edge Cases

### EF-1 ~ EF-6 對應 AC

| EF | 對應 AC |
|----|---------|
| EF-1 Schema 驗證失敗 | AC-3.1 |
| EF-2 檔案過大 | AC-BR.6 |
| EF-3 節點自連 | AC-3.2 |
| EF-4 引用無效欄位 | AC-3.3 |
| EF-5 DB 寫入失敗 | AC-BR.8 |
| EF-6 匯出空模板 | AC-1.2 |

### EC-1 ~ EC-7 對應 AC

#### AC-EC.1: 同名模板處理（見 AC-5.1 ~ AC-5.4）

#### AC-EC.2: 未對應 placeholder 軟提示（見 AC-6.2）

#### AC-EC.3: 孤兒節點警告（見 AC-9.1）

#### AC-EC.4: 多重連線警告（見 AC-9.2）

#### AC-EC.5: 環狀連線放行（見 AC-9.3）

#### AC-EC.6: 單一節點模板放行

**Given** 模板僅 1 個節點，無 connection
**When** 匯入
**Then**
- 允許匯入，不擋
- 不顯示任何警告

#### AC-EC.7: 重複觸發匯入

**Given** 使用者短時間內帶相同 X-Idempotency-Key 重複呼叫 /confirm
**When** 第二次呼叫到達
**Then**
- 不重複建立 Template
- 回傳第一次呼叫的結果（idempotent，5 分鐘內有效）

## 8.5 AC for Non-Functional Requirements

### NFR-1: Import API latency p99 < 500ms

#### AC-NFR.1

**Verification level**: Verifiable pre-release

**Test method**: Load test

**Setup**: 50 concurrent users，每人每分鐘上傳 1 個 200KB JSON 檔案（典型大小），持續 10 分鐘

**Pass criteria**:
- p99 latency < 500ms
- Error rate < 0.1%

**Tool**: k6 或 Locust

**Notes**: Staging 環境規格相當於 prod 50%；prod 預期表現會更好

---

### NFR-2: Max file size 5 MB

#### AC-NFR.2

**Verification level**: Verifiable pre-release

**Test method**: Functional test

**Pass criteria**:
- 上傳 5 MB - 1 byte 的檔案：通過
- 上傳 5 MB + 1 byte 的檔案：回傳 400 FILE_TOO_LARGE

---

### NFR-3: Only authenticated workspace members

#### AC-NFR.3

**Verification level**: Verifiable pre-release

**Test method**: Functional test

**Pass criteria**:
- 未登入呼叫 import / export → 401
- 登入但非 workspace member → 403
- 登入且是 workspace member → 通過

---

### NFR-4: No real IDs in export

#### AC-NFR.4

**Verification level**: Verifiable pre-release

**Test method**: Static check on exported files

**Pass criteria**:
- 匯出檔案中不出現 user_id 欄位（任何形式）
- 匯出檔案中不出現 workspace_id 欄位
- 匯出檔案中所有 ID 為 file-local（如 `node_1`, `conn_1`），非 UUID

---

### NFR-6: Import atomicity

#### AC-NFR.6

**Verification level**: Partial verification (simulated)

**Test method**: Chaos test — 在 DB commit 階段注入失敗

**Pass criteria**:
- DB 不留下任何半成品
- 使用者收到 500 錯誤
- 重試後可成功

**Notes**: 真實 prod 場景的 atomicity 由 DB transaction 保證，但需 chaos test 驗證 application 層的 rollback 處理正確

---

### NFR-7: Seed loading failure must not block startup

#### AC-NFR.7

**Verification level**: Verifiable pre-release

**Test method**: Integration test

**Pass criteria**:
- 故意放入不合法 seed 檔案
- 系統啟動仍成功，其他合法 seed 正常載入
- 不合法檔案的錯誤寫入 log

## 8.6 Test Coverage Matrix

| Requirement | AC Coverage |
|-------------|-------------|
| FR-1 | AC-1.1, AC-1.2 |
| FR-2 | AC-2.1, AC-2.2, AC-2.3 |
| FR-3 | AC-3.1, AC-3.2, AC-3.3 |
| FR-4 | AC-4.1 |
| FR-5 | AC-5.1, AC-5.2, AC-5.3, AC-5.4 |
| FR-6 | AC-6.1, AC-6.2 |
| FR-7 | AC-7.1, AC-7.2 |
| FR-8 | AC-8.1, AC-8.2 |
| FR-9 | AC-9.1, AC-9.2, AC-9.3 |
| BR-1 | AC-BR.1 |
| BR-2 | (covered by AC-3.1) |
| BR-3 | AC-BR.3 |
| BR-4 | (covered by AC-3.2) |
| BR-5 | (covered by AC-3.3) |
| BR-6 | AC-BR.6 |
| BR-7 | (covered by AC-6.1) |
| BR-8 | AC-BR.8 |
| State transitions | AC-S.1 ~ AC-S.99 |
| EF-1 ~ EF-6 | (covered by AC-3.x, AC-BR.x, AC-1.2) |
| EC-1 ~ EC-7 | AC-EC.1 ~ AC-EC.7 |
| NFR-1 ~ NFR-4, NFR-6, NFR-7 | AC-NFR.1 ~ AC-NFR.7 |
| NFR-5 (no encryption) | 由 D-0003 ADR 記錄，無 AC（POC 不做） |
| NFR-8, NFR-9 (observability) | 由 §9.3 規範，無 AC（運維驗證） |
