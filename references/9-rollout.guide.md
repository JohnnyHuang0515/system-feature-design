# Reference Guide: 9-rollout.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/9-rollout.template.md`.
> Instructions here are English; the quoted blocks are scripts spoken to the user — use them as written.

## Purpose

Define how it ships safely and how it's operated afterwards. Read by SRE, DevOps and whoever is on call.

## Whether to write it at all

Ask in one line before starting:

```
最後一份是 rollout(上線與運維)— 選填。

判斷要不要做:
- 對 prod 流量有影響(非純內部工具)
- 涉及多個 service 互動
- 有資料 migration / schema 變更
- 業務關鍵(出問題會影響營收 / 使用者)

任一是「是」 → 建議寫。
都是「否」 → 可省,spec 到 §8 結束。

要做 §9 嗎?
```

A 「不做」 goes straight to the flow in `references/full-spec-review.md`.

## Opening

```
進入第九份(最後一份):上線與運維。

最小必寫集合:
- §9.1 Rollout Strategy
- §9.3 Observability
- §9.6 Rollback Plan

其餘節依需求填:
- §9.2 Migration / Seed - 有資料遷移時必寫
- §9.4 Alerting - 寫了 observability 通常一起寫
- §9.5 Runbook - 有 alert 時必寫(本 spec 階段提供骨架 + 「由運維補」佔位)
- §9.7 Post-Launch Review - 有 success metrics 時建議

我會推導所有節,沒適用的標 「[不適用]」 或省略。
```

## Derivation

### Rollout strategy

From §1 Stage (POC / MVP / production) plus §2 NFRs:

- POC → simplified stages (dogfood → beta → GA)
- MVP or production → the full five (dogfood → canary 1% → 10% → 50% → 100%)
- Feature flag in the standard format

### Migration

From §3 entity changes plus any seed data mentioned in §1.5. New entities or fields → a schema migration. Seed data → a loading mechanism. Neither → skip the section.

### Observability

Reverse-engineer concrete metrics from §2.2.4 NFRs:

- Core SLIs: latency, error rate, throughput
- Business metrics: reverse-engineered from §1.4 success criteria
- Logging rules: must log, and must not log (compliance)
- Tracing: only where services span

### Alerts

From §9.3 metrics: 1–2 alerts per key SLI, severity on the standard scale (P0/P1/P2/P3).

### Runbook

One RB per alert, **as a skeleton with 「由運維補」 placeholders**:

- Symptoms — derived from the alert condition
- Diagnosis steps — derive what you can (which dashboard, which log); leave the rest as `{由運維補：...}` placeholders, matching the template
- Common causes — derive 3–5
- Escalation — a `{由運維補：...}` placeholder; this needs real operational knowledge

### Rollback

Three standard levels: feature flag off (seconds), code rollback (5–15 minutes), schema rollback (hours, usually not applicable to a POC).

Every trigger is quantified, never subjective.

## Questions you must ask

1. **POC vs MVP vs production** — sets how detailed the stages get
2. **Any SLA commitment** — sets alert thresholds
3. **Rollback rehearsal sign-off** — who is the tech lead

## Open question candidates

- SLA target uncertain
- Canary percentage uncertain (1% vs 5% vs 10%)
- Monitoring tool choice (Datadog vs Prometheus vs …)

## Display format

### Step 1: summary

```
我推導出 rollout 計畫:

- Stages:{N} 個(POC 簡化 / MVP 完整)
- Migration:{有 schema change / 有 seed data / 無}
- Observability:{N} 個核心 SLI、{M} 個業務 metric
- Alerts:{N} 個(P0:X / P1:Y / P2:Z / P3:W)
- Runbooks:{N} 份(骨架 + 「由運維補」佔位)
- Rollback:三層 + 演練 sign-off

需要你拍板:[N 個]
```

### Step 2: section by section

For a POC, foreground §9.1 + §9.3 + §9.6. Offer the other sections as 精簡版 or 完整版 and let the user pick.

### Step 3: the decisions

```
有幾件事需要你拍板:

1. 你說這是 POC,我給 3 個 stages(dogfood → beta → GA)。對嗎?
   還是你希望加入 1% canary?

2. NFR-1 latency p99 < 500ms,對應 alert 我設「p99 > 1s 持續 10 分鐘」。
   太敏感還是不夠?

3. Rollback 演練 sign-off 由誰負責?(影響 release gate 設計)
```

## Where you'll get stuck

### The user has never planned a rollout

Push a full version and let them delete what they don't need. Deleting is easier than starting from a blank page.

### A POC user thinks it's too much

Offer the POC-lite vs MVP-full comparison. A POC can run on §9.1 + §9.3.2 (logs) + §9.6 Level 1 alone.

### The runbook content won't come

Accept the skeleton-plus-placeholder form. Inventing operational steps is worse than leaving the gap visible.

## Reflection check, before the full-spec review

- [ ] §9.1 rollout stages have quantified success and abort criteria
- [ ] §9.3 observability maps to §2.2.4 NFRs
- [ ] Every §9.4 alert has a §9.5 runbook
- [ ] §9.6 rollback triggers are quantified, not subjective
- [ ] §9.6 rehearsal has an explicit sign-off mechanism
- [ ] Every 「由運維補」 placeholder in a runbook names what's missing and who fills it, rather than sitting blank

## Closing summary

```
§9 rollout 完成!

- Stages:{N} 個
- Migration / Seed:{有 / 無}
- Metrics:{N} 個 SLI + {M} 業務指標
- Alerts:{N} 個
- Runbooks:{N} 份(含「由運維補」佔位)
- Rollback:三層 + 演練 sign-off

整份 spec 所有文件 + decisions/ 子目錄都已產出!

要不要跑一次完整 spec 的總 review?
我會檢查跨文件的一致性(編號 reference、必填覆蓋、孤兒檢查、概念一致性)。

要跑嗎?
```

Then enter the flow in `references/full-spec-review.md`.
