# 02 — 匯入 JSON 檔並存成 Draft

**What to build:** 使用者上傳一份合法的模板 JSON，系統解析後建立模板與其節點、連線，
狀態為 Draft，並導回模板列表看得到這筆。未登入 / 未授權的匯入被擋下。

**Blocked by:** 01 — 匯出模板成 JSON 檔（格式契約由它定義）

**Status:** ready-for-agent

## Acceptance criteria

- [ ] AC-2.1: 成功匯入合法檔案（無同名）
- [ ] AC-2.3: 未授權匯入
- [ ] AC-6.1: 匯入後狀態為 Draft
- [ ] AC-6.2: 使用者手動啟用才轉為 Active

## Spec references

- FR: FR-2, FR-6
- UF: UF-1
- ADR: D-0008（匯入一律先存 Draft）

> 這張票刻意窄：不含 schema 驗證（03）、不含預覽頁（04）、不含同名處理（05）。
> 只做「合法檔案進得來、存得住、看得到」這條最短的完整路徑。
