# 5. Presentation Specification

> 本文件描述 feature 對外的呈現方式 — 使用者視角的所有資訊。
>
> 內容類型依 5.1 Presentation Type 而定：
> - GUI → 完整 6 節
> - API Only / Background Job / CLI / Notification → 只寫 5.1-5.3

## 5.1 Presentation Type

選擇本 feature 對外的呈現方式（可選多個，標明主要類型）：

- [ ] **GUI** — 圖形使用者介面（網頁、app）
- [ ] **API Only** — 純對外 API，無 UI
- [ ] **Background Job** — 定時任務或事件驅動，使用者不直接觸發
- [ ] **CLI** — 命令列工具
- [ ] **Notification** — 通知系統（email、push、in-app message）
- [ ] 其他：______

**Selected type**: {勾選}

**Description**: {一段描述，說明使用者如何接觸這個 feature}

## 5.2 User Stories / Consumer Stories

> 標準格式：**作為 [persona]，我想要 [做什麼]，以便 [獲得什麼價值]**
> 按 persona 分組列出。

**作為 {Persona 1}**：
- 我想要 {做什麼}，以便 {價值}
- 我想要 {做什麼}，以便 {價值}

**作為 {Persona 2}**：
- 我想要 {做什麼}，以便 {價值}

## 5.3 User Flows / Execution Flows

> 視 Presentation Type 而定：
> - **GUI**: User Flow（使用者操作流程）
> - **API Only**: Consumer Flow（API 呼叫者的使用流程）
> - **Background Job**: Execution Flow（觸發 → 執行 → 結果）
> - **CLI**: Command Flow
> - **Notification**: Trigger Flow（事件 → 通知）

### UF-1: {流程名稱}

**Persona / Consumer**: {誰}
**Related FR**: FR-{N}
**Preconditions**: {前置條件}

**Steps**:
1. {步驟（使用者視角，不寫系統內部細節）}
2. ...

**Expected outcome**: {結束時的狀態}

---

### UF-2: ...

---

> **以下 5.4 - 5.6 僅在 Presentation Type 為 GUI 時撰寫。**

## 5.4 Design System & Visual Notes

> 重點：本 feature 的**新增 / 特殊**部分，不重複既有 Design System。

**Existing tokens / components used**: {沿用既有 Design System，或寫「本專案無既有 Design System」}

**New tokens introduced by this feature**:
- `{token-name}`: {用途}

**Component-specific visual notes**:
- {特殊的視覺規範，例：本 component 用特定狀態指示色}

## 5.5 Component Inventory

> 列出 feature 用到的 UI component。
> 層次 3：列 component + 角色 + 視覺尺寸 + 狀態。不寫 props / event handler。

### C-1: {Component 名稱}

**Used in**: P-{N}
**Role**: {一句話描述這個 component 的角色}

**Sub-content** / **Internal structure**:
- {子區塊或內容描述}

**States**: {idle / hover / selected / disabled / loading / error / ...}

**Size**: {尺寸，如果固定}

---

### C-2: ...

## 5.6 Page / Screen 結構

> 每個 page 描述版面結構、區塊責任。

### P-1: {Page 名稱}

**URL**: {URL pattern，如果適用}
**Entry from**: UF-{N}, UF-{N} (從哪些 user flow 進入)

**Layout**:

```
┌─────────────────────────────────┐
│  {區塊 T-1}                     │
├──────────────────┬──────────────┤
│                  │              │
│  {區塊 T-2}      │  {區塊 T-3}  │
│                  │              │
└──────────────────┴──────────────┘
```

**區塊責任**:
- **T-1 {區塊名稱}**: 使用 C-{N}。負責 {責任描述}
- **T-2 {區塊名稱}**: 使用 C-{N}。負責 {責任描述}
- **T-3 {區塊名稱}**: 使用 C-{N}。負責 {責任描述}

---

### P-2: ...
