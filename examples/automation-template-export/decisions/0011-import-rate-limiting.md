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

## Options

**(a) 不限流,靠 feature flag 止血**

- Pros：零實作;§9.1 的 per-workspace flag 已經能在事故當下直接關掉
- Cons：止血是全有全無的,一個客戶端迴圈 retry 會拖累整個 workspace 的其他使用者;沒有任何訊號能在事故前示警

**(b) Per-user 限流,由 API gateway 統一處理**

- Pros：匯入是低頻操作,per-user 門檻不會誤傷正常使用;gateway 統一處理表示 Template Service 不必自己實作;Seed 載入不走 gateway 天然不受限
- Cons：要新增 `429 RATE_LIMITED` 進 §6.5 catalog 並補前端 UX;閾值在沒有流量資料前只能先猜再調

**(c) Per-workspace 限流,Template Service 自行實作**

- Pros：直接對應 §9.1 的 flag 粒度,計費與配額未來也是以 workspace 為單位
- Cons：同一 workspace 內一個人就能吃掉全隊配額;service 自行實作等於把限流邏輯散進每支 API

**建議方向：(b)**。匯入低頻,per-user 的門檻寬到不會誤傷,而 gateway 統一處理讓這條規則不會在下一支 API 重寫一次。閾值先取 10 次 / 分鐘,Beta 期間依實際分佈調整。

AI 路徑沿用既有扣點機制,不重複限流 —— 扣點本身就限制了呼叫量。

## Why Not Decided Yet

- POC 內部試用，使用者少且可信，無實際濫用風險
- 無流量資料，現在訂閾值是憑空猜測
- Feature flag（§9.1）已提供緊急止血手段（per-workspace 直接關閉）

## Next Steps

- Beta 期間觀察 §9.3.1 的 `templates_imported_per_day` 與 import API 流量分佈
- 對外開放（MVP）前由 @tech-lead 決議，屆時轉為 Accepted ADR
- 若決定實作，同步更新 §6.2 / §6.5 與前端錯誤處理
