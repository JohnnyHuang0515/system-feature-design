# 8. Acceptance Criteria

> 本文件定義「功能完成」的判定標準。
> 所有 AC 使用 **Given-When-Then (BDD)** 格式。

## 8.1 AC for Functional Requirements

> 對應 §2.1 的每條 FR。
>
> **AC 編號規則**：AC-{FR}.{seq}，例：AC-1.1 對應 FR-1 的第 1 個 AC。
>
> **最低覆蓋**：
> - 寫入類 FR（POST/PUT/DELETE）：至少 1 happy path + 1 failure path
> - 純查詢類 FR：至少 1 happy path
> - 涉及 authorization 的 FR：必須額外有「未授權」AC

### FR-1: {FR 描述}

#### AC-1.1: {AC 簡述}

**Given** {前置狀態}
**When** {觸發動作}
**Then**
- {可驗證結果 1}
- {可驗證結果 2}

#### AC-1.2: {AC 簡述}

**Given** ...
**When** ...
**Then**
- ...

---

### FR-2: {FR 描述}

...

## 8.2 AC for State Transitions

> 對應 §3.3 的 state machine。
> **每條轉換寫合法觸發 + 違規嘗試兩種 AC**。

### {Entity} State Transitions

#### AC-S.1: {合法轉換情境}

**Given** {Entity 處於 {State A}}
**When** {觸發動作}
**Then**
- {Entity.status = {State B}}
- {Side effects}

#### AC-S.2: {違規嘗試情境}

**Given** ...
**When** ...
**Then**
- 回傳 {error}
- {Entity.status 保持不變}
- 不觸發任何 side effect

#### AC-S.99: 所有未列出的狀態轉換皆應被拒絕

**Given** Entity 處於任何狀態
**When** 嘗試執行該狀態不允許的轉換（參照 §3.3 state machine）
**Then**
- 回傳 INVALID_STATE_TRANSITION
- 狀態不改變
- 不觸發 side effect

## 8.3 AC for Business Rules

> 對應 §3.4 的每條 BR。
> 若 BR 已透過 state machine guard 實現，可 reference §8.2 的對應 AC。

### BR-1: {BR 描述}

#### AC-BR.1

**Given** ...
**When** ...
**Then**
- ...

---

### BR-2: {BR 描述}

（參見 AC-S.{N}）

註：本 AC 由 state machine guard 實現，測試情境已在 §8.2 涵蓋。

## 8.4 AC for Error & Edge Cases

> 對應 §4.2 (EF) 跟 §4.3 (EC)。

### EF-1: {錯誤情境}

#### AC-EF.1

**Given** {觸發錯誤的條件}
**When** ...
**Then**
- 回傳 {error code}
- {副作用：no state change, no event, etc}

---

### EC-1: {邊界情境}

#### AC-EC.1

**Given** ...
**When** ...
**Then**
- {特殊處理結果}

## 8.5 AC for Non-Functional Requirements

> 對應 §2.2 的每條 NFR。
> 不同於 functional AC，NFR AC 寫**怎麼測 + 達標標準**。
>
> **測試環境注意**：明確標註以下三類：
> 1. **Verifiable pre-release**：可在 staging 完全驗證
> 2. **Partial verification (simulated)**：僅能透過模擬部分驗證
> 3. **Production-monitoring only**：必須上 prod 後監控驗證

### NFR-1: {NFR 描述}

#### AC-NFR.1

**Verification level**: Verifiable pre-release | Partial | Production-monitoring only

**Test method**: {Load test / Monitoring / Chaos test / Code review}

**Setup**: {測試環境設定}

**Pass criteria**:
- {量化標準 1}
- {量化標準 2}

**Tool**: {工具}

**Notes**: {若是 partial / prod-only，說明為什麼以及 prod 驗證計畫}

## 8.6 Test Coverage Matrix

> 選填。中大型 feature（FR + NFR > 10 條）強烈建議做。
> **Source of truth 是 8.1-8.5 各節**，本節為匯總視圖。

| Requirement | AC Coverage |
|-------------|-------------|
| FR-1 | AC-1.1, AC-1.2 |
| FR-2 | AC-2.1, AC-2.2 |
| BR-1 | AC-BR.1 |
| BR-2 | (covered by AC-S.2) |
| State transitions | AC-S.1 ~ AC-S.99 |
| EF-1 ~ EF-N | AC-EF.1 ~ AC-EF.N |
| EC-1 ~ EC-N | AC-EC.1 ~ AC-EC.N |
| NFR-1 ~ NFR-N | AC-NFR.1 ~ AC-NFR.N |
