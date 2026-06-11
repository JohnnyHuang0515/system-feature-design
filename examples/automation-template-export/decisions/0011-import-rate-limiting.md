# D-0011: 匯入 API 是否需要 rate limiting

- **Status**: Proposed
- **Date**: 2026-05-14
- **Affects**: §6.2 (POST /api/templates/import), §6.5 (error catalog), §2.2
- **Owner**: @tech-lead
- **Target Date**: Before MVP

## Context

`POST /api/templates/import` 接收檔案上傳（最大 5 MB, BR-6）並觸發 schema + 結構驗證，是相對昂貴的操作（解析 + 驗證 CPU 密集）。可能的濫用 / 誤用場景：

- 客戶端 bug 造成的迴圈 retry
- 惡意使用者連續上傳大檔案消耗驗證資源
- AI 生成路徑（SF-3）的自動 retry 重投

目前的相關防線：idempotency key 去重（EC-7，但只防重複寫入、不防驗證資源消耗）、feature flag per-workspace 開關（§9.1）、認證要求（NFR-3）。POC 為內部試用，流量小且使用者可信。

## Open Questions

需要決定的具體事項：

1. **限流維度？** Per-user、per-workspace、還是 global？匯入是低頻操作，per-user 可能就足夠
2. **閾值多少？** 無實際流量資料前難以定錨
3. **超限的回應？** 需新增 `429 RATE_LIMITED` 進 §6.5 error catalog，前端要有對應 UX
4. **AI 生成路徑是否同樣限流？** AI 模組已有扣點機制，天然限制呼叫量，可能不需要重複限制
5. **實作層級？** API gateway 統一處理，還是 Template Service 自行實作？

## Tentative Direction

初步方向（待討論）：

- **Per-user 限流**（例：10 次 / 分鐘），由 API gateway 統一處理，service 不自行實作
- **超限回 429 RATE_LIMITED**，補進 §6.5 catalog；前端顯示「請稍後再試」
- **Seed 載入（SF-4）不受限**：系統內部行為，不走 API gateway
- **AI 路徑沿用扣點機制**，不額外限流

## Why Not Decided Yet

- POC 內部試用，使用者少且可信，無實際濫用風險
- 無流量資料，現在訂閾值是憑空猜測
- Feature flag（§9.1）已提供緊急止血手段（per-workspace 直接關閉）

## Next Steps

- Beta 期間觀察 §9.3.1 的 `templates_imported_per_day` 與 import API 流量分佈
- 對外開放（MVP）前由 @tech-lead 決議，屆時轉為 Accepted ADR
- 若決定實作，同步更新 §6.2 / §6.5 與前端錯誤處理
