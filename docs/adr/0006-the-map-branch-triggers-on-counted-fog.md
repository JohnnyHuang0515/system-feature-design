# The Map branch triggers on counted fog at the §1 gate

Status: accepted · 2026-08-02

Work can be too large to specify in one context window. The Spec branch's context-hygiene rule — keep the whole run in one unbroken window, ceiling around 120k — says what to do when the work fits and is silent when it doesn't. The Map branch fills that, charting the work as decision tickets resolved one per session.

The obvious trigger is *"when the work is too big for one window, chart a map instead."* **That trigger would never fire.** The finding this package was built on, across eight seeded-defect runs, is that anything with a checkable bar gets executed and anything that only persuades gets asserted — and "too big" is a judgment made by the same model that wants to start writing §1.

**Decided:** the trigger is a **count**, taken at a gate that already fires. §1's stage question already forces a fork and already declares the Path, so the fog count is taken at the same moment, before §2 opens.

**Fog** is defined against machinery already enforced elsewhere: every `[待拍板]` must ship with options (a)(b)(c) and a recommendation, so *"a decision you cannot yet write options for"* is already a first-class failure in this package rather than a new judgment. Two conditions, both required:

1. You can name the area of the decision but **cannot write its options**, because they depend on an answer you don't have.
2. **Documents downstream cannot be written until it is answered.**

One or more fog items means the run does not fit and a Map is charted. Zero means §2 opens normally.

## Considered options

**Trigger on document count or estimated tokens** — rejected. Both are guesses made before the work, and neither is knowable at §1.

**Trigger on the number of open decisions** — rejected. It over-fires. Ten decisions that can each be written as options are ten answerable questions and they fit one window; the count that matters is of the ones that *can't* be phrased.

**Make it a mode inside the Spec branch rather than a branch** — rejected. A user who arrives already knowing the work is huge would have no way in, and the branch table is the package's user-facing map.

## Consequences

Condition 2 is what keeps Map from swallowing §7.2. A decision that is unphrasable but **doesn't block** downstream documents is an Open Question, gets a `D-NNNN`, and the spec carries on — that distinction is the whole boundary between the two mechanisms, and losing it turns every spec run into a map.

Map and Tickets both carry blocking edges and a frontier, which invites conflation. They are kept apart by noun and by file: Map's items are **questions** and land in `map/`, Tickets' items are **slices** and land in `issues/`. A Map never writes into `issues/`, or a resuming session reads the wrong graph.

What catches a regression here is a run on work with a genuinely unanswerable blocking decision, checking whether §2 opens anyway. See `docs/adr/0001`.
