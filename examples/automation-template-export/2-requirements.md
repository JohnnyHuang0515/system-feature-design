# 2. Requirements

## 2.1 Functional Requirements

| ID | Description | Persona | Priority | Related |
|----|-------------|---------|----------|---------|
| FR-1 | Allow users to export the current automation template as a JSON file | PM | Must | 1.3, 1.5 |
| FR-2 | Allow users to import an automation template from a JSON file upload | PM | Must | 1.3 |
| FR-3 | Validate imported JSON against schema and structure rules, show errors when invalid | PM | Must | FR-2 |
| FR-4 | Show a preview page before final import, including template info, flow thumbnail, and warnings | PM | Must | FR-2 |
| FR-5 | Detect duplicate template name on import, offer overwrite / create new / cancel | PM | Must | FR-2 |
| FR-6 | Persist imported templates as Draft, requiring user action to activate | PM | Must | FR-2 |
| FR-7 | Allow AI-generated template content to write to database via the same import path | AI user | Must | FR-2, FR-3 |
| FR-8 | Load system seed templates from a designated folder at system startup | RD / Admin | Must | 1.5 |
| FR-9 | Detect and warn about structural anomalies (orphan nodes, duplicate connections) without blocking import | PM | Should | FR-3 |

## 2.2 Non-Functional Requirements

### 2.2.1 Performance

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-1 | Import API latency for typical files | p99 < 500ms | 不含檔案解析時間，5 MB 以下 |
| NFR-2 | Max file size for import | 5 MB | POC 階段限制 |

### 2.2.2 Security & Authorization

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-3 | Only authenticated workspace members can import / export | Required | 沿用既有 auth 機制 |
| NFR-4 | Exported files MUST NOT contain real user_id, workspace_id, or DB internal IDs | Always | placeholder 機制 |
| NFR-5 | Exported files are plaintext JSON (no encryption / signing) | POC | 未來重新評估 |

### 2.2.3 Reliability

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-6 | Import write must be atomic — failure leaves no partial data | 100% | DB transaction |
| NFR-7 | Seed template loading failure must not block system startup | Required | 失敗檔案 skip + log |

### 2.2.4 Observability

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-8 | Log all import attempts (success / fail) with reason | Required | 對應 §9.3.2 |
| NFR-9 | Track seed template loading status per file at startup | Required | RD 排查用 |

## 2.3 Out of Scope Requirements

§1.5 的 Out of scope 已涵蓋。本節無額外項目。

## 2.4 Priority Summary

> FR + NFR = 18 條，邊界值，列出方便決策。

| Priority | Items |
|----------|-------|
| **Must (P0)** | FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-7, FR-8, NFR-1, NFR-3, NFR-4, NFR-6, NFR-7, NFR-8 |
| **Should (P1)** | FR-9, NFR-2, NFR-5, NFR-9 |
| **Could (P2)** | — |
| **Won't (POC)** | （見 §1.5 Out of scope） |
