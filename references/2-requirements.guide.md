# Reference Guide: 2-requirements.md

> 基於 `0-skill-mode.md` 的推導模式。配合 `templates/2-requirements.template.md` 使用。

## 文件目的

把 §1 的「要做的事」拆成具體的功能需求(FR)跟非功能需求(NFR)。每條需求可獨立驗證、可被 §8 的 acceptance criteria 引用。

## 進入這份文件時的開場

```
進入第二份:需求清單。

我會根據 §1 推導出功能需求(FR)清單跟非功能需求(NFR)清單,
你確認 / 修正即可。

預估 5-10 分鐘。
```

## Claude 推導指南

### FR 推導來源

| 推導對象 | 推導來源 |
|---|---|
| FR 清單 | §1.5 in scope 的每一項展開為 1-N 條 FR |
| FR Description | 用 "Allow X to do Y" 句型(系統能力,不寫使用者動作) |
| FR Persona | 對應 §1.3 的 persona |
| FR Priority | 從 §1.5 推測,POC 階段預設 Must,選填類預設 Should |
| FR Related | reference 到 §1 的小節 |

### NFR 推導來源

按以下分類推導,**沒適用的分類整節省略**:

| 分類 | 何時要推 |
|---|---|
| Performance | 對外服務、有效能要求時 |
| Security & Authorization | 任何 feature 都要(最低限度:認證 / 授權) |
| Reliability | 對外服務、業務關鍵時 |
| Observability | 對外服務、有運維需求時 |
| Scalability | 預期成長快時 |
| Compliance & Audit | 處理使用者資料 / 金流 / 醫療等 |

每條 NFR 的 Target 用 `[需確認]` 標推測值。

### Priority Summary 推導

FR + NFR 合計 > 10 條時自動產出 Priority Summary。

## 必要決策點(要問使用者的)

通常不需要問。但有兩種情境要主動確認:

1. **量化目標值不確定**:NFR latency / QPS 等推測值,標 `[需確認]` 讓使用者調整,不要直接問
2. **scope 邊界 FR 模糊**:某條 FR 看不出是 Must 還是 Should,標 `[待拍板]`

### 不該問的(Claude 應該推)

- ❌ 「FR 有哪些?」(從 §1.5 推)
- ❌ 「NFR 怎麼分類?」(從 feature 性質判斷哪些分類適用)
- ❌ 「優先級怎麼排?」(預設 Must,使用者調整)

## Open Question 候選

- 某條 FR 邊界模糊(「這算 FR 還是 enhancement?」)
- NFR 目標值無基準參考(「latency 目標多嚴格才合理?」)
- Priority 模糊(「FR-X 是 Must 還是 Should?」)

## 展示給使用者的格式

### 步驟 1:摘要

```
我推導出 N 條 FR 跟 M 條 NFR:

FR 重點:
- FR-1: [簡述]
- FR-2: [簡述]
...

NFR 分類:[列出有用到的分類]

需要你拍板:[N 個]
```

### 步驟 2:完整表格

按 template 結構展示 §2.1 FR 表格 + §2.2 NFR 各分類表格。

推測 Target / Priority 用 `[需確認]` 標記。

### 步驟 3:問必要決策點

```
有幾個我推測的數字想跟你確認:

1. NFR-1 我推測 p99 latency < 500ms,合理嗎?或你心中有別的目標?
2. FR-9 (結構警告) 我預設 Should,要不要提升到 Must?
```

## 容易卡住的點

### 使用者覺得 FR 太多

問:「哪些是 must-have、哪些可以延後?」幫使用者收斂。

### 使用者沒概念 NFR 目標值

給「業界常見值」+「你的情境可能要調」,讓使用者有參考點:

```
類似 feature 的 latency 目標通常 p99 < 500ms ~ 1s,
你這個是內部使用還是對外?內部可以寬鬆,對外建議嚴格點。
```

## 反思檢查(進 §3 前)

- [ ] 每條 §1.5 in scope 都對應至少 1 條 FR
- [ ] 每條 FR 的 Persona 都對應到 §1.3 列出的 persona
- [ ] NFR 至少涵蓋 Security & Authorization
- [ ] FR + NFR 合計 > 10 條時有 Priority Summary
- [ ] 標記都已使用得當

## 文件結束時的 summary

```
§2 requirements 完成!

- FR:{N} 條(Must {M} / Should {S} / Could {C})
- NFR:{N} 條,涵蓋 {分類列表}
- Priority Summary:[有 / 跳過]

接下來進入 §3 domain-model,我會推導 entities、state machines、business rules。要進嗎?
```
