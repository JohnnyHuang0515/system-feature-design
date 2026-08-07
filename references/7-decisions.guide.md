# Reference Guide: 7-decisions.md + decisions/

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/7-decisions.template.md` and `templates/decisions/NNNN-template.md`.
> Instructions here are English; the quoted blocks are scripts spoken to the user — use them as written.

## Purpose

Record the key design decisions — why A and not B, which alternatives were weighed, what remains undecided.

The ADRs are split: `7-decisions.md` is the index, and each decision gets its own file under `decisions/`.

## Opening

```
進入第七份:設計決策。

這份用 ADR (Architecture Decision Record) 格式記錄關鍵決策。

我會:
1. 掃描前面文件,蒐集已經做過的關鍵決策
2. 把這些決策寫成 ADR(每個一份檔案)
3. 整理 Open Questions(待拍板事項)

你的工作主要是「確認 ADR 內容對」+「為 Open Questions 拍板」。
```

## Derivation

### Scan the earlier documents for ADR candidates

| Source | What usually becomes an ADR |
|---|---|
| §5.8 Interaction Decisions | A frontend decision that shapes the data model or is irreversible once shipped — a partial-success strategy driving API design, say. §5 escalates these; this table is where they land |
| §1.5.1 POC table | **Every row is a candidate, not an automatic ADR.** Apply the threshold below row by row; expand only what clears it. Expanded rows propagate back into §1.5.1's `Related ADR` column; the rest keep `—` |
| §3.1 Bounded Contexts | 「為什麼這樣切?」 |
| §3.3 State Machine | The load-bearing choices in the transitions |
| §4.1 SF | How services interact (sync vs async) |
| §6.2 API | Significant API design choices (single-stage vs two-stage) |
| §6.6 Versioning | The versioning strategy |
| Every `[待拍板]` in the spec | All become open-question candidates |

### ADR content

| Field | Source |
|---|---|
| Title | One sentence naming the decision |
| Context | Why this decision was needed, from the earlier documents |
| Decision | The call that was made |
| Rationale | Why it was made that way, from the earlier documents |
| Alternatives | Derive 2–3 alternatives unprompted, each with pros and cons |
| Consequences | Positive and negative effects |
| Affects | References to specific §X.Y |

### The ADR threshold

Any one of these justifies writing it:

1. In three months someone will ask 「為什麼當初這樣?」
2. Changing it is expensive — it touches several sections or services
3. A reasonable alternative exists (it isn't just the industry default)
4. It affects another team

**Code style, settled industry practice (use HTTPS) and pure technology preference stay out.**

### Filter before you show

Apply the threshold **internally first** and show only what clears it. Mention the rest in one line — 「另有 N 個候選不到門檻,留在 §1.5 / §2.3 即可:{列名}」 — so the user can pull one back. Writing full ADRs for every candidate *before* asking is wasted work.

Pure scope trade-offs (「POC 不做 X」, where the reason is simply "keep it simple first") rarely clear it: §1.5 and §2.3 already record them, and expanding them into ADRs is noise.

Note: the example feature ships 11 ADRs because it is large — **that is not a target**. A small feature typically has 3–6.

### Open questions

Every `[待拍板]` in the spec collects into §7.2 and expands into an ADR file with Status: Proposed.

## Questions you must ask

Once the ADRs are written, **put every open question to the user**:

```
有 {N} 個待拍板事項,我幫你整理選項,你決定:

D-{N}: {議題}
建議方向:{Claude 的傾向,但需你決定}
- (a) {選項 A} (Pros: ... Cons: ...)
- (b) {選項 B} (Pros: ... Cons: ...)
- (c) 先放著 → 列入 §7.2 待解
```

## Open question candidates

§7 raises no new open questions — its job is **converging the `[待拍板]` markers scattered through the earlier documents**.

A genuinely new one here means an earlier section has a gap. Go back and fill it first.

## Display format

### Step 1: summary

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

### Step 2: confirm each Accepted ADR

Give a one-paragraph summary so the user can confirm quickly:

```
D-0001: Task 欄位採內嵌儲存,預留外部引用欄位

簡述:POC 階段 task 欄位內嵌在模板中,但 schema 保留
     `task_template_ref` 欄位以便未來改用引用模式。

完整 ADR 已寫在 decisions/0001-task-fields-embedded-with-future-ref.md

OK 嗎?有要補的 alternative 或 consequence?
```

### Step 3: settle each open question

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

## Where you'll get stuck

### The user thinks there are too many ADRs

Filter with them: 「我列了 {N} 個候選,你看哪些是『真的重要要記』,哪些可以省」.

### The user can't think of alternatives

Derive 2–3 reasonable ones yourself; the user only has to say whether they're reasonable.

### The user can't answer an open question either

Accept 「先放著」 and record it in §7.2 for later, with an Owner and a Target Date — a rough milestone like 「Post-POC」 is fine.

## Reflection check, before §8

- [ ] Every `[待拍板]` in the spec is handled — settled into Accepted, or parked in §7.2
- [ ] Every Accepted ADR has at least one Alternative Considered
- [ ] Every ADR's Affects column references a real §X.Y
- [ ] Every open question has Owner and Target Date
- [ ] Every §1.5.1 POC row was judged against the ADR threshold — expanded rows carry `Related ADR`, the rest carry `—`
- [ ] §1.5.1 is propagated in sync (new ADRs checked against the table; ADR title and Decision changes reflected)

## Closing summary

```
§7 decisions 完成!

- Accepted ADR:D-0001 ~ D-{N}({M} 個檔案)
- Open Questions:D-{N+1} ~ D-{N+K}({K} 個待拍板)
- Superseded:{N 個 / 無}

接下來進入 §8 acceptance,我會推導每條 FR / state / BR / EF / EC / NFR 對應的驗收條件。要進嗎?
```
