# 2. Requirements

## 2.1 Functional Requirements

> 用 "system shall" 風格描述系統能力。每條給 ID（FR-N）方便後面引用。

| ID | Description | Persona | Priority | Related |
|----|-------------|---------|----------|---------|
| FR-1 | {Allow X to do Y} | {Persona} | Must / Should / Could | {1.3, FR-X} |
| FR-2 | ... | ... | ... | ... |
| FR-3 | ... | ... | ... | ... |

## 2.2 Non-Functional Requirements

> 按以下分類整理。**不是每個分類都需要填**，沒適用的省略整個小節。
>
> 建議的最低集合：
> - 任何 feature：Security & Authorization
> - 對外服務：加上 Performance、Reliability、Observability
> - 處理使用者資料：加上 Compliance & Audit
> - 預期成長快：加上 Scalability

### 2.2.1 Performance

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-1 | {延遲 / 吞吐量 / 容量} | {目標值} | {備註} |

### 2.2.2 Security & Authorization

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-X | {認證 / 授權 / 資料保護} | ... | ... |

### 2.2.3 Reliability

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-X | {可用性 / 容錯 / 一致性} | ... | ... |

### 2.2.4 Observability

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-X | {Logging / Metrics / Tracing / Alerting} | ... | ... |

### 2.2.5 Scalability

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-X | {預期成長 / 擴展點} | ... | ... |

### 2.2.6 Compliance & Audit

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-X | {法規 / 審計需求} | ... | ... |

## 2.3 Out of Scope Requirements

> 選填。若 1.5 已寫得夠細可省。複雜 feature 建議寫。

- **{需求 1}**：{為什麼不做}
- **{需求 2}**：{為什麼不做}

## 2.4 Priority Summary

> 選填。FR + NFR 合計 > 15 條時建議做。
> **Source of truth 是 2.1 與 2.2 的 Priority 欄位**，本節為匯總視圖。

| Priority | Items |
|----------|-------|
| **Must (P0)** | FR-1, FR-2, NFR-1 |
| **Should (P1)** | FR-3, NFR-2 |
| **Could (P2)** | FR-4 |
| **Won't (this release)** | — |
