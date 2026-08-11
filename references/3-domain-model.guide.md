# Reference Guide: 3-domain-model.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/3-domain-model.template.md`.

## Purpose

Define the system's core domain model — entities, states, business rules. **This is the conceptual layer, not a DB schema.**

## Opening

```
進入第三份:領域模型。

這份描述系統「內部由什麼組成」 — entity、欄位、狀態流轉、業務規則。
這是後端工程師最關注的文件。

重要原則:這不是資料庫 schema,我們寫概念,DB 細節留給實作階段。

我會根據前面文件先推導,你確認 / 修正。
```

## Derivation

| Target | Source |
|---|---|
| §3.1 Bounded Contexts | Responsibility blocks inferred from §1.5 in scope. A small feature needs one; many entities may split into a 「管理 X」, an 「匯入匯出 X」 and a 「驗證 X」 context. Uncertain how to cut → one context, because over-design costs more than the split saves |
| §3.2 Entities | Reverse-engineered from the nouns and verbs in §2.1 FRs — 「使用者建立訂單」 → an Order entity |
| §3.2 Entity fields | Required fields from the FRs, plus inferred standard fields (id, created_at, updated_at) |
| §3.3 State Machines | Every entity with a status field gets one: initial state, main states, terminal states, and each transition's trigger, guard and side effect — Draft → Submitted → Paid |
| §3.4 Business Rules | The 「絕對不能違反」 rows of the §1.5.1 POC table, the security and compliance rules implied by §2.2 NFRs, constraints stated in FRs (「至少 1 個 Node 才能 Activate」), and standard domain sense (「金額不可為負」) |
| §3.5 Domain Events | State transitions plus cross-context interactions |

### Worked entity derivation

From FR-2 "Allow users to import an automation template":

- Noun: template → a Template entity
- Implied: what a template contains → Node, Connection entities
- Required fields: id, name, status, workspace_id, created_at…

## Questions you must ask

Deriving and confirming usually suffices. Two situations call for a question:

1. **A branch in the state machine** — several transition paths are reasonable. Mark `[待拍板]`.
2. **How strict a business rule should be** — loose vs strict. Mark `[待拍板]`.

## Open question candidates

- Several reasonable bounded-context cuts (fine-grained vs merged)
- Several state-transition designs (A→B direct, or A→intermediate→B)
- Business rule strictness (ban self-connection vs allow it)
- Whether an event is emitted at all (internal-only vs published)

## Display format

### Step 1: summary

```
我推導出領域模型如下:

- {N} 個 entity:{列名稱}
- {M} 個 state machine:{列哪些 entity 有}
- {K} 條 business rule
- {J} 個 domain event(若有)

需要你拍板:[N 個關鍵決策]
```

### Step 2: full content, section by section

Show §3.1 through §3.5 in order. With many entities, give 1–2 at a time so the user can absorb them.

### Step 3: the decisions

```
有幾件事需要你拍板:

❓ **Q1** — **Template 狀態**:(a)「草稿 → 啟用中 → 已封存」三態 (b) 中間再加一個「待審核」
➡️ 建議 (a) —— 沒有人提到審核流程,加了就要連帶設計審核者與權限

❓ **Q2** — **名稱唯一性怎麼比**:(a) 大小寫與前後空白都忽略 (b) 完全相符才算重複
➡️ 建議 (a) —— 「訂單流程」跟「訂單流程 」對使用者是同一個,判成不同會讓人困惑

❓ **Q3** — **Domain events**:(a) 就 TemplateImported / Exported / Activated 三個 (b) 再加 TemplateArchived
➡️ 建議 (a) —— 這三個對應狀態機上的三次轉換;封存目前沒有任何消費者
```

## Where you'll get stuck

### The user isn't sure how to cut entities

Give them the splitting rule: **anything independently created, deleted or queried is usually its own entity.**

In 「使用者匯入模板」, Template and Node are separate — Template is independently queryable, Node belongs to a Template and isn't.

### The user can't draw a state machine

Hand them a Mermaid diagram draft to nod at or change.

### The user thinks there are too many business rules

Ask 「哪些是『絕對不能違反』、哪些是『一般情況才這樣』?」 — the latter is business logic, not an invariant. The question does the separating for them.

## Handing the language to the repo

§3 is where the project's **ubiquitous language** is settled — entity names, the words for each state, what a business rule calls the thing it constrains. That language is worth more alive in the repo than frozen in a spec: an agent that has it names variables, functions and files consistently, navigates faster, and spends fewer tokens re-explaining the domain each session.

The Scaffold branch carries it into the repo — `references/scaffold.guide.md` says how, and from then on the repo's copies are the living ones.

Two things follow for how you write §3:

- **Pick one word per concept and stick to it** across every document. Where the user offers synonyms — 帳號 / 使用者 / 會員 — settle on the canonical one and note the rejected ones, because that note is what stops the drift later.
- **Definitions are what a thing *is***, in a sentence or two, not what it does. The behaviour lives in §4 flows.

## Reflection check, before §4

- [ ] Every §2.1 FR is implementable with these entities
- [ ] Every entity with a status has a state machine
- [ ] Every BR names its enforcement mechanism
- [ ] Fields use logical types (UUID, Timestamp…), not DB types (BIGSERIAL…)
- [ ] One canonical word per concept across the whole spec, with rejected synonyms noted — this is what seeds the repo's `CONTEXT.md`

Then run the three checks from inside the spec folder and **say what they printed**:

- [ ] `grep -c "\[需確認\|\[待拍板" 3-domain-model.md` → `0`
- [ ] `python3 <skill-path>/scripts/check-sections.py .` → ✓
- [ ] `python3 <skill-path>/scripts/check-example-ids.py .` → ✓

## Closing summary

```
§3 domain-model 完成!

- Contexts:{N 個}
- Entities:{列名稱}
- State machines:{列哪些 entity}
- Business rules:BR-1 ~ BR-{N}
- Domain events:{N 個 / 跳過}

接下來進入 §4 flows,我會推導系統內部執行流程、錯誤處理、邊界情境。要進嗎?
```
