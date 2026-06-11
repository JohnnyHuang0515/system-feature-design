# D-0007: 模板採 self-contained（檔案內完整），不依賴外部引用

- **Status**: Accepted
- **Date**: 2026-05-14
- **Affects**: §3.2 (Entities, JSON Schema), §4.1 (SF-1, SF-2)
- **Supersedes**: —
- **Superseded by**: —

## Context

匯出檔案的核心目標是「可攜帶」：能在任意工作區、甚至未來跨組織匯入（§1.1）。若檔案內容引用目標環境不存在的資源（具體成員、外部 task 模板、其他模板），匯入就會失敗或產生 dangling reference。

需要決定檔案的完整性策略：所有內容內嵌（self-contained），還是允許引用外部資源。

## Decision

匯出檔案採 self-contained，檔案本身包含重建模板所需的全部資訊：

- 節點的 task 欄位定義完整內嵌（`task_structure.fields`，配合 D-0001 的 `task_template_ref` 固定 null）
- 執行人轉為 placeholder，不帶具體 user_id（BR-3）
- 節點 / 連線使用 file-local ID（`node_1`, `conn_1`），匯入時重新分配 DB UUID（SF-1 step 6）
- 匯入即複製，不建立跨工作區引用（§1.5 out of scope）

## Rationale

- 「匯入到任何工作區都成功」是 POC 的核心驗證目標（§1.4），外部依賴直接威脅這一點
- 檔案單獨可讀、可離線檢視，對 debug 與人工審閱友善
- 匯入邏輯單純：驗證 → 重新配 ID → 寫入，不需要 resolve 外部資源
- 與 AI 生成（SF-3）、seed 載入（SF-4）共用同一格式時，三條路徑都不需要環境前置條件

## Alternatives Considered

### A1: 允許引用來源工作區的資源

**Pros**:
- 檔案小、無重複內容
- 來源更新時引用方可同步（資料一致性）

**Cons**:
- 目標工作區無法 resolve 來源資源（跨工作區存取權限問題）
- 來源資源被刪除後檔案即失效
- POC 明確不支援跨工作區引用（§1.5）

**Why rejected**: 違反「可攜帶」的根本目標

### A2: 混合模式（核心內嵌、選擇性外部引用）

**Pros**:
- 兼顧可攜帶與去重

**Cons**:
- 匯入端要實作兩套讀取路徑與 fallback 邏輯
- Schema 與驗證規則複雜度倍增

**Why rejected**: POC 不需要；D-0001 已用 `task_template_ref` 預留欄位，未來可漸進演進到此模式

## Consequences

**Positive**:
- 模板檔案可攜帶到任何工作區，無環境前置條件
- 匯入 / 驗證邏輯單純，SF-1 / SF-3 / SF-4 共用無分支
- 檔案可獨立 debug、人工審閱、進版控

**Negative**:
- 檔案較大（內容重複），需留意 5 MB 上限（BR-6）
- 相同 task 定義在多個模板間複製，無法集中更新（同 D-0001 negative）
- 未來模板市集若要做內容去重 / 引用共享，需基於 `task_template_ref` 再設計
