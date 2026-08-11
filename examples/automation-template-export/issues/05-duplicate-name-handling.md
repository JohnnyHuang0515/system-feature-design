# 05 — 同名衝突處理

**What to build:** 匯入時偵測 workspace 內是否已有同名模板。有的話跳 Modal 讓使用者選
「覆蓋 / 建立新的 / 取消」，三個分支各自把資料處理到正確狀態。

**Blocked by:** 02 — 匯入 JSON 檔並存成 Draft

**Status:** ready-for-agent

## Acceptance criteria

- [ ] AC-5.1: 同名偵測跳出 Modal
- [ ] AC-5.2: 「覆蓋既有」儲存為新版本
- [ ] AC-5.3: 「建立新的」加 suffix
- [ ] AC-5.4: 同名但未提供 action

## Spec references

- FR: FR-5
- UF: UF-1
- ADR: D-0004（同名處理在確認階段跳 Modal）

> 與 03 / 07 互不阻塞 —— 02 落地後這三張可以同時發包。
