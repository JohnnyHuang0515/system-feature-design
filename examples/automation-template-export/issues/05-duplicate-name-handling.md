# 05 — 同名衝突處理

**What to build:** 匯入時偵測 workspace 內是否已有同名模板。有的話跳 Modal 讓使用者選
「覆蓋 / 建立新的 / 取消」，三個分支各自把資料處理到正確狀態。

**Blocked by:** 02 — 匯入 JSON 檔並存成 Draft

**Status:** ready-for-agent

## Acceptance criteria

- [ ] AC-5.1: 偵測到同名時跳出選擇 Modal
- [ ] AC-5.2: 選「覆蓋」更新既有模板
- [ ] AC-5.3: 選「建立新的」產生新模板
- [ ] AC-5.4: 選「取消」不留下任何變更

## Spec references

- FR: FR-5
- UF: UF-1
- ADR: D-0004（同名處理在確認階段跳 Modal）

> 與 03 / 07 互不阻塞 —— 02 落地後這三張可以同時發包。
