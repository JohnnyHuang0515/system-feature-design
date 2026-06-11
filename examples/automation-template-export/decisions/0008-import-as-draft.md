# D-0008: 匯入後初始狀態為草稿，使用者主動啟用

- **Status**: Accepted
- **Date**: 2026-05-14
- **Affects**: §3.3 (state machine), §3.4 (BR-7), §5.3 (UF-5)
- **Supersedes**: —
- **Superseded by**: —

## Context

匯入的模板若直接進入 Active 狀態，會立刻被 Automation 引擎觸發。但匯入的模板通常「還沒準備好」：

- Assignee placeholder 尚未對應到具體成員（EC-2, D-0002），觸發後無法派發 task
- 使用者可能還想檢查或微調內容（孤兒節點警告等，FR-9）
- 匯入來源（檔案 / AI 生成）的內容未經使用者在本工作區的確認

需要決定匯入後的初始狀態，以及由誰、在什麼時點啟用。

## Decision

所有使用者觸發的匯入路徑（檔案匯入 SF-1、AI 生成 SF-3）寫入後 `status = Draft`（BR-7, FR-6），不可直接 Active。使用者在編輯器完成設定後主動點擊「啟用」（UF-5），經 state machine 的 `activate()` 轉換（§3.3，guard：至少 1 個 Node）。

啟用時若仍有未對應 placeholder，跳軟提示 Modal（C-8）但不阻擋（EC-2）。

## Rationale

- 安全預設：不讓未檢查的內容直接影響執行中的業務流程
- 與「先匯入再編輯」的主流程一致（UF-1 結尾即進編輯器）
- Draft 狀態天然容納「不完整」（placeholder 未對應、孤兒節點），與 D-0002 / D-0005 的寬鬆匯入策略互補
- 啟用是明確的使用者意圖表達，audit 上有清楚的責任人（TemplateActivated 事件）

## Alternatives Considered

### A1: 匯入後直接 Active

**Pros**:
- 少一步操作，匯入即可用

**Cons**:
- 未對應 placeholder 的節點觸發時派發失敗，產生執行錯誤
- 使用者未確認的內容直接生效，風險高
- 覆蓋匯入（EC-1）時會立刻切換執行中的流程版本

**Why rejected**: 對「匯入內容不可信任」的場景完全沒有防線

### A2: 匯入時讓使用者選擇 Draft 或 Active

**Pros**:
- 對「我很確定這份模板沒問題」的使用者省一步

**Cons**:
- 多數情況仍需先進編輯器補 placeholder 對應，選 Active 的場景很少
- 多一個決策點，匯入流程變長
- State machine 多一條 import → Active 路徑，guard 邏輯複雜化

**Why rejected**: 為少數場景增加常態流程的複雜度，不划算

## Consequences

**Positive**:
- 匯入永遠安全：不會意外觸發、不會影響執行中的 task
- State machine 入口單一（[*] → Draft），驗證與測試簡單（AC-6.1, AC-S.1）
- 與 EC-2 軟提示組成完整的「啟用前防呆」體驗

**Negative**:
- 使用者多一步啟用操作，匯入後忘記啟用的模板可能堆積
- 需以 `import_source_to_activation_rate` 指標（§9.3.1）觀察「匯入但從未啟用」的比例，作為流程改善依據
