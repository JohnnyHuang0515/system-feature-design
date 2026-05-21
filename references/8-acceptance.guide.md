# Reference Guide: 8-acceptance.md

> 基於 `0-skill-mode.md` 的推導模式。配合 `templates/8-acceptance.template.md` 使用。

## 文件目的

定義「功能完成」的判定標準。給工程跟 QA 看的契約。所有 AC 使用 **Given-When-Then (BDD)** 格式。

## 進入這份文件時的開場

```
進入第八份:驗收標準。

這份對應前面所有有「可驗證行為」的內容 — FR / state / BR / error / edge case / NFR — 
寫成 BDD 格式的測試情境。

由於 AC 數量會很多,我會分節推導,你逐節確認。

預估 15-30 分鐘(視前面 FR/BR 數量)。
```

## Claude 推導指南

### AC 推導來源

| AC 類別 | 推導來源 |
|---|---|
| §8.1 AC for FR | 每條 §2.1 FR 推 1-N 個 AC(happy + failure) |
| §8.2 AC for State Transitions | 每條 §3.3 transition 推合法 + 違規兩個 AC |
| §8.3 AC for Business Rules | 每條 §3.4 BR 推驗證情境(或 reference 其他 AC) |
| §8.4 AC for Error & Edge | 每條 §4.2 EF + §4.3 EC 推對應 AC |
| §8.5 AC for NFR | 每條 §2.2 NFR 推怎麼測 + 達標標準 |
| §8.6 Coverage Matrix | 自動產出對應表 |

### BDD 格式推導

**Given**:
- 從前置狀態推(已登入 / 某 entity 處於某 state / 某資料已存在)

**When**:
- 從觸發動作推(呼叫某 API / 點某按鈕 / state 轉換)

**Then**:
- 從 SF / EF / state machine 的 side effect 推
- **每條結果必須可驗證**(回傳 X / DB 變化 / 發出事件 / 顯示 Toast)

### 最低覆蓋規則

- **寫入類 FR**(POST/PUT/DELETE/狀態變更):至少 1 happy + 1 failure
- **純查詢類 FR**:至少 1 happy(failure 由 §6.5 error model 涵蓋)
- **涉及 authorization 的 FR**:必須額外有「未授權」AC
- **每條 state transition**:合法 + 違規兩個 AC + catch-all
- **每條 BR**:獨立 AC 或 reference

### UI 行為的處理

UI 行為(跳轉、Toast、Modal)寫在 FR 的 Then 段落,**不寫視覺細節**(顏色、尺寸)— 那些歸 Design System。

## 必要決策點(要問使用者的)

### 必補問題

通常不需要問。AC 推導後展示讓使用者確認 / 增刪即可。

例外:NFR 的目標值在 §2.2 已確認,§8.5 寫怎麼驗證,可能需要使用者確認測試環境設定。

### 不該問的

- ❌ 「FR-1 的 AC 是什麼?」(從 FR 推)
- ❌ 「State transition 的 AC?」(從 §3.3 推)
- ❌ 「Error 的 AC?」(從 EF 推)

## Open Question 候選

§8 階段很少產生新 Open Question。如果有,代表前面節有模糊處,先回頭釐清。

可能的 OQ:NFR 測試環境設定(staging 規格不確定)→ 標 `[待拍板]`。

## 展示給使用者的格式

### 步驟 1:摘要

```
我推導出整套 AC:

- §8.1 AC for FR:{N} 個(涵蓋 FR-1 ~ FR-{M})
- §8.2 AC for State:{N} 個(涵蓋所有 transition + catch-all)
- §8.3 AC for BR:{N} 個(含 reference 其他 AC 的)
- §8.4 AC for Error & Edge:{N} 個
- §8.5 AC for NFR:{N} 個(標註 verification level)

整體 {總計} 個 AC,涵蓋率 100%。
```

### 步驟 2:分節展示

AC 數量大時不要一次倒出來,**分節展示**:

```
先看 §8.1 AC for FR 部分。我列出 FR-1 的 AC,你看格式跟內容對嗎?
若 OK,我就批次給你 FR-2 ~ FR-N 的 AC。
```

使用者確認 §8.1 格式後,可以批次展示其他節。

### 步驟 3:問必要決策點(若有)

通常 §8 不需要問什麼。如果 §8.5 NFR 有 verification 環境不確定,問:

```
NFR-1 測試:我推測在 staging 跑 load test(50 concurrent users, 10 分鐘)。
你們的 staging 規格大概是 prod 多少比例?需要調整測試設定嗎?
```

## 容易卡住的點

### 使用者覺得 AC 太多

正常 — BDD 格式比條列細,數量自然多。摘要強調「不是要使用者全部寫,是我推導完讓你確認」。

### 使用者覺得 AC 重複

舉例「AC-2.1 跟 AC-EF.1 看起來像」→ 解釋差別(2.1 是 happy path,EF.1 是 error path)。

### NFR 測試環境不確定

接受 [待拍板],或預設「staging 完整驗證」+ 補註「實際環境差異請補」。

## 反思檢查(進 §9 前)

- [ ] 每條 §2.1 FR 都有對應 AC
- [ ] 每條 state transition 都有合法 + 違規 AC + catch-all
- [ ] 每條 §3.4 BR 都有對應 AC 或 reference
- [ ] 每條 §4.2 EF + §4.3 EC 都有對應 AC
- [ ] 每條 §2.2 NFR 都有對應 AC + verification level
- [ ] §8.6 Coverage Matrix 完整
- [ ] AC 用 BDD 格式 + Then 段落可驗證

## 文件結束時的 summary

```
§8 acceptance 完成!

- AC for FR:{N} 個
- AC for State:{N} 個(含 catch-all)
- AC for BR:{N} 個(含 reference)
- AC for Error & Edge:{N} 個
- AC for NFR:{N} 個
- Coverage Matrix:完成

整份 spec 已涵蓋 8 份核心文件。

接下來最後一份 §9 rollout(選填)— 上線策略、監控、Runbook。

要做 §9 嗎?還是 spec 到這裡結束?
```
