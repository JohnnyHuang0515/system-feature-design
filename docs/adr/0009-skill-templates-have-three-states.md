# Skill templates have three states, and the folder is which

Status: accepted · 2026-08-02

`mattpocock/skills` keeps 15 of its 47 skills outside the live set — 10 in `in-progress/`, 5 in `deprecated/`. That is a large fraction, and it is what lets the remaining 32 mean something: **live is a claim, not a location.** This package had no such place. A half-written skill template either shipped on every scaffold or didn't exist.

**Decided:** `scaffold/assets/templates/skills/` gets the same three states — top level ships, `in-progress/` is drafted, `deprecated/` is retired — and `scaffold.py` enforces the split rather than describing it. A live template nothing ships raises; a name in a subfolder while still on the shipped list raises rather than resolving to one of them.

The check is the point. The folders alone would be documentation, and this package's own record is that documentation loses to defaults — see `0007`. Making the script fail is what makes the folder mean what it says.

## Consequences

Neither folder is created empty. That follows the package's own rule — subfolders arrive with their contents — and it is also how upstream looks: its `deprecated/` holds five real skills, not a placeholder. The mechanism honours the folders the moment one appears.

The entry rule that matters: **a template goes to `in-progress/` when it stops being ready, including when a run it should have passed fails.** Until now a failing skill stayed live because there was nowhere else to put it, and the live set silently meant "written" rather than "tested". It leaves `in-progress/` on a passing run, not on reading well.

This does not extend to `references/` or to the Spec branch's documents. Those are parts of one artifact rather than independently shippable units, and their lifecycle is already carried by ADR `Status:` lines — `0006` is superseded and still readable, which is the same idea applied where it fits.
