# 7. Decisions

本 feature 的設計決策記錄在 `decisions/` 目錄中，每個 decision 一個檔案。

## 7.1 Decision Index

> **這張表是已拍板決策的唯一去處。** §7.2 的某條被拍板了，就把該檔的 Status 改成
> Accepted、把那一列從 §7.2 搬過來 —— 不要另開一節放「已決事項」。門檻以下、
> 不值得展開成 ADR 的，留在 §1.5.1 或 §2.3，也不進這裡。

### Accepted Decisions

| ID | Title | Status | Date | Affects |
|----|-------|--------|------|---------|
| [D-0001](./decisions/0001-{title}.md) | {決策標題} | Accepted | YYYY-MM-DD | §3.X, §5.X |
| [D-0002](./decisions/0002-{title}.md) | ... | Accepted | ... | ... |

### Superseded / Deprecated

| ID | Title | Status | Superseded by |
|----|-------|--------|---------------|
| [D-0000](./decisions/0000-{title}.md) | ~~{舊決策標題}~~ | Superseded by D-{N} | D-{N} |

## 7.2 Open Questions

> 列出 Status: Proposed 的 D-N，等待決議。
> **一條都沒有時，整節就寫一個「無」，不要寫一句話說明沒有。**
> 標記的字面本身是被 grep 的目標 —— 一句「沒有未決事項」只要帶到那四個字，
> 就會被收尾檢查與 full-spec-review Check 0 當成殘留標記報錯。

| ID | Title | Blocking? | Owner | Target Date |
|----|-------|-----------|-------|-------------|
| [D-0003](./decisions/0003-{title}.md) | {待決議標題} | Yes / No | @{name} | YYYY-MM-DD |
