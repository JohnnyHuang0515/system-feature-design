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

## Options

**(a) 只支援當前版本 —— 舊版一律拒絕，附升版說明**

- Pros：實作最小，沒有 migration 程式碼要維護；schema 可以自由演進
- Cons：使用者手上的檔案會突然失效，跨工作區分享的舊檔案全部要重做；違背 §1.1 的可攜性主張

**(b) 支援前一個 major 版本，migration 嵌在 Validation Service**

- Pros：import endpoint 維持單純，版本差異在驗證階段吸收；一次只需維護一組轉換規則
- Cons：Validation Service 同時承擔驗證與轉換兩種責任；跨兩版以上的舊檔案仍會失效

**(c) 永久支援所有歷史版本，獨立 migration service 串接轉換**

- Pros：任何時期匯出的檔案永遠可用，可攜性最強
- Cons：轉換規則隨版本數線性累積，每次 schema 變更都要回頭補所有路徑；POC 階段養不起

**建議方向：(b)**。可攜性是本 feature 的核心主張，(a) 直接打掉它；(c) 的維護成本要等真的有多版本、有使用量才划算。(b) 給使用者一個 major 版本的緩衝，也留著之後升級成 (c) 的空間。

Migration 失敗時擋下匯入並明確指出無法轉換的欄位 —— 半成品比明確失敗更傷信任（§0.4 PER-1 洞察）。

## Why Not Decided Yet

- POC 階段所有檔案都是 v0.1，無實際 migration 需求
- 等 v0.2 schema 設計時自然會出現具體需求
- 過早決定可能限制未來 schema 設計

## Next Steps

- 在 v0.2 schema 設計討論中一併決定
- 規劃 v0.2 出現的時程（暫無）
- 參考其他類似系統的 schema versioning 實踐
