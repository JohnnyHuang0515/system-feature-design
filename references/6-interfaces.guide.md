# Reference Guide: 6-interfaces.md

> 基於 `0-skill-mode.md` 的推導模式。配合 `templates/6-interfaces.template.md` 使用。

## 文件目的

定義系統的對外契約 — 對前端、整合方、其他服務暴露的介面。工程師翻最多的文件,必須精確。

## 進入這份文件時的開場

```
進入第六份:介面契約。

這份定義對外暴露的 API、events、整合點 — 前後端對齊的關鍵。

我會根據 §3 entity 跟 §4 SF 推導完整 API spec,你確認 / 修正。

預估 15-25 分鐘。
```

## Claude 推導指南

### Overview 推導

掃描 §4.1 SF 跨界互動點,整理成總覽表。

### REST API 推導

| 推導對象 | 推導來源 |
|---|---|
| Endpoint 清單 | 每個 §4.1 SF 的對外入口 |
| Request schema | §3.2 entity 欄位 + FR 的輸入 |
| Response schema | §3.2 entity 欄位 + 對外可揭露的部分 |
| Auth 要求 | §2.2.2 NFR |
| Errors | 每個 endpoint 涉及的 §4.2 EF |

### Error Model 推導

從 §4.2 所有 EF 反推 error code:
- HTTP status 對應 EF 的失敗類型
- Error code 用 UPPER_SNAKE_CASE
- 同一個 code 在不同 endpoint 必須回同樣 status

**所有 §6.2 endpoint 用到的 code 必須在 §6.5 catalog 註冊**。Claude 推導時自動建立 catalog。

### Webhooks(若有)

從 §4.1 SF 中接收外部 callback 的部分推。沒有就跳過。

### Outbound Events 推導

§6.4.1 對應 §3.5 中「對外發布」的子集:
- 純內部 event 不列(只列在 §3.5)
- 對外 event 列出 channel / schema / consumers / retention

### External Integrations 推導

§6.4.2 列 §4.1 SF 中對外部 service 的呼叫,**timeout + retry + failure handling 三項必寫**。

## 必要決策點(要問使用者的)

### 必補問題

1. **API 設計風格**:單階段 vs 兩階段(例:匯入是「上傳直接寫」還是「先預覽後確認」)
2. **Schema 細節**:某些欄位是否暴露(內部用 vs 對外用)
3. **Rate limiting**:是否需要(對外服務通常需要)

### 不該問的

- ❌ 「API endpoint 有哪些?」(從 SF 推)
- ❌ 「Error code 有哪些?」(從 EF 推)
- ❌ 「Schema 結構?」(從 entity 推)

## Open Question 候選

- API 設計風格(REST resource-oriented vs RPC-style)
- 匯入流程是單階段還是兩階段
- 版本管理機制(URL path vs Header)
- 大檔案處理(stream vs 一次上傳)

## 展示給使用者的格式

### 步驟 1:Overview

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

### 步驟 2:逐個 endpoint 展開

對複雜 endpoint,一次展示 1 個。簡單的可批次。

每個 endpoint 給:method + path + auth + request + response + errors。

### 步驟 3:Error catalog

整理完所有 endpoint 後,展示完整 error code catalog。

### 步驟 4:問必要決策點

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

## 容易卡住的點

### 使用者不熟 API 設計

主動 propose 兩種設計給使用者選,不要讓使用者從零想。

### 使用者糾結 schema 細節

聚焦「對外契約」層級,提醒「實作層細節(例:DB column 是 varchar 還是 text)留給後端」。

### Error code 命名糾結

提供命名原則:UPPER_SNAKE_CASE、HTTP status + 具體描述(例:404 TEMPLATE_NOT_FOUND 而非 404 NOT_FOUND)。

## 反思檢查(進 §7 前)

- [ ] 每條 §2.1 FR 都對應到至少 1 個 endpoint
- [ ] 每個 endpoint 都對應到至少 1 個 SF
- [ ] 每個 endpoint 的 errors 都在 §6.5 catalog 註冊
- [ ] 每個 published event 都在 §3.5 列出
- [ ] 每個 external integration 都有 timeout + retry + failure handling
- [ ] 標記使用得當

## 文件結束時的 summary

```
§6 interfaces 完成!

- REST endpoints:{N} 個
- Webhooks:{N} 個 / 無
- Published events:{N} 個
- External integrations:{N} 個
- Error codes:{N} 個

接下來進入 §7 decisions,我會整理前面散落的關鍵決策成正式 ADR,並列出待拍板事項。要進嗎?
```
