# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

<!-- TODO: Replace above with 2–3 sentences on what this project does, who uses it, and what's unusual about it. This is the single most valuable section. -->

---

## Behavioral guidelines

*From [Karpathy-inspired guidelines](https://github.com/forrestchang/andrej-karpathy-skills). For trivial tasks, use judgment.*

### 1. Think Before Coding

**Say what you assumed, and put the fork to the human.**

Before implementing:
- State your assumptions explicitly. Where you are uncertain, ask.
- Where the request reads two ways, present both and let the human pick.
- Where a simpler approach exists, say so. Push back when warranted.
- Where something is unclear, stop and name what is confusing.

### 2. Simplicity First

**The minimum code that solves the problem asked for.**

- Build what was asked, and stop there.
- Introduce an abstraction on its second caller.
- Add configurability when something needs configuring.
- Handle the failures that can actually happen.
- Where 200 lines could be 50, rewrite it as 50.

Ask yourself: *"Would a senior engineer say this is overcomplicated?"* If yes, simplify.

### 3. Surgical Changes

**Every changed line traces to the request. Clean up after your own edits.**

When editing existing code:
- Leave adjacent code, comments and formatting as they are.
- Refactor what the change requires, and leave the rest working as it is.
- Match existing style, even where you would do it differently.
- Where you spot unrelated dead code, mention it and leave it in place.

When your changes create orphans:
- Remove the imports, variables and functions **your** edits made unused.
- Leave pre-existing dead code alone until someone asks for it.

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

**Stack:** {{STACK}} · **Tests:** {{TEST_FRAMEWORK}} · **Entry point:** `{{ENTRY_POINT}}`

**Commands:** install `{{INSTALL_CMD}}` · test `{{TEST_CMD}}` · lint `{{LINT_CMD}}` · dev `{{DEV_CMD}}`

**Rules:** see `.claude/rules/` (code-style, testing, api-conventions, codebase-design)

{{PIPELINE_LINE}}

**Shared language:** read `CONTEXT.md` (if present) before naming anything, and respect ADRs in `docs/adr/` for the area you're touching.

<!-- TODO:
- [ ] Describe repo layout if non-obvious (src/, tests/, etc.)
- [ ] List external services (DB, APIs, queues)
- [ ] Note project-specific jargon
-->
