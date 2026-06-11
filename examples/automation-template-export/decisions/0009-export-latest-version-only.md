# D-0009: 匯出只含最新版，不含歷史

- **Status**: Accepted
- **Date**: 2026-05-14
- **Affects**: §4.1 (SF-2), §3.2 (Template.template_version)
- **Supersedes**: —
- **Superseded by**: —

## Context

模板有版本概念：覆蓋匯入會產生新版本（EC-1, v1 → v2），啟用版本切換沿用既有規則。匯出時需決定檔案要不要帶版本歷史：只帶當前最新版，還是完整歷史？

匯出的主要用途是「把模板搬到別的工作區使用」（FR-1, §1.3），而非備份或稽核。

## Decision

匯出只序列化當前最新版本（SF-2 step 1），不含版本歷史（§1.5 out of scope）。

- 檔案 `metadata.template_version` 帶版本號供參考
- 匯入時不繼承版本號，在目標工作區從 v1.0 重新起算（§3.2 Template.template_version「匯入時不繼承」）

## Rationale

- 接收方要的是「可用的模板」，來源工作區的歷史對他沒有意義
- 版本歷史會放大檔案大小，與 5 MB 上限（BR-6）衝突
- 匯入端只需處理單一版本寫入，schema 與匯入邏輯都單純
- 歷史屬於來源工作區的稽核資料，外洩到檔案反而有資訊治理疑慮

## Alternatives Considered

### A1: 匯出完整版本歷史

**Pros**:
- 接收方可追溯模板演進
- 可作為完整備份

**Cons**:
- 檔案大小隨版本數線性膨脹，易撞 BR-6 上限
- 匯入端要決定「多版本如何落地」（全部建立？只建最新？），複雜度高
- 跨工作區場景下歷史幾乎不被使用

**Why rejected**: 成本高、需求未被驗證；§1.5 已明確列為 out of scope

### A2: 讓使用者選擇匯出哪個版本（或多選）

**Pros**:
- 彈性最大，可匯出舊版分享

**Cons**:
- 匯出 UI 複雜化（版本選擇器）
- API 需增加版本參數與對應驗證
- POC 無此需求訊號

**Why rejected**: 過度設計；§1.5.1 已將「多版本匯出」列為未來方向，等需求出現再做

## Consequences

**Positive**:
- 檔案小、schema 單純（單一 nodes / connections 結構，§3.2）
- 匯出與匯入邏輯都只處理一個版本，實作與測試簡單（AC-1.1）
- 來源工作區的版本歷史不外洩

**Negative**:
- 版本歷史不可攜帶，搬到新工作區即「斷代」
- 未來若做多版本匯出，JSON Schema 需擴充（nodes / connections 要掛在版本層級下），屬 breaking change，需配合 schema_version 升版（D-0010）
