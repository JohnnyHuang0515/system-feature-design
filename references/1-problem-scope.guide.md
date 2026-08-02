# Reference Guide: 1-problem-scope.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/1-problem-scope.template.md`.
> Instructions here are English; the quoted blocks are scripts spoken to the user — use them as written.

## Purpose

Define **why we're building it, who for, and where the edges are**. This is the head of the whole spec; every later document references it.

## Opening

```
我們進入第一份文件:問題與範圍。

我會根據你剛才的描述先推導內容,再給你確認。
這份決定整個 spec 的方向,所以會比較仔細跟你確認。
```

## Derivation

Pull the pieces out of the user's opening 重點 + 方向 + 結果.

> **Where §0 market research ran**, §1 no longer runs on that one sentence — take §0's findings first. §1.3 personas cite §0.4 PER-N directly rather than being reverse-engineered; §1.1 problem carries the sharpest pain from §0.5/§0.6; §1.4 quantitative targets benchmark against §0.1 and competitors; §1.5 scope is steered by §0.6 opportunities and §0.7 implications.
> Where §0 was skipped, derive from the description per the table below and mark inferences `[需確認]`.

| Target | Source |
|---|---|
| §1.1 Problem Statement | With §0: sharpest pain from §0.5/§0.6 + §0.0 problem framing. Without: the "what's broken / what's missing" in the description, plus the reverse-engineered cost of not solving it |
| §1.2 Background | Existing systems and "why now" the user mentioned (omit the optional section if unmentioned) |
| §1.3 Personas | With §0: cite §0.4 PER-N (name the PER-X and its label as the target persona). Without: who the user said it's for, plus the reverse-engineered "who else is indirectly affected" |
| §1.4 Success Criteria (required part) | Reverse-engineered from the outcome the user described; with §0, benchmark quantitative targets against §0.1 and competitors |
| §1.4 quantitative targets | **Mark `[需確認]`** — inferred from the nature of the feature, tuned by the user |
| §1.5 In Scope | What the user explicitly said they want |
| §1.5 Out of Scope | **Propose 3–5 unprompted** — things the user might assume are included but aren't |
| §1.5 Future | Expansion the user mentioned wanting later, or a reasonable inferred direction |
| §1.5.1 POC table | Where the user said "POC" or "簡單版 first", list the likely "simple now vs expand later" issues. `Related ADR` stays `—` at this stage; §7 backfills it |
| §1.6 Assumptions & Constraints | Inferred from context — a 5MB limit the user mentioned is a constraint |

### Marking rules

Inferred content takes `[需確認]`: quantitative targets, persona pain points the user never stated, out-of-scope entries you added yourself.

A genuine fork takes `[待拍板]` with options and a recommendation. Missing information takes `[待拍板]` too, pending the user. Neither is a licence to invent.

## Questions you must ask

One paragraph usually derives most of the document. A few things need asking when the user's description omits them.

### Required, when unmentioned

**Q-Stage** — POC, MVP, or production launch? Decides whether §1.5.1's POC table exists, and shapes §1.6 constraints (a POC is usually schedule-tight).

**Q-Time** — any schedule pressure? Feeds §1.6 Constraints.

**Q-Integration** — which existing systems does it touch? Feeds §1.2 Background and §1.6 Assumptions.

### Optional, depending on the feature

Expected volume and scale (small tool vs high traffic)? Compliance requirements (payments, medical, PII)? Multi-user collaboration or single-user?

Ask in everyday language, **3 questions at a time, maximum**.

## Open question candidates

- Two reasonable ways to cut scope (「這算 in scope 還是 out of scope?」)
- A fuzzy persona (「PM 是指流程設計者,還是含一般使用者?」)
- An uncertain quantitative range (「成功率目標 95% 還是 99%?」)

These go to the user, not to your own judgment.

## Display format

### Step 1: summary

```
我整理一下對你的 feature 的理解:

要做什麼:[一句話 problem statement]
給誰用:[列 persona]
主要範圍:[3-5 條 in scope]
明確不做:[列 2-3 條 out of scope,含「為什麼」]
成功標準:[一句話判定]

需要你拍板:[N 個決策點,列關鍵詞]
```

### Step 2: full content

Show §1.1–§1.6 filled in against the template structure, with inferences marked: `[需確認]` for what you inferred or added (quantitative values, persona pain points, out-of-scope entries) and `[待拍板]` where two answers are reasonable or information is missing.

### Step 3: the decisions

Everyday language, **1–3 at a time**:

```
有幾件事需要你拍板:

1. 你說想做匯入功能 — 是只想支援「使用者上傳檔案」,還是
   也要支援「使用者貼上 JSON 文字」?
   (影響 in scope 範圍)

2. 你提到 AI 生成也走匯入路徑 — 如果 AI 生成的 JSON 不合法,
   你希望系統怎麼處理?
   (a) 直接報錯,使用者重新生成
   (b) 自動修正能修的部分
   (c) 視為「AI 生成失敗」走既有失敗流程

3. 你說這是 POC — 那 POC 結束後預期會進入什麼階段?是 MVP
   還是正式上線?(影響我幫你規劃 future work 的範圍)
```

## Where you'll get stuck

### The user gives one sentence: 「我想做 X」

Catch it with 1–2 questions rather than sending it back:

```
你說想做 [X] — 主要想解決什麼困擾?例如使用者現在沒這功能怎麼辦?
順便問一下,主要是給誰用?
```

Start deriving as soon as they answer. Five questions before you begin is worse than two.

### The user's description is long and detailed

Pull out the three things — 重點 / 方向 / 結果 — and hold the rest for later sections:

```
我從你的描述中拆出三個核心:
- 重點:[一句話]
- 方向:[一句話]
- 結果:[一句話]

其他細節(例如 entity 設計、API 結構),我會在後續節展開。
先看 §1 推導對不對。
```

### The user amends §1 and it needs to propagate

Later requests like 「persona 再加一個」 or 「scope 要擴」 follow `Amending earlier documents` in `0-skill-mode.md`.

## Reflection check, before §2

- [ ] §1.1 problem has the user's explicit confirmation
- [ ] §1.3 personas are specific, not a vague 「使用者」
- [ ] §1.4 has at least one sentence of pass/fail criteria
- [ ] §1.5 in scope is itemized, not a single line like 「做匯入匯出功能」
- [ ] §1.5 out of scope has at least 2 entries — the section people new to specs most often skip
- [ ] §1.5.1 POC table exists, where this is a POC
- [ ] Marker lifecycle done: confirmed markers deleted, surviving `[待拍板]` carry options and a recommendation, deferred ones converted to a D-NNNN reference

Anything unconfirmed gets finished before §2 starts.

## Closing summary

```
§1 problem-scope 完成!摘要:

- 要做:[一句話 feature 描述]
- 給:[persona 列表]
- 解決:[problem 簡述]
- 不做:[out of scope 條列簡述]
- 成功標準:[一句話判定 + 量化指標]
- POC 設計表格:[若有,N 條議題]
- Open Questions:[若有,等 §7 拍板]

接下來進入 §2 requirements,把「要做的事」拆成具體功能需求清單(FR)跟非功能需求(NFR)。
我會繼續用同樣模式 — 我先推導,你再確認。

要進嗎?
```
