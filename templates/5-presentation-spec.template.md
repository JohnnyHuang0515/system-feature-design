# 5. Presentation Specification

> 本文件描述 feature 對外的呈現方式 — 使用者視角的所有資訊。
>
> 內容類型依 5.1 Presentation Type 而定：
> - GUI → 完整 9 節
> - API Only / Background Job / CLI / Notification → 只寫 5.1-5.3

## 5.1 Presentation Type

選擇本 feature 對外的呈現方式（可選多個，標明主要類型）：

> 類型指「使用者怎麼接觸 feature」，不是 feature 的領域。
> 例：站內通知中心有鈴鐺 + 面板 UI → 主類型是 GUI；Notification 指 email / push 等投遞通道本身。

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

> **以下 5.4 - 5.9 僅在 Presentation Type 為 GUI 時撰寫。**

## 5.4 User Journey（使用者旅程）

> 把 §5.3 的 UF-1 ~ UF-N 抽高一層：使用者為了達成目標，從頭到尾經過哪些**階段**、
> 每階段想完成什麼、可能在哪卡住。給 UX / 前端看「整體體驗」，不是逐步操作（那是 §5.3）。
> 一個 feature 通常 3-6 個階段。卡點欄對齊 §4 的 EF / EC。

**主要旅程：{persona} 完成 {目標}**

| 階段 | 使用者想完成 | 觸及點（UF / Page） | 可能卡點（EF / EC） | 體驗重點 |
|---|---|---|---|---|
| 1. {認知 / 進入} | {想做什麼} | UF-{N} / P-{N} | EF-{N}：{卡點} | {這階段最在意什麼} |
| 2. {操作} | {想做什麼} | UF-{N} / P-{N} | EC-{N}：{卡點} | {…} |
| 3. {完成 / 後續} | {想做什麼} | UF-{N} / P-{N} | — | {…} |

> 多 persona 時，每個主要 persona 各一條旅程。次要 / 一次性的可省略。

## 5.5 Design System & Visual Notes

> 重點：本 feature 的**新增 / 特殊**部分，不重複既有 Design System。

**既有 Design System 狀態**（先拍板，決定 §5.9 交接內容）:
- [ ] **已有** — 沿用，下方「Existing tokens」填參照來源（Figma / Storybook / 程式庫連結）
- [ ] **沒有** — 本專案尚無 Design System。這是**前端開工的前置條件**，需於實作前產出（見 §5.9）

**Existing tokens / components used**: {沿用既有 Design System 的來源，或寫「本專案無既有 Design System，見 §5.9」}

**New tokens introduced by this feature**:
- `{token-name}`: {用途}

**Component-specific visual notes**:
- {特殊的視覺規範，例：本 component 用特定狀態指示色}

## 5.6 Component Inventory

> 為 feature 用到的 UI component **命名**，讓 §6 / §7 / §8 有東西可以指涉。
> 寫：角色、必須承載什麼、有哪些行為狀態。
> 不寫：長什麼樣（尺寸、hover、色彩）、怎麼做（props / event handler）。

### C-1: {Component 名稱}

**Used in**: P-{N}
**Role**: {一句話描述這個 component 的角色}

**Must carry**:
- {它必須讓使用者看到或做到的事，一條一行}

**States**: {對行為有意義的狀態，例如 empty / loading / error / disabled / selected。
純視覺狀態（hover、focus ring 等）歸 Design System}

---

### C-2: ...

## 5.7 Page / Screen 結構

> 為 page 命名，寫清楚它的職責與各區塊負責什麼。
> 版面（誰左誰右、幾欄）是設計決定，不在這裡 —— 這裡只寫「不管怎麼排都要成立」的約束。

### P-1: {Page 名稱}

**Entry from**: UF-{N}, UF-{N} (從哪些 user flow 進入)
**Responsibility**: {這個 page 讓使用者完成什麼}

**區塊責任**:
- **T-1 {區塊名稱}**: 使用 C-{N}。負責 {責任描述}
- **T-2 {區塊名稱}**: 使用 C-{N}。負責 {責任描述}

**版面約束**（只寫有理由的；沒有就整段省略）:
- {例：T-1 與 T-2 必須同時可見 —— 改 T-1 會即時改變 T-2 的可選項}
- {例：T-3 在手機上可摺疊 —— 非主要決策資訊}

**Key states**: {空狀態 / 載入中 / 錯誤時這個 page 顯示什麼；與 §5.8 對齊}

---

### P-2: ...

## 5.8 Interaction Decisions（互動體驗決策）

> 前端體驗決策清單（見 reference guide）的拍板結果，給前端工程師與 AI agent 的快速索引。
> 每列一個維度；不適用的維度寫「N/A — 原因」，不留空。
> 影響資料模型或不可逆的決策升級為 ADR，Related ADR 欄填 D-NNNN；其餘留「—」。

| 維度 | 決定 | 理由（一句話） | Related ADR |
|---|---|---|---|
| 進入點與導覽 | {例：模板列表頁「建立」選單內新增入口} | {為什麼} | — |
| 容器形式 | {獨立頁 / Modal / Drawer} | {為什麼} | — |
| 操作模式 | {單頁表單 / 分步精靈 / inline 編輯} | {為什麼} | — |
| 空狀態與首次使用 | {第一次進來看到什麼} | {為什麼} | — |
| 錯誤與部分成功 | {失敗 / 部分成功時的呈現} | {為什麼} | — |
| 操作回饋與防呆 | {Toast / Banner / 確認 Modal / Undo} | {為什麼} | — |
| 資料量呈現 | {分頁 / 無限捲動 / 搜尋篩選 / 預設排序} | {為什麼} | — |
| 裝置與即時性 | {桌機 only / RWD；手動刷新 / 輪詢 / 即時} | {為什麼} | — |

## 5.9 Design Handoff（前端設計交接）

> 這份 spec **命名**前端的東西，並規定它們必須成立什麼（有哪些 page/component、怎麼互動、出錯怎麼辦）。
> 長什麼樣 —— 版面、hi-fi mockup、色彩、字級 —— **不在本 spec**，是下游產物。
> 本節是交接清單：說清楚前端開工前還缺什麼、從這份 spec 怎麼接出去，避免靜默開洞。

**Design System 來源**（對齊 §5.5 的拍板）:
- {已有 → 連結 / 名稱；或：尚無 → 需先產出，建議用 {工具 / skill}（如 ckm-design-system / ui-ux-pro-max / design-taste-frontend / Pencil MCP）}

**Mockup / 視覺稿**:
- 產出方式：{Figma 連結 / 用設計工具從本 spec 生成 / 實作階段定案}
- 餵給設計工具的輸入：§5.6 component（角色 + 必須承載什麼 + 狀態）、§5.7 page（職責 + 區塊責任 + 版面約束 + Key states）、§5.8 互動決策
- 視覺以 {來源} 為準；本 spec 與之衝突時，回頭同步 §5.6/§5.7

**前端開工前的前置清單**:
- [ ] Design System / tokens 就緒（或確認沿用既有）
- [ ] Hi-fi mockup 或視覺參照備妥（{Figma / 工具產出}）
- [ ] 響應式斷點確認（對齊 §5.8「裝置與即時性」）
- [ ] 文案 / microcopy 來源（錯誤訊息、空狀態、按鈕字 — 散見 §5.3 flows，需彙整）

> 凡標為「前置條件」而本 spec 不產的（最常見：尚無 Design System），於 §7 記一條 Open Question 或 ADR，補 Owner + Target Date，不要讓它浮著。
