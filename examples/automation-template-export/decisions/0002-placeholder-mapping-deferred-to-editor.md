# D-0002: Placeholder 對應統一在編輯器，預覽頁不做 mapping

- **Status**: Accepted
- **Date**: 2026-05-14
- **Affects**: §4.3 (EC-2), §5.3 (UF-1, UF-5), §5.7 (P-5)
- **Supersedes**: —
- **Superseded by**: —

## Context

匯出時 assignees 一律轉為 placeholder，不帶具體 user_id（BR-3）。匯入後，使用者終究要把 placeholder 對應到目標工作區的具體成員，否則相關節點觸發時無法派發 task。

需要決定 mapping 動作發生在哪裡：匯入預覽頁 (P-5)，還是匯入後的流程編輯器 (P-2)。

## Decision

預覽頁只**列出**待對應項目（C-6 的「待對應項目區塊」），不提供 mapping UI。Placeholder 對應統一在流程編輯器中完成（沿用既有節點執行人指派 UI）。

啟用模板前若仍有未對應的 placeholder，跳出軟提示 Modal（EC-2, C-8, UF-5），但不阻擋啟用。

## Rationale

- 預覽頁的職責是「確認這是不是我要的模板」，不是「設定模板」；混入 mapping 會拉長匯入流程
- 編輯器已有完整的執行人指派 UI，預覽頁再做一套是重複開發
- 使用者在預覽階段尚未決定要不要匯入，先強迫 mapping 是浪費的 friction
- 軟提示機制（EC-2）已涵蓋「忘記指派就啟用」的風險

## Alternatives Considered

### A1: 預覽頁內建 mapping 精靈

**Pros**:
- 匯入完成即可直接啟用，一步到位

**Cons**:
- 預覽頁複雜度大增（要載入工作區成員清單、處理部分對應狀態）
- 與編輯器的指派 UI 重複開發
- 使用者尚未確認要匯入就得先花時間 mapping

**Why rejected**: §1.5.1 已將「匯入時自動 mapping 精靈」列為未來方向；POC 不需要

### A2: 匯入時強制完成 mapping 才能寫入

**Pros**:
- 進系統的模板都「可直接啟用」

**Cons**:
- 阻擋「先匯入再慢慢設定」的合理流程
- 目標工作區可能尚無對應角色的成員，會把使用者卡死在匯入階段

**Why rejected**: 與 BR-7「匯入即 Draft」的設計哲學矛盾；Draft 狀態本來就允許不完整

## Consequences

**Positive**:
- 預覽頁 (P-5) 保持唯讀、簡單（C-6 只展示不互動）
- 重用編輯器既有指派 UI，前端工作量小
- 匯入流程短，使用者保有「先匯入再設定」的彈性

**Negative**:
- 使用者可能忘記指派就啟用（以 EC-2 軟提示緩解，但不阻擋）
- 匯入後多一個「到編輯器補指派」的步驟，動線較長
