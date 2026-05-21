# 6. Interface Contracts

## 6.1 Interface Overview

| Type | Identifier | Direction | Purpose |
|------|------------|-----------|---------|
| REST API | `POST /api/templates/import` | Inbound | 上傳檔案或 JSON body 匯入模板 |
| REST API | `POST /api/templates/import/confirm` | Inbound | 確認匯入（從預覽進入寫入） |
| REST API | `GET /api/templates/:id/export` | Inbound | 匯出模板為 JSON |
| Event | `TemplateImported` | Outbound | 通知 audit log |
| Event | `TemplateExported` | Outbound | 通知 audit log |
| Event | `TemplateActivated` | Outbound | 通知（未來擴充） |
| Event | `SeedTemplateLoadFailed` | Outbound | RD log monitoring |
| Internal call | `ValidationService.validate()` | Outbound | 呼叫驗證服務 |

> **協定說明**：本 spec 以 REST API 為預設。所有 endpoint 使用 JSON 作為 request / response body（除上傳檔案使用 multipart）。

## 6.2 REST API Specifications

### POST /api/templates/import

匯入模板的第一步：上傳檔案或提供 JSON 內容，執行驗證並回傳預覽資訊。
**注意：此 endpoint 不直接寫入 DB**，需透過 `/confirm` 完成寫入。

**Related**: FR-2, FR-3, FR-4, FR-7, SF-1, SF-3
**Auth**: Required (workspace member)

#### Request

**Variant A：檔案上傳**（給檔案匯入用）

Content-Type: `multipart/form-data`

```
file: <binary, JSON file, max 5 MB>
```

**Variant B：JSON body**（給 AI 生成寫入用）

Content-Type: `application/json`

```json
{
  "source": "ai",
  "template": { /* 完整 schema，見 §3.2 */ }
}
```

#### Response

**200 OK**（驗證通過，待確認）
```json
{
  "preview_token": "string，用於 /confirm 的暫存 token，5 分鐘有效",
  "template_info": {
    "name": "string",
    "description": "string | null",
    "node_count": "integer",
    "connection_count": "integer"
  },
  "thumbnail": {
    "nodes": [ /* 簡化的節點資訊 */ ],
    "connections": [ /* 簡化的連線資訊 */ ]
  },
  "warnings": [
    {
      "type": "orphan_node | duplicate_connection",
      "message": "string"
    }
  ],
  "duplicate_name_detected": "boolean"
}
```

**Errors**:
- `400 INVALID_SCHEMA` — schema 驗證失敗（對應 EF-1），response 包含具體錯誤位置
- `400 INVALID_STRUCTURE` — 結構驗證失敗（節點自連、連線引用不存在的欄位等）（對應 EF-3, EF-4）
- `400 FILE_TOO_LARGE` — 檔案超過 5 MB（對應 EF-2）
- `400 INVALID_REQUEST` — request 格式錯誤
- `401 UNAUTHORIZED` — 未認證
- `415 UNSUPPORTED_MEDIA_TYPE` — Content-Type 非預期類型

---

### POST /api/templates/import/confirm

確認匯入：根據 preview_token 寫入資料庫，回傳新建立的 template_id。

**Related**: FR-2, FR-5, FR-6, SF-1
**Auth**: Required (workspace member)

#### Request

Content-Type: `application/json`

Header (optional): `X-Idempotency-Key: <uuid>` （重複觸發去重，5 分鐘內視為同一筆）

```json
{
  "preview_token": "string，來自 /import 回應",
  "duplicate_name_action": "overwrite | create_new | null"
}
```

- `duplicate_name_action`: 若 preview 階段 `duplicate_name_detected = true`，必須提供 `overwrite` 或 `create_new`；否則回傳 409
- 若 `duplicate_name_detected = false`，本欄位填 null 或省略

#### Response

**201 Created**
```json
{
  "template_id": "uuid",
  "name": "string (可能加 suffix，若 action=create_new)",
  "status": "Draft",
  "version": "v1.0",
  "created_at": "ISO8601"
}
```

**Errors**:
- `400 INVALID_PREVIEW_TOKEN` — token 過期或無效
- `409 DUPLICATE_NAME_UNRESOLVED` — 偵測到同名但未提供 action（對應 EC-1）
- `401 UNAUTHORIZED` — 未認證
- `403 FORBIDDEN` — 認證但無權限寫入該 workspace
- `500 INTERNAL_ERROR` — DB 寫入失敗（對應 EF-5），transaction 已 rollback

---

### GET /api/templates/:id/export

將指定模板匯出為 JSON 檔案。

**Related**: FR-1, SF-2
**Auth**: Required (workspace member, must own or have read access)

#### Request

Path parameter:
- `id`: Template UUID

#### Response

**200 OK**

Content-Type: `application/json`
Content-Disposition: `attachment; filename="{template_name}_{YYYYMMDD}.json"`

Body: 符合 §3.2 完整 JSON Schema 的內容

**Errors**:
- `404 TEMPLATE_NOT_FOUND` — 模板不存在
- `403 FORBIDDEN` — 無權限存取該模板
- `422 EMPTY_TEMPLATE` — 模板無任何節點（對應 EF-6）
- `500 INTERNAL_ERROR` — 序列化失敗

## 6.3 Webhooks / Inbound Events

本 feature 不接收外部 webhook。本節省略。

## 6.4 Outbound Events & Integrations

### 6.4.1 Published Events

> 對應 §3.5 Domain Events 中對外發布的部分。

#### TemplateImported

**Published when**: Template 從匯入路徑寫入成功（SF-1, SF-3, SF-4 完成後）
**Channel**: Internal event bus（POC 階段可用同步呼叫 audit service，未來轉 Kafka topic `template.events`）
**Schema**:
```json
{
  "event_type": "TemplateImported",
  "event_id": "uuid",
  "occurred_at": "ISO8601",
  "template_id": "uuid",
  "workspace_id": "uuid",
  "imported_by": "uuid | null（seed 載入時為 null）",
  "source": "file | ai | seed"
}
```
**Known consumers**: Audit Service
**Ordering**: 同一 workspace 內保證順序
**Retention**: 90 days（POC 階段，未來依 audit 政策調整）

---

#### TemplateExported

**Published when**: 使用者觸發匯出 API 成功
**Channel**: Internal event bus
**Schema**:
```json
{
  "event_type": "TemplateExported",
  "event_id": "uuid",
  "occurred_at": "ISO8601",
  "template_id": "uuid",
  "exported_by": "uuid",
  "workspace_id": "uuid"
}
```
**Known consumers**: Audit Service
**Retention**: 90 days

---

#### SeedTemplateLoadFailed

**Published when**: 系統啟動載入 seed 檔案失敗
**Channel**: Internal event bus + system log
**Schema**:
```json
{
  "event_type": "SeedTemplateLoadFailed",
  "event_id": "uuid",
  "occurred_at": "ISO8601",
  "file_path": "string",
  "error_code": "string",
  "error_message": "string"
}
```
**Known consumers**: System monitoring（RD log）
**Retention**: 30 days

### 6.4.2 External Integrations

#### ValidationService.validate()

**Purpose**: 驗證匯入的 JSON schema 與結構（schema 規則 + BR-4, BR-5）
**Called from**: SF-1 step 2, SF-3 step 3, SF-4 對每個檔案
**Timeout**: 3 seconds
**Retry**: 不 retry（validation 失敗不會因 retry 變成成功）
**Failure handling**: Validation Service 不可用時，import API 回傳 503 SERVICE_UNAVAILABLE 給呼叫端；對 seed 載入則 log + skip 檔案（NFR-7）
**Idempotency**: N/A（無副作用，純驗證）

## 6.5 Error Model

### 6.5.1 Error Response Format

```json
{
  "error": {
    "code": "STRING_CONSTANT",
    "message": "human-readable description",
    "details": {
      "path": "JSON path of error, e.g., /nodes/0/name",
      "warnings": [ /* 結構警告陣列，若適用 */ ]
    },
    "trace_id": "uuid"
  }
}
```

### 6.5.2 Error Code Catalog

> **Source of truth for all error codes used by this feature**。

| HTTP Status | Code | Meaning | Used by |
|------------|------|---------|---------|
| 400 | INVALID_REQUEST | 請求格式錯誤 | All endpoints |
| 400 | INVALID_SCHEMA | 匯入檔案 schema 不符 | POST /import |
| 400 | INVALID_STRUCTURE | 結構驗證失敗（節點自連、引用錯誤） | POST /import |
| 400 | FILE_TOO_LARGE | 檔案超過 5 MB | POST /import |
| 400 | INVALID_PREVIEW_TOKEN | preview_token 過期或無效 | POST /import/confirm |
| 401 | UNAUTHORIZED | 未認證 | All authed endpoints |
| 403 | FORBIDDEN | 已認證但無權限 | POST /import/confirm, GET /export |
| 404 | TEMPLATE_NOT_FOUND | 模板不存在 | GET /export |
| 409 | DUPLICATE_NAME_UNRESOLVED | 偵測到同名但未提供處理動作 | POST /import/confirm |
| 415 | UNSUPPORTED_MEDIA_TYPE | Content-Type 非預期類型 | POST /import |
| 422 | EMPTY_TEMPLATE | 模板無任何節點，無法匯出 | GET /export |
| 500 | INTERNAL_ERROR | 系統錯誤（含 DB 寫入失敗） | All endpoints |
| 503 | SERVICE_UNAVAILABLE | 下游服務（Validation Service）不可用 | POST /import |

## 6.6 Versioning & Compatibility

POC 階段沿用既有 API versioning 策略，不另外定義。

**未來方向**（後續展開為 ADR）：
- `schema_version` 欄位機制（在匯入檔案內）允許跨版本相容
- API path versioning（例：`/v1/templates/...`）由更上層 API gateway 統一處理
- Schema 升版時的 migration 機制（POC 不做，列為 future work）
