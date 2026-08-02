# 01 — 匯出模板成 JSON 檔

**What to build:** 使用者在流程編輯器或模板列表按「匯出」，瀏覽器下載一份自包含的 JSON 檔，
內含該模板最新版本的節點與連線。空模板（無節點）擋下並顯示錯誤。

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

## Acceptance criteria

- [ ] AC-1.1: 成功匯出含節點的模板
- [ ] AC-1.2: 匯出無節點模板應失敗

## Spec references

- FR: FR-1
- UF: UF-3
- ADR: D-0007（模板自包含）、D-0009（只匯出最新版本）

> 這張票同時把 JSON 格式契約落地，後面所有匯入相關的票都吃它。
