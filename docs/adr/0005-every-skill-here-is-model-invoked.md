# Every skill here is model-invoked

Status: accepted · 2026-08-02

`mattpocock/skills`, which this package borrows its shape from, organises everything on one axis: **user-invoked** (`disable-model-invocation: true`, reachable only by a human typing its name, zero context load, pays cognitive load, job is to orchestrate) versus **model-invoked** (keeps its `description`, reachable by humans, agents and other skills, job is to hold reusable discipline). This package sets `disable-model-invocation` on nothing at all, which reads like the axis was never applied.

**Decided:** the axis was applied, and every skill here resolves to model-invoked. His test for the split is *"could the model usefully reach for this autonomously?"* — asked of the top-level skill and of each of the nine that ship on a scaffold, the answer is yes every time.

The axis earns its second position when a repo has enough skills that a human cannot hold their names, which is what his router skill exists to cure. This package is **one entry point and nine disciplines**. A user-invoked orchestrator here would route to itself, and making the entry point user-invoked would mean 「做一份功能規格」 no longer reaches it — trading away the discoverability that was the reason to merge two packages into one.

## Consequences

If this package ever grows a second human entry point, the axis has a second position to occupy and this decision should be revisited rather than assumed. The trigger is a human having to remember which name to type.

`SKILL.md`'s `description` is doing the work `disable-model-invocation` would otherwise do — it is long on purpose, carrying the Chinese and English phrasings for all four branches, because model invocation is only as good as the description it matches against.
