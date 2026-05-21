# Reference Guide: 4-flows.md

> 基於 `0-skill-mode.md` 的推導模式。配合 `templates/4-flows.template.md` 使用。

## 文件目的

描述**系統內部的執行流程** — 給後端工程師看的。使用者視角的流程放 §5.3。

## 進入這份文件時的開場

```
進入第四份:系統流程。

重要區分:
- 本份寫「系統做什麼」 — sequence、跨 component 互動、錯誤處理
- 使用者操作流程放下一份(§5.3)

我會根據前面文件推導系統流程、錯誤處理、邊界情境,你確認。

預估 10-20 分鐘。
```

## Claude 推導指南

### SF 推導來源

| 推導對象 | 推導來源 |
|---|---|
| §4.1 SF 清單 | 從 §2.1 每條 FR 推「系統內部怎麼跑」 |
| SF Sequence diagram | 跨 service 互動時用 Mermaid |
| SF Key steps | 結合 §3.3 state transition + §3.5 events |

### EF 推導來源(主動推,使用者沒提到也要)

對每個 SF 推可能的失敗:

| 失敗類型 | 對應位置 |
|---|---|
| Validation errors | 輸入驗證階段 |
| Business rule violations | 對應 §3.4 BR 的違反 |
| External dependency failures | 跨 service 呼叫 |
| Concurrency conflicts | 共享資源 |
| Authorization failures | 跨 boundary 階段 |

### EC 推導來源(主動推)

從常見模式推:
- 空資料 / null / 極大值
- 重複觸發(使用者連點、整合方 retry)
- 時序問題(併發、過期資料)
- 狀態邊界(剛好處於轉換中)

### Concurrency 推導

回答三個問題決定怎麼寫:
1. 有共享資源嗎?
2. 事件順序重要嗎?
3. 會被重複觸發嗎?

都是「否」→ 一行帶過。任一是「是」→ 列處理策略。

## 必要決策點(要問使用者的)

### 必補問題

很少需要問。Error / edge case 推導後展示讓使用者增刪即可。

### 不該問的

- ❌ 「SF 有哪些步驟?」(從 FR 推)
- ❌ 「EF 有哪些?」(從常見失敗類型推)
- ❌ 「EC 有哪些?」(從常見模式推)

## Open Question 候選

- 某個失敗情境的處理策略多種合理(rollback vs retry vs 部分成功)
- 併發處理機制選擇(optimistic lock vs pessimistic lock)
- 異步 vs 同步處理選擇

## 展示給使用者的格式

### 步驟 1:摘要

```
我推導出 {N} 個 system flow + {M} 個 error flow + {K} 個 edge case:

主要流程:
- SF-1: [簡述]
- SF-2: [簡述]

可能的失敗:
- EF-1: [簡述]
- EF-2: [簡述]

邊界情境:
- EC-1: [簡述]

併發:[有風險並列處理 / 無風險]
```

### 步驟 2:逐個 SF 展開

對複雜 feature,一次展示 1-2 個 SF + 對應 EF/EC,讓使用者吸收。

### 步驟 3:問必要決策點

```
有幾件事需要你拍板:

1. EC-7:使用者短時間連點兩次匯入按鈕,系統怎麼處理?
   (a) 建兩筆模板(同名會跳同名 Modal)
   (b) Server 端用 idempotency key,5 分鐘內視為同一筆
   (c) Client 端 button disable 就好

2. EF-5:DB 寫入到一半失敗(connection drop),怎麼處理?
   你預期是 transaction rollback(整批回滾)還是部分保留?
```

## 容易卡住的點

### 使用者沒想過 Error / Edge case

主動推一份草稿給使用者:「這些是我推測可能發生的情境,看哪些需要處理、哪些可忽略」。

### 使用者覺得 EC 推太多

可以歸類:「常見類 vs 罕見類」。罕見類使用者覺得不重要可省。

## 反思檢查(進 §5 前)

- [ ] 每條 §2.1 FR 對應到至少 1 個 SF
- [ ] 每個 SF 至少有 1-2 個 EF(沒失敗情境的 SF 很可疑)
- [ ] SF 中提到的 state transition / event 都在 §3 定義
- [ ] §4.4 三個觸發問題都回答了
- [ ] 標記使用得當

## 文件結束時的 summary

```
§4 flows 完成!

- System flows:SF-1 ~ SF-{N}
- Error flows:EF-1 ~ EF-{N}
- Edge cases:EC-1 ~ EC-{N}
- Concurrency:{處理策略 / 無風險}

接下來進入 §5 presentation-spec,我會推導使用者視角的呈現方式(user story、user flow、UI 元件、頁面)。
注意:這份是回頭給每個 SF 補 "Related UF" 欄位的關鍵節點。

要進嗎?
```
