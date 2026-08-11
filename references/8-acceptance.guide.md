# Reference Guide: 8-acceptance.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/8-acceptance.template.md`.
> Instructions here are English; the quoted blocks are scripts spoken to the user — use them as written.

## Purpose

Define what "done" means. This is the contract engineering and QA work against. Every AC uses **Given-When-Then (BDD)** format.

## Opening

```
進入第八份:驗收標準。

這份對應前面所有有「可驗證行為」的內容 — FR / state / BR / error / edge case / NFR —
寫成 BDD 格式的測試情境。

由於 AC 數量會很多,我會分節推導,你逐節確認。
```

## Derivation

| AC group | Source |
|---|---|
| §8.1 AC for FR | 1–N ACs per §2.1 FR (happy plus failure) |
| §8.2 AC for State Transitions | Two per §3.3 transition — legal and violation — plus **one** shared catch-all (`AC-S.99`) for the whole state machine, not one per transition. Where no interface can trigger a violation, write 「不適用 + 原因」 instead of inventing an error code |
| §8.3 AC for Business Rules | A verification scenario per §3.4 BR (or a reference to another AC) |
| §8.4 AC for Error & Edge | One per §4.2 EF and §4.3 EC |
| §8.5 AC for NFR | How each §2.2 NFR is measured, and what passing looks like |
| §8.6 Coverage Matrix | Generated from §8.1–§8.5. **Selfsame gate as §2.4: write it when FR + NFR exceeds 10, skip it below** — under that, the matrix restates a list short enough to read |

### Writing the BDD

**Given** — the precondition: logged in, an entity in some state, some data already present.

**When** — the trigger: an API call, a button press, a state transition.

**Then** — the side effect, taken from the SF / EF / state machine. **Every outcome must be verifiable**: a return value, a DB change, an emitted event, a Toast shown.

### How many ACs an FR gets

The table above sets the count everywhere else; §8.1 is the one that varies:

- **Write-side** (POST/PUT/DELETE/state change) — at least 1 happy + 1 failure
- **Read-only** — at least 1 happy; failures are covered by the §6.5 error model
- **Involving authorization** — an extra unauthorized AC is mandatory

### UI behaviour

UI behaviour — navigation, Toast, Modal — belongs in the FR's Then clause. Visual detail (colour, size) belongs to the Design System, not here.

## Questions you must ask

Usually none. Derive the ACs, then show them for the user to confirm, add to or cut.

The one exception, and §8's only likely open question: NFR targets were settled in §2.2, but §8.5 describes *how* they're verified, and the test environment may be the user's to name.

## Open question candidates

§8 rarely raises new ones. A new one means an earlier section is ambiguous — go back and clarify it first.

## Display format

### Step 1: summary

```
我推導出整套 AC:

- §8.1 AC for FR:{N} 個(涵蓋 FR-1 ~ FR-{M})
- §8.2 AC for State:{N} 個(涵蓋所有 transition + catch-all)
- §8.3 AC for BR:{N} 個(含 reference 其他 AC 的)
- §8.4 AC for Error & Edge:{N} 個
- §8.5 AC for NFR:{N} 個(標註 verification level)

整體 {總計} 個 AC,涵蓋率 100%。
```

### Step 2: section by section

With a large AC count, don't dump it all at once:

```
先看 §8.1 AC for FR 部分。我列出 FR-1 的 AC,你看格式跟內容對嗎?
若 OK,我就批次給你 FR-2 ~ FR-N 的 AC。
```

Once the user approves the §8.1 format, batch the remaining sections.

### Step 3: the decisions, if any

§8 usually needs none. Where the §8.5 verification environment is uncertain:

```
❓ **NFR-1 的驗證環境**:(a) staging 完整驗證 (b) staging 打折驗證,再標註與 prod 的差距
➡️ 建議 (a) —— 除非你們 staging 規格明顯小於 prod,那就走 (b) 並在 §8.5 寫下比例

我先假設在 staging 跑 load test(50 concurrent users, 10 分鐘)。
```

## Where you'll get stuck

### The user thinks there are too many ACs

Expected — BDD is finer-grained than a bullet list, so the count is naturally high. The summary should stress 「不是要使用者全部寫,是我推導完讓你確認」.

### The user thinks ACs are duplicated

Take their example — 「AC-2.1 跟 AC-EF.1 看起來像」 — and name the difference: 2.1 is the happy path, EF.1 is the error path.

## Reflection check, before §9

- [ ] Every §2.1 FR has an AC
- [ ] Every state transition has legal + violation + catch-all ACs (or an explicit 「不適用 + 原因」)
- [ ] Every §3.4 BR has an AC or a reference
- [ ] Every §4.2 EF and §4.3 EC has an AC
- [ ] Every §2.2 NFR has an AC plus a verification level
- [ ] §8.6 exists where FR + NFR exceeds 10, and where it exists every row carries a specific AC number with no blanks
- [ ] ACs use BDD format, and every Then clause is verifiable

Then run the three checks from inside the spec folder and **say what they printed**:

- [ ] `grep -c "\[需確認\|\[待拍板" 8-acceptance.md` → `0`
- [ ] `python3 <skill-path>/scripts/check-sections.py .` → ✓
- [ ] `python3 <skill-path>/scripts/check-example-ids.py .` → ✓

## Closing summary

```
§8 acceptance 完成!

- AC for FR:{N} 個
- AC for State:{N} 個(含 catch-all)
- AC for BR:{N} 個(含 reference)
- AC for Error & Edge:{N} 個
- AC for NFR:{N} 個
- Coverage Matrix:[完成 / 跳過(FR + NFR ≤ 10)]

整份 spec 已涵蓋 8 份核心文件。

接下來最後一份 §9 rollout — 上線策略、監控、Runbook。

要做 §9 嗎?還是 spec 到這裡結束?
```

**Check the README's §9 row first.** §1's path may have already settled it — `⏭️ 跳過` means say so and close rather than re-opening a decision the user made. Ask only where the row is still `⬜ 待產`. On the production route §9 is not optional and there is nothing to ask.
