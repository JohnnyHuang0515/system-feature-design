# What "hard to reverse" means in a prompt repo

Status: accepted · 2026-08-02

The three-condition ADR bar this package ships — hard to reverse, surprising without context, the result of a real trade-off — reads against a *code* repo, where hard-to-reverse means shipped, depended on, migrated. Read literally against a repo whose artifacts are prompts, almost nothing qualifies: every line here is one edit away from any other line, so the bar would admit nothing and this folder would stay empty.

**Decided:** in this repo, a decision is hard to reverse when **reverting it is cheap but re-discovering that the reversal was wrong is not** — specifically, when the regression is invisible to reading and only catchable by a seeded-defect run on a live model.

That is not a softening of the bar, it is where the cost actually sits. Three of the fixes recorded here were found by paying for runs that failed, and in each case **the broken version reads better than the working one**: "this table is a gate" is cleaner prose than the condition-as-written wording that replaced it, and it *lost the test*. A future editor pruning for concision — the discipline this package deliberately adopted — will delete exactly these lines, and nothing in the file will object.

So the pruning discipline is itself the reversal pressure. That is the trade-off: bend the first condition and record findings that would otherwise be lost, or hold it literally and let paid-for knowledge live only in a chat log.

## Consequences

Anything admitted under this reading **says so and names the run that found it**, so a reader can weigh the evidence rather than take the entry on faith. An entry that cannot name what would catch its regression has not met this bar and does not belong here.

This reading is scoped to **this repo only**. `scaffold/assets/templates/skills/grilling.md` and `domain-glossary.md` ship into code repos, where the literal reading is the correct one and stays unchanged.
