# Reference Guide: 7-decisions.md + decisions/

> 基於 `0-skill-mode.md` 的推導模式。配合 `templates/7-decisions.template.md` + `templates/decisions/NNNN-template.md` 使用。

## 文件目的

記錄關鍵設計決策 — 為什麼選 A 不選 B、考慮過哪些替代方案、有哪些待決議事項。

ADR 拆檔:`7-decisions.md` 是索引,每個 decision 一個檔案在 `decisions/` 子目錄。

## 進入這份文件時的開場

```
進入第七份:設計決策。

這份用 ADR (Architecture Decision Record) 格式記錄關鍵決策。

我會:
1. 掃描前面文件,蒐集已經做過的關鍵決策
2. 把這些決策寫成 ADR(每個一份檔案)
3. 整理 Open Questions(待拍板事項)

你的工作主要是「確認 ADR 內容對」+「為 Open Questions 拍板」。

預估 10-20 分鐘。
```

## Claude 推導指南

### 掃描前面文件蒐集 ADR 候選

從以下位置掃描:

| 來源 | 通常產出 ADR 的位置 |
|---|---|
| §1.5.1 POC 表格 | **每一條都是「ADR 候選」,不是「自動 ADR」**。逐條套用 ADR 門檻判斷,夠重要才展開。展開後 propagate 回 §1.5.1 的 `Related ADR` 欄;不展開的留 `—` |
| §3.1 Bounded Contexts | 「為什麼這樣切?」 |
| §3.3 State Machine | 狀態流轉的關鍵設計選擇 |
| §4.1 SF | 跨服務互動方式(同步 vs 異步) |
| §6.2 API | 重要的 API 設計選擇(單階段 vs 兩階段) |
| §6.6 Versioning | versioning 策略 |
| 整份 spec 的 `[待拍板]` 標記 | 全部變成 Open Question 候選 |

### ADR 內容推導

對每個 ADR 候選,Claude 推導:

| 欄位 | 推導來源 |
|---|---|
| Title | 從決策本質一句話描述 |
| Context | 從前面文件推「為什麼需要這個決定」 |
| Decision | 已做的決定本身 |
| Rationale | 從前面文件推「為什麼這樣做」 |
| Alternatives | 主動推 2-3 個替代方案,各列 pros/cons |
| Consequences | 推 positive / negative 影響 |
| Affects | reference 到具體 §X.Y |

### ADR 門檻

判斷依據(任一條成立就寫):

1. 三個月後可能被質疑「為什麼當初這樣?」
2. 改變成本高(影響多個 section / 多個 service)
3. 有合理替代方案(不是「業界標準」)
4. 跨團隊影響

**不該寫**:code style、業界定論(用 HTTPS)、純技術選型偏好。

### Open Question 處理

整份 spec 中所有 `[待拍板]` 標記都集中到 §7.2,展開為 Status: Proposed 的 ADR 檔案。

## 必要決策點(要問使用者的)

### 必補問題

ADR 寫完後,**對每個 Open Question 都要問使用者拍板**:

```
有 {N} 個待拍板事項,我幫你整理選項,你決定:

D-{N}: {議題}
建議方向:{Claude 的傾向,但需你決定}
- (a) {選項 A} (Pros: ... Cons: ...)
- (b) {選項 B} (Pros: ... Cons: ...)
- (c) 先放著 → 列入 §7.2 待解
```

### 不該問的

- ❌ 「有哪些 decisions 要寫?」(掃描前面文件推)
- ❌ 「Alternative 是什麼?」(主動推)
- ❌ 「Rationale 是?」(從前面文件推)

## Open Question 候選

§7 階段不再產生新 Open Question — 這份的工作是「**收斂前面散落的 `[待拍板]`**」。

如果有,代表前面節有遺漏,先回頭補。

## 展示給使用者的格式

### 步驟 1:摘要

```
我從前面 6 份文件掃描出 {N} 個 ADR 候選:

Accepted({M} 個,已做的決定):
- D-0001: Task 欄位採內嵌儲存
- D-0002: 同名模板處理跳 Modal
- ...

Open Questions({K} 個,待拍板):
- D-{N+1}: Schema 升版機制
- D-{N+2}: 是否需要 rate limiting
- ...
```

### 步驟 2:逐個 Accepted ADR 確認

對每個 Accepted ADR,給「一段話總結」讓使用者快速確認:

```
D-0001: Task 欄位採內嵌儲存,預留外部引用欄位

簡述:POC 階段 task 欄位內嵌在模板中,但 schema 保留
     `task_template_ref` 欄位以便未來改用引用模式。

完整 ADR 已寫在 decisions/0001-task-fields-embedded-with-future-ref.md

OK 嗎?有要補的 alternative 或 consequence?
```

### 步驟 3:逐個 Open Question 拍板

```
D-0010: Schema 升版機制(待拍板)

背景:目前 schema_version = v0.1,未來可能升 v0.2、v0.3...
     需要決定怎麼處理舊版檔案的相容性。

選項:
(a) 永久向後相容:支援所有歷史版本,維護成本高
(b) 滾動 window:只支援前一版,deprecate 舊版
(c) 提供升版工具:讓使用者把舊檔案 migrate 為新版

建議方向:(b) 滾動 window — 平衡相容性跟維護成本

你的決定?(可以選一個,或說「現在不決定先放著」)
```

## 容易卡住的點

### 使用者覺得 ADR 太多

主動篩選:「我列了 {N} 個候選,你看哪些是『真的重要要記』,哪些可以省」。

### 使用者對 alternatives 想不出來

Claude 主動推 2-3 個合理替代方案,使用者只要說「合理 / 不合理」。

### Open Question 使用者也答不出來

接受「先放著」,記入 §7.2 等未來決定。給 Owner 跟 Target Date(可以是「Post-POC」這種粗略 milestone)。

## 反思檢查(進 §8 前)

- [ ] 整份 spec 的 `[待拍板]` 標記都已處理(拍板 → Accepted,或留 §7.2)
- [ ] 每個 Accepted ADR 都有 Alternatives Considered(至少 1 個)
- [ ] 每個 ADR 的 Affects 欄位正確 reference §X.Y
- [ ] 每個 Open Question 都有 Owner + Target Date
- [ ] §1.5.1 POC 表格每一條都已用 ADR 門檻判斷 — 展開的填 `Related ADR`,不展開的留 `—`
- [ ] §1.5.1 已 propagate 同步(新增 ADR 是否影響表格、ADR 標題 / Decision 變更是否同步)

## 文件結束時的 summary

```
§7 decisions 完成!

- Accepted ADR:D-0001 ~ D-{N}({M} 個檔案)
- Open Questions:D-{N+1} ~ D-{N+K}({K} 個待拍板)
- Superseded:{N 個 / 無}

接下來進入 §8 acceptance,我會推導每條 FR / state / BR / EF / EC / NFR 對應的驗收條件。要進嗎?
```
