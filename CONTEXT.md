# system-feature-design

A skill package that turns a feature idea into an AI-development-ready spec, cuts a spec into buildable work, charts work too large for one context window, and scaffolds the repo that will implement it. This file fixes the vocabulary the package uses about *itself* — the terms below mean these things in `SKILL.md`, in `references/`, and in every conversation about editing them.

## Language

**Branch**:
One of the four entry points in `SKILL.md` — Spec, Map, Tickets, Scaffold. Each runs alone and each can start from what another produced.
_Avoid_: mode, phase, step, pipeline stage

**Path**:
POC / MVP / Production. Settled by §1's stage question; declares which documents a Spec run carries and how deep each goes.
_Avoid_: tier, level, track, mode

**Guide**:
A file under `references/` read on demand at the moment its document or branch starts. Carries derivation tables, required questions and reflection checklists — never loaded upfront.
_Avoid_: doc, spec, instructions, manual

**Marker**:
`[需確認]` or `[待拍板]`. Lives in the conversation only; a file on disk carries neither.
_Avoid_: TODO, flag, placeholder, annotation

**Gate**:
A rule with a bar that can be checked, which stops the run until it is met. Distinct from guidance, which only persuades. Every gate states the bar as a condition, not as an intention.
_Avoid_: check, rule, guideline, principle

**Fog**:
A decision you can point at but cannot yet write options for, *and* which blocks documents downstream. Fog is what a Map exists to clear.
_Avoid_: unknown, uncertainty, TBD, open question

**Open Question**:
A decision that is phrasable as options but deliberately deferred. Lives in §7.2 with a `D-NNNN` reference, and does not block the spec.
_Avoid_: fog, TBD, parked item

**Frontier**:
The items takeable right now. A Map's frontier is what can be **decided**; a Tickets frontier is what can be **built**. Always say which.
_Avoid_: next steps, backlog, ready queue

**Decision ticket**:
A Map item — a question whose resolution is a decision, sized to one session.
_Avoid_: ticket, issue, task, story

**Slice**:
A Tickets item — a tracer bullet cutting a narrow but complete path through every layer, demoable on its own.
_Avoid_: task, story, ticket, layer

**Seeded-defect run**:
The verification method for this package. Plant defects of known type across different checks, run the flow on a cheap model, score, fix, re-run. What survives is what has a bar.
_Avoid_: test, QA, eval, trial

## Related

Decisions are in `docs/adr/`. `docs/adr/0001` defines what "hard to reverse" means for this repo, which is what admits most of the rest.
