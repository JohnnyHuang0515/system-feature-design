# {Feature Name}

{一句話描述這個 feature 是什麼}

- **Status**: Draft | In Review | Approved | Implemented
- **Owner**: @{name}
- **Last updated**: YYYY-MM-DD

## Documents

| # | File | What's inside |
|---|------|---------------|
| 1 | [problem-scope.md](./1-problem-scope.md) | 要解決的問題、目標使用者、成功指標、scope 邊界 |
| 2 | [requirements.md](./2-requirements.md) | 功能需求清單（FR）、非功能需求（NFR）、優先級 |
| 3 | [domain-model.md](./3-domain-model.md) | 核心 entity、欄位、狀態機、業務規則 |
| 4 | [flows.md](./4-flows.md) | 系統內部流程、錯誤處理流程、邊界情境 |
| 5 | [presentation-spec.md](./5-presentation-spec.md) | 呈現方式、使用者故事、使用者流程、UI 元件、頁面結構 |
| 6 | [interfaces.md](./6-interfaces.md) | 對外 API、事件、整合點、錯誤回應格式 |
| 7 | [decisions.md](./7-decisions.md) | 關鍵設計決策索引、待決議事項 |
| 8 | [acceptance.md](./8-acceptance.md) | 每個 FR 對應的驗收情境（Given-When-Then） |
| 9 | [rollout.md](./9-rollout.md) | 上線策略、監控、Runbook（選填） |

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
| T-N | Page Section / Region | 5-presentation-spec.md §5.6 |
| D-NNNN | Decision (ADR) | decisions/ |
| AC-* | Acceptance Criteria | 8-acceptance.md |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v0.1 | YYYY-MM-DD | @{name} | Initial draft |
