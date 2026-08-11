# 07 — 系統啟動載入 Seed 模板

**What to build:** 系統啟動時掃描指定資料夾，把裡面的模板 JSON 走匯入路徑寫入，
成為系統內建模板。重複啟動不重複建立。單一檔案失敗不影響其他檔案載入。

**Blocked by:** 02 — 匯入 JSON 檔並存成 Draft

**Status:** ready-for-agent

## Acceptance criteria

- [ ] AC-8.1: Seed 載入成功
- [ ] AC-8.2: Seed 載入失敗 skip

## Spec references

- FR: FR-8
- UF: UF-6
- ADR: D-0006（seed 模板以資料夾提供）
