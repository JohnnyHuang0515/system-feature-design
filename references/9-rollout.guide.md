# Reference Guide: 9-rollout.md

> 基於 `0-skill-mode.md` 的推導模式。配合 `templates/9-rollout.template.md` 使用。

## 文件目的

定義「怎麼安全地上線」+「上線後怎麼運維」。給 SRE / DevOps / on-call 看的。

## 是否要做這份文件

進入這份前,先用一句話問:

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

使用者說「不做」→ 直接跳到 §9 後的「完整 spec 總 review」流程(見 `0-skill-mode.md`)。

## 進入這份文件時的開場

```
進入第九份(最後一份):上線與運維。

最小必寫集合:
- §9.1 Rollout Strategy
- §9.3 Observability
- §9.6 Rollback Plan

其餘節依需求填:
- §9.2 Migration / Seed - 有資料遷移時必寫
- §9.4 Alerting - 寫了 observability 通常一起寫
- §9.5 Runbook - 有 alert 時必寫(本 spec 階段提供骨架 + TODO 標記)
- §9.7 Post-Launch Review - 有 success metrics 時建議

我會推導所有節,沒適用的標 「[不適用]」 或省略。

預估 10-20 分鐘。
```

## Claude 推導指南

### Rollout Strategy 推導

從 §1 Stage(POC / MVP / 正式)+ §2 NFR 推:
- POC → 簡化 stages(dogfood → beta → GA)
- MVP / 正式 → 完整 5 stages(dogfood → canary 1% → 10% → 50% → 100%)
- Feature flag 標準格式

### Migration 推導

從 §3 entity 變化 + §1.5 提到的 seed data 推:
- 有新 entity / 新欄位 → 寫 schema migration
- 有 seed data → 寫 seed loading 機制
- 都沒有 → 跳過

### Observability 推導

從 §2.2.4 NFR 反推具體指標:
- 核心 SLI:latency / error rate / throughput
- 業務 metrics:從 §1.4 success criteria 反推
- Logs 規範:Must log + Must NOT log(合規)
- Tracing:跨 service 才需要

### Alerts 推導

從 §9.3 metrics 推 alert 條件:
- 每個關鍵 SLI 對應 1-2 個 alert
- Severity 按業界標準(P0/P1/P2/P3)

### Runbook 推導

每個 alert 對應一個 RB,**用骨架 + TODO 標記**:
- Symptoms:從 alert 條件推
- Diagnosis Steps:推可推的(看哪個 dashboard、查哪個 log),不可推的標 `[TODO 由運維補]`
- Common Causes:推 3-5 個常見原因
- Escalation:標 `[TODO 由運維補]`(需實際運維知識)

### Rollback 推導

按業界標準三層:
- Level 1: feature flag off(秒級)
- Level 2: code rollback(5-15 分鐘)
- Level 3: schema rollback(小時級,通常 POC 不適用)

每個 Trigger 量化(不可主觀)。

## 必要決策點(要問使用者的)

### 必補問題

1. **POC vs MVP vs 正式**:影響 stages 設計詳細度
2. **是否有 SLA 承諾**:影響 alert threshold 設定
3. **Rollback 演練 sign-off**:誰是 tech lead

### 不該問的

- ❌ 「Rollout 怎麼分階段?」(從 stage 推)
- ❌ 「要監控什麼?」(從 NFR 推)
- ❌ 「Alert 條件是?」(從 metrics 推)

## Open Question 候選

- SLA 目標不確定
- Canary 比例不確定(1% vs 5% vs 10%)
- 監控工具選擇(Datadog vs Prometheus vs ...)

## 展示給使用者的格式

### 步驟 1:摘要

```
我推導出 rollout 計畫:

- Stages:{N} 個(POC 簡化 / MVP 完整)
- Migration:{有 schema change / 有 seed data / 無}
- Observability:{N} 個核心 SLI、{M} 個業務 metric
- Alerts:{N} 個(P0:X / P1:Y / P2:Z / P3:W)
- Runbooks:{N} 份(骨架 + TODO 標記)
- Rollback:三層 + 演練 sign-off

需要你拍板:[N 個]
```

### 步驟 2:分節展示

POC 階段重點展示 §9.1 + §9.3 + §9.6。其他節給「精簡版 / 完整版」讓使用者選。

### 步驟 3:問必要決策點

```
有幾件事需要你拍板:

1. 你說這是 POC,我給 3 個 stages(dogfood → beta → GA)。對嗎?
   還是你希望加入 1% canary?

2. NFR-1 latency p99 < 500ms,對應 alert 我設「p99 > 1s 持續 10 分鐘」。
   太敏感還是不夠?

3. Rollback 演練 sign-off 由誰負責?(影響 release gate 設計)
```

## 容易卡住的點

### 使用者沒做過 rollout planning

主動推完整版讓使用者刪除不需要的,比要求使用者從零想容易。

### POC 階段使用者覺得「寫太多」

提供「POC 精簡版 vs MVP 完整版」對照,POC 可以只寫 §9.1 + §9.3.2(logs) + §9.6 Level 1。

### Runbook 內容寫不出來

接受「骨架 + TODO 由運維補」,不要編造運維操作步驟。

## 反思檢查(進總 review 前)

- [ ] §9.1 Rollout Stages 有量化 success / abort criteria
- [ ] §9.3 Observability 對應 §2.2.4 NFR
- [ ] 每個 §9.4 alert 都有對應 §9.5 runbook
- [ ] §9.6 Rollback Triggers 量化(不主觀)
- [ ] §9.6 Rehearsal 有明確 sign-off 機制
- [ ] Runbook TODO 標記都清楚

## 文件結束時的 summary

```
§9 rollout 完成!

- Stages:{N} 個
- Migration / Seed:{有 / 無}
- Metrics:{N} 個 SLI + {M} 業務指標
- Alerts:{N} 個
- Runbooks:{N} 份(含 TODO 由運維補)
- Rollback:三層 + 演練 sign-off

整份 spec 9 份文件 + decisions/ 子目錄都已產出!

要不要跑一次完整 spec 的總 review?
我會檢查跨文件的一致性(編號 reference、必填覆蓋、孤兒檢查、概念一致性)。

預估 5-10 分鐘,會列出問題清單讓你決定要不要修。

要跑嗎?
```

進入「完整 spec 總 review」流程(見 `0-skill-mode.md` 末段)。
