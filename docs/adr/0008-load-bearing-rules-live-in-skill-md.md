# Load-bearing rules live in SKILL.md, not only in a guide

Status: accepted · 2026-08-02

Nine runs across three fixtures, cheap model. Sorting them by how many tool calls each made produces a clean split with no exceptions:

| Tool calls | Runs | Outcome |
|---|---|---|
| ≥ 8 | 4 | all passed — correct fog count, correct map charted, planted prior art found |
| ≤ 5 | 5 | all failed — talked itself out of the count, offered a menu, fabricated a zero, designed provisionally anyway |

The shallow runs were not applying the rule badly. They **never read the section the rule was in** — `1-problem-scope.guide.md` past line 179 — and ran on SKILL.md plus whatever they had already loaded. Four consecutive attempts to fix this by rewording the rule were fixing a file that wasn't open.

**Decided:** a rule that decides whether the run proceeds belongs in `SKILL.md`, stated completely enough to act on. The guide keeps the detail, the tables and the scripts; it does not hold the only copy of anything load-bearing.

The evidence was already in the package. The marker invariant — the one rule that has held in every run since it was written — lives in `SKILL.md`'s per-document loop, step 5. It was never better-worded than the rules that failed; it was better-placed.

## Consequences

This is not an exception to progressive disclosure — it is the test being applied correctly, which the first version of this ADR got wrong. `writing-great-skills` states it directly: **inline what every branch needs, and push behind a pointer what only some branches reach.** Every Spec run needs the fog reading, so it is inline; only §1 needs §1's derivation table, so that stays disclosed. The rule was never "disclose everything you can".

It also names the mechanism behind the shallow runs: **a context pointer's wording, not its target, decides how reliably the agent reaches the material.** The pointer here was a table row — *starting document N → read the guide* — which states an occasion and no reason.

The remaining cost is that "fog" now has a definition in two files. Carry it as a **leading word** rather than a restatement: the guide defines it once, `SKILL.md` uses the word and states the action. When they drift, `SKILL.md` is the copy that ran.

What catches the regression: a run whose tool-call count is low. If a shallow run still applies a rule, the rule is placed correctly; if only deep runs apply it, it is buried. See `docs/adr/0001`.
