---
name: system-feature-design
description: Spec a feature for AI-assisted development, research the market that shapes it, chart oversized work as a map of decisions, cut a spec into tickets, or scaffold a repo's Claude Code conventions. Use when the user asks for 「做一份功能規格」 or a spec / PRD for a new feature; 「市場調研」 or competitive analysis and market sizing; 「這件事很大,先幫我理清楚」 or "this is too big to plan in one go"; 「拆票」 or "break this into tickets"; 「初始化專案」 or "scaffold a Claude Code project" — CLAUDE.md, rules, sub-agents.
---

# system-feature-design

Four branches. Each runs alone, and each can start from what another produced.

| Branch | Produces | Reach for it when |
|---|---|---|
| **Spec** | up to 10 interlinked documents (§0–§9) in a `{feature-name}/` folder | the user has a feature in mind and needs it specified |
| **Map** | a map of decision tickets, resolved one per session | the work doesn't fit one context window — too many unanswerable questions to specify it yet. Runs *before* Spec |
| **Tickets** | tracer-bullet tickets with blocking edges | a spec, plan or conversation is ready to become buildable work |
| **Scaffold** | a repo's `CLAUDE.md` + `.claude/` — rules, skills, sub-agents | the user is starting a codebase, or moving an existing one onto Claude Code conventions |

Each spec document is claimable by one role — PM / backend / frontend / UX / QA / SRE — and readable by an AI coding agent downstream. Exact IDs across documents are what make that split work. Implementation happens after this skill, not inside it.

**Entering mid-way is the point.** A spec the user wrote themselves, one a manager handed over, one another agent produced — all go straight into Tickets without the Spec branch ever running. Ask which branch fits rather than assuming the user starts at §0.

**And say so when none of them fits.** A change that touches one module inside a repo the user already has doesn't earn ten documents: no market to research, no frontend checklist, no BDD coverage matrix. What it earns is being interrogated until the decision tree is settled, with the terms and the load-bearing decisions written down — which is the `grilling` skill in a scaffolded repo, alongside `domain-glossary`. Point there and stop; marching a two-hour change through §1–§8 is the failure mode this skill is most likely to produce.

The Spec branch earns its weight when the work spans several sessions, several roles, or several people who need the same picture.

---

# Branch: Spec

## Before the first reply

Read `references/0-skill-mode.md` in full. It is the working model every step below assumes: **derive vs ask**, the `[需確認]` / `[待拍板]` markers, everyday-language questioning, propagation, and the closing review.

Read everything else on demand — 10 guides, 11 spec templates and a worked example ship here, and loading them upfront spends the context the work needs.

| When | Read |
|---|---|
| starting document N | `references/{N}-*.guide.md` + `templates/{N}-*.template.md` |
| checking your own spec's IDs resolve | run `python3 <skill-path>/scripts/check-example-ids.py <spec-folder>` — it reports dangling IDs and broken coverage chains |
| wanting to see what a finished chain looks like | the matching file under `examples/automation-template-export/` — read it for shape, never to source content |

## Opening

Follow `Opening` in `0-skill-mode.md`: greet, take the user's one-sentence description, ask 1–3 everyday-language follow-ups.

Then offer §0 market research, and take one of three routes:

- the user wants it, or already has research to fold in → run §0 first
- an internal tool with no market dimension, or the user simply declines → start at §1 and mark §0 `⏭️ 跳過（原因）` in the README
- the request *is* the research → §0 is the whole job; offer the rest of the spec once it lands

**The recorded reason is the one that was given.** A user who says only 「跳過」 has given 「使用者要求跳過」 — write that and stop. 「內部工具,無市場調研需求」 is a finding about their business, and putting one on the record that nobody made means the README is later read as though someone had. The same holds for every `⏭️ 跳過` row whose reason came from the user rather than from the Paths table.

## Context hygiene

**Keep the whole Spec branch — and Tickets, if it follows — in one unbroken context window.** Don't compact and don't clear between documents: §5 re-reads §4, §8 re-reads everything, and a summarized §3 is a §3 you will silently get wrong.

The ceiling is the window in which the model still reasons sharply, roughly 120k tokens on current models. Approaching it before the spec is finished, don't push on degraded — write out what's confirmed, hand off to a fresh session, and resume from the README's 狀態 column.

Work that was never going to fit takes the **Map** branch instead, and §1's fog count is where that gets decided rather than discovered at 110k. Handing off mid-spec rescues a run that ran long; a Map is for work whose *decisions* don't fit, which handing off does not fix.

Implementation is the opposite: each ticket starts in a **fresh** window, working from the ticket alone.

## Per-document loop

Documents go in order, §0 through §9, because each one references the last. For each:

**1. Read** `references/{N}-*.guide.md` and `templates/{N}-*.template.md`. The guide carries that document's derivation table, required questions, OQ candidates, display format, stuck points, reflection checklist and closing summary. (§7 and §8 are consolidation stages — they route open questions rather than raise new ones.)

**2. Derive** from the user's description, the documents already on disk, and the guide's derivation table. Structure is yours to derive; business and context decisions are the user's to make.

> **§0 inverts this.** It is research-driven: `WebSearch` / `WebFetch` the market and competitors, `Read` any data the user supplies. State the research plan in one line and take the single direction-confirm (`Direction check before the run`), then run to completion uninterrupted. Every figure and competitor fact carries a source and a confidence level. See `references/0-market-research.guide.md`.

If §1 established this is a **POC / side project**, apply `POC fast mode` from `0-skill-mode.md`: auto-apply low-risk recommendations in a one-line announcement, and hard-stop only on irreversible, money-direction, or data-model-shaping forks. Target ≤5–8 hard stops for the whole session.

Mark what you inferred: `[需確認]` for anything the user should verify, `[待拍板]` for a live fork — and a `[待拍板]` always ships with options (a)(b)(c) plus your recommended direction. Where you can neither derive nor form options, ask for context.

**3. Show** using the 3-step display format in `0-skill-mode.md` — summary, then full content, then the decisions you need. Put decisions in everyday language with concrete options.

**4. Iterate** on the feedback: confirm / small fix / major change / back-edit / more detail, each patterned in `0-skill-mode.md`. A back-edit to an earlier document triggers a downstream propagation scan — surface what it touches and ask before syncing.

**5. Close out.** Run the guide's reflection checklist and fix what it catches, then ask the one question no per-document guide covers: **does anything here mean an earlier document needs amending?** Say so and offer the edit. Then run the marker lifecycle, and treat its outcome as an invariant: **a file on disk carries no bare `[需確認]` or `[待拍板]`.** Every marker leaves by one of exactly two doors — deleted, because the user confirmed the item; or converted into a §7.2 Open Question with a `D-NNNN` reference left in its place, because they deferred it. An item that is neither confirmed nor deferred is not ready to be written, so resolve it before writing rather than shipping the marker. Markers live in the conversation only; §7.2 is the one place an unresolved item persists, and nothing — the README included — becomes a second parking spot for them. (`Marker lifecycle` in `0-skill-mode.md`.)

Write the file, note its path, give the closing summary, and confirm the user is ready for the next document.

## Documents

| § | File | Holds |
|---|---|---|
| 0 | `0-market-research.md` *(optional, runs first)* | market sizing, segments, competitors, research-backed personas, sentiment, differentiation — feeds §1 and §2 |
| 1 | `1-problem-scope.md` | problem, users, success criteria, scope, assumptions |
| 2 | `2-requirements.md` | FRs, NFRs, priority |
| 3 | `3-domain-model.md` | entities, state machines, business rules, events |
| 4 | `4-flows.md` | system flows, error flows, edge cases — system-side only |
| 5 | `5-presentation-spec.md` | presentation type, user stories, user flows, journey (§5.4), components, pages, interaction decisions (§5.8), design handoff (§5.9) |
| 6 | `6-interfaces.md` | REST APIs, events, integrations, error catalog |
| 7 | `7-decisions.md` + `decisions/NNNN-*.md` | decision index + open questions; full ADR bodies live in `decisions/` |
| 8 | `8-acceptance.md` | acceptance criteria, BDD format |
| 9 | `9-rollout.md` *(optional)* | rollout, observability, runbook, rollback |
|   | `README.md` | index, ID system, revision history |

## Paths

§1's stage question — POC, MVP, or production — settles **which documents this run carries and how deep each goes**. Say which path you're on once it's answered; a path carrying documents it doesn't need is the most common way this gets heavy.

The same moment takes one more reading: **which decisions here can nobody answer yet?** One that you can name but **cannot write options for**, and which **also blocks §2 onward**, is **fog** — a fact someone has to go and find, not a choice the user can make. 「不知道,要查了才知道」 is fog; 「沒想過,你建議呢」 is a `[待拍板]`.

Report the count as a number and name what each item blocks. Then say the thing the user can't see: those sections would be written from a guess and rewritten when the fact lands. **Planning to write a provisional version and reconcile later is what being blocked looks like, not a way around it.**

§1's own lines are blocked the same way. A success criterion or a scope entry resting on a fog item **goes in the report, not onto disk behind a marker** — the marker invariant holds here, and fog is the one thing it has no §7.2 to park in yet.

Then recommend the Map branch and hand back. Escalating into a heavier process is the user's call, and they can make it only once they can see it — so the reading is done when the count, the blocked sections and the cost are in front of them and they have answered. `references/1-problem-scope.guide.md` carries the detail; this paragraph is the whole rule.

| Path | Carries | Depth |
|---|---|---|
| **POC / side project** | §1–§8. §0 and §9 skipped | POC fast mode. §4 takes the happy path plus the failures that will actually happen, not an exhaustive sweep. §6 covers what the frontend actually calls. §5.4–§5.9 only where there's a GUI |
| **MVP** | §1–§8, plus §9 where it touches production traffic, plus §0 where the market shapes the requirements | §4 gets the full EF / EC sweep. §6 covers every consumer, not just the first one |
| **Production / revenue-carrying** | §0–§9 | Exhaustive throughout, and §9 stops being optional — rollout, alerting and rollback all get written |

Depth is the lever that matters more than presence. A POC's §4 is three flows and the two failures that bite; a production §4 is every error path enumerated. Same document, different weight.

**Skipping §0** — leave the file uncreated and mark its README row `⏭️ 跳過（原因）`. §1.3 personas fall back to derive-plus-`[需確認]` with no PER-N references. Nothing downstream hard-depends on §0.

**Skipping §9** — sweep §1–§8 for forward references into §9 (an NFR saying「詳見 §9.3」, an EF pointing at「§9.4 alert」), rewrite or remove each, and drop the §9 row from the README index.

## Where files land

A `{feature-name}/` folder in the user's current working directory — settle the kebab-case slug with them at the start, e.g. `template-export-import/`. `examples/automation-template-export/` shows the finished shape, and each document starts from its file in `templates/`.

**Create the `{feature-name}/` folder up front** — every document lands inside it, and the README's index is only meaningful relative to it. Writing spec documents loose in the working directory is wrong even for a single-document run.

**Its subfolders grow as their contents arrive**, though: `decisions/` appears when the first ADR is written, `map/` when the Map branch charts one, `issues/` when the Tickets branch runs. An empty subdirectory named after a document that doesn't exist yet is noise the user has to interpret.

Names are literal — the subfolder is `decisions/`, never `{decisions}/`. Braces in this file mark a slot for you to fill, never a character to type.

Inside an existing project repo, ask whether the spec belongs under `docs/specs/{feature-name}/` or at the repo root.

**Write each document the moment the user confirms it** (end of step 5). The user gets to read the real file between documents, later documents re-read earlier ones by §X.Y instead of trusting memory, and an interrupted session keeps its work.

Create `README.md` right after §1 confirms, with placeholder rows for §2–§9 and a `v0.1 — Initial draft` revision row. Its **狀態 column** (`✅ v0.1` / `⬜ 待產` / `⏭️ 跳過`) is the session's progress tracker — update it on every write. After the last document, sweep the links and the ID table.

**Resuming a broken session**: read the README's 狀態 column to find where work stopped, re-read the documents already on disk — they are the source of truth — and re-enter the loop at the first `⬜ 待產`.

## Closing review

After the last document, offer the full-spec review: wording, the seven checks (0–6, opening with a mechanical grep pass), and result bucketing are all in `references/full-spec-review.md`. If the user passes on it, deliver the handoff guide instead — which role reads which sections.

Then offer the two branches the spec feeds:

- **Tickets** — cut it into buildable work. The natural next step.
- **Scaffold** — set up the repo that will implement it. The spec already names the stack, the entry point and the commands, so that interview is mostly confirmation. A repo that already has `CLAUDE.md` skips it. §3's entity vocabulary and §7's ADRs carry over as the repo's `CONTEXT.md` and `docs/adr/`, where the `domain-glossary` skill keeps them alive.

## ID system

| Prefix | Meaning | Defined in |
|--------|---------|------------|
| MS-N | Market Segment | §0.2 |
| CMP-N | Competitor / Comparable | §0.3 |
| PER-N | Persona | §0.4 |
| OPP-N | Differentiation Opportunity | §0.6 |
| FR-N | Functional Requirement | §2.1 |
| NFR-N | Non-Functional Requirement | §2.2 |
| BR-N | Business Rule | §3.4 |
| SF-N | System Flow | §4.1 |
| EF-N | Error Flow | §4.2 |
| EC-N | Edge Case | §4.3 |
| UF-N | User Flow | §5.3 |
| C-N | Component | §5.6 |
| P-N | Page | §5.7 |
| T-N | Page Section | §5.7 |
| D-NNNN | Decision (ADR) | `decisions/` |
| AC-* | Acceptance Criteria | §8 |

Domain events (§3.5) are referenced by PascalCase name — `TemplateImported` — with no ID. §6's error codes (`UPPER_SNAKE_CASE`) and §9's runbooks (`RB-N`) are **document-local**: cite them freely inside their own document, and don't expect them to resolve from elsewhere.

Cite by ID, always: `FR-3`, never "the third requirement". When a section gains an item, assign the next number in sequence and say so out loud — "adding this as FR-3".

**A `D-NNNN` citation means the file exists.** Two decisions reach `decisions/` by different routes and only one of them is immediate: a `[待拍板]` the user **defers** gets its number and its file right then, because §7.2 needs something to point at. A decision the user **settles on the spot** is authored at §7, the consolidation stage — so until §7 runs, leave the `Related ADR` column as `—` rather than citing a number you have not written yet. A cited ID with no file is exactly what `check-example-ids.py` reports as dangling.

---

# Branch: Map

For work that **does not fit one context window** — charted as decision tickets and resolved one per session, until the way to the destination is clear and the Spec branch can run normally. Read `references/map.guide.md` before step 1; templates are `templates/map.template.md` and `templates/map-ticket.template.md`.

**The user brings you here.** 「這件事很大」、「先幫我理清楚」, or §1's fog count showing them what nobody can answer yet and what it blocks. Escalating into a heavier process is their call — §1 makes the cost visible and recommends; it doesn't switch branches on its own. `references/1-problem-scope.guide.md` carries the count.

**Fog** is a decision you can name but **cannot write options for**, which **also blocks §2 onward**. Both conditions — an unphrasable decision that doesn't block is a §7.2 Open Question, and ten decisions you *can* write options for are a spec run however long the list.

**Two modes.**

**Chart** — name the destination first, since it fixes the scope. Then grill **breadth-first** across the whole space rather than deep on one thread. If that surfaces no fog, stop and say so: the work fits, and a map for it is pure overhead. Otherwise write `map.md`, write the tickets you can phrase, wire the blocking edges in a second pass, name the frontier, and stop. Charting resolves nothing.

**Work through** — read the map, take a frontier ticket, claim it before any work, resolve it, record the answer in the ticket and one line on the map. Then update the edges: graduate fog that became phrasable, rule out anything the answer pushed past the destination. **One ticket per session**, research excepted.

**Plan, don't do.** Every ticket resolves a decision. The urge to just build it is the signal you've reached the edge of the map — hand off there. A `task` ticket is the one that does rather than decides, and it earns that by unblocking a decision, never by delivering the destination.

**A HITL ticket only resolves through live exchange with the human.** An agent that answers its own grilling questions has broken the single rule this branch has.

Map items are **questions** and land in `map/`; Tickets items are **slices** and land in `issues/`. Both have blocking edges and a frontier, which is why they get confused — the Map's frontier is what can be **decided** now, the Tickets frontier is what can be **built** now. A Map never writes into `issues/`.

---

# Branch: Tickets

Cuts a spec, a plan, or the current conversation into **tracer bullets** — vertical slices, each declaring the tickets that block it. Read `references/tickets.guide.md` before step 2; it carries the slicing rules, the expand–contract exception, and the spec-to-ticket mapping. Ticket bodies start from `templates/ticket.template.md`, and `examples/automation-template-export/issues/` is a worked set with its dependency graph.

**1. Gather the source.** Work from what's in the conversation. Given a path, an issue number or a URL, fetch it and read the body and comments in full. A `{feature-name}/` spec folder means reading §2 (FR), §5.3 (UF), §7 (ADRs) and §8 (AC) at minimum.

**2. Survey the codebase**, where there is one — greenfield, or a spec sitting outside any repo, skips this step. Ticket titles use the project's own vocabulary, and ADRs in the area you're touching still bind. Note any prefactoring that would make the slices land easier — *make the change easy, then make the easy change* — and give it its own ticket, first.

Where the source is a conversation or a plan rather than a spec that already ran §1, run the prior-art check from `references/1-problem-scope.guide.md` here — searching by domain concept rather than the request's wording, and reporting where you looked. Slicing up work that already exists is the one mistake this step is positioned to catch.

**3. Draft the slices.** Each cuts a narrow but complete path through every layer, lands demoable on its own, and fits in one fresh context window. Give each its blocking edges. A wide refactor goes to expand–contract instead — see the guide.

**4. Quiz the user** on granularity, on whether each blocking edge is real, and on what to merge or split. Iterate to approval.

**5. Publish.** By default, local files inside the spec folder the tickets came from — `<spec-folder>/issues/NN-slug.md`, numbered blockers-first — plus an `issues/README.md` carrying the dependency graph, the blocker table and the **frontier**. Use a real tracker instead where the project has one, with its native blocking links. Either way, name the frontier out loud: the tickets whose blockers are all done, takeable now, in parallel if there's more than one.

Each ticket cites the spec IDs it implements (`FR-3`, `UF-2`, `AC-3.1`) so the implementing agent can read back into the spec. Start each implementation in a fresh context window, working from the ticket.

---

# Branch: Scaffold

Writes `CLAUDE.md`, `CLAUDE.local.md` and `.claude/{rules,skills,agents,references}` into a target repo. `scaffold/scripts/scaffold.py` does the substitution and verifies its own output; your job is the interview and the config.

**1. Interview.** Required: project name, one-line description, stack, install / test / lint / dev commands, entry point, target directory (defaults to cwd). Optional: deploy target, which of the five agents (`planner`, `tester`, `implementer`, `reviewer`, `researcher`), and whether to gitignore `PLAN.md` / `FIX_PLAN.md`. Skip whatever the user already told you.

**2. Write the config** to a JSON file in the scratchpad. Field-by-field schema, the multi-language form, and which stacks have specialised templates: `references/scaffold.guide.md`.

**3. Run it.**

```bash
python3 scaffold/scripts/scaffold.py --config <config.json> --target <target-dir>
```

Add `--dry-run` first when the target is uncertain. The script refuses a target that already holds `CLAUDE.md`, `.claude/`, or `CLAUDE.local.md` — ask the user, then re-run with `--force` on their say-so.

**4. Report** in a few lines: point at the project-overview section CLAUDE.md leaves as a TODO, and name the two git steps — commit `CLAUDE.md .claude/ .gitignore` as team config; `CLAUDE.local.md` stays local and is already gitignored.

When the script exits non-zero it names the problem — fix that and re-run. `references/scaffold.guide.md` maps each failure message to its fix, and explains what each piece of `.claude/` is for when the user asks.
