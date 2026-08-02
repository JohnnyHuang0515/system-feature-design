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

This cuts against progressive disclosure, which is why it needs stating: **the branch that decides whether to keep going cannot be disclosed progressively.** Read-on-demand is right for a document's derivation table, which is only needed once that document starts; it is wrong for a check that determines whether that document should be written at all.

The cost is duplication between `SKILL.md` and the guide, which the package otherwise treats as sediment. Accept it for gates, and only for gates. When they drift, `SKILL.md` is the copy that ran.

What catches the regression: a run whose tool-call count is low. If a shallow run still applies a rule, the rule is placed correctly; if only deep runs apply it, it is buried. See `docs/adr/0001`.
