# 9. Rollout & Operations

> **POC 階段**：本 feature 內部試用為主，未對外開放。本文件聚焦最小必寫集合 + 必要的 seed loading 機制。Canary / Gradual rollout 等留待 MVP 階段補。

## 9.1 Rollout Strategy

### Stages（POC 簡化版）

| Stage | Audience | Duration | Success Criteria | Abort Criteria |
|-------|----------|----------|------------------|----------------|
| Internal dogfood | RD + 2 位 PM | 1 week | 無 P0 bug、匯入成功率 > 90% | 任何 P0 bug |
| Beta（內部測試） | 全公司 PM | 2 weeks | 匯入成功率 > 95%、無資料完整性問題 | 匯入成功率 < 80% 或資料損毀 |
| GA（POC 完成） | 所有 workspace | — | Stable for 2 weeks | 任何 critical bug |

### Feature Flag

- **Flag name**: `feature.template_import_export.enabled`
- **Flag type**: Per-workspace 開關
- **Default**: off
- **Kill switch**: 可即時關閉，不需重啟

> 未來進入 MVP 後加入 percentage rollout + canary。

## 9.2 Migration Plan

### Seed Templates 載入

**Location**: `/seeds/automation-templates/`

**Strategy**: 系統啟動時掃描資料夾，對每份 .json 檔案執行 schema 驗證後載入

**載入時機**: 系統啟動完成後（不阻擋 boot sequence）

**Validation**: 共用 §6.4.2 的 ValidationService

**Failure handling**: 
- 單一檔案失敗 → log + skip + 發出 SeedTemplateLoadFailed 事件
- 整體載入失敗 → 不阻擋系統啟動（NFR-7）

**Rollback**: 
- 系統內建模板可隨時從資料夾移除，重啟生效
- POC 階段不做版本管理，覆蓋 = 直接生效

### Schema Migration

POC 階段所有檔案為 schema_version `v0.1`，無 migration 需求。
未來 v0.2 出現時的 migration 機制待 D-0010 ADR 決議。

## 9.3 Observability

> 本節是 §2.2.4 NFR-8、NFR-9 的具體實作。

### 9.3.1 Metrics

**核心 SLI**：

| Metric | Description | Target | Alert Threshold |
|--------|-------------|--------|-----------------|
| `template_import_success_rate` | 匯入成功比例（成功 / 總嘗試） | > 95% | < 90% for 30 min |
| `template_import_latency_p99` | 匯入 API 99th percentile latency | < 500ms | > 1s for 10 min |
| `template_import_validation_failure_rate` | Schema 驗證失敗比例 | < 20% | > 50% for 30 min（可能 schema bug） |
| `seed_template_load_failure_count` | 系統啟動時 seed 載入失敗檔案數 | 0 | > 0 |
| `template_export_success_rate` | 匯出成功比例 | > 99% | < 95% for 30 min |

**業務指標**：

| Metric | Description |
|--------|-------------|
| `templates_created_per_day` | 每日新建模板數（含匯入 + 新建 + AI 生成） |
| `templates_imported_per_day` | 每日匯入模板數 |
| `import_source_breakdown` | 匯入來源分佈（file / ai / seed） |
| `import_source_to_activation_rate` | 匯入後啟用比例（衡量是否被實際使用） |

### 9.3.2 Logs

**Required fields** in every log:
- `timestamp` (ISO8601)
- `trace_id`
- `user_id` (對 seed 載入為 null)
- `workspace_id` (對 seed 載入為 null)
- `event_type`（例：`template.import.attempt`, `template.import.success`, `template.import.failure`）
- `level` (DEBUG / INFO / WARN / ERROR)

**Must log**:
- 所有匯入 / 匯出嘗試（成功 + 失敗）
- 匯入失敗的具體原因（schema error / structure error / DB failure）
- Seed template 載入結果（每份檔案）
- State transitions（Draft → Active → Archived）
- 結構警告觸發（即使匯入成功）

**Must NOT log**:
- 完整的模板內容（避免機敏資料外洩，特別是 task 中可能含業務邏輯）
- 使用者個資（email、姓名等，沿用既有 PII 政策）

### 9.3.3 Tracing

POC 階段單一 service 內 feature，無跨 service 追蹤需求。

> 未來若 Validation Service 獨立部署，需補上 distributed tracing。

## 9.4 Alerting

### Alert Definitions

| Alert | Trigger | Severity | Notification | Runbook |
|-------|---------|----------|--------------|---------|
| ImportFailureSpike | success_rate < 90% for 30 min | P1 | Slack #automation-alerts | RB-1 |
| ImportLatencyHigh | latency_p99 > 1s for 10 min | P2 | Slack #automation-alerts | RB-2 |
| ValidationFailureRateAnomaly | validation_failure_rate > 50% for 30 min | P2 | Slack #automation-alerts | RB-3 |
| SeedLoadFailure | seed_template_load_failure_count > 0 at startup | P3 | Email to RD | RB-4 |
| DataIntegrityViolation | 偵測到不合法 state（例：active 模板無節點） | P0 | PagerDuty | RB-5 |

### Severity Definitions

- **P0**: 系統嚴重損壞，資料完整性風險。立刻處理
- **P1**: 服務劣化或部分功能掛掉。1 小時內處理
- **P2**: 性能或非關鍵功能問題。當天處理
- **P3**: 訊息性，不影響使用者。下個 sprint 處理

## 9.5 Runbook

### RB-1: ImportFailureSpike

**Symptoms**: 匯入成功率 < 90%，持續 30 分鐘

**Diagnosis Steps**:
1. [TODO 由運維補：哪個 dashboard 查 import metrics]
2. 看失敗集中在哪個 error code（參照 §6.5）：
   - 大量 INVALID_SCHEMA → 可能是 schema 升版相容性問題或使用者上傳異常檔案
   - 大量 INVALID_STRUCTURE → 可能是 Validation Service 邏輯 bug
   - 大量 500 → Template Service 內部問題（DB / dependency）
3. 查近期 deploy log，是否有相關變更
4. 查 trace 看失敗環節（Validation? DB?）

**Common Causes & Actions**:
- **Validation Service 異常**: 確認其健康狀態，必要時 page validation team
- **DB connection pool exhausted**: [TODO 由運維補：實際操作步驟，如擴容或 restart]
- **Recent deploy 引發 regression**: 評估 rollback（feature flag off）
- **某種特定檔案結構觸發 bug**: 收集 failed payload sample 給 RD 分析
- **[TODO 由運維新增上線後實際遇到的 cause]**

**Escalation**: [TODO 由運維補：升級條件與對象]

---

### RB-2: ImportLatencyHigh

**Symptoms**: 匯入 API p99 latency > 1s，持續 10 分鐘

**Diagnosis Steps**:
1. [TODO 由運維補：查 latency dashboard]
2. 看 latency 是集中在哪個階段：
   - Validation 階段慢 → Validation Service 問題
   - DB 寫入慢 → DB 問題（lock contention? slow query?）
   - 整體都慢 → 可能是 traffic spike
3. 查當前 throughput，是否異常高

**Common Causes & Actions**:
- **DB lock contention**: [TODO 由運維補]
- **Validation Service 變慢**: 確認其 latency metrics，必要時 escalate
- **Traffic spike**: 評估是否需要 scale up

**Escalation**: [TODO]

---

### RB-3: ValidationFailureRateAnomaly

**Symptoms**: Schema 驗證失敗比例 > 50%，持續 30 分鐘

**Diagnosis Steps**:
1. 查失敗 sample 的 error code 分佈
2. 看是否集中在某種 error type（例：突然大量 path: "/nodes/X/Y"）
3. 確認 ValidationService 邏輯近期是否變更

**Common Causes & Actions**:
- **ValidationService 部署有 bug**: 對照 Service 的版本，必要時 rollback
- **使用者集中上傳異常檔案**: 可能是某個第三方工具產生不合 schema 的檔案，shrug
- **Schema 升版了但客戶端尚未跟上**: 評估是否需 backwards compat

**Escalation**: [TODO]

---

### RB-4: SeedLoadFailure

**Symptoms**: 系統啟動時偵測到 seed template 載入失敗

**Diagnosis Steps**:
1. 查啟動 log 中 SeedTemplateLoadFailed 事件
2. 看 file_path + error_message 找到具體檔案
3. 手動驗證該檔案的 schema

**Common Causes & Actions**:
- **檔案格式錯誤**: 修正 seed 檔案，下次重啟生效
- **Schema 升版但 seed 檔案未更新**: 升版 seed 檔案到新 schema

**Escalation**: 無需 escalate，由 RD 自行處理

---

### RB-5: DataIntegrityViolation

**Symptoms**: 偵測到不合法 state（例：Active 模板無節點，違反 BR）

**Diagnosis Steps**:
1. [TODO 由運維補：哪個 query 查資料完整性]
2. 確認受影響範圍（多少 templates / workspaces）
3. 確認是否仍在發生中

**Common Causes & Actions**:
- **State machine bug** → 立即 rollback 到前一版本
- **直接 DB 操作繞過 application logic** → 找出操作來源並停止

**Escalation**: 立即 page tech lead；資料完整性問題不可延遲

## 9.6 Rollback Plan

### Rollback Triggers

任一條件滿足，立刻 rollback：
- 任何 P0 alert（DataIntegrityViolation）
- Import success rate < 80% 持續 1 hour
- 偵測到資料損毀（已有 Template 內容被誤覆蓋等）

### Rollback Procedure

**Level 1 (Feature flag off)** — 秒級生效
1. 設定 `feature.template_import_export.enabled = 0`（per-workspace 或全域）
2. 新流量無法觸發匯入 / 匯出
3. 已建立的 Template 保留，可被既有 Automation 引擎使用

**Level 2 (Code rollback)** — 5-15 分鐘
1. Deploy 前一版本
2. Feature flag 在新版本中失效，影響範圍最小化
3. 需確認舊 code 兼容當前 schema_version

**Level 3 (Schema rollback)** — POC 階段不適用
- POC 階段為新 feature，無既有 schema 需要 rollback

### Rollback Rehearsal

**Plan**: 上線前在 staging 演練 Level 1 至少 1 次。Level 2 演練在 release 流程中已涵蓋。

**Verify**:
- Feature flag off 後新匯入請求收到適當錯誤訊息（例：feature unavailable）
- 既有匯入的模板不受影響
- 預估時間：Level 1 < 30s, Level 2 < 15 min

**Sign-off required**: Tech lead 確認演練通過，才能進入 Beta stage（§9.1）

## 9.7 Post-Launch Review

### Review Schedule

- **T+1 week** (Internal dogfood 結束): 確認無 P0 bug，蒐集 RD/PM 使用回饋
- **T+1 month** (Beta 結束): 業務指標檢視，比對 §1.4 Success Criteria
- **T+3 months** (POC 完成後): 完整 retrospective，含 ADR 修訂

### Review Checklist

- [ ] §1.4 Success Criteria 是否達標？
  - [ ] 匯入成功率 > 95%？
  - [ ] 匯入後模板結構完整？
  - [ ] 3 個月後是否 > 30% 新模板來自匯入路徑？
- [ ] 哪些 EF / EC 在 prod 真的發生？發生頻率如何？
- [ ] Open Questions (§7.2) 是否解決？
  - [ ] D-0010 Schema migration 是否需要進入 MVP？
  - [ ] D-0011 Rate limiting 是否在 prod 表現中需要？
- [ ] 哪些 ADR 需要修訂或新增？
  - [ ] D-0001 (內嵌 vs 引用) 是否實際看到使用者需要引用模式？
  - [ ] D-0005 (驗證嚴格度) 是否擋住合理場景或漏了該擋的？
- [ ] Runbook 是否覆蓋實際遇到的 incident？需要新增哪些？
- [ ] NFR-1 latency 在 prod 是否實際達標？
- [ ] 是否該進入 MVP（對外開放）？需要補上哪些 rollout 細節？
