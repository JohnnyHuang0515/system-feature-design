# D-0010: Schema 升版時的 migration 機制

- **Status**: Proposed
- **Date**: 2026-05-14
- **Affects**: §3.2 (schema_version), §4.1 (SF-1)
- **Owner**: @bobo
- **Target Date**: Post-POC（schema v0.2 出現前需決定）

## Context

匯入檔案內有 `schema_version` 欄位（目前 `v0.1`）。當系統未來升級到 v0.2 時，需要決定：

1. 舊版（v0.1）檔案是否仍能匯入？
2. 如果可以，如何 migrate 到新版？
3. Migration 邏輯放在 import 階段還是獨立的 migration 服務？

POC 階段所有檔案都是 v0.1，沒有版本相容問題。但隨著 schema 演進（例：新增「並行分支」、改變欄位結構），這個問題必然出現。

## Open Questions

需要決定的具體事項：

1. **支援哪些舊版？** 永久支援所有歷史版本？只支援前一版？支援滾動 window（最近 N 個版本）？
2. **Migration 邏輯寫在哪？** 嵌入 import endpoint？獨立 migration service？前端做？
3. **Migration 失敗時的行為？** 擋下匯入？降級匯入（只匯能對應的部分）？提示使用者手動修正？
4. **是否提供「升版工具」？** 讓使用者可以把舊檔案先 migrate 為新版檔案，再使用？

## Tentative Direction

初步方向（待討論）：

- **支援前一個 major 版本**：v0.2 出來時，支援 v0.1 跟 v0.2；v0.3 出來時 deprecate v0.1
- **Migration 邏輯嵌入 Validation Service**：保持 import endpoint 簡單，內部處理版本差異
- **Migration 失敗 = 擋下匯入並提示**：明確告訴使用者「v0.1 的 X 欄位無法 migrate，請手動處理」

## Why Not Decided Yet

- POC 階段所有檔案都是 v0.1，無實際 migration 需求
- 等 v0.2 schema 設計時自然會出現具體需求
- 過早決定可能限制未來 schema 設計

## Next Steps

- 在 v0.2 schema 設計討論中一併決定
- 規劃 v0.2 出現的時程（暫無）
- 參考其他類似系統的 schema versioning 實踐
