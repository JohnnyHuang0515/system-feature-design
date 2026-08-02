# Reference Guide: 6-interfaces.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/6-interfaces.template.md`.
> Instructions here are English; the quoted blocks are scripts spoken to the user — use them as written.

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

Reverse-engineer error codes from every §4.2 EF. HTTP status maps to the EF's failure type; codes are UPPER_SNAKE_CASE; the same code returns the same status on every endpoint.

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

1. 匯入流程:我設計成「兩階段」 — 先 POST /import 取得預覽 token,
   再 POST /import/confirm 寫入。這樣可以在預覽頁停留時驗證結果保留。
   你比較想要這樣,還是「單階段」(POST 一次直接寫入)?

2. 失敗時的 error message 要不要包含「具體錯誤位置」(例:
   `path: "/nodes/0/name"`)?好處是 client 可以精準指出哪裡錯,
   壞處是 schema 細節曝光。

3. Rate limiting:POC 階段需要做嗎?還是先不做?
```

## Where you'll get stuck

### The user isn't familiar with API design

Propose two designs and let them pick. Starting from a blank page is the hard part.

### The user gets tangled in schema detail

Hold the conversation at the contract level, and note that implementation detail — whether a DB column is varchar or text — belongs to the backend.

### Error-code naming goes in circles

Give the naming rule: UPPER_SNAKE_CASE, HTTP status plus a specific description — `404 TEMPLATE_NOT_FOUND`, not `404 NOT_FOUND`.

## Reflection check, before §7

- [ ] Every §2.1 FR maps to at least one endpoint, inbound event / webhook (§6.3), or background job trigger
- [ ] Every endpoint maps to at least one SF
- [ ] Every endpoint's errors are registered in the §6.5 catalog
- [ ] Every published event is listed in §3.5
- [ ] Every external integration has timeout + retry + failure handling
- [ ] Marker lifecycle done: confirmed markers deleted, surviving `[待拍板]` carry options and a recommendation, deferred ones converted to a D-NNNN reference

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
