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

It also names the mechanism behind the shallow runs, and prescribes an order this ADR originally skipped. `GLOSSARY.md`'s **Context Pointer** entry: *its wording, not the target, decides when the agent reaches — and how reliably.* **A must-have target behind a weakly worded pointer is a variance bug: fix the wording first, and inline the material only if sharpening fails.**

Inlining is the fallback, not the first move. Two cases here, and only one of them was handled right:

- **The §0 skip reason** — no pointer can fire, because a run that skips §0 never opens §0's guide. Sharpening was never available, so inlining into `SKILL.md` beside the routing was correct.
- **The fog reading** — the pointer *does* fire, since every Spec run starts §1 and opens its guide. It was simply weak: a table row reading *starting document N → read the guide*, stating an occasion and no reason. That one should have had its wording sharpened and measured before anything moved. It didn't; the material was inlined straight away.

So the rule stated above is narrower than it reads: **a rule that decides whether the run proceeds belongs in `SKILL.md` once a sharpened pointer has failed to reach it, or cannot fire at all.**

**The sharpened pointer was then measured, and it works.** A cheap-model run given no instruction to read anything reproduced 「fog 檢查:0 項 — 都問得出選項」 and 「這次走:MVP」 — phrasings that appear zero times in `SKILL.md` and only at line 256 of a 264-line guide. It opened the guide and read to the end of it.

That does **not** license pulling the fog rule back down, for two reasons. The run had zero fog, so it never exercised the path that failed five times; and there is nothing left to pull, since the duplication was already resolved by making `SKILL.md` own the test and the guide point up at it. What remains inline costs ten lines and is the only configuration nine runs have verified.

The result matters for everything else instead: **a rule placed in a guide can now be expected to be reached.** Rules do not need hoisting into `SKILL.md` by default — only when their pointer cannot fire, as with §0's skip.

The remaining cost is that "fog" now has a definition in two files. Carry it as a **leading word** rather than a restatement: the guide defines it once, `SKILL.md` uses the word and states the action. When they drift, `SKILL.md` is the copy that ran.

What catches the regression: a run whose tool-call count is low. If a shallow run still applies a rule, the rule is placed correctly; if only deep runs apply it, it is buried. See `docs/adr/0001`.
