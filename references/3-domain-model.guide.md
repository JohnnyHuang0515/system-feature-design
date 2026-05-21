# Reference Guide: 3-domain-model.md

> 基於 `0-skill-mode.md` 的推導模式。配合 `templates/3-domain-model.template.md` 使用。

## 文件目的

定義系統內部的核心領域模型 — entity、state、business rule。**這不是 DB schema**,是概念層。

## 進入這份文件時的開場

```
進入第三份:領域模型。

這份描述系統「內部由什麼組成」 — entity、欄位、狀態流轉、業務規則。
這是後端工程師最關注的文件。

重要原則:這不是資料庫 schema,我們寫概念,DB 細節留給實作階段。

我會根據前面文件先推導,你確認 / 修正。

預估 10-15 分鐘。
```

## Claude 推導指南

### 從前面文件推導

| 推導對象 | 推導來源 |
|---|---|
| §3.1 Bounded Contexts | 從 §1.5 in scope 推「責任區塊」(小 feature 寫一行帶過) |
| §3.2 Entities | 從 §2.1 FR 中的名詞動詞反推(例:「使用者建立訂單」→ Order entity) |
| §3.2 Entity 欄位 | 從 FR 推必要欄位 + 推測標準欄位(id, created_at, updated_at) |
| §3.3 State Machines | 若 entity 有 status 概念,推狀態流轉(例:訂單 Draft → Submitted → Paid) |
| §3.4 Business Rules | 從 §1.5 約束 + §2.2 NFR + FR 隱含的不變規則推 |
| §3.5 Domain Events | 從 state transition + 跨 context 互動推 |

### Entity 推導範例

從 FR-2「Allow users to import an automation template」推導:
- 名詞:template → Template entity
- 隱含:template 包含什麼 → Node, Connection entities
- 必要欄位:id, name, status, workspace_id, created_at...

### Bounded Context 推導

小 feature 通常 1 個 context 就夠。多 entity 時可切:
- 「管理 X」context vs 「處理 X 的 import/export」context vs 「驗證 X」context

不確定怎麼切時用單一 context,不要過度設計。

### State Machine 推導

凡是有 status 欄位的 entity 都推一個 state machine:
- 初始狀態 + 主要狀態 + 終止狀態
- 每個 transition 的 trigger / guard / side effect

### Business Rule 推導

從以下來源推:
- §1.5.1 POC 表格的「絕對不能違反」事項
- §2.2 NFR 的 security / compliance 隱含規則
- FR 中的 constraint(例:「至少 1 個 Node 才能 Activate」)
- 標準 domain 常識(例:「金額不可為負」)

## 必要決策點(要問使用者的)

### 必補問題

通常推導後給使用者確認即可。但有兩種情境要問:

1. **State machine 的選擇分支**:多種合理流轉時,標 `[待拍板]`
2. **Business Rule 的嚴格度**:某條規則寬鬆 vs 嚴格,標 `[待拍板]`

### 不該問的

- ❌ 「有哪些 entity?」(從 FR 推)
- ❌ 「state machine 怎麼設計?」(推完讓使用者確認)
- ❌ 「business rule 有哪些?」(推完讓使用者確認)

## Open Question 候選

- Bounded context 切法多種合理(切細 vs 合併)
- State 轉換多種設計(直接 A→B,還是 A→中間→B)
- Business rule 嚴格度(自連禁 vs 允許自連)
- Event 是否要發出(純內部 vs 對外)

## 展示給使用者的格式

### 步驟 1:摘要

```
我推導出領域模型如下:

- {N} 個 entity:{列名稱}
- {M} 個 state machine:{列哪些 entity 有}
- {K} 條 business rule
- {J} 個 domain event(若有)

需要你拍板:[N 個關鍵決策]
```

### 步驟 2:完整內容(分節展示)

依序展示 §3.1 ~ §3.5。Entity 多時可一次給 1-2 個讓使用者吸收。

### 步驟 3:問必要決策點

```
有幾件事需要你拍板:

1. Template 的 status 我設計成「草稿 → 啟用中 → 已封存」三個狀態,
   合理嗎?還是你心中有別的流程(例如需要審核狀態)?

2. 業務規則「Template 名稱在 workspace 內必須唯一」 — 大小寫敏感嗎?
   (「訂單流程」跟「訂單流程 」算同一個還是不同?)

3. 我推測會發出 TemplateImported / Exported / Activated 三個事件,
   有需要的事件我漏了嗎?
```

## 容易卡住的點

### 使用者不確定 entity 怎麼切

給 entity 拆分原則:「會獨立被建立 / 刪除 / 查詢的東西通常是獨立 entity」。

例:「使用者匯入模板」中,Template 跟 Node 是分開的(Template 可獨立查、Node 屬於 Template 不獨立)。

### 使用者不會畫 state machine

直接給 Mermaid diagram 草稿,讓使用者點頭或改。

### 使用者覺得 Business Rule 寫太多

問:「哪些是『絕對不能違反』、哪些是『一般情況才這樣』?後者其實是業務邏輯不是 invariant」幫使用者區分。

## 反思檢查(進 §4 前)

- [ ] 每條 §2.1 FR 都能用這些 entity 實現
- [ ] 每個有 status 的 entity 都有 state machine
- [ ] 每條 BR 都有明確 enforcement 機制
- [ ] Logical type(UUID, Timestamp...),不是 DB type(BIGSERIAL...)
- [ ] 標記使用得當

## 文件結束時的 summary

```
§3 domain-model 完成!

- Contexts:{N 個}
- Entities:{列名稱}
- State machines:{列哪些 entity}
- Business rules:BR-1 ~ BR-{N}
- Domain events:{N 個 / 跳過}

接下來進入 §4 flows,我會推導系統內部執行流程、錯誤處理、邊界情境。要進嗎?
```
