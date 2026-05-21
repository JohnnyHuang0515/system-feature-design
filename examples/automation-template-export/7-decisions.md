# 7. Decisions

本 feature 的設計決策記錄在 `decisions/` 目錄中，每個 decision 一個檔案。

## 7.1 Decision Index

### Active Decisions

| ID | Title | Status | Date | Affects |
|----|-------|--------|------|---------|
| [D-0001](./decisions/0001-task-fields-embedded-with-future-ref.md) | Task 欄位採內嵌儲存，預留外部引用欄位 | Accepted | 2026-05-14 | §3.2 (Node.task_template_ref), §4.1 (SF-1) |
| [D-0002](./decisions/0002-placeholder-mapping-deferred-to-editor.md) | Placeholder 對應統一在編輯器，預覽頁不做 mapping | Accepted | 2026-05-14 | §4.3 (EC-2), §5.3 (UF-1), §5.6 (P-5) |
| [D-0003](./decisions/0003-no-encryption-for-poc.md) | POC 階段匯出檔案不做加密 / 簽章 | Accepted | 2026-05-14 | §2.2 (NFR-5) |
| [D-0004](./decisions/0004-duplicate-name-modal-on-confirm.md) | 同名模板處理用 Modal 三選一（覆蓋 / 建新 / 取消） | Accepted | 2026-05-14 | §4.3 (EC-1), §5.3 (UF-1) |
| [D-0005](./decisions/0005-structure-validation-strictness.md) | 結構驗證嚴格度：自連禁、孤兒警告、環狀放行 | Accepted | 2026-05-14 | §3.4 (BR-4), §4.2 (EF-3), §4.3 (EC-3, EC-4, EC-5) |
| [D-0006](./decisions/0006-seed-templates-via-folder.md) | 系統內建模板透過 seed 資料夾載入，POC 不做後台 | Accepted | 2026-05-14 | §4.1 (SF-4), §5.3 (UF-6), §9.2 |
| [D-0007](./decisions/0007-self-contained-templates.md) | 模板採 self-contained（檔案內完整），不依賴外部引用 | Accepted | 2026-05-14 | §3.2 (Entities), §4.1 (SF-1, SF-2) |
| [D-0008](./decisions/0008-import-as-draft.md) | 匯入後初始狀態為草稿，使用者主動啟用 | Accepted | 2026-05-14 | §3.3 (state machine), §3.4 (BR-7), §5.3 (UF-5) |
| [D-0009](./decisions/0009-export-latest-version-only.md) | 匯出只含最新版，不含歷史 | Accepted | 2026-05-14 | §4.1 (SF-2) |

### Superseded / Deprecated

（本 spec 尚無被取代的 decision）

## 7.2 Open Questions

| ID | Title | Blocking? | Owner | Target Date |
|----|-------|-----------|-------|-------------|
| [D-0010](./decisions/0010-schema-version-migration.md) | Schema 升版時的 migration 機制 | No | @bobo | Post-POC |
| [D-0011](./decisions/0011-import-rate-limiting.md) | 匯入 API 是否需要 rate limiting | No | @tech-lead | Before MVP |
