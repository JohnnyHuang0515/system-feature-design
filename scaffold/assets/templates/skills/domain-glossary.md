---
name: domain-glossary
description: Build and sharpen this project's shared language in CONTEXT.md, and record hard-to-reverse decisions as ADRs. Use when a term is fuzzy or overloaded, when the same concept has three names in the codebase, when naming a new module or entity, or when another skill needs to keep the domain model current.
---

# Domain Glossary

A shared language between the humans and the agents. Agents dropped into a project have to infer the jargon as they go, so they use twenty words where one would do — and name variables, functions and files inconsistently while they're at it. `CONTEXT.md` fixes that.

The payoff compounds: names stay consistent, the codebase gets easier to navigate, and every session spends fewer tokens saying the same thing.

> "There's a problem when a lesson inside a section of a course is made 'real' — given a spot in the file system"
> → **"There's a problem with the materialization cascade."**

This is the *active* discipline — challenging terms, stress-testing them, writing them down the moment they crystallise. Merely *reading* `CONTEXT.md` for vocabulary is a one-line habit any skill can do; this skill is for when the model is being **changed**.

## Files, created lazily

```
CONTEXT.md              ← the glossary, repo root
docs/adr/0001-slug.md   ← decisions, sequentially numbered
```

Create either only when there's something to write. No `CONTEXT.md` yet → create it when the first term is resolved. No `docs/adr/` → create it when the first ADR is needed.

Where a repo has several distinct domains, a `CONTEXT-MAP.md` at the root lists each context, where its `CONTEXT.md` lives, and how they relate (which events flow between them, which types they share).

## During a session

**Challenge against the glossary.** A term that conflicts with what's already written gets called out immediately: *"your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"*

**Sharpen fuzzy language.** A vague or overloaded word gets a precise canonical replacement proposed: *"you're saying 'account' — do you mean the Customer or the User? Those are different things."*

**Stress-test with concrete scenarios.** When relationships are being discussed, invent scenarios that probe the edges and force precision about where one concept ends and the next begins.

**Cross-reference the code.** When the human states how something works, check whether the code agrees. A contradiction gets surfaced: *"your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"*

**Write it down inline.** A resolved term goes into `CONTEXT.md` right then. Batching them up loses the ones that felt obvious at the time.

## CONTEXT.md format

```md
# {Context name}

{One or two sentences: what this context is and why it exists.}

## Language

**Order**:
A customer's request for goods, from placement through fulfilment.
_Avoid_: purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: bill, payment request
```

Rules:

- **Be opinionated.** Several words for one concept → pick the best and list the rest under `_Avoid_`. That line is what stops the drift.
- **Definitions stay tight** — one or two sentences. Define what it **is**, not what it does.
- **Only terms specific to this project.** Timeouts, error types and utility patterns are general programming concepts and don't belong, however much the project uses them. The test: is this unique to this context, or would it mean the same thing in any codebase?
- **Group under subheadings** when natural clusters appear; a flat list is fine when they don't.

**`CONTEXT.md` is a glossary and nothing else.** It carries no implementation details, no spec, no scratch notes, no decisions — those have their own homes, and the moment it becomes a dumping ground it stops being readable at a glance, which was the whole point.

## ADRs

Offer one only when **all three** are true:

1. **Hard to reverse** — changing your mind later costs something real
2. **Surprising without context** — a future reader will ask "why did they do it this way?"
3. **The result of a genuine trade-off** — there were real alternatives and one was chosen for reasons

Miss any one and skip it. Code style, settled industry practice and pure preference are not ADRs.

Keep them small. An ADR can be a single paragraph — the value is recording *that* a decision was made and *why*, not filling in sections:

```md
# {Short title of the decision}

{1–3 sentences: the context, what was decided, and why.}
```

Add `Status` frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) when decisions get revisited, **Considered Options** when the rejected alternatives are worth remembering, and **Consequences** when a downstream effect isn't obvious. Most ADRs need none of them.

Number by scanning `docs/adr/` for the highest and incrementing.

## Seeding from a spec

Where the project was designed with a `{feature}/` spec folder, §3 domain-model already did this work at design time: its entities, business rules and events are the first draft of the glossary, and §7's ADRs are the first decisions. Carry them over rather than starting blank — §3.2 entity names become `CONTEXT.md` terms, and `decisions/NNNN-*.md` files move to `docs/adr/`.

From then on the repo's `CONTEXT.md` is the living one. When it and the spec disagree, the code and its glossary have moved on — update the spec or note it as superseded.
