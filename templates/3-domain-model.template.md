# 3. Domain Model

> 本文件定義 feature 內部的領域模型（概念層）。
> **這不是 DB schema** — 寫 logical types，DB 細節留給後續 schema design。

## 3.1 Bounded Contexts / Modules

> 把系統切成幾個有清楚邊界的責任區塊。
> 不熟悉 bounded context 概念？把它想成「子模組」即可。
> 超小 feature（單一 module）可寫一行帶過。

- **{Context 名稱}**：{核心職責}。包含 {entities}。{與其他 context 的關係}
- **{Context 名稱}**：...

## 3.2 Entities

> 系統的核心資料物件。寫 logical type（UUID, Timestamp, Decimal），不寫 PostgreSQL 特有 type。

### {Entity 名稱}

{一句描述}

**Context**: {3.1 哪個 context}

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| id | UUID | Yes | 主鍵 | 系統生成 |
| {field} | {Type} | Yes/No | {說明} | {約束} |

**Relationships**:
- {關係描述，例：1 Order has many OrderItems}

---

### {Entity 名稱 2}

...

## 3.3 State Machines

> 對有狀態流轉的 entity，定義狀態跟轉換規則。
> 任何有 "status" 欄位的 entity 都該有 state machine。

### {Entity} State Transitions

**狀態圖**：

```mermaid
stateDiagram-v2
    [*] --> {InitialState}
    {InitialState} --> {NextState}: {trigger}
    {NextState} --> {EndState}: {trigger}
    {EndState} --> [*]
```

**轉換規則**：

| From | To | Trigger | Guard | Side Effects |
|------|----|---------|---------|-------------|
| {State A} | {State B} | {動作 / 事件} | {前置條件} | {副作用} |
| ... | ... | ... | ... | ... |

## 3.4 Business Rules / Invariants

> 必須永遠成立的規則 — 違反就代表系統 bug。
> 集中管理所有 BR，方便交叉檢查與 acceptance criteria 引用。

| ID | Rule | Scope | Enforcement |
|----|------|-------|-------------|
| BR-1 | {規則描述} | {適用範圍} | {DB constraint / Application logic / State machine guard} |
| BR-2 | ... | ... | ... |

## 3.5 Domain Events

> 選填。純 CRUD 的小 feature 可省。
> 有跨 context 互動或未來預期擴充通知 / 整合的 feature 必填。
>
> **本節列出 context 內所有有意義的事件**（含對內、對外）。
> 對外發布的事件契約細節另見 6.4.1。

| Event | Triggered When | Payload | Consumers |
|-------|----------------|---------|-----------|
| {EventName} | {何時發生，對應 state machine 或某動作} | {payload 關鍵欄位} | {誰處理} |
