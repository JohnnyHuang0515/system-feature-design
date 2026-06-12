# {Feature Name}

{一句話描述這個 feature 是什麼}

- **Status**: Draft | In Review | Approved | Implemented
- **Owner**: @{name}
- **Last updated**: YYYY-MM-DD

## Documents

| # | File | What's inside | 狀態 |
|---|------|---------------|------|
| 1 | [problem-scope.md](./1-problem-scope.md) | 要解決的問題、目標使用者、成功指標、scope 邊界 | ⬜ 待產 |
| 2 | [requirements.md](./2-requirements.md) | 功能需求清單（FR）、非功能需求（NFR）、優先級 | ⬜ 待產 |
| 3 | [domain-model.md](./3-domain-model.md) | 核心 entity、欄位、狀態機、業務規則 | ⬜ 待產 |
| 4 | [flows.md](./4-flows.md) | 系統內部流程、錯誤處理流程、邊界情境 | ⬜ 待產 |
| 5 | [presentation-spec.md](./5-presentation-spec.md) | 呈現方式、使用者故事、使用者流程、使用者旅程、UI 元件、頁面結構、互動體驗決策、設計交接 | ⬜ 待產 |
| 6 | [interfaces.md](./6-interfaces.md) | 對外 API、事件、整合點、錯誤回應格式 | ⬜ 待產 |
| 7 | [decisions.md](./7-decisions.md) | 關鍵設計決策索引、待決議事項 | ⬜ 待產 |
| 8 | [acceptance.md](./8-acceptance.md) | 每個 FR 對應的驗收情境（Given-When-Then） | ⬜ 待產 |
| 9 | [rollout.md](./9-rollout.md) | 上線策略、監控、Runbook（選填） | ⬜ 待定 |

> 狀態值：`✅ vN`（已落盤）/ `⬜ 待產` / `⏭️ 跳過（原因）`。每份文件落盤時更新本欄 — 這是 session 中斷後恢復進度的依據。

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
| P-N | Page / Screen | 5-presentation-spec.md §5.7 |
| C-N | Component | 5-presentation-spec.md §5.6 |
| T-N | Page Section / Region | 5-presentation-spec.md §5.7 |
| D-NNNN | Decision (ADR) | decisions/ |
| AC-* | Acceptance Criteria | 8-acceptance.md |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v0.1 | YYYY-MM-DD | @{name} | Initial draft |
