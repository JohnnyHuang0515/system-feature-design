# D-0006: 系統內建模板透過 seed 資料夾載入，POC 不做後台

- **Status**: Accepted
- **Date**: 2026-05-14
- **Affects**: §4.1 (SF-4), §5.3 (UF-6), §9.2
- **Supersedes**: —
- **Superseded by**: —

## Context

系統需要提供官方內建模板給各工作區套用（FR-8），由 RD / 系統管理員維護（§1.3）。POC 階段需決定 RD 把這些模板放進系統的機制：做後台管理介面，還是更輕量的做法。

官方範本的特性：數量少、變動頻率低、由 RD 維護（非一般使用者操作）。

## Decision

RD 將 .json 檔案放入 `/seeds/automation-templates/` 資料夾，系統啟動時掃描、逐檔驗證、載入為系統內建模板（SF-4，標記 system flag）。

- 驗證失敗的檔案 skip + log + 發出 SeedTemplateLoadFailed 事件，不阻擋系統啟動（NFR-7）
- 相同檔名 + 內容 hash 去重，重啟不重複載入（§4.4）
- POC 不做後台管理介面（§1.5 out of scope）

## Rationale

- 官方範本變動頻率低，後台介面的開發成本與使用頻率不成比例
- Seed 檔案與匯出檔案是同一個 schema，可直接拿匯出結果當 seed，零轉換成本
- 共用 Validation Service（與 SF-1 同一條驗證路徑），壞檔案進不了系統
- 檔案進版控，官方範本的變更歷史天然可追溯

## Alternatives Considered

### A1: 後台模板管理介面

**Pros**:
- RD 不需要碰程式碼 / 部署流程
- 可即時上下架，不用重啟

**Cons**:
- POC 開發成本高（完整 CRUD UI + 權限）
- 使用頻率極低（官方範本不常變動）

**Why rejected**: §1.5.1 已列為未來方向；POC 階段 RD 手動操作可接受

### A2: 直接寫 DB seed script

**Pros**:
- 不需要掃描資料夾的 loader 機制

**Cons**:
- 繞過 Validation Service，不合法內容會直接污染資料
- 與匯入路徑邏輯分叉，schema 演進時要改兩處

**Why rejected**: 違反「所有寫入路徑共用同一驗證」的設計原則（SF-1 / SF-3 / SF-4 一致）

## Consequences

**Positive**:
- 重用匯入路徑與 Validation Service，幾乎零額外領域邏輯
- RD 操作簡單：放檔案、重啟、生效；移除檔案即可下架（§9.2 Rollback）
- 失敗隔離：單檔失敗不影響其他檔案與系統啟動（NFR-7, AC-8.2）

**Negative**:
- 更新模板需要重啟系統，無法即時生效
- 無版本管理、無熱度排序（§1.5.1 列為未來調整）
- RD 需要學習 seed 資料夾的操作慣例（檔名、覆蓋規則）
