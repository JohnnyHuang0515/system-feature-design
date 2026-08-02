# The reviewer takes one axis per dispatch

Status: accepted · 2026-08-02

Code review runs on two axes — Standards and Spec — which must not be merged or reranked against each other. The obvious implementation gives the scaffolded `reviewer` agent both axes and has it spawn a sub-agent per axis. That was the first version, and it is wrong: **a sub-agent cannot reliably spawn its own sub-agents.**

**Decided:** `reviewer` takes one named axis per dispatch, and the **caller** fans out — `CLAUDE.md` instructs dispatching it twice in parallel with `axis: Standards` and `axis: Spec`, then presenting both reports under their own headings, each keeping its own verdict.

The tool grant follows: `reviewer` gets `Read, Grep, Glob, Bash` and not `Agent`. Removing the tool is what makes the constraint structural rather than advisory.

## Consequences

Reconciling the two axes is the human's call, not a combined verdict — which is the property the whole design exists to protect, and it survives the fan-out moving to the caller. Keeping the axes in separate context windows was the point either way.

This shape is baked into three files that must agree: the `CLAUDE.md` template, `reviewer.md`, and `references/scaffold.guide.md`. Every repo already scaffolded carries a copy, so a revert here leaves generated repos inconsistent with the template — this one is hard to reverse in the ordinary sense, not only under `docs/adr/0001`.
