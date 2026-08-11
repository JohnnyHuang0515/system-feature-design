# 06 — AI 生成內容走同一條匯入路徑

**What to build:** AI 生成的模板內容不另開寫入路徑，走與檔案上傳相同的驗證與寫入流程，
因此同樣會被 schema 驗證擋下、同樣存成 Draft。生成內容不合法時，回到 AI 生成的失敗流程。

**Blocked by:** 03 — Schema 驗證與錯誤呈現（AI 內容必須經過同一道驗證）

**Status:** ready-for-agent

## Acceptance criteria

- [ ] AC-7.1: AI 生成走匯入機制
- [ ] AC-7.2: AI 生成不合法應走 AI 失敗流程

## Spec references

- FR: FR-7
- UF: UF-4

> 這張票的價值在於「不新增第二條寫入路徑」。兩條路徑各自驗證，
> 遲早會漂移成兩套規則。
