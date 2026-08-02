# Never ask the model to escalate itself

Status: accepted · 2026-08-02 · supersedes `0006`

`0006` made §1's fog count switch branches: non-zero meant chart a Map before §2. Five live runs on the fixture that should fire it produced one honest pass, three menus, and one fabricated zero. The fixture that should *not* fire it passed first time and never wavered.

That asymmetry is the finding. **Every failure was the model refusing to escalate on its own authority; none was it wrongly escalating.** It talked itself out of the count, then offered 「(a) 走 Map (b) 直接做規格」, then — after the wording was tightened again — recited the closing line 「沒有卡住後面的未知」 in a step-1 summary without ever taking the count. Four attempts to fix it by wording failed, including one that moved the jurisdiction, which had worked for the NFR gate.

**Decided:** don't ask a model to promote a session into a heavier process mid-flow. §1 keeps the count and the report — naming each item and the section it blocks, which ran reliably — and **recommends** the Map. Choosing it is the user's.

This is how `mattpocock/skills` already handles it, which is what settled it. `wayfinder` is `disable-model-invocation: true`, and by his invocation rule a user-invoked skill cannot be reached by another skill — so **there is no route into it at all**; the human types it. His only fog check runs the other way: *if this surfaces no fog, you don't need a map, stop and ask the user*. An escape hatch out of a process the human already chose, never a gate into one.

## Consequences

The case `0006` was built to catch — a user who doesn't know their work is too big — is still caught, because §1 still surfaces the items and states the cost. What changed is who acts on it. A run that quietly starts specifying without naming them has decided by omission, and that remains the failure the count prevents.

`0005` stands: Map stays a branch of the one entry point, reachable from the description (「這件事很大」). Splitting it into a separate user-invoked skill would buy Matt's exact architecture at the cost of 「太多了」, which is the constraint the package was merged under.

The general rule, which outlives this gate: **a rule that asks the model to escalate loses; a rule that asks it to stop and hand back wins.** Write checks in the de-escalating direction wherever there's a choice — and when a rule must run the other way, expect wording not to carry it.
