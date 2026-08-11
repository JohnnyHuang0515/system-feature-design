# Reference Guide: the Map branch

> Instructions here are English; the quoted blocks are scripts spoken to the user — use them as written.
> Pairs with `templates/map.template.md` and `templates/map-ticket.template.md`.

## Purpose

Chart work that **does not fit one context window** as a map of decision tickets, then resolve them one per session until the way to the destination is clear.

A Map holds **questions**. It is not a plan of what to build — that is the Tickets branch, and confusing the two is the main way this goes wrong. See `Not the Tickets branch` at the bottom.

## When it runs

**The user asks for it.** Either they arrive knowing the work is large — 「這件事很大,先幫我理清楚」 — or §1's fog count showed them decisions nobody can answer yet, they saw what those block, and they chose this. Both routes end in the user saying so; §1 recommends and does not switch on its own.

Where the work fits one window, it does not need a map and charting one is pure overhead. A long list of answerable questions is a spec run, not a map — and if breadth-first grilling below turns up no fog at all, say so and stop rather than charting anyway.

## Plan, don't do

Every ticket resolves a **decision**. The map is done when nothing is left to decide before someone goes and builds — not when the thing is built.

**The urge to just do the work is the signal you have reached the edge of the map.** That is the moment to hand off, not to keep going. A map session that ends with production code has failed, however good the code.

## Name the destination first

The destination is what reaching the end of this map looks like — and because it fixes the scope, it is settled before any ticket exists.

It varies. A spec to hand to the Spec branch. A single decision to lock before planning starts. A change made in place, like a data-model migration. Name it in one or two lines; every session re-reads it before choosing a ticket.

```
在開票之前,先定一件事:這張地圖走到底,產出的是什麼?

我的理解是 [X]。對嗎?
還是你要的其實是 [Y]?
```

## The map

One file — `{feature-name}/map.md`, from `templates/map.template.md`. Five sections: **Destination**, **Notes**, **Decisions so far**, **Not yet specified**, **Out of scope**.

**The map is an index, not a store.** A decision lives in exactly one place — its own ticket — and the map carries one line and a link. Restating it in both means two copies drifting apart, and the map stops being loadable at a glance, which is its only job.

Open tickets are **not listed on the map**. They are files in `map/`, found by looking.

**Refer to tickets by name, never by bare number.** A wall of `03, 04, 07` is illegible; names read at a glance. The number rides inside the link.

## Tickets

One file each: `{feature-name}/map/NN-question-slug.md`, from `templates/map-ticket.template.md`. The body is **the question**, sized to one session.

Each declares the tickets that block it. A ticket is **unblocked** when every ticket blocking it is resolved. The **frontier** is the open, unblocked, unclaimed tickets — the edge of what can be decided now.

**Claim before working**, by marking the ticket claimed in its own file, so a parallel session skips it. An open unclaimed ticket is takeable.

The answer is not part of the question. It is written on resolution.

### Four types

Every ticket is **HITL** — worked live with a human who speaks for themselves — or **AFK**, driven alone.

| Type | Mode | For |
|---|---|---|
| `grilling` | HITL | The default. A decision settled by interrogation, a round of questions at a time |
| `research` | AFK | A fact a decision waits on, living outside this working directory — docs, a third-party API, prior art |
| `prototype` | HITL | 「長什麼樣」/「怎麼運作」 questions that words keep failing to settle. Cheap throwaway artifact to react to |
| `task` | either | Manual work blocking a decision — provisioning access, signing up for a service so its API can be judged, moving data so its shape is visible |

**A HITL ticket only resolves through that live exchange. Never stand in for the human's side of it** — an agent that answers its own grilling questions has broken the one rule this branch has. If the human isn't there, the ticket stays open.

`task` is the only type that *does* rather than decides, and it earns its place by unblocking a decision — never by delivering a piece of the destination. Work that delivers the destination is a Tickets slice.

## Fog of war

The map is **deliberately incomplete**. Beyond the live tickets are the decisions you can tell are coming but cannot yet pin down, because they hang on questions still open. Those go in **Not yet specified** — loosely, as an area to revisit.

**Fog or ticket?** The test is whether you can **state** the question precisely now — *not* whether you can answer it.

- **Ticket** when the question is already sharp, even if it is blocked and unactionable.
- **Not yet specified** when you can't phrase it that sharply yet.

Leave fog at the size you can actually see it. It is coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

Resolving a ticket clears the fog ahead of it. Whatever has become phrasable **graduates into fresh tickets** and leaves **Not yet specified**, so it lives in exactly one place.

## Out of scope

Fog only ever gathers *toward* the destination. Work past the destination is not fog — it is out of scope, and it gets its own section.

**Scope, not sharpness, lands it here**, and it **never graduates**. It returns only if the destination is redrawn, and then as a fresh map rather than a resumption.

A ticket that turns out to sit past the destination — mis-scoped while charting, or exposed by an answer — is **closed**, with one line in **Out of scope** giving the gist and the reason. It stays out of **Decisions so far**, which records the route actually walked; a scope boundary is not a step on it.

Where the user themselves declines the request, it also earns an entry in `.out-of-scope/` — see `references/1-problem-scope.guide.md`.

## Mode: chart the map

1. **Name the destination.** Grill until it is settled. Scope depends on it, so nothing else starts first.
2. **Map the frontier — breadth-first.** Fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first ones takeable now. Going deep here produces a beautifully resolved corner of a map you haven't drawn.
3. **If this surfaces no fog, stop.** The way is already clear and the work fits one session — say so and offer the Spec branch instead. Charting a map for work that doesn't need one is the failure mode of this branch.
4. **Write the map**: Destination and Notes filled, Decisions so far empty, fog sketched into Not yet specified.
5. **Write the tickets you can specify now**, then wire the blocking edges in a **second pass** — a ticket needs its number before another can reference it.
6. **Name the frontier out loud** and stop. Charting is one session's work and resolves nothing.

## Mode: work through the map

1. **Read `map.md`** — the low-resolution view. Not every ticket body.
2. **Choose a ticket.** The user's, if they named one; otherwise the first on the frontier. **Claim it before any work.**
3. **Resolve it.** Zoom on demand: fetch the full body of a related or resolved ticket when you need it, not upfront. Use the skills the Notes section names.
4. **Record the resolution** in the ticket, mark it resolved, and append one line plus a link to the map's **Decisions so far**.
5. **Update the map's edges** — add tickets the answer surfaced, graduate fog that became phrasable and clear it from Not yet specified, rule out-of-scope anything the answer pushed past the destination, and revise or delete tickets the decision invalidated.

**Resolve exactly one ticket per session** — research tickets excepted, since they return facts rather than decisions. Each resolution changes the map, and a second ticket worked from the pre-change picture is worked from a map that no longer exists.

The user may work unblocked tickets in parallel, so expect the files to have moved since you read them.

## When the map clears

No open tickets and no fog means the way to the destination is clear. Say so, and hand off by what the destination was:

- **A spec** → the Spec branch, entering at §1 with the map's Decisions so far as settled input. Those decisions are answers, not `[待拍板]` — they don't get re-asked.
- **A decision to lock** → it's locked. Write the ADR under `{feature-name}/decisions/` and stop.
- **A change to make** → the Tickets branch.

## Not the Tickets branch

Both carry blocking edges and a frontier, which is exactly why they get confused. Keep them apart:

| | Map | Tickets |
|---|---|---|
| An item is | a **question** | a **slice** |
| Its frontier is | what can be **decided** now | what can be **built** now |
| Resolving it produces | a decision | working software |
| Lands in | `map/` | `issues/` |
| Per session | one ticket, research excepted | one slice, fresh window |

**A Map never writes into `issues/`.** A resuming session that finds questions in the slice graph reads the wrong picture of what's buildable.

Map runs first where both apply: it settles what to build, Tickets cuts it up.
