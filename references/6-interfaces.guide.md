# Reference Guide: 6-interfaces.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/6-interfaces.template.md`.

## Purpose

Define the system's outward contract — what it exposes to the frontend, to integrators, to other services. Engineers open this document more than any other, so it has to be exact.

## Opening

```
進入第六份:介面契約。

這份定義對外暴露的 API、events、整合點 — 前後端對齊的關鍵。

我會根據 §3 entity 跟 §4 SF 推導完整 API spec,你確認 / 修正。
```

## Derivation

### Overview

Scan §4.1 SFs for boundary-crossing points and collect them into the overview table.

### REST APIs

| Target | Source |
|---|---|
| Endpoint list | The outward entry point of each §4.1 SF |
| Request schema | §3.2 entity fields plus the FR's inputs |
| Response schema | §3.2 entity fields, limited to what's safe to expose |
| Auth requirement | §2.2.2 NFR |
| Errors | The §4.2 EFs each endpoint can hit |

### Error model

Reverse-engineer error codes from every §4.2 EF. HTTP status maps to the EF's failure type; the same code returns the same status on every endpoint; codes are UPPER_SNAKE_CASE and specific — `404 TEMPLATE_NOT_FOUND`, not `404 NOT_FOUND`.

**Every code used by a §6.2 endpoint must be registered in the §6.5 catalog.** Build the catalog as you derive.

### Webhooks and inbound events, where they exist

Derive from the externally-triggered parts of §4.1 SFs. Two shapes:

- **Webhook** — an external system calls us over HTTP (has a path, HMAC, HTTP response)
- **Event subscription** — we subscribe to a message queue or event bus (has a channel, dedup, DLQ; no HTTP response)

An event-driven FR (「收到來源事件就建立 X」) legitimately has no endpoint — this section is where its contract lives. Skip the section when neither shape applies.

### Outbound events

§6.4.1 is the externally-published subset of §3.5. Internal-only events stay in §3.5 and are not listed here. Published events carry channel, schema, consumers and retention.

### External integrations

§6.4.2 lists the outbound service calls in §4.1 SFs. **Timeout, retry and failure handling are all mandatory** for each.

## Questions you must ask

1. **API shape** — single-stage or two-stage (is import 「上傳直接寫」 or preview-then-confirm)?
2. **Schema exposure** — is this field internal or safe to expose?
3. **Rate limiting** — needed? External-facing services usually are.

## Open question candidates

- API style (REST resource-oriented vs RPC-style)
- Single-stage vs two-stage import
- Versioning mechanism (URL path vs header)
- Large-file handling (stream vs single upload)

## Display format

### Step 1: overview

```
我整理出對外介面總覽:

REST endpoints({N} 個):
- POST /api/templates/import - 匯入
- GET /api/templates/:id/export - 匯出
- ...

Events({N} 個):
- TemplateImported(對外發布)
- ...

External integrations({N} 個):
- ValidationService.validate()
- ...
```

### Step 2: endpoint by endpoint

One at a time for complex endpoints; batch the simple ones. Each gets method + path + auth + request + response + errors.

### Step 3: error catalog

Once every endpoint is covered, show the full catalog.

### Step 4: the decisions

```
有幾件事需要你拍板:

❓ **Q1** — **匯入流程幾階段**:(a) 兩階段 —— 先 POST /import 取預覽 token,再 POST /import/confirm 寫入 (b) 單階段 —— POST 一次直接寫入
➡️ 建議 (a) —— 預覽頁停留時驗證結果還在,使用者不必重傳一次檔案

❓ **Q2** — **失敗訊息帶不帶錯誤位置**(例 `path: "/nodes/0/name"`):(a) 帶 (b) 不帶
➡️ 建議 (a) —— 這是內部工具,而「不知道哪裡錯」是匯入最常見的挫折

❓ **Q3** — **Rate limiting**:(a) POC 先不做 (b) 現在就做
➡️ 建議 (a) —— 內部試用流量小,而 §9 的 feature flag 已經能緊急止血
```

## Where you'll get stuck

### The user isn't familiar with API design

Propose two designs and let them pick. Starting from a blank page is the hard part.

### The user gets tangled in schema detail

Hold the conversation at the contract level, and note that implementation detail — whether a DB column is varchar or text — belongs to the backend.

### Error-code naming goes in circles

Give them the naming rule from `Error model` above and pick for them.

## Reflection check, before §7

- [ ] Every §2.1 FR maps to a named §6 item — an endpoint (§6.2), an inbound event or webhook (§6.3), or a published event (§6.4.1). An FR whose only answer is 「背景工作做的」 has no interface written, so name the event that starts it
- [ ] Every endpoint maps to at least one SF
- [ ] Every endpoint's errors are registered in the §6.5 catalog
- [ ] Every published event is listed in §3.5
- [ ] Every external integration has timeout + retry + failure handling

Then run the three checks from inside the spec folder and **say what they printed**:

- [ ] `grep -c "\[需確認\|\[待拍板" 6-interfaces.md` → `0`
- [ ] `python3 <skill-path>/scripts/check-sections.py .` → ✓
- [ ] `python3 <skill-path>/scripts/check-example-ids.py .` → ✓

## Closing summary

```
§6 interfaces 完成!

- REST endpoints:{N} 個
- Webhooks:{N} 個 / 無
- Published events:{N} 個
- External integrations:{N} 個
- Error codes:{N} 個

接下來進入 §7 decisions,我會整理前面散落的關鍵決策成正式 ADR,並列出待拍板事項。要進嗎?
```
