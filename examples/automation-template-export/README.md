# Automation Template Export/Import

讓使用者可以將 Automation 模板匯出為 JSON 檔案、從 JSON 匯入到工作區，並讓 AI 生成的模板能透過同一條路徑寫入資料庫。

- **Status**: Draft (POC v0.1)
- **Owner**: @bobo
- **Last updated**: 2026-05-14

## Documents

| # | File | What's inside |
|---|------|---------------|
| 1 | [problem-scope.md](./1-problem-scope.md) | 要解決的問題、目標使用者、成功指標、scope 邊界（POC 設計決定） |
| 2 | [requirements.md](./2-requirements.md) | 功能需求（FR）、非功能需求（NFR）、優先級 |
| 3 | [domain-model.md](./3-domain-model.md) | Template / Node / Connection entities、狀態機、業務規則、JSON schema |
| 4 | [flows.md](./4-flows.md) | 匯出 / 匯入 / AI 生成 / Seed 載入的系統流程、錯誤處理、邊界情境 |
| 5 | [presentation-spec.md](./5-presentation-spec.md) | 使用者故事、使用者流程、UI 元件、頁面結構 |
| 6 | [interfaces.md](./6-interfaces.md) | 匯出 / 匯入 API、錯誤碼 |
| 7 | [decisions.md](./7-decisions.md) | POC 階段的關鍵設計決策（ADR）、待決議事項 |
| 8 | [acceptance.md](./8-acceptance.md) | 對應 FR / state / BR / error / NFR 的驗收情境 |
| 9 | [rollout.md](./9-rollout.md) | Seed 載入、Observability、Rollback Plan（POC 階段精簡版） |

## ID 編號系統

| Prefix | Meaning | Defined in |
|--------|---------|------------|
| FR-N | Functional Requirement | 2-requirements.md §2.1 |
| NFR-N | Non-Functional Requirement | 2-requirements.md §2.2 |
| BR-N | Business Rule | 3-domain-model.md §3.4 |
| SF-N | System Flow | 4-flows.md §4.1 |
| EF-N | Error Flow | 4-flows.md §4.2 |
| EC-N | Edge Case | 4-flows.md §4.3 |
| UF-N | User Flow | 5-presentation-spec.md §5.3 |
| P-N | Page / Screen | 5-presentation-spec.md §5.6 |
| C-N | Component | 5-presentation-spec.md §5.5 |
| T-N | Page Section | 5-presentation-spec.md §5.6 |
| D-NNNN | Decision (ADR) | decisions/ |
| AC-* | Acceptance Criteria | 8-acceptance.md |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v0.1 | 2026-05-14 | @bobo | Initial POC draft |
