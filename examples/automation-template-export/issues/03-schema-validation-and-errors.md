# 03 — Schema 驗證與錯誤呈現

**What to build:** 匯入時先對 JSON 做 schema 與結構驗證。不合法就停在原頁、不寫入，
並顯示具體哪裡錯。結構異常（孤兒節點、重複連線）只警告不擋，讓使用者自己決定要不要繼續。

**Blocked by:** 02 — 匯入 JSON 檔並存成 Draft

**Status:** ready-for-agent

## Acceptance criteria

- [ ] AC-3.1: schema 不合法時拒絕並顯示錯誤位置
- [ ] AC-3.2: 結構異常只警告不阻擋
- [ ] AC-3.3: 驗證失敗不產生任何寫入
- [ ] AC-9.1 ~ AC-9.3: 孤兒節點 / 重複連線 / 自連的警告呈現

## Spec references

- FR: FR-3, FR-9
- UF: UF-1
- ADR: D-0005（結構驗證的嚴格度：警告不阻擋）
