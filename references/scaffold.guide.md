# Scaffold guide

Disclosed reference for the **Scaffold** branch: the config schema, the failure map, and what each piece of `.claude/` is for.

## Config schema

```json
{
  "project_name": "orderflow",
  "project_description": "Internal order management API",
  "stack": "Python 3.12 + FastAPI + PostgreSQL",
  "languages": ["python"],
  "test_frameworks": ["pytest"],
  "entry_point": "src/orderflow/main.py",
  "install_cmd": "uv sync",
  "test_cmd": "pytest",
  "lint_cmd": "ruff check .",
  "dev_cmd": "uvicorn src.orderflow.main:app --reload",
  "deploy_target": "Fly.io",
  "agents": ["planner", "tester", "implementer", "reviewer", "researcher"],
  "gitignore_plans": true
}
```

`deploy_target`, `agents`, `gitignore_plans`, `build_cmd` and `deploy_cmd` are optional — everything else is required.

- `deploy_target` — omitting it skips the deploy skill entirely.
- `build_cmd` / `deploy_cmd` — only the deploy skill reads them, so they matter only alongside `deploy_target`. Left out, each renders as a `# TODO` line in the shipped skill: a visible gap the user fills, rather than a plausible wrong command. **Ask for both whenever `deploy_target` is set.**
- `agents` — the five names, and the four pipeline roles (`planner`, `tester`, `implementer`, `reviewer`) ship together or not at all. CLAUDE.md and the shipped rules route work through all four, so a subset would write a repo that dispatches agents it does not have; the script refuses it. `["researcher"]` alone is legal, and CLAUDE.md then carries no pipeline line.
- `gitignore_plans` — defaults to true.

**Specialised templates** exist for languages `python` / `typescript` / `javascript` / `go`, and two testing ones: `pytest`, and a JS-runner template shared by `jest` / `vitest` / `mocha`. Anything else resolves to the generic template.

**Multi-language repos** list every entry, and the script emits one `code-style-{lang}.md` and one `testing-{framework}.md` per entry:

```json
{ "languages": ["typescript", "python"], "test_frameworks": ["jest", "pytest"] }
```

The singular `"language"` / `"test_framework"` string form still parses.

## Failure map

The script exits non-zero with the reason. Fix the named cause and re-run it — hand-writing the files it would have written defeats the point of a deterministic scaffold.

Two of the rows below offer a choice between registering a template as live and demoting it to `in-progress/`. **A run passing is what decides it** — live means tested, not finished. See `Three states` below.

| Message | Cause and fix |
|---|---|
| Existing Claude files detected | The target already holds `CLAUDE.md`, `CLAUDE.local.md`, or `.claude/{agents,rules,skills,references}`. Ask the user, then re-run with `--force`. (`.claude/settings.local.json` belongs to Claude Code and never triggers this.) |
| Template not found | The skill's own files are incomplete — tell the user to reinstall. |
| VALIDATION FAILED — unreplaced placeholders | Rare. The files landed with raw `{{FOO}}` in them; report the specific placeholders and ask the user what they should be. |
| Config missing required fields | A required key is absent from the JSON. Add it and re-run. |
| Skill templates nothing ships | A `.md` sits at the top of `templates/skills/` that no config path emits. Add it to the shipped list, or move it to `in-progress/`. |
| `X` is in skills/in-progress/ but the scaffold still ships it | The folder and the shipped list disagree. Pick one. |

## Anatomy of the output

### CLAUDE.md
The entry point, committed and team-shared. It carries what would otherwise cost an hour of exploring: what the project is and why it exists (2–3 sentences), the install / test / lint / dev commands, pointers into `rules/`, and the deprecated patterns and legacy paths to steer around.

Keep it current and keep it project-specific. Tutorials belong in the code or the README, and a line a human could already guess is a line that dilutes the rest.

### CLAUDE.local.md
Personal overrides, gitignored, one per developer — "I use pyenv with Python 3.12", "I'm mid-way through the auth refactor, pick up there", "treat 'quick fix' as skip-the-tests".

### .claude/rules/
One topic per file, in depth — `code-style-{lang}.md`, `testing-{framework}.md`, `api-conventions.md`, `codebase-design.md`. Modular so CLAUDE.md can point at one file for one concern, and so a single area can be revised without touching the rest. Grow it as the project earns it: `commit-style.md`, `database.md`, `frontend.md`.

`codebase-design.md` is the odd one out: it carries **vocabulary**, not conventions — module / interface / depth / seam / adapter / leverage / locality, plus the **deletion test**. `planner`, `implementer` and `reviewer` all read it so the three of them describe module shape the same way. It ships on every scaffold because the words cost nothing until a module is being designed.

### .claude/skills/
Repeatable workflows Claude triggers on its own. A folder with a `SKILL.md`, YAML frontmatter (`name`, `description`) and a markdown body. Anything that fires once, or reads as documentation, belongs in `rules/` instead.

Eight ship on every scaffold, plus `deploy` when a deploy target is configured:

| Skill | What it's for |
|---|---|
| `grilling` | The relentless interview, before any non-trivial change. Works a design tree in **rounds** — each round asks the whole frontier, every question carrying a recommended answer; facts get looked up, decisions go to the human; nothing gets built until the tree is settled. Drives `domain-glossary` so the session leaves a paper trail instead of evaporating. |
| `diagnosing-bugs` | Six-phase discipline for hard bugs. Its whole thesis is **Phase 1 is the skill** — no red-capable feedback loop, no hypothesis. Gives 10 ranked ways to build one and refuses to proceed without a command it has already run. |
| `domain-glossary` | Builds and sharpens `CONTEXT.md`, the project's shared language, and records hard-to-reverse decisions as ADRs. The `_Avoid_` line under each term is what stops three names for one concept. |
| `improve-codebase-architecture` | Periodic upkeep — scans for shallow modules worth deepening, presents them as a visual HTML report with before/after diagrams and a recommendation strength, then works the one the user picks. |
| `prototype` | Throwaway code answering one design question — a pure logic module behind one self-contained HTML file the decision-owner drives themselves, or several radically different UI variants embedded in an existing page behind `?variant=`. Kept afterwards as a primary source on a throwaway branch. |
| `handoff` | Compacts a conversation into a document in the OS temp dir so a fresh session can continue. References other artifacts rather than duplicating them; redacts secrets. |
| `resolving-merge-conflicts` | Hunk by hunk, resolved by intent traced to each side's primary source. Never `--abort`. |
| `security-review` | Trust boundaries, classic vulnerabilities, auth and secrets. |

`domain-glossary` is the bridge back to the Spec branch: §3's entities and business rules seed `CONTEXT.md`, and `decisions/NNNN-*.md` seed `docs/adr/`. From then on the repo's copies are the living ones.

#### Three states, and the folder is which

A skill template ships, or it doesn't yet, or it used to:

| Where it sits | State |
|---|---|
| `templates/skills/*.md` | **live** — ships on every scaffold, or on its config key |
| `templates/skills/in-progress/` | **drafted** — being written, tested, or waiting on a decision |
| `templates/skills/deprecated/` | **retired** — kept so the reasoning survives, and so a superseding skill can point at it |

Neither subfolder reaches a target repo. `scaffold.py` enforces it both ways: a live template nothing ships is an error, and a name sitting in a subfolder while still on the shipped list is an error rather than a silent preference.

Both folders arrive with their first occupant. A skill goes to `in-progress/` the moment it stops being ready — half-written, or failing the run that would have proved it — which is what keeps the live set meaning *tested*. It comes back out when a run passes, not when it reads well.

### .claude/agents/
Specialised roles, each in its own context window with its own tool scope — which is the point: a reviewer that cannot edit code, an implementer uncontaminated by the planner's exploratory reads.

The five defaults map to the phases of any engineering task — **plan / test / do / check / research**:

- `planner` writes `PLAN.md` or `FIX_PLAN.md`, self-reviews it against four angles (scope / technical soundness / completeness / risk), and stops for human approval. A bug whose cause isn't already visible goes to the `diagnosing-bugs` skill instead.
- `tester` agrees the **seams** with the human, then writes the failing test for **one vertical slice**.
- `implementer` writes the minimum production code that turns that slice green, and hands back.
- Those two **alternate per slice** until the work is done — see below.
- `reviewer` checks the whole diff along **one named axis per dispatch** — Standards or Spec. Dispatch it twice in parallel and present both reports side by side without merging. (A sub-agent can't reliably spawn its own sub-agents, so the fan-out belongs to the caller; keeping the axes in separate windows is the point either way.)
- `researcher` runs as a parallel track for heavy file reads and external lookups.

**Why tester and implementer alternate.** Writing the whole suite up front and then all the implementation is *horizontal slicing*: bulk tests verify imagined behaviour, they test the shape of things rather than what users do, and they freeze a test structure decided before anyone understood the implementation. One test → one implementation → repeat lets each cycle respond to what the last one taught you. `.claude/references/testing-tdd.md` carries the loop rules and the seam gate.

The separation is what buys you a plan-stage quality gate (cheaper than fixing code later), tests that record the approved intent before production code exists, an implementer that isn't re-litigating scope while it codes, and a durable `PLAN.md` you iterate on by editing markdown rather than re-prompting.

**Five is the ceiling, not a target.** Anthropic recommends 3–5 for most workflows; token cost scales linearly with agent count while benefit does not. This bundle sits at the top of that range because `tester` earns a distinct seat — translating an approved plan into executable tests is its own job. Split further only against a concrete pain point, such as a dedicated `prompt-reviewer` on an AI-heavy codebase.

Design rules for any agent you add: one responsibility each; an action-oriented description ("Use PROACTIVELY when…") so Claude auto-delegates; tools scoped to the role (`planner` / `reviewer` / `researcher` read-only on `Read, Grep, Glob, Bash`; `tester` writes test files; `implementer` writes both); `sonnet` by default, `opus` for the heaviest reasoning, `haiku` for simple scans.

### .claude/references/

Three files the **agents** read mid-task — not human documentation, and not loaded unless
an agent reaches for them:

| File | Read by | Holds |
|---|---|---|
| `plan-schema.md` | `planner` writes to it, `tester` and `implementer` read from it | the exact shape of `PLAN.md` and `FIX_PLAN.md` — every section, including the verification checklist and the four-angle self-review |
| `testing-tdd.md` | `tester`, `implementer`, `reviewer` | the red-green discipline the pipeline runs on, and what counts as a seam |
| `review-lenses.md` | `reviewer` | the per-lens checklists a diff gets read against |

They ship on every scaffold. The scaffolder refuses to run when one is missing rather than
writing a repo whose agents point at documents it does not have.

### Not generated here
`settings.json` / `settings.local.json` are Claude Code's own — direct the user to `/init` and the permissions UI. `commands/` is too project-specific to template; help the user write one as a one-off.

## Writing rules that pull their weight

The test: **a human skimming the rule learns something new about this specific project.**

| Pulls its weight | Why |
|---|---|
| "pytest", "SQLAlchemy 2.0" | Specific — names the actual thing |
| "We don't use Redux, Zustand, or Jotai. If you think you need one, raise it with the team first." | Opinionated, and says what to do at the fork |
| "We ship daily, we fix in prod, we iterate." | Honest about constraints — sets realistic review expectations |
| "Default to server components; add `use client` only for state, effects, or browser APIs." | Actionable — tells Claude what to do differently |

Lines like "write clean code", "follow best practices", "use descriptive names" describe a world everyone already agrees on. Replace each with the project's actual answer: which convention, whose practice, `camelCase` or `snake_case`.

## Evolving the folder

Start minimal and let real needs pull files in — a pattern that keeps coming out wrong earns a rule, a workflow that keeps repeating earns a skill, a review you keep wishing were independent earns an agent. Speculative structure dilutes the signal that is actually there.

## Git steps

```bash
git add CLAUDE.md .claude/ .gitignore
git commit -m "Add Claude Code configuration"
```

`CLAUDE.local.md` and `.claude/settings.local.json` stay local — both are gitignored.
