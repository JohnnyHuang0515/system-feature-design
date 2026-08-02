# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

<!-- TODO: Replace above with 2–3 sentences on what this project does, who uses it, and what's unusual about it. This is the single most valuable section. -->

---

## Behavioral guidelines

*From [Karpathy-inspired guidelines](https://github.com/forrestchang/andrej-karpathy-skills). For trivial tasks, use judgment.*

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: *"Would a senior engineer say this is overcomplicated?"* If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

**The test:** Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

## Project

**Stack:** {{STACK}} · **Tests:** {{TEST_FRAMEWORK}}

**Commands:** install `{{INSTALL_CMD}}` · test `{{TEST_CMD}}` · lint `{{LINT_CMD}}` · dev `{{DEV_CMD}}`

**Rules:** see `.claude/rules/` (code-style, testing, api-conventions, codebase-design)

**Agents:** for non-trivial work, `planner` → human approves → then **`tester` and `implementer` alternate one vertical slice at a time** (one failing test → make it green → next slice) → review the whole diff by **dispatching `reviewer` twice in parallel, once with `axis: Standards` and once with `axis: Spec`**, and present both reports one after the other under their own `## Standards` / `## Spec` headings, each keeping its own verdict. Trivial changes skip the pipeline. Reconciling the two axes is the human's call, not a combined verdict.

**Skills:** `grilling` before any non-trivial change — let it interrogate you until the decision tree is resolved, and it records what gets settled · `diagnosing-bugs` for any bug that resisted a first glance (build the feedback loop before theorising) · `domain-glossary` to sharpen a fuzzy term into `CONTEXT.md` or record an ADR · `improve-codebase-architecture` as upkeep every few days · `prototype` to answer a design question with throwaway code · `handoff` to carry context into a fresh session · `resolving-merge-conflicts` · `security-review`

**Shared language:** read `CONTEXT.md` (if present) before naming anything, and respect ADRs in `docs/adr/` for the area you're touching.

<!-- TODO:
- [ ] Describe repo layout if non-obvious (src/, tests/, etc.)
- [ ] List external services (DB, APIs, queues)
- [ ] Note project-specific jargon
-->
