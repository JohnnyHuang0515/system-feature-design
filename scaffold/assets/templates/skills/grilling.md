---
name: grilling
description: Interview the user relentlessly about a plan, a design, or a change until every branch of the decision tree is resolved — and record what gets settled. Use when the user says grill me, 拷問我, 幫我想清楚, stress-test this, poke holes in this, or asks to think a change through before building it. Also use before any non-trivial change where the user has a direction but not the details.
---

# Grilling

Writing software is a few hundred small decisions in a row — what happens on empty input, what happens when the connection drops, what happens to the half-written record. Handing a vague idea to an agent hands it those decisions too, and it will answer them all plausibly and invisibly.

This skill inverts that. **You interrogate; the human decides.** They don't have to arrive with a finished design — finding the holes is your job. Theirs is to call each one.

## Before the first question

Read the code the change touches — not a sample of it. Follow the imports out from the obvious file until you reach the edges of what this change can affect, including the paths that *consume* the thing being changed. A refund path that never recomputes a discount is invisible from the pricing file, and it is exactly the sort of thing that turns a clean design into a money bug three weeks later.

Read `CONTEXT.md` if it exists, and the ADRs covering this area — a decision already made and recorded is not a branch to re-open.

**Name the files you read, before your first question.** It is the cheapest way for the human to catch you grilling from a partial picture.

## The loop

Map the work as a **design tree**: every decision branches into the decisions hanging off it. Then work the tree in **rounds**.

**The frontier is every decision whose prerequisites are already settled** — the questions you can ask *now* without guessing at an answer you haven't heard. **Ask the whole frontier in one round**, numbered, each carrying your recommended answer.

```
❓ **Q1** — **<標題>**:<問題本身,可以多段,可以帶選項>

➡️ <你建議的答案,以及一句為什麼>
```

**A question whose answer depends on another question still open this round belongs to a later round.** That constraint is what makes batching safe: the round is exactly the frontier, never a convenient handful. Get it wrong and you are asking the human to answer something you don't yet have the context to have asked properly.

Each round's answers reshape the tree — settled decisions push the frontier outward and unblock what depended on them. Recompute and ask the next round. **Every question carries your recommended answer**; a bare question makes the human do the generating too.

**A fact you can look up, you look up** — read the code, run the query, check the config. Where finding it is slow, send it off and **keep going**: only the questions downstream of that fact wait, so ask the rest of the frontier now rather than blocking the whole round on one lookup. Only *decisions* go to the human; burning their attention on what you could have found is what makes them stop answering.

**Act only once they confirm you have a shared understanding** — the whole tree, not a partial one.

Ask in whatever language the user is writing in.

## What to grill about

Push on the places code usually rots:

- **Boundaries** — empty, zero, one, maximum, off-by-one around every limit
- **Failure** — what the user sees, what state is left behind, what can be retried
- **Repeats** — a double-clicked button, a retried webhook, a re-run job
- **Concurrency** — two people editing the same thing, order of arrival mattering
- **Irreversibility** — anything deleting, locking, publishing, or charging
- **Naming** — the moment two words are used for one concept, stop and settle it

Each round opens the next layer. That is the point of the tree — a question you couldn't have asked before the last round is the sign it's working.

## Leaving a paper trail

A grilling session produces decisions worth more than the conversation that made them, and a conversation is not a record. Run the **`domain-glossary`** skill alongside this one and **write files as each answer lands**, not at the end:

- A term the human sharpens, or one you find doing two jobs → **write it into `CONTEXT.md` before the next question.** Create the file if it doesn't exist.
- A decision that is **hard to reverse**, **surprising without context**, and **the result of a real trade-off** → **write an ADR under `docs/adr/`.** All three conditions, or skip it.

Deliberately running without a trail — a throwaway or exploratory session — is fine, but say so up front so the human knows nothing is being kept.

**Completion criterion for the trail.** Before reporting the session done, state the **paths you wrote**, and confirm two things: every term settled during the session appears in `CONTEXT.md`, and every decision clearing all three ADR conditions has a file. Summarising the decisions in your reply is not the trail — a reply is gone next session, which is the entire problem this exists to solve. If you catch yourself writing 「記錄位置：…」 about a file you did not create, you have not left a trail.

The payoff compounds: the next session opens with the vocabulary and the settled decisions in hand instead of spending its first half rediscovering them.

## When it's done

The tree is settled when **the frontier is empty** — no answer you hold opens a branch you haven't put to the human — and the human says the picture matches theirs. Running out of things to ask is not the same as running out of the human's patience — if you stop early, say which branches you left unexplored rather than presenting a partial tree as a complete one.

Then hand off:

- Small enough to build now → `planner`, or straight to the slice if it's trivial
- Big enough to need writing down → a spec, and from there tickets
- The question turned out to need a runnable answer → the **`prototype`** skill, and come back

A session that ends with you writing code before the human confirmed is a session that failed, however good the code.
