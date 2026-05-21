# D-0001: Task 欄位採內嵌儲存，預留外部引用欄位

- **Status**: Accepted
- **Date**: 2026-05-14
- **Affects**: §3.2 (Node.task_template_ref, Node.fields), §4.1 (SF-1 Import flow)
- **Supersedes**: —
- **Superseded by**: —

## Context

Automation 模板的每個節點都包含「task 欄位定義」（field_key、field_type 等）。POC 階段需決定欄位定義是內嵌在模板中（self-contained），還是引用外部 Task 模板。

兩種模式各有取捨：
- 內嵌：模板檔案完整可攜帶，匯入後不依賴外部
- 外部引用：可重用 task 定義、減少重複，但增加跨 entity 依賴與版本管理複雜度

## Decision

POC 採內嵌儲存，但 schema 預留 `task_template_ref` 欄位（固定 null）以便未來升級為引用模式。

兩種模式設計為可共存：
- `task_template_ref` 有值 → 引用模式（未來啟用）
- `task_template_ref` 為 null → 內嵌模式（POC 預設）

匯入時依此欄位判斷讀取路徑。

## Rationale

- POC 目標是驗證模板攜帶機制，外部引用增加複雜度且現階段不需要
- 預留欄位讓未來升級不需要 schema migration
- 兩種模式共存的設計支援漸進採用，不強迫全量遷移
- Self-contained 檔案對 debug、跨組織分享、版本化都更友善

## Alternatives Considered

### A1: 完全內嵌，不預留欄位

**Pros**:
- 最簡單，schema 更乾淨
- 不需要思考未來升級

**Cons**:
- 未來改用引用模式需要 schema migration
- 對既有匯入 / 匯出檔案需要轉換
- POC 期間如有方向改變成本高

**Why rejected**: 未來幾乎必然會做引用模式（task 重用是 power user 的需求），避免遷移成本值得多寫一個固定 null 欄位

### A2: 直接做引用模式

**Pros**:
- 一步到位，沒有未來遷移成本
- 支援 task 重用，避免重複定義

**Cons**:
- POC 增加跨 entity 依賴與版本管理
- 影響整個匯入 / 匯出邏輯複雜度（要處理「引用的外部 task 版本鎖定」）
- 違反 POC「先驗證核心機制」的精神
- 跨工作區匯入時，引用的外部 task 可能不存在

**Why rejected**: POC 階段不需要這個彈性，過度設計。等實際有使用者反映 task 重用需求時再做。

## Consequences

**Positive**:
- POC 邏輯簡單，self-contained 檔案易於 debug
- 預留欄位讓未來升級成本低（schema 不變）
- 模板可獨立攜帶到任何工作區，不依賴外部資源

**Negative**:
- 目前 schema 多了一個固定 null 的欄位，對讀者有解釋成本
- 兩種模式並存的「未來架構」增加長期 maintenance 複雜度
- Task 定義重複（相同 task 在多個模板中複製）
