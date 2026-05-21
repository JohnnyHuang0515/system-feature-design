---
name: system-feature-design
description: Use this skill when the user wants to design a new system feature and needs a complete, AI-development-ready specification. Triggers on requests like "幫我做 system feature design", "我想設計一個新功能", "做一份功能規格", "design a new feature spec", "write a feature design document", "create a PRD for X", or any request involving feature planning that will be handed off for AI-assisted full-stack development (frontend + backend + UX). Produces a folder of 9 interlinked spec documents covering problem framing, requirements, domain model, system flows, presentation spec, interface contracts, design decisions (ADRs), acceptance criteria, and rollout — designed so each artifact can be claimed by a different role (PM / backend / frontend / UX / QA / SRE) and consumed by AI coding agents downstream.
---

# system-feature-design

## What this skill does

Guide the user through producing a complete, multi-document feature spec — designed for handoff to AI-assisted full-stack development. The output is a folder of 9 interlinked markdown documents (plus an ADR sub-folder), each with a single focus and explicit cross-references via a shared ID system.

This skill is **not** a passive template. The core working model is:

> User provides **focus + direction + desired outcome** in plain language. Claude **derives** all structured content (FR / entity / flow / API / AC / etc.), **shows** it to the user with clear markers for things needing confirmation or decision, and **iterates** based on feedback.

## When to use

Use this skill when:
- The user describes a new feature they want to design
- The user mentions writing a spec, PRD, or design document for a feature
- The user wants documents that can be split across roles (PM / backend / frontend / UX / QA)
- Output will be consumed by AI coding agents (so cross-document consistency matters)

Do NOT use this skill for:
- Coding a feature directly (this only produces specs, not code)
- Architecture decisions at the system-of-systems level (this is feature-scoped)
- Pure brainstorming / ideation (the user should have at least a rough direction)

## Step 1: Read the working model first

**Before responding to the user**, read `references/0-skill-mode.md` in full. This file defines:

- The **derive → show → verify** loop that applies to every document
- The marking system: `[需確認]` for Claude's inferences, `[待拍板]` for decisions needing user input
- When to derive vs when to ask (key principle: derive structure, ask about business/context decisions)
- Friendly questioning style (avoid technical jargon — use everyday language)
- Allowing the user to go back and modify previous sections, with propagation
- The full-spec review flow at the end

Every behavioral guideline below is grounded in this file. **Do not skip reading it.**

### Context budget: read on demand, not upfront

This skill ships with 10 reference guides (`0-skill-mode.md` + 9 per-document guides) and a full example folder. **Do NOT read all of them at the start** — that will burn through context before you start producing.

The correct pattern:
- **At start**: read only `references/0-skill-mode.md`.
- **Before each document N**: read only `references/{N}-{name}.guide.md` and `templates/{N}-{name}.template.md`.
- **Examples folder (`examples/automation-template-export/`)**: **reference only when stuck** — for example, when the user has trouble visualizing what a finished document looks like. It is a "finished product reference", **not a step-by-step SOP to copy**. Do not preload it.

## Step 2: Opening — collect the minimum from the user

After reading the skill mode reference, greet the user with:

> 要做新的 system feature design 嗎?跟我說說你想做什麼就好 —
> 一段話描述「**要做什麼、給誰用、重點是什麼**」即可,細節我會幫你展開。
>
> 例如:
> 「我想做模板匯出匯入功能,給 PM 用,重點是讓模板可以跨工作區搬移,
>  也要支援 AI 生成的模板能寫入。」

If the user's response is very brief ("我想做 X"), compensate with 1-2 follow-up questions (NOT 5). Ask in everyday language:

- 你說想做 [X] — 主要想解決什麼困擾?
- 主要是給誰用?

After getting a basic picture, optionally check 1-3 of these only when relevant:
- 這是 POC、MVP、還是要直接上 prod?
- 有時程壓力嗎?
- 跟哪些既有系統有關聯?

Then start §1 immediately. **Do not ask the user to fill out a structured form**.

## Step 3: For each document, follow the per-document loop

The spec has 9 documents, produced in order. For each one:

### 3a. Read the document's reference guide

Before starting document N, read `references/{N}-{name}.guide.md`. Each guide tells you:
- What this document is for
- The opening line to say to the user
- A derivation table: what to infer from prior documents
- Required questions (what Claude must ask) vs forbidden questions (what Claude must derive)
- Open Question candidates (situations needing `[待拍板]`)
- The display format (usually 3 steps: summary → full content → necessary decisions)
- Common stuck points and how to handle them
- Reflection checklist before moving on
- Closing summary template

### 3b. Derive internally

Use:
- The user's initial description
- Previously completed documents
- The reference guide's derivation table
- The example folder (`examples/automation-template-export/`) as a reference if needed

**Mark inferences clearly**:
- `[需確認]` — Claude inferred this, user should verify (default for inferred numbers, persona pain points, derived FRs, etc.)
- `[待拍板]` — Two reasonable options, or missing information; user must decide

**Never fabricate**: if information is missing and can't be inferred, mark `[待拍板]` and ask.

### 3c. Show to user (3-step display)

1. **Summary first** (3-5 lines): the core content of this document
2. **Full content**: filled-in template with markers visible
3. **Necessary decisions**: 1-3 items needing the user's call, asked in everyday language

Example of decision-asking style:

> ✅ 「同名模板要怎麼處理?常見做法有三種:
>     (a) 直接拒絕,請使用者改名後再匯入
>     (b) 自動覆蓋
>     (c) 跳出選單讓使用者選『覆蓋 / 建立新的 / 取消』
>     你傾向哪個?」

NOT:

> ❌ 「Idempotency 策略是?同名衝突如何 handle?」

### 3d. Receive feedback and iterate

The user may:
- **Confirm** → move to next document
- **Small fix** → adjust and re-confirm
- **Major change** → re-derive the affected section
- **Go back and modify a prior document** → accept, then proactively scan downstream documents for propagation effects; ask the user if they want those synced
- **Request more detail** → expand the relevant section

### 3e. Internal reflection before moving on

Check the reflection checklist in the guide. If anything is incomplete or inconsistent, fix it before moving to the next document. Then give the closing summary and confirm with the user before proceeding.

## Step 4: Document order, output location, and write timing

Produce documents in this exact order (later docs reference earlier ones):

1. `1-problem-scope.md` — Problem, users, success criteria, scope, assumptions
2. `2-requirements.md` — FRs, NFRs, priority
3. `3-domain-model.md` — Entities, state machines, business rules, events
4. `4-flows.md` — System flows, error flows, edge cases (system-side only)
5. `5-presentation-spec.md` — Presentation type, user stories, user flows, components, pages
6. `6-interfaces.md` — REST APIs, events, integrations, error catalog
7. `7-decisions.md` + `decisions/NNNN-*.md` — ADRs, open questions
8. `8-acceptance.md` — Acceptance criteria (BDD format)
9. `9-rollout.md` (optional) — Rollout, observability, runbook, rollback

Plus:
- `README.md` — Index, ID system reference, revision history

### Output location

Files go into **a `{feature-name}/` folder in the user's current working directory** (not a fixed sandbox path). At the start of the session, decide the folder name with the user — usually a kebab-case slug derived from the feature, e.g. `template-export-import/`. Create the folder structure mirroring `examples/automation-template-export/`.

If the user is in an existing project repo, ask whether to put the spec under `docs/specs/{feature-name}/` or at repo root — don't assume.

Use the corresponding files in `templates/` as the structural starting point — copy and fill in, don't reinvent the structure.

### When to write each file

**Write each document to disk as soon as the user confirms it** (end of step 3e for that document). Do NOT wait until all 9 are done. Reasons:
- The user can review the actual file between docs.
- Later docs reference earlier docs by §X.Y — having them on disk lets you re-read instead of re-deriving from memory.
- If the session is interrupted, work is preserved.

After writing, briefly note the path (`wrote 3-domain-model.md`) so the user knows where it landed.

### When to write README.md

Create `README.md` **immediately after §1 is confirmed** (so it exists as an index from the start), with placeholder rows for §2–§9. Update its Revision History row with `v0.1 — Initial draft` and the current date. After §9 (or §8 if §9 is skipped), do a final pass to make sure all document links and the ID system table are accurate.

## Step 5: Full-spec review (after all 9 documents)

Once all documents are complete, **proactively ask the user**:

> 9 份文件都完成了!
>
> 要不要跑一次完整 spec 的總 review?
> 我會檢查跨文件的一致性,例如:
> - 所有 FR 是否都有對應的驗收條件
> - 編號 reference 是否全部對得上
> - 同一個概念在不同文件描述是否一致
> - 有沒有遺漏或孤兒內容
>
> 預估 5-10 分鐘,會列出問題清單讓你決定要不要修。
>
> 要跑嗎?

If yes, run all 5 checks defined in `references/0-skill-mode.md` (the "完整 spec 做完後的總 review" section):
1. Cross-document ID reference consistency
2. Required coverage completeness
3. Orphan check (defined-but-unused elements)
4. Concept consistency across documents
5. Unresolved items

Report results in three buckets:
- ✅ **Pass** (no action needed)
- ⚠️ **Warning** (suggest review)
- ❌ **Error** (recommend fixing)

Offer to fix the Errors and show Warnings on request.

If no, deliver the spec with a brief handoff guide:

> Spec 完成!建議的角色認領:
> - PM 看 §1, §2, §5, §7, §8
> - 後端工程師看 §3, §4, §6, §8
> - 前端工程師看 §5, §6, §8
> - UX 設計師看 §5
> - QA 看 §8
> - SRE 看 §9
>
> 未來想跑總 review 隨時告訴我。

## ID system (used across all documents)

| Prefix | Meaning | Defined in |
|--------|---------|------------|
| FR-N | Functional Requirement | §2.1 |
| NFR-N | Non-Functional Requirement | §2.2 |
| BR-N | Business Rule | §3.4 |
| SF-N | System Flow | §4.1 |
| EF-N | Error Flow | §4.2 |
| EC-N | Edge Case | §4.3 |
| UF-N | User Flow | §5.3 |
| P-N | Page | §5.6 |
| C-N | Component | §5.5 |
| T-N | Page Section | §5.6 |
| D-NNNN | Decision (ADR) | decisions/ |
| AC-* | Acceptance Criteria | §8 |

When introducing new items in any section, automatically assign the next number in sequence and tell the user explicitly (e.g., "I'm adding this as FR-3").

## Key principles (summary)

1. **Derive > ask** — Claude does the structural work; user provides direction and decisions
2. **Show > silently fill** — every derivation is displayed for user verification
3. **Everyday language > jargon** — see vocabulary table in `0-skill-mode.md`
4. **Two markers, not five** — `[需確認]` and `[待拍板]` only
5. **Cross-document consistency matters** — for AI development handoff, references must be exact
6. **Allow backtracking** — user can go back any time; Claude propagates changes
7. **End with optional full review** — ask, don't force

## Folder structure (this skill)

```
system-feature-design/
├── SKILL.md                          (this file)
├── templates/                        (structural skeletons to fill)
│   ├── README.template.md
│   ├── 1-problem-scope.template.md
│   ├── 2-requirements.template.md
│   ├── 3-domain-model.template.md
│   ├── 4-flows.template.md
│   ├── 5-presentation-spec.template.md
│   ├── 6-interfaces.template.md
│   ├── 7-decisions.template.md
│   ├── 8-acceptance.template.md
│   ├── 9-rollout.template.md
│   └── decisions/
│       └── NNNN-template.md
├── references/                       (how-to guides for Claude)
│   ├── 0-skill-mode.md               ← READ FIRST
│   ├── 1-problem-scope.guide.md
│   ├── 2-requirements.guide.md
│   ├── 3-domain-model.guide.md
│   ├── 4-flows.guide.md
│   ├── 5-presentation-spec.guide.md
│   ├── 6-interfaces.guide.md
│   ├── 7-decisions.guide.md
│   ├── 8-acceptance.guide.md
│   └── 9-rollout.guide.md
└── examples/                         (filled-out example for reference)
    └── automation-template-export/
        ├── README.md
        ├── 1-problem-scope.md
        ├── ... (all 9 docs)
        └── decisions/
            └── 0001-*.md, etc.
```

## Final reminder

This skill produces specs that will be read by AI coding agents. Cross-document precision is the whole point — vague references defeat the purpose. Always:

- Use exact IDs (FR-3, not "the third requirement")
- Mark inferences with `[需確認]`, never leave them ambiguous
- Mark open decisions with `[待拍板]`, never invent business rules
- Verify with the user before moving on

If at any point you're uncertain about scope or direction, **stop and ask the user**, in everyday language, with a concrete choice rather than an open question.
