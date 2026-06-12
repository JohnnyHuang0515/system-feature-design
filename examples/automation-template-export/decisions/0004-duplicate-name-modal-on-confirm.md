# D-0004: 同名模板處理用 Modal 三選一（覆蓋 / 建新 / 取消）

- **Status**: Accepted
- **Date**: 2026-05-14
- **Affects**: §4.3 (EC-1), §5.3 (UF-1 step 8), §5.6 (C-7), §6.2 (POST /import/confirm)
- **Supersedes**: —
- **Superseded by**: —

## Context

Template name 在 workspace 內必須唯一（BR-1），但匯入檔案的 metadata.name 完全可能與既有模板撞名（例：同事間互傳同一份模板）。需要決定：

1. 撞名時的處理策略 — 拒絕？自動改名？覆蓋？問使用者？
2. 在哪個時點處理 — 上傳當下，還是確認匯入時？

## Decision

在預覽頁點「確認匯入」時偵測同名，跳出選擇 Modal（C-7）三選一：

- **覆蓋既有**：替換目標模板內容，儲存為該模板的新版本（v1 → v2），原版本保留
- **建立新的**：建立全新模板，名稱自動加 suffix（例：「訂單流程 (2)」）
- **取消**：不寫入

API 層以 `duplicate_name_action` 欄位承接（§6.2 /confirm）；偵測到同名但未提供 action 回 409 DUPLICATE_NAME_UNRESOLVED。

## Rationale

- 「覆蓋」與「建新」都是真實需求（更新既有模板 vs 並存比較），系統不應替使用者決定
- 放在「確認匯入」時點：使用者已看完預覽（P-5），有足夠資訊做決定
- 覆蓋實作為「新版本」而非「刪除重建」，原版本保留，誤操作可救
- 覆蓋後新版本預設 Draft（BR-7），不會立刻影響執行中的 task instance

## Alternatives Considered

### A1: 直接拒絕，要求使用者修改檔案內的名稱

**Pros**:
- 實作最簡單，BR-1 直接擋下

**Cons**:
- 使用者得手動編輯 JSON 改名再重新上傳，friction 極大
- 「我就是要更新既有模板」的場景完全做不到

**Why rejected**: 把系統該處理的問題丟回給使用者

### A2: 自動加 suffix 建新模板，不詢問

**Pros**:
- 無 Modal，流程不中斷

**Cons**:
- 「更新既有模板」場景做不到
- 重複匯入會默默堆出「訂單流程 (2) (3) (4)」垃圾模板

**Why rejected**: 替使用者做了錯誤假設；清理成本轉嫁給使用者

### A3: 上傳檔案當下立刻詢問

**Pros**:
- 早期失敗，不用走完預覽流程

**Cons**:
- 使用者還沒看到預覽內容，無法判斷「該覆蓋還是建新」
- 預覽後取消的話，詢問是白問的

**Why rejected**: 決策時點早於資訊到位的時點

## Consequences

**Positive**:
- 覆蓋 = 新版本，版本歷史不丟，安全可回退
- 使用者保有完整決策權，三種真實意圖都被支援
- 與既有「切換啟用版本」規則銜接（執行中 task 跑舊版完成）

**Negative**:
- 多一個 Modal 元件（C-7）與 API 分支（409 DUPLICATE_NAME_UNRESOLVED）
- QA 案例增加（AC-5.1 ~ AC-5.4 共 4 條）
- 「建立新的」suffix 命名規則未來與 BR-1 大小寫敏感規則交互時需注意（例：suffix 後再撞名）
