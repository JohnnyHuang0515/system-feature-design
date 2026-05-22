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

## How SKILL.md and 0-skill-mode.md split responsibilities

This SKILL.md is the **flow skeleton** — what to read, what order to produce documents in, where files go, when to write them, the ID system.

`references/0-skill-mode.md` is the **work philosophy** — derive vs ask, the marker system (`[需確認]` / `[待拍板]`), everyday-language questioning style, propagation rules, full-spec review checks.

When this file says "follow the X pattern in 0-skill-mode.md", go read that section there. Don't try to do everything from this file alone.

## Step 1: Read the working model first

**Before responding to the user**, read `references/0-skill-mode.md` in full. Every behavioral guideline in this skill is grounded in that file — opening pattern, derive-vs-ask judgment, marker rules, propagation, full review checks.

### Context budget: read on demand, not upfront

This skill ships with 10 reference guides (`0-skill-mode.md` + 9 per-document guides) and a full example folder. **Do NOT read all of them at the start** — that will burn through context before you start producing.

The correct pattern:
- **At start**: read only `references/0-skill-mode.md`.
- **Before each document N**: read only `references/{N}-{name}.guide.md` and `templates/{N}-{name}.template.md`.
- **Examples folder (`examples/automation-template-export/`)**: reference only when stuck — for example, when the user has trouble visualizing what a finished document looks like. It is a "finished product reference", **not a step-by-step SOP to copy**. Do not preload it.

## Step 2: Opening

Follow the opening pattern defined in `0-skill-mode.md` (the "開場" section): greet, accept the user's one-sentence description, ask at most 1–3 everyday-language follow-ups, then start §1 immediately. Do not ask the user to fill out a structured form.

## Step 3: Per-document loop

The spec has 9 documents, produced in order. For each one:

### 3a. Read the document's reference guide

Before starting document N, read `references/{N}-{name}.guide.md` and `templates/{N}-{name}.template.md`. The guide tells you the derivation table, required questions, OQ candidates, display format, stuck points, reflection checklist, and closing summary template.

### 3b. Derive internally

Use the user's initial description, previously completed documents on disk, and the guide's derivation table. Apply the **derive vs ask** judgment from `0-skill-mode.md` — derive structure, ask about business/context decisions.

Mark every inference:
- `[需確認]` — Claude inferred this; user verifies
- `[待拍板]` — Two reasonable options exist; **must come with options (a)(b)(c) + recommended direction** (see the rule in `0-skill-mode.md`)

Never fabricate. If you can't derive and can't form options, stop and ask the user for context.

### 3c. Show to user

Use the 3-step display format (summary → full content → necessary decisions) defined in `0-skill-mode.md` and refined per-document in each guide. Ask decisions in everyday language with concrete options, not jargon.

### 3d. Receive feedback and iterate

Handle confirm / small fix / major change / back-edit / request-more-detail per the patterns in `0-skill-mode.md`. When the user back-edits a prior document, proactively scan downstream for propagation effects and ask before syncing.

### 3e. Reflect, write to disk, and move on

Run the guide's reflection checklist. Fix gaps. Write the document to disk (see Step 4). Give the closing summary. Confirm the user is ready before proceeding to the next document.

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

## Step 5: Full-spec review

After the last document is written, proactively offer the full-spec review. The wording, the 5 check categories, and the result-bucketing format are all defined in `0-skill-mode.md` (the "完整 spec 做完後的總 review" section). If the user declines, deliver the handoff guide (role-by-section reading recommendations).

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

## Folder structure (this skill)

```
system-feature-design/
├── SKILL.md                          (this file — flow skeleton)
├── templates/                        (structural skeletons to fill)
│   ├── README.template.md
│   ├── 1-problem-scope.template.md
│   ├── ... (2-9)
│   └── decisions/
│       └── NNNN-template.md
├── references/                       (how-to guides for Claude)
│   ├── 0-skill-mode.md               ← READ FIRST (work philosophy)
│   ├── 1-problem-scope.guide.md
│   └── ... (2-9)
└── examples/                         (filled-out example — reference only when stuck)
    └── automation-template-export/
```

## Final reminder

This skill produces specs that will be read by AI coding agents. Cross-document precision is the whole point. Always:

- Use exact IDs (FR-3, not "the third requirement")
- Mark inferences with `[需確認]`
- Mark open decisions with `[待拍板]` **together with options + recommendation** — never standalone
- Verify with the user before moving on

If you're uncertain about scope or direction, stop and ask in everyday language with a concrete choice.
