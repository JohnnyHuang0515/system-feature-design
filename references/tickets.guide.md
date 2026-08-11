# Tickets guide

Disclosed reference for the **Tickets** branch: how to cut a spec into **tracer bullets**, how to declare **blocking edges**, and the one case where vertical slicing is the wrong shape.

## Tracer bullets

A **tracer bullet** is a narrow but *complete* path through every layer — schema, API, UI, tests — that lands working. Four rules:

- **Each slice cuts vertically.** One slice carries its own schema change, its own logic and its own screen. A slice of one layer is not a slice.
- **A completed slice is demoable or verifiable on its own.** Finish it, open the browser, see it work.
- **Each slice fits in a single fresh context window.** The implementing agent starts clean and reads only that ticket. Count it rather than eyeballing it: **one entity, one or two endpoints, one screen** is the shape that fits. A slice you can only describe by listing three or more of each is two tickets.
- **Prefactoring goes first**, as its own ticket. *Make the change easy, then make the easy change.*

The failure this prevents: an agent left to plan on its own builds every table, then every service, then the screens — and nothing is testable until the last step, so a wrong table surfaces days late.

### Enabling work rides inside the first slice that needs it

Auth, session handling, a base schema, an API client — work that exists only to serve later slices is **not a slice of its own**. Given its own ticket it becomes a layer that blocks everything, which is the layer-first pattern again with a ticket number attached.

The test: **can a user observe the deliverable?** "Employee can log in and see an empty leave list" is a tracer bullet — it cuts SSO, the session, one endpoint and one screen, and you can demo it. "Set up authentication and role-based access control" is a layer: nothing to look at, and every other ticket waits on it.

So fold the enabling work into the first slice that needs it, and let the slices after that inherit it through their blocking edge.

**Prefactoring is the exception, and it is narrow.** Prefactoring reshapes code that *already exists* to make the coming change easy — it adds no behaviour, so there is nothing for a user to observe and its own ticket is right. Building something new that later slices will use is not prefactoring, however foundational it feels.

```
Layer-first (what to avoid)          Tracer bullets
┌───────────────────────┐            ┌──────┐ ┌──────┐ ┌──────┐
│ all schema            │            │schema│ │schema│ │schema│
├───────────────────────┤            │logic │ │logic │ │logic │
│ all logic             │            │  UI  │ │  UI  │ │  UI  │
├───────────────────────┤            │ test │ │ test │ │ test │
│ all UI                │            └──────┘ └──────┘ └──────┘
└───────────────────────┘             login   add-to-cart  checkout
 testable only at the end             each one testable on landing
```

## Blocking edges

Every ticket declares the tickets that must land before it can start. A ticket with none starts immediately.

Work the **frontier**: any ticket whose blockers are all done. Edges are what make parallelism safe — two tickets on the frontier can go to two agents at once. A purely linear chain is just a frontier of one.

Derive edges from real gates, not from convenience. "Checkout needs a cart to exist" is an edge; "I'd rather do them in this order" is not.

## Wide refactors are the exception

A **wide refactor** is one mechanical change — renaming a column, retyping a shared symbol — whose **blast radius** fans across the codebase, so a single edit breaks thousands of call sites and no vertical slice can land green. Forcing it into a tracer bullet produces a ticket that cannot be finished.

Sequence it as **expand–contract** instead:

1. **Expand** — add the new form beside the old. Nothing breaks. One ticket.
2. **Migrate** — move call sites over in batches sized by blast radius (per package, per directory). Each batch is its own ticket, blocked by the expand, and CI stays green batch to batch because the old form still exists.
3. **Contract** — delete the old form once no caller remains. One ticket, blocked by every migrate batch.

When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket — green is promised only there. Say so in the tickets.

## Quiz the user before publishing

Present the breakdown as a numbered list. Per ticket: **title**, **blocked by**, **what it delivers** (the end-to-end behaviour it makes work).

Then ask three things:

- Does the granularity feel right — too coarse, too fine?
- Are the blocking edges real? Does each ticket depend only on what genuinely gates it?
- Anything to merge or split further?

Iterate until the user approves. Publishing an unapproved breakdown wastes the tracker.

## Publishing

Ticket bodies come from `templates/ticket.template.md` — the single source of truth for the format. Only the destination changes:

**Local files** (default) — one file per ticket at `<spec-folder>/issues/NN-slug.md`, numbered from `01` in dependency order, blockers first. One ticket per file. The tickets live **inside the spec folder they came from**, whatever it is called; with no spec folder, put them under a `{feature-name}/issues/` you agree with the user.

Alongside them write `issues/README.md`: the dependency graph, the table of tickets with their blockers, and the **frontier** — which tickets are takeable right now, and which become takeable as each lands. That is what makes parallel work visible at a glance instead of requiring seven files to be opened.

A worked set sits in `examples/automation-template-export/issues/`.

**A real tracker** (GitHub via `gh`, Linear, Jira) — one issue per ticket, published in dependency order so each ticket's edges reference real identifiers. Use the platform's native blocking or sub-issue relationship where it has one; otherwise keep the "Blocked by" section as text. Apply the `ready-for-agent` label — these tickets are agent-grabbable by construction. Leave the parent issue alone.

## Keep tickets out of date-able

**No file paths, no code snippets.** Both go stale within days, and a ticket carrying a stale path sends the implementing agent to the wrong file with full confidence.

The exception is a snippet a **prototype produced** that encodes a *decision* more precisely than prose can — a state machine, a reducer, a schema, a type shape. Inline it, note where it came from, and trim to the decision-rich part. A snippet you wrote to illustrate an idea is prose with syntax, and goes stale like a path does.

## Coming from a spec

When the source is a spec folder, the mapping is mostly mechanical:

| Spec | Ticket |
|---|---|
| §5.3 UF-N (user flow) | usually one tracer bullet each — a user flow *is* a vertical path |
| §2.1 FR-N | what the slice delivers |
| §8 AC-* | the ticket's acceptance criteria, copied verbatim |
| §3.2 entities, §6.2 endpoints | the layers the slice cuts through — named, never as file paths |
| §7 ADRs | constraints the slice honours; reference by `D-NNNN` |

Cite spec IDs in the ticket so the implementing agent can read back into the spec.

### When the spec is partial

Entering mid-way, the spec often stops short — requirements written, §5.3 user flows and §8 acceptance criteria never reached. §8 is the one that matters: **acceptance criteria are the ticket's entire verification surface**, and inventing them silently hands the implementing agent criteria that look authoritative and aren't.

So say what's missing before slicing, and offer the choice:

- **Write §8 first** — the shorter path when the spec is nearly there, and it makes every ticket's criteria citable.
- **Slice now with derived criteria** — fine, provided the ticket is honest about it. Put one line above the criteria — `Derived from §2, not from §8: confirm before building` — and leave the criteria themselves unmarked. The user confirms them by approving the breakdown, which is the same gate §8 would have been.

  Don't reach for `[需確認]` here. That marker belongs to the spec's own lifecycle, where it must be gone before a document is written, and the full-spec review's Check 0 greps every `*.md` for it and calls each hit an Error — a ticket carrying it would fail a review it was never part of.

Missing §5.3 is cheaper: derive the user flows to slice against, and leave the `UF:` line out rather than citing an ID that doesn't exist. Missing §7 the same way — no ADRs means no `D-NNNN` line, and worth mentioning, because the implementing agent may re-litigate decisions nobody recorded.
