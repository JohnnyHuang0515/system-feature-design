# Reference Guide: 5-presentation-spec.md

> 基於 `0-skill-mode.md` 的推導模式。配合 `templates/5-presentation-spec.template.md` 使用。

## 文件目的

描述 feature 對外呈現方式 — 給前端 / UX 工程師看的「說明書」。視覺細節歸 Design System,這份只寫「**用什麼 component、在什麼 page、走什麼 flow**」。

## 進入這份文件時的開場

```
進入第五份:呈現規格。

這份描述 feature 怎麼對外呈現給使用者 — 不一定是 UI,
也可能是 API only / Background Job / CLI / Notification。

我會先推導,你確認 / 修正。

預估 15-30 分鐘(GUI 較長,API only / Job 較短)。
```

## Claude 推導指南

### Presentation Type 推導

從 §1 + §2 推測類型:
- 使用者有「點按鈕、看畫面」的描述 → GUI
- 純 API 整合 → API Only
- 定時任務 / 系統行為 → Background Job
- 命令列工具 → CLI
- 通知 / email / push → Notification

**標 `[需確認]` 讓使用者確認**(可能有多種類型)

### 後續節推導(依 Presentation Type)

| Type | 5.2 | 5.3 | 5.4-5.6 |
|---|---|---|---|
| GUI | User Story | User Flow | 寫 |
| API Only | Consumer Story | Consumer Flow | 跳 |
| Background Job | Trigger Story | Execution Flow | 跳 |
| CLI | Command Story | Command Flow | 跳 |
| Notification | Recipient Story | Trigger Flow | 跳 |

### User Story 推導

從 §1.3 persona + §2.1 FR 推:
- 每個 persona 配對自己會用的 FR
- 用「作為 X,我想要 Y,以便 Z」格式
- 一個 persona 通常 1-3 個 story

### User Flow 推導

從 §4.1 SF 反推「使用者視角」:
- SF 寫「系統做什麼」,UF 寫「使用者看到 / 做什麼」
- 每個 SF 對應 1-N 個 UF
- 用 step by step 描述,不要寫系統內部細節

### Component / Page 推導(僅 GUI)

從 user flow 推:
- 每個 step 涉及的 UI 元素 → component(C-N)
- 每個 step 發生在哪個畫面 → page(P-N)
- 每個 page 的版面結構 → 區塊(T-N)

### 回填 §4

§5.3 寫完 UF 後,**主動回頭把 §4 各 SF 的 "Related UF" 欄位補上對應 UF-N**。

## 必要決策點(要問使用者的)

### 必補問題

1. **Presentation Type 確認**:推測類型後讓使用者確認
2. **Component 視覺細節**:若使用者有特殊視覺要求(例:節點卡片必須是 160x140),補問

### 不該問的

- ❌ 「User stories 寫什麼?」(從 persona + FR 推)
- ❌ 「有哪些 component?」(從 user flow 推)
- ❌ 「Page 結構是?」(從 user flow 推)

## Open Question 候選

- Presentation Type 不確定(多種類型混合)
- Component 拆法多種合理(一個大的 vs 多個小的)
- Page 配置多種合理(獨立頁 vs Modal vs 抽屜)

## 展示給使用者的格式

### 步驟 1:確認 Presentation Type

先快速問:

```
我從前面文件推測這個 feature 主要透過 GUI 呈現給使用者。對嗎?
還是有其他形式(例如後台 cron job)我漏了?
```

### 步驟 2:摘要

```
我推導出:

- Presentation type:{類型}
- User stories:{N 個} (覆蓋 {M} 個 persona)
- User flows:UF-1 ~ UF-{N}
- Components(若 GUI):C-1 ~ C-{N}
- Pages(若 GUI):P-1 ~ P-{N}

需要你拍板:[N 個]
```

### 步驟 3:逐節展開

對 GUI 類:
- 先確認 user stories(快)
- 再 user flows(中等)
- 最後 components + pages(慢,需要視覺確認)

### 步驟 4:問必要決策點

```
有幾件事需要你拍板:

1. UI 元件「節點卡片」我設計成 160x140 px,跟你 PRD 一致。OK 嗎?
2. 匯入預覽頁我設計成獨立頁(P-5),不是 Modal。可以嗎?
   (考量:預覽內容多,Modal 會擠;但獨立頁多一次跳轉)
3. 「啟用前確認」我設計成軟提示 Modal,不阻擋啟用。對嗎?
```

## 容易卡住的點

### 使用者沒寫過 UI spec

明確說:「我們不寫實作層(props、event handler 等),只寫:這個 component 角色是什麼、有哪些狀態、用在哪些 page。視覺細節歸 Design System。」

### 使用者想直接給 Figma 連結

接受。Reference 寫:「視覺以 Figma 為準([連結]),本 spec 只描述結構 + 互動」。

### 使用者描述 UI 卡在抽象

主動 propose:「我幫你列幾個可能的 component:[列舉]。看哪些符合你想的,哪些不在範圍。」

## 反思檢查(進 §6 前)

- [ ] Presentation type 已確認
- [ ] 每個 user story 對應到至少 1 個 persona + FR
- [ ] 每個 user flow 對應到 SF(GUI 類)
- [ ] §4 各 SF 的 "Related UF" 欄位已回填
- [ ] 每個 page 用到的 component 都在 §5.5 定義(GUI 類)
- [ ] 每個 component 至少出現在 1 個 page(無孤兒)(GUI 類)

## 文件結束時的 summary

```
§5 presentation-spec 完成!

- Presentation type:{類型}
- User stories:{N 個}
- User flows:UF-1 ~ UF-{N}
- Components:C-1 ~ C-{N}(若 GUI)
- Pages:P-1 ~ P-{N}(若 GUI)
- §4 SF 的 "Related UF" 已回填

接下來進入 §6 interfaces,我會推導對外 API、events、整合點。要進嗎?
```
