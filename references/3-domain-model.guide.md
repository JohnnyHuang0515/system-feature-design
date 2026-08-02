# Reference Guide: 3-domain-model.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/3-domain-model.template.md`.
> Instructions here are English; the quoted blocks are scripts spoken to the user — use them as written.

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
| §3.1 Bounded Contexts | Responsibility blocks inferred from §1.5 in scope (one line for a small feature) |
| §3.2 Entities | Reverse-engineered from the nouns and verbs in §2.1 FRs — 「使用者建立訂單」 → an Order entity |
| §3.2 Entity fields | Required fields from the FRs, plus inferred standard fields (id, created_at, updated_at) |
| §3.3 State Machines | Where an entity has a status concept, derive its transitions — Draft → Submitted → Paid |
| §3.4 Business Rules | Constraints in §1.5, §2.2 NFRs, and the invariants implied by FRs |
| §3.5 Domain Events | State transitions plus cross-context interactions |

### Worked entity derivation

From FR-2 "Allow users to import an automation template":

- Noun: template → a Template entity
- Implied: what a template contains → Node, Connection entities
- Required fields: id, name, status, workspace_id, created_at…

### Bounded contexts

A small feature usually needs one. With many entities you might split: a 「管理 X」 context, a 「處理 X 的 import/export」 context, a 「驗證 X」 context.

Uncertain how to cut it → use a single context. Over-design costs more than the split saves.

### State machines

Every entity with a status field gets one: initial state, main states, terminal states, and each transition's trigger, guard and side effect.

### Business rules

Sources: the "absolutely must not be violated" items in the §1.5.1 POC table; the security and compliance rules implied by §2.2 NFRs; constraints stated in FRs (「至少 1 個 Node 才能 Activate」); and standard domain sense (「金額不可為負」).

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

1. Template 的 status 我設計成「草稿 → 啟用中 → 已封存」三個狀態,
   合理嗎?還是你心中有別的流程(例如需要審核狀態)?

2. 業務規則「Template 名稱在 workspace 內必須唯一」 — 大小寫敏感嗎?
   (「訂單流程」跟「訂單流程 」算同一個還是不同?)

3. 我推測會發出 TemplateImported / Exported / Activated 三個事件,
   有需要的事件我漏了嗎?
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

So when the Scaffold branch runs, §3.2 entity names and §3.4 rule vocabulary seed the repo's `CONTEXT.md`, and §7's `decisions/NNNN-*.md` seed `docs/adr/`. The `domain-glossary` skill maintains them from then on.

Two things follow for how you write §3:

- **Pick one word per concept and stick to it** across every document. Where the user offers synonyms — 帳號 / 使用者 / 會員 — settle on the canonical one and note the rejected ones, because that note is what stops the drift later.
- **Definitions are what a thing *is***, in a sentence or two, not what it does. The behaviour lives in §4 flows.

## Reflection check, before §4

- [ ] Every §2.1 FR is implementable with these entities
- [ ] Every entity with a status has a state machine
- [ ] Every BR names its enforcement mechanism
- [ ] Fields use logical types (UUID, Timestamp…), not DB types (BIGSERIAL…)
- [ ] One canonical word per concept across the whole spec, with rejected synonyms noted — this is what seeds the repo's `CONTEXT.md`
- [ ] Marker lifecycle done: confirmed markers deleted, surviving `[待拍板]` carry options and a recommendation, deferred ones converted to a D-NNNN reference

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
