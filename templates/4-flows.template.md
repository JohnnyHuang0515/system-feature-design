# 4. System Flows

> 本文件描述**系統內部的執行流程**。
> 使用者視角的流程（User Flow）放在 5-presentation-spec.md §5.3。

## 4.1 System Flows

> 對每個重要場景描述系統內部怎麼執行。涉及多 component 互動時用 sequence diagram。

### SF-1: {流程名稱}

**Related User Flows**: UF-{N}（reference 5-presentation-spec）
**Related FR**: FR-{N}
**Components involved**: {涉及的 service / context}

**Sequence**:

```mermaid
sequenceDiagram
    participant A as Component A
    participant B as Component B
    A->>B: {動作}
    B-->>A: {回應}
    ...
```

**Key steps**:
1. {步驟，可包含「為什麼這時做這件事」的說明}
2. ...

---

### SF-2: ...

## 4.2 Error & Exception Flows

> 對應 4.1 的每個 SF，列出可能的失敗情境跟處理方式。

### EF-1: {失敗情境名稱}

**Triggers in**: SF-{N} 的哪個步驟
**Detection**: {怎麼知道失敗了}

**System behavior**:
1. {系統的處理動作}
2. {回傳什麼錯誤 / status}
3. {副作用：rollback、release lock、發 alert 等}

**Recovery**: {使用者或系統如何恢復}

---

### EF-2: ...

## 4.3 Edge Cases

> 不是「錯誤」但需要特別處理的邊界情境。
> **不確定是 error 還是 edge case 的，預設放這裡**。

### EC-1: {邊界情境名稱}

**Scenario**: {何時發生}
**Handling**: {怎麼處理}

### EC-2: ...

## 4.4 Concurrency & Ordering

> 回答以下問題：
>
> 1. **共享資源**：本 feature 是否有多個 user / process 可能同時操作的資源？
>    （例：庫存、座位、額度、配額、唯一名稱）
>
> 2. **事件順序**：本 feature 的事件處理順序是否會影響結果？
>    （例：付款必須在出貨之前；通知必須在狀態更新之後）
>
> 3. **重複觸發**：本 feature 的呼叫者是否可能重試或重複觸發？
>    （例：webhook 重投、使用者點擊兩次、整合方 retry）
>
> 如果以上皆為「否」，本節寫一行「本 feature 無共享資源、無順序依賴、無重複觸發風險」即可。

- **{議題 1}**: {處理策略}
- **{議題 2}**: {處理策略}
