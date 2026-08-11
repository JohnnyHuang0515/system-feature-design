# 2. Requirements

## 2.1 Functional Requirements

> 用 "system shall" 風格描述系統能力。每條給 ID（FR-N）方便後面引用。

| ID | Description | Persona | Priority | Related |
|----|-------------|---------|----------|---------|
| FR-1 | {Allow X to do Y} | {Persona} | Must / Should / Could | {1.3, FR-X} |
| FR-2 | ... | ... | ... | ... |
| FR-3 | ... | ... | ... | ... |

## 2.2 Non-Functional Requirements

> **這是 gate 不是 menu。** 每個小節下方寫著它的觸發條件 —— 條件沒發生就整節省略。
> 「為了完整性」加進來的分類，會生出一個沒人量的目標值和一條 §8 沒人寫的 AC。

### 2.2.1 Performance

> 選填。觸發條件：對外服務，或使用者講了一個效能數字。

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-1 | {延遲 / 吞吐量 / 容量} | {目標值} | {備註} |

### 2.2.2 Security & Authorization

> 唯一無條件的分類 —— 至少要有認證與授權。

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-X | {認證 / 授權 / 資料保護} | ... | ... |

### 2.2.3 Reliability

> 選填。觸發條件：對外服務，或業務關鍵。

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-X | {可用性 / 容錯 / 一致性} | ... | ... |

### 2.2.4 Observability

> 選填。觸發條件：對外服務，或有人要 on call。

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-X | {Logging / Metrics / Tracing / Alerting} | ... | ... |

### 2.2.5 Scalability

> 選填。觸發條件：預期會快速成長。

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-X | {預期成長 / 擴展點} | ... | ... |

### 2.2.6 Compliance & Audit

> 選填。觸發條件：處理金流、醫療紀錄，或受規範的個人資料。

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-X | {法規 / 審計需求} | ... | ... |

## 2.3 Out of Scope Requirements

> 選填。若 1.5 已寫得夠細可省。複雜 feature 建議寫。

- **{需求 1}**：{為什麼不做}
- **{需求 2}**：{為什麼不做}

## 2.4 Priority Summary

> 選填。FR + NFR 合計 > 10 條時建議做（與 guide 門檻一致）。
> **Source of truth 是 2.1 與 2.2 的 Priority 欄位**，本節為匯總視圖。

| Priority | Items |
|----------|-------|
| **Must (P0)** | FR-1, FR-2, NFR-1 |
| **Should (P1)** | FR-3, NFR-2 |
| **Could (P2)** | FR-4 |
| **Won't (this release)** | — |
