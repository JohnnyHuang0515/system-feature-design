# 9. Rollout & Operations

> **本文件整體選填**。
> 如果你的 feature 屬於以下任一類型，**強烈建議寫**：
> - 對 prod 流量有影響（非純內部工具）
> - 涉及多個 service 互動
> - 有資料 migration 或 schema 變更
> - 業務關鍵（出問題會影響營收或使用者）
>
> **最小必寫集合**（決定寫 rollout 文件後）：
> - 9.1 Rollout Strategy
> - 9.3 Observability
> - 9.6 Rollback Plan

## 9.1 Rollout Strategy

### Stages

| Stage | Traffic | Duration | Success Criteria | Abort Criteria |
|-------|---------|----------|------------------|----------------|
| Internal dogfood | Team only | {天數} | {標準} | {標準} |
| Canary | 1% | 24 hours | {標準} | {標準} |
| Gradual | 10% | 48 hours | {標準} | {標準} |
| Full rollout | 50% | 24 hours | {標準} | {標準} |
| Complete | 100% | — | Stable for {天數} | Any rollback |

### Feature Flag

- **Flag name**: `{feature.name.enabled}`
- **Flag type**: Percentage rollout (per-user / per-tenant)
- **Default**: off
- **Kill switch**: 可即時設為 0% 不重啟服務

## 9.2 Migration Plan

> 選填。有資料遷移時必寫（schema 變更、backfill、狀態轉換、seed data）。

### Schema Changes / Data Backfill

**Scope**: {遷移範圍}

**Strategy**: {Online migration / Offline / Backfill job}

1. **Phase 1**: {第一階段，含 backwards compatibility 處理}
2. **Phase 2**: ...
3. **Phase 3**: ...

**Estimated duration**: {預估時間}

**Rollback**: {遷移失敗時的回復策略}

### Seed Data（若有）

> 系統內建資料、預設模板、測試資料等。

- **來源**: {例：RD 手動放入 /seeds/ 目錄，啟動時載入}
- **載入時機**: {啟動時 / 部署時 / on demand}
- **驗證**: {載入時做哪些驗證}

## 9.3 Observability

> 本節是 §2.2.4 NFR 的具體實作。

### 9.3.1 Metrics

**核心 SLI (Service Level Indicators)**：

| Metric | Description | Target | Alert Threshold |
|--------|-------------|--------|-----------------|
| `{metric_name}` | {說明} | {目標值} | {alert 條件} |

**業務指標 (Business Metrics)**：

| Metric | Description |
|--------|-------------|
| `{metric_name}` | {說明} |

### 9.3.2 Logs

**Required fields** in every log:
- `timestamp` (ISO8601)
- `trace_id`
- `user_id` (如適用)
- `event_type`
- `level` (DEBUG / INFO / WARN / ERROR)

**Must log**:
- {重要事件 1}
- {重要事件 2}

**Must NOT log**:
- {敏感資料 1，例：密碼、PII、金流完整資訊}

### 9.3.3 Tracing

> 選填。單一 service 內 feature 可省。跨 3+ service 必寫。

- **追蹤鏈**: {Service A → Service B → ...}
- **Trace propagation**: {方式，例：W3C Trace Context}
- **Sampling**: {採樣策略}
- **Retention**: {保留時間}

## 9.4 Alerting

### Alert Definitions

| Alert | Trigger | Severity | Notification | Runbook |
|-------|---------|----------|--------------|---------|
| {AlertName} | {條件} | P0/P1/P2/P3 | {PagerDuty / Slack / Email} | RB-{N} |

### Severity Definitions

- **P0**: 系統嚴重損壞，資料完整性風險。立刻處理，oncall 必須中斷一切
- **P1**: 服務劣化或部分功能掛掉。1 小時內處理
- **P2**: 性能或非關鍵功能問題。當天處理
- **P3**: 訊息性，不影響使用者。下個 sprint 處理

## 9.5 Runbook

> 對應 §9.4 的每個 alert，必須有對應 runbook。

### RB-1: {Runbook 標題}

**Symptoms**: {如何辨識問題}

**Diagnosis Steps**:
1. [TODO 由運維補：具體 dashboard / 查詢]
2. {可推測的步驟}
3. ...

**Common Causes & Actions**:
- **{原因 1}**: {處理動作}
- **{原因 2}**: [TODO 由運維補：實際操作步驟]
- **{原因 3}**: {處理動作}

**Escalation**: [TODO 由運維補：升級條件與對象]

---

### RB-2: ...

## 9.6 Rollback Plan

### Rollback Triggers

任一條件滿足，立刻 rollback：
- 任何 P0 alert
- {量化條件 1}
- {量化條件 2}
- {業務指標崩盤條件}

### Rollback Procedure

**Level 1 (Soft rollback)** — 秒級生效
1. 設定 `{feature_flag} = 0`
2. 新流量走舊路徑
3. 既有資料保留

**Level 2 (Code rollback)** — 5-15 分鐘
1. Deploy 前一版本
2. Feature flag 自動失效
3. 需確認舊 code 兼容新 schema

**Level 3 (Schema rollback)** — 小時級，風險高
1. {步驟}
2. 需要 DBA 介入

### Rollback Rehearsal

**Plan**: 上線前在 staging 環境完整演練 Level 1 + Level 2，至少各執行一次。

**Verify**:
- Rollback 後流量回到舊路徑，新 feature 不被觸發
- 既有 in-flight 資料不被破壞
- 預估時間：Level 1 < 30s，Level 2 < 15 min

**Sign-off required**: Tech lead 確認演練通過，才能進入 §9.1 的 Canary stage。

## 9.7 Post-Launch Review

> 選填，有 success metrics 的 feature 建議做。

### Review Schedule

- **T+7 days**: 系統健康確認，整理初期 incident
- **T+30 days**: 業務指標檢視，比對 §1.4 Success Criteria
- **T+90 days**: 完整 retrospective，含 ADR 修訂

### Review Checklist

- [ ] §1.4 Success Criteria 是否達標？哪些沒達標、為什麼
- [ ] 哪些 EF / EC 在 prod 真的發生？發生頻率如何？
- [ ] Open Questions (§7.2) 是否都解決？
- [ ] 哪些 ADR 需要修訂或新增？
- [ ] Runbook 是否覆蓋實際遇到的 incident？需要新增哪些？
- [ ] NFR 在 prod 是否實際達標？
