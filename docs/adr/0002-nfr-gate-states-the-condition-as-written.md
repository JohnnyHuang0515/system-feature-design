# The NFR gate states its condition as written

Status: accepted · 2026-08-02

§2's non-functional-requirement table is a gate: a category only produces NFRs when its condition fires. The first attempt at enforcing this said so in exactly those words — *"this table is a gate, not a menu"* — and **failed a seeded-defect run**. The model constructed related-sounding justifications for categories whose condition had not fired, and overrode the user's own 「沒有特殊合規要求」 to do it. Ten NFRs across five categories on a 50-user internal tool.

**Decided:** the gate carries three things the persuasive version lacked — the condition must be met **as written** rather than in spirit, **the user's own words close a row** with no table-stakes override, and a **calibration example** (a 50-user internal tool fires two categories). The re-run produced five NFRs across two categories.

Keeping this requires keeping all three. The wording is verbose on purpose; it is the difference between a rule the model applies and a rule the model argues with.

## Consequences

Reverting is a one-line edit and looks like an improvement in concision. What catches the regression is re-running §2 on a small internal tool with a user who states no compliance requirement, and counting the categories that fire. More than two means this was undone. See `docs/adr/0001`.
