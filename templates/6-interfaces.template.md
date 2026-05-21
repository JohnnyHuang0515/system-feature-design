# 6. Interface Contracts

> 本文件定義系統的對外契約 — 對前端、整合方、其他服務暴露的介面。

## 6.1 Interface Overview

> 系統暴露的所有介面類型總覽，方便快速掌握全貌。

| Type | Identifier | Direction | Purpose |
|------|------------|-----------|---------|
| REST API | `POST /endpoint` | Inbound | {用途} |
| Webhook | {名稱} | Inbound | {用途} |
| Event | `{EventName}` | Outbound | {用途} |
| External call | `{Service.method}` | Outbound | {用途} |

## 6.2 REST API Specifications

> 本節以 REST API 為預設。其他協定（GraphQL / gRPC / WebSocket）改寫對應結構，
> 但核心欄位不變：認證、輸入、輸出、錯誤、與 FR/SF 的對應。

### {METHOD} {/path}

{一句話描述}

**Related**: FR-{N}, SF-{N}
**Auth**: {認證要求}

#### Request

```json
{
  "field_name": "type (constraints)"
}
```

#### Response

**{Success Status Code}**:
```json
{
  "field_name": "type"
}
```

**Errors**:
- `{Status} {ERROR_CODE}` — {何時發生}（對應 EF-{N}）

---

### {METHOD} {/path 2}

...

## 6.3 Webhooks / Inbound Events

> 選填：無外部 callback 的 feature 省略。

### POST {/webhook-path}

{描述：誰會呼叫、為什麼呼叫}

**Source**: {誰呼叫}
**Auth**: {驗證方式，例：HMAC signature}
**Idempotency**: {去重策略}
**Retry**: {來源系統的 retry 行為}

#### Payload

```json
{
  "field_name": "type"
}
```

#### Response

- **200 OK** — {說明}
- **400** — {說明}
- **401** — {說明}

**Triggers**: SF-{N} 的 webhook 階段

## 6.4 Outbound Events & Integrations

### 6.4.1 Published Events

> 本節是 §3.5 Domain Events 的子集 — 只有「對外發布」的部分。
> 對應到 §3.5 的事件，補上 channel、schema、consumers 等契約細節。

#### {EventName}

**Published when**: {對應 state machine 或某動作}
**Channel**: {Kafka topic / SNS / Pub/Sub topic 名稱}
**Schema**:
```json
{
  "event_type": "{EventName}",
  "event_id": "uuid",
  "occurred_at": "ISO8601",
  ...
}
```
**Known consumers**: {誰會訂閱}
**Ordering**: {順序保證}
**Retention**: {保留時間}

### 6.4.2 External Integrations

> 對外部系統的呼叫。
> 每個 integration 必須明確寫出 timeout、retry、failure handling。

#### {Service.method}

**Purpose**: {為什麼呼叫}
**Called from**: SF-{N} step {N}
**Timeout**: {秒數}
**Retry**: {次數 + 策略，例：3 次 exponential backoff}
**Failure handling**: {失敗時的處理，對應 EF-{N}}
**Idempotency**: {idempotency key 設計}

## 6.5 Error Model

> 系統統一的錯誤回應格式。所有 endpoint 的 errors 都對應這裡。

### 6.5.1 Error Response Format

```json
{
  "error": {
    "code": "STRING_CONSTANT",
    "message": "human-readable description",
    "details": {},
    "trace_id": "uuid"
  }
}
```

### 6.5.2 Error Code Catalog

> **Source of truth for error codes**。所有 6.2 endpoint 提到的 error code 都必須在此註冊。

| HTTP Status | Code | Meaning | Used by |
|------------|------|---------|---------|
| 400 | INVALID_REQUEST | 請求格式錯誤 | All endpoints |
| 401 | UNAUTHORIZED | 未認證 | All authed endpoints |
| 403 | FORBIDDEN | 已認證但無權限 | All authed endpoints |
| 404 | {RESOURCE}_NOT_FOUND | {資源}不存在 | {endpoints} |
| 409 | {SPECIFIC_CONFLICT} | {衝突描述} | {endpoints} |
| 422 | BUSINESS_RULE_VIOLATION | 違反業務規則 | All write endpoints |
| 429 | RATE_LIMITED | 達到速率限制 | All endpoints |
| 500 | INTERNAL_ERROR | 系統錯誤 | All endpoints |

## 6.6 Versioning & Compatibility

> 選填：純內部 API、或 feature 是現有 API 的小增量，可寫一行「沿用既有 versioning 策略」。

- **Version scheme**: {URL path versioning / Header versioning}
- **Backwards compatibility rules**:
  - {規則}
- **Deprecation policy**: {標記 deprecated 後的保留時間 + 通知方式}
- **Breaking changes**: {何時必須升 major version}
