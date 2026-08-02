# Reference Guide: 2-requirements.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/2-requirements.template.md`.
> Instructions here are English; the quoted blocks are scripts spoken to the user — use them as written.

## Purpose

Break §1's "what we're doing" into concrete functional requirements (FR) and non-functional requirements (NFR). Each one is independently verifiable and citable by §8 acceptance criteria.

## Opening

```
進入第二份:需求清單。

我會根據 §1 推導出功能需求(FR)清單跟非功能需求(NFR)清單,
你確認 / 修正即可。
```

## Derivation

### FRs

> **Where §0 market research ran**, FR priority isn't set by §1.5 alone — it also takes §0.6 differentiation opportunities. An FR that lands one of the `OPP-N` entries gets a **priority bump** and cites that OPP-N in its Related column.
> This is the receiving end of §0.7's promise that OPP feeds §2 priority. An opportunity declared in §0 and never picked up is an opportunity wasted.

| Target | Source |
|---|---|
| FR list | Each §1.5 in-scope item expands into 1–N FRs |
| FR Description | "Allow X to do Y" — a system capability, not a user action |
| FR Persona | Maps to a §1.3 persona (a PER-N where §0 ran) |
| FR Priority | Inferred from §1.5; POC defaults to Must, optional-feeling items to Should. **With §0, FRs carrying an OPP-N move up** |
| FR Related | References the §1 subsection; an FR carrying a differentiation opportunity also cites its `OPP-N` |

### NFRs

**This table is a gate, not a menu.** Only Security & Authorization is unconditional. For every other row, name the condition in this feature that fires it — no condition, no section. A category included "for completeness" produces a target nobody will measure and an AC in §8 nobody will write.

| Category | Fires when |
|---|---|
| Security & Authorization | Always — at minimum authentication and authorization |
| Performance | External-facing, or the user stated a performance requirement |
| Reliability | External-facing, or business-critical |
| Observability | External-facing, or someone is on call for it |
| Scalability | Fast growth is expected |
| Compliance & Audit | Handling payments, medical records, or regulated personal data |

Two rules keep it a gate:

- **The condition has to be met as written.** A related-sounding reason is not the condition. "Leave approvals are important decisions" is not *business-critical*; "an audit trail would be nice" is not *someone is on call for it*. Where you find yourself constructing the justification rather than pointing at a fact, the row hasn't fired.
- **The user's own words close a row.** 「沒有特殊合規要求」 closes Compliance & Audit. 「50 人以內」 closes Scalability. There is no table-stakes override — if you think they're wrong, say so out loud and let them decide, rather than adding the section quietly.

Calibration: a 50-user internal tool usually fires two — Security, plus Performance where someone named a number. A public revenue-carrying service usually fires most of them. Landing on five or six for something small means the table was read as a checklist.

Every NFR Target is an inferred value marked `[需確認]`.

### Priority Summary

Produce one automatically once FR + NFR exceeds 10 entries.

**Where §0 ran**: FRs carrying an `OPP-N` are usually Must as well, sitting alongside table stakes — so Must / Should / Could alone can't show which Must is the differentiating one. The Priority Summary therefore **marks OPP-carrying FRs as 差異化核心 and lists them first**, noted as build-first and cut-last. Without that, the real top priority drowns in a pile of Musts.

## Questions you must ask

Usually none. Two situations call for one:

1. **An uncertain quantitative target** — NFR latency, QPS and similar. Mark it `[需確認]` for the user to tune rather than asking outright.
2. **A scope-boundary FR** — an FR that could read as Must or Should. Mark it `[待拍板]`.

## Open question candidates

- A fuzzy FR boundary (「這算 FR 還是 enhancement?」)
- An NFR target with no benchmark (「latency 目標多嚴格才合理?」)
- Ambiguous priority (「FR-X 是 Must 還是 Should?」)

## Display format

### Step 1: summary

```
我推導出 N 條 FR 跟 M 條 NFR:

FR 重點:
- FR-1: [簡述]
- FR-2: [簡述]
...

NFR 分類:[列出有用到的分類]

需要你拍板:[N 個]
```

### Step 2: full tables

Show the §2.1 FR table and the §2.2 NFR tables per category, against the template structure. Inferred Targets and Priorities carry `[需確認]`.

### Step 3: the decisions

```
有幾個我推測的數字想跟你確認:

1. NFR-1 我推測 p99 latency < 500ms,合理嗎?或你心中有別的目標?
2. FR-9 (結構警告) 我預設 Should,要不要提升到 Must?
```

## Where you'll get stuck

### The user thinks there are too many FRs

Ask 「哪些是 must-have、哪些可以延後?」 to help them converge.

### The user has no sense of an NFR target

Give an industry-typical value plus a reason their situation might differ, so they have something to push against:

```
類似 feature 的 latency 目標通常 p99 < 500ms ~ 1s,
你這個是內部使用還是對外?內部可以寬鬆,對外建議嚴格點。
```

## Reflection check, before §3

- [ ] Every §1.5 in-scope item maps to at least one FR
- [ ] Every FR's Persona maps to a persona listed in §1.3
- [ ] Where §0 ran, every §0.6 OPP-N maps to an FR whose priority was raised — no opportunity dropped
- [ ] NFRs cover Security & Authorization at minimum
- [ ] Every other NFR category present can point at the fact that fired it — and none contradicts something the user said
- [ ] A Priority Summary exists where FR + NFR exceeds 10
- [ ] Marker lifecycle done

## Closing summary

```
§2 requirements 完成!

- FR:{N} 條(Must {M} / Should {S} / Could {C})
- NFR:{N} 條,涵蓋 {分類列表}
- Priority Summary:[有 / 跳過]

接下來進入 §3 domain-model,我會推導 entities、state machines、business rules。要進嗎?
```
