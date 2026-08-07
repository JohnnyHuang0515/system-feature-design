---
name: improve-codebase-architecture
description: Scan the codebase for deepening opportunities — shallow modules worth turning into deep ones — present them as a visual HTML report, then work through whichever the user picks. Use as periodic upkeep every few days, or when the user says the codebase is getting hard to change, hard to test, or hard for an agent to navigate.
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and agent-navigability, not tidiness.

This is upkeep, not feature work. Run it every few days.

Built on `.claude/rules/codebase-design.md` — **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**, the deletion test, the dependency categories. Use those words exactly; drifting into "component", "service", "API" or "boundary" loses the precision the whole exercise depends on.

## 1. Scope before you scan

Deepening pays off by making *future* changes easier, so weight recent activity. Decide where to look before looking:

- The user named a direction — a module, a subsystem, a pain point → take it.
- Otherwise walk back a good stretch of `git log --oneline` for the hot spots — the files and areas that keep coming up — and let those pull your attention first. Scattered changes with no hot spot → widen the net.

Read `CONTEXT.md` for the domain vocabulary and any ADRs covering the area first.

## 2. Explore

Walk the codebase and note where you experience friction:

- Understanding one concept requires bouncing between many small modules
- Modules are **shallow** — the interface is nearly as complex as the implementation
- Pure functions were extracted purely for testability, while the real bugs hide in how they're called (no **locality**)
- Tightly-coupled modules leak across their seams
- Parts that are untested, or hard to test through their current interface

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity across N callers, or just move it? "Concentrates" is the signal.

## 3. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory — resolve `$TMPDIR`, falling back to `/tmp` (`%TEMP%` on Windows) — as `architecture-review-<timestamp>.html`, so nothing lands in the repo and each run gets a fresh file. Open it (`open` / `xdg-open` / `start`) and tell the user the absolute path.

**Be visual.** Each candidate gets a card:

- **Files** — which modules are involved
- **Problem** — why the current shape causes friction
- **Solution** — plain English, what would change
- **Benefits** — in terms of locality and leverage, and how tests would improve
- **Before / after diagram** — side by side, showing the shallowness and the deepening
- **Recommendation strength** — `Strong`, `Worth exploring`, or `Speculative`, as a badge

Diagram patterns, roughly in order of usefulness:

| Shape | Use it for |
|---|---|
| Graph / flow diagram | Dependencies and call flow — the workhorse |
| Hand-built boxes and arrows | When automatic layout fights the point you're making |
| Cross-section | Layered shallowness — thin slices stacked |
| Mass diagram | "The interface is as wide as the implementation" |
| Call-graph collapse | Before: N callers each wiring the same five calls. After: one door |

Use `CONTEXT.md` vocabulary for the domain and `codebase-design.md` vocabulary for the architecture. If `CONTEXT.md` defines "Order", write "the Order intake module" — not "the FooBarHandler", and not "the Order service".

**ADR conflicts**: where a candidate contradicts an existing ADR, surface it only if the friction is real enough to warrant reopening that decision, and mark it clearly on the card. Listing every refactor an ADR forbids is noise.

End with a **Top recommendation**: which you'd tackle first, and why.

**Propose no interfaces yet.** After the file is written, ask: which of these would you like to explore?

## 4. Work the chosen candidate

Once the user picks one, walk the decision tree with them the way **`grilling`** does — a round at a time, each round asking the whole frontier. Constraints and dependencies come first because the shape of the deepened module hangs off them; the shape then settles what sits behind the seam, and the seam settles which tests survive.

Side effects happen inline as decisions crystallise:

- **Naming the deepened module after a concept not in `CONTEXT.md`?** Add the term there and then.
- **Sharpening a fuzzy term mid-conversation?** Update `CONTEXT.md` right there.
- **The user rejects a candidate for a load-bearing reason?** Offer to record it as an ADR — *"want me to record this so future architecture reviews don't re-suggest it?"* Only where a future explorer would actually need it; skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces?** Use the **design it twice** pattern in `codebase-design.md`.

A candidate whose real finding is "there is no good seam here" is still a result — record it.
