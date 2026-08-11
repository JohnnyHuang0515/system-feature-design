# Reference Guide: 4-flows.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/4-flows.template.md`.

## Purpose

Describe **what the system does internally** — for backend engineers. The user's-eye view of the same work lives in §5.3.

## Opening

```
進入第四份:系統流程。

重要區分:
- 本份寫「系統做什麼」 — sequence、跨 component 互動、錯誤處理
- 使用者操作流程放下一份(§5.3)

我會根據前面文件推導系統流程、錯誤處理、邊界情境,你確認。
```

## Derivation

### System flows

| Target | Source |
|---|---|
| §4.1 SF list | For each §2.1 FR, how the system runs it internally |
| SF sequence diagram | Mermaid, where services interact |
| SF key steps | §3.3 state transitions combined with §3.5 events |

### Error flows — derive these unprompted

For every SF, derive the ways it can fail:

| Failure type | Where it lands |
|---|---|
| Validation errors | Input validation stage |
| Business rule violations | A §3.4 BR being broken |
| External dependency failures | Cross-service calls |
| Concurrency conflicts | Shared resources |
| Authorization failures | Boundary crossings |

### Edge cases — derive these unprompted

From the usual patterns: empty data / null / extreme values; repeat triggers (a user double-clicking, an integrator retrying); timing problems (concurrency, stale data); state boundaries (caught mid-transition).

### Concurrency

Three questions decide how much to write: is there a shared resource? Does event order matter? Can it be triggered twice?

All no → one line. Any yes → list the handling strategy.

## Questions you must ask

Rarely any. Derive the errors and edge cases, then show them for the user to add to or cut.

## Open question candidates

- Several reasonable strategies for one failure (rollback vs retry vs partial success)
- Concurrency mechanism (optimistic vs pessimistic lock)
- Async vs sync processing

## Display format

### Step 1: summary

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

### Step 2: one SF at a time

For a complex feature, show 1–2 SFs with their EFs and ECs per turn so the user can absorb them.

### Step 3: the decisions

```
有幾件事需要你拍板:

❓ **Q1** — **EC-7 連點兩次匯入**:(a) 建兩筆(同名會跳 Modal) (b) Server 端 idempotency key,5 分鐘內視為同一筆 (c) Client 端 disable 按鈕
➡️ 建議 (b) —— (c) 擋不住重送與網路重試,而重複匯入是使用者最難自己收拾的錯

❓ **Q2** — **EF-5 寫入中途斷線**:(a) Transaction rollback,整批回滾 (b) 保留已寫入的部分讓使用者接續
➡️ 建議 (a) —— §1.4 的反指標寫著「匯入失敗時不留下半成品」
```

## Where you'll get stuck

### The user has never thought about errors or edge cases

Hand them a derived draft: 「這些是我推測可能發生的情境,看哪些需要處理、哪些可忽略」.

### The user thinks there are too many edge cases

Group them into common vs rare. The rare ones can go if the user judges them unimportant.

## Reflection check, before §5

- [ ] Every §2.1 FR maps to at least one SF
- [ ] Every SF has at least 1–2 EFs — an SF with no failure mode is suspicious
- [ ] Every state transition and event named in an SF is defined in §3
- [ ] All three §4.4 trigger questions are answered

Then run the three checks from inside the spec folder and **say what they printed**:

- [ ] `grep -c "\[需確認\|\[待拍板" 4-flows.md` → `0`
- [ ] `python3 <skill-path>/scripts/check-sections.py .` → ✓
- [ ] `python3 <skill-path>/scripts/check-example-ids.py .` → ✓

## Closing summary

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
