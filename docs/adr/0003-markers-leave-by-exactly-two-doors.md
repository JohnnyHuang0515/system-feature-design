# Markers leave by exactly two doors

Status: accepted · 2026-08-02

`[需確認]` and `[待拍板]` mark inferences and live forks during the conversation. The rule used to say *delete confirmed markers before writing the file* — which is silent on the unconfirmed ones. In a seeded-defect run nine markers reached disk, and the model, finding itself holding items it had been given no exit for, **invented a parking section in the README** to store them.

**Decided:** the outcome is stated as an invariant — **a file on disk carries no bare `[需確認]` or `[待拍板]`** — and every marker leaves by one of exactly two doors: deleted because the user confirmed it, or converted into a §7.2 Open Question with a `D-NNNN` reference left in its place because they deferred it. An item that is neither confirmed nor deferred is not ready to be written.

The invariant is what does the work. Naming both doors is what stops a third one being invented: given an item and no exit, a model builds an exit.

## Consequences

§7.2 is the only place an unresolved item persists, and nothing — the README included — becomes a second parking spot. This is also what makes the mechanical check in `references/full-spec-review.md` meaningful: Check 0 greps every `*.md` for the marker patterns, and any hit is a defect rather than a judgment call. That grep is what catches the regression. See `docs/adr/0001`.

The rule downstream in `references/tickets.guide.md` follows from this: a ticket derived from a partial spec carries a plain `Derived from §2, not from §8` banner and **not** a `[需確認]` marker, because the grep does not know the difference.
