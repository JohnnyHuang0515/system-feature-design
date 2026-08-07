# Skill Mode: Derive → Show → Verify

> The working model. `SKILL.md` sequences the flow — order, write timing, which guide to read; this file holds **how**: derivation judgment, display format, questioning style, markers, propagation, the full-spec review. Every reference guide builds on it.
>
> **Language rule: instructions here are English; everything spoken to the user is Chinese.** The quoted blocks below are scripts — use them as written.

## The working model

The user supplies **重點 + 方向 + 結果** — the gist, the direction, the outcome. You derive every piece of structure from it.

```
使用者輸入：一段話（要做什麼、給誰、重點是什麼）
   ↓
Claude 推導：FR / entity / flow / API / AC 等所有結構
   ↓
展示給使用者：用容易理解的方式呈現
   ↓
使用者驗證：確認 / 修正 / 拍板必要決策
   ↓
進入下一份文件
```

Four rules run through the whole session:

- You derive; the user verifies, corrects and decides. Structural decomposition is where they are weakest, so it stays on your side.
- Ask in everyday language, grounded in real situations.
- Show your derivation and say "this is how I understood it" before filling anything in.
- When two answers are both reasonable, mark it as an open question and let the user call it.

## Opening

### First message

```
要做新的 system feature design 嗎？跟我說說你想做什麼就好 —
一段話描述「要做什麼、給誰用、重點是什麼」即可，細節我會幫你展開。

例如：
「我想做模板匯出匯入功能，給 PM 用，重點是讓模板可以跨工作區搬移，
 也要支援 AI 生成的模板能寫入。」
```

### After their answer

1. **Analyse internally** — pull problem / scope / persona / core capabilities out of the description.
2. **Ask 1–3 key questions**, if needed: 「這是 POC 還是要直接上 prod？」「有時程限制嗎？」「有既有系統需要整合嗎？」「介面是長在既有產品裡，還是全新的？」

### Offer §0 market research

**Offer it unprompted** before §1 — §0 feeds §1 personas and problem framing, and §2 priorities.

```
要不要先做一份市場研究？我可以查市場規模、競品 / 類似做法、別人的強弱項、
使用者真正在抱怨什麼，整理出「我們的切入點」，再開始設計。
（你已經很清楚市場、想直接設計的話，跟我說就跳過。）
```

Three routes:

- **Wants it, or has research to fold in** → run §0 (opening and method in `0-market-research.guide.md`)
- **Declines, or it's a pure internal tool with no market dimension** → skip to §1, mark `⏭️ 跳過` in the README
- **The request *is* market research / competitive analysis** → §0 is the main event; offer the rest of the spec once it lands

§1 problem-scope starts after §0 completes or is skipped.

### When the description is too thin

A bare 「我想做 X 功能」 gets caught, not returned. Fill the gap with 1–2 everyday questions:

```
✅ 「你說想做匯入匯出 — 主要解決什麼困擾？例如使用者現在沒這功能怎麼辦？」
✅ 「主要是給誰用？PM 自己用，還是要分享給其他人？」

❌ 「請完整描述 problem statement、target users、success criteria 後再開始」
```

## Display format

**Lead with the conclusion** (3–5 lines):

```
我推導出這份文件的核心內容如下：
- [一句話總結]
- [一句話總結]
- [一句話總結]
有 [N] 個地方需要你拍板。
```

**Then the content**, at a depth matched to the document's size:

> **Large-document rule**: a document you expect to exceed ~150 lines (typically §5 / §6 / §8) gets **summary plus open decisions only** in conversation — write the full text to disk and have the user open the file. Pasting the full text *and* writing it doubles the tokens and makes the user read it twice.

```
詳細內容（已套用 template 結構）：
[展示填好的 template 內容]
```

**Close with the decisions you need**:

```
需要你拍板的決策：

1. [生活化問題 1]
   例如：A 還是 B？你比較傾向哪個？

2. [生活化問題 2]
   ...
```

## Five kinds of feedback

| The user says | You do |
|---|---|
| 「OK 沒問題」 | Write to disk, move to the next document |
| 「persona 改成 X」 (small fix) | Correct it, confirm again |
| 「整個 scope 不對，應該是 Y」 (major change) | Re-derive that section |
| 「§1.3 的 persona 我想改」 (back-edit) | Amend, then propagate downstream — see [Amending earlier documents](#amending-earlier-documents) |
| 「§3.2 詳細展開給我看」 | Give the full content |

## Derive vs ask

> The answer is **a business or context call** → ask the user.
> The answer is **structural derivation** → do it yourself.

### Derive these

**Structure**: problem → scope; scope → FR; FR → entity; entity → state machine (where a status concept exists); entity → API endpoint; FR + state machine → acceptance criteria; FR → error and edge cases; user flow → page and component.

**Inference** (derive, then have the user verify): persona pain points (reverse-engineered from the problem described), reasonable NFR ranges (mark `[需確認]`), latent edge cases the user never mentioned — concurrency, repeat triggers.

### Ask about these

**Business calls** — which same-name strategy? Accept repeat triggers or dedupe? Do failed runs follow the existing charge rule or a new one? What's in and out for the POC?

**Context** — expected volume? Schedule pressure? Which existing systems does it integrate with? Any compliance requirements?

**Cross-feature logic** — should this event notify other services? Which side owns the source of truth for this field?

**Frontend experience** (the 前端體驗決策清單 in `5-presentation-spec.guide.md`) — where does the feature get entered from: a new sidebar item, or a button on an existing page? Its own page, a modal, or a drawer? What does the user see on an empty state or a failure? Mobile support? Does the view refresh itself?

> The frontend dividing line: *which* components and pages exist is structural derivation, yours to do. What they look like, how they behave, what happens on failure is experience — you propose, the user decides. Filing all of the frontend under "structural" is how the discussion gets skipped.

## POC fast mode

Once §1 establishes the stage as POC or side project, later documents run fast:

- **Low-risk calls don't stop the user.** Where an industry convention or an obvious default exists and reversing later is cheap — naming, loose NFR numbers, reversible structural choices — take the recommendation and announce it in one line: 「以下 N 項我直接採建議值（列清單），要改再說」.
- **§5 frontend is the exception.** It is the only part the user sees directly. Use a **one-shot confirmation pack** instead: list the recommended value for each relevant dimension of the frontend checklist and confirm the whole set at once, counting as a single hard stop.
- **§0 runs compressed**: 3 competitors instead of 5, rough demand sizing instead of full TAM/SAM/SOM, weight on the differentiation angle (§0.6); with no feedback data, §0.5 gives web demand signals only. Sourcing discipline holds — a POC is no licence to invent numbers. §0's single hard stop is the **direction check before the research run** (see `0-market-research.guide.md`): confirm once, run to completion, then show results.
- **Hard-stop only on high-risk forks.** Any one of these qualifies:
  - (a) Irreversible — account locking, deletion, publishing outward
  - (b) Money or directional rules — who pays more, who goes first
  - (c) A root choice that shapes the data model — single ledger vs multiple
  - (d) No mainstream convention, and getting it wrong is expensive to redo
- Rule of thumb: **5–8 hard stops for an entire POC session.** Few and loud beats many and quiet.

Non-POC work (MVP, production launch) keeps decision-by-decision confirmation.

## Everyday-language questioning

**The principle**: ask through real situations.

### Jargon → plain Chinese

| Jargon | Say instead |
|---|---|
| Bounded context | 責任區塊 / 子模組 |
| Entity | 系統裡的核心東西 / 概念 |
| State machine | 狀態流轉 |
| Idempotency | 重複觸發處理 |
| Side effect | 同時會發生什麼事 |
| Acceptance criteria | 驗收條件 / 怎麼算做完 |
| Source of truth | 資料以哪個為準 |
| Webhook | 別人主動通知我們 |
| Versioning | 版本演進 / 升版 |
| Atomicity | 全做或全不做 |

### Sentence shape: swap the term for a concrete situation plus one example

```
entity      →「這個功能裡會涉及哪些『東西』？例如『訂單』、『使用者』、『支付方式』這種」
idempotency →「使用者如果連點兩次按鈕，你希望系統怎麼處理？是建兩筆？還是只算一筆？」
NFR         →「你預期同時會有多少人用這個功能？反應時間希望多快？」
empty state →「使用者第一次進來、一筆資料都沒有的時候，你想讓他看到什麼？
              引導他建立第一筆？還是就一張空表？」
```

The same swap covers state machines (「訂單從建立到結束會經過哪些階段？」), business rules (「有沒有什麼規則是『絕對不可以違反』的？」) and entry points (「使用者要從哪裡進到這個功能？」).

### Giving options

When the user can't answer off the top of their head, give concrete options rather than handing the jargon back:

```
✅ 「同名模板要怎麼處理？常見的做法有三種：
    (a) 直接拒絕，請使用者改名後再匯入
    (b) 自動覆蓋
    (c) 跳出選單讓使用者選『覆蓋 / 建立新的 / 取消』

    你傾向哪個？或有別的想法？」
```

### Which questions go together

**Ask the frontier** — every decision whose prerequisites are already settled, meaning you can put it without guessing at an answer you haven't heard yet. A question that depends on another one still open in this round belongs to the **next** round; asking it now means asking the user to decide something you don't yet have the context to have framed properly.

Then the user's answers push the frontier outward. Recompute it and ask the next round.

**Size is not the constraint; framing is.** Six questions each carrying options and your recommendation cost the user less than two bare ones — they skim, agree with most, and argue with the one that matters. What tires people is being made to generate answers, not being shown several at once. `Iron rule` below is what makes this hold.

### Using AskUserQuestion

Where the tool exists, every decision goes through it — clicking beats typing:

- **The tool takes at most 4 questions per call.** A frontier larger than that gets split across consecutive calls, or asked in numbered prose instead — either way the split is a **rendering** decision, so keep questions that belong to the same round in the same round rather than inventing an order to make them fit.
- Style each option as above: outcome-shaped label, pros and cons in the description, recommended option first and marked 「(推薦)」.
- An interruption or a refusal to answer means the user has something to say → ask what they want to clarify before re-asking the same set.

## Open questions

Where two answers are both reasonable, mark `[待拍板]`.

### Iron rule: `[待拍板]` always ships with options and a recommendation

**Writing `[待拍板]` obliges you to give the options and your recommendation in the same place**:

```
同名模板處理 [待拍板]
- (a) 直接拒絕，請使用者改名
- (b) 自動覆蓋
- (c) 跳 Modal 讓使用者選「覆蓋 / 建立新的 / 取消」
建議：(c) — 平衡彈性跟誤操作風險
```

Options carry pros and cons; the recommendation carries its reasoning.

Wanting to mark `[待拍板]` but being unable to produce options means this isn't "two reasonable answers" — it's missing information. Go back and ask.

### Directional and money decisions

Decisions with a direction — who pays more or less, who goes first, keep or overwrite — are read backwards easily. Even with examples attached, a user skims them against their own expectation. Two extra rules:

1. **Label options by outcome, not mechanism**:
   - ❌ 「餘數都算給付款人」 (mechanism — the reader can't tell whether the payer ends up over or under)
   - ✅ 「付款人**少出**（100 元 3 人 → 付款人 33、其他人 33/34）」
   - ✅ 「付款人**多出**（100 元 3 人 → 付款人 34、其他人 33/33）」

2. **Read the decision back out loud before writing it down.** For money rules, irreversible states and data deletion, the **first sentence** of your reply after the user chooses restates the outcome with concrete numbers: 「確認一下：100 元 3 人分 → 付款人付 33，其他兩人 33 與 34，對嗎？」. Users don't read business rules line by line, so an error buried in a BR surfaces several documents later.

### After the call is made

- **The user picks an option** → the open question becomes an ADR (D-NNNN, Status: Accepted)
- **The user says 「先放著」** → it stays an open question (Status: Proposed) in §7.2, and **must carry Owner and Target Date** (e.g. `Owner: 待補`, `Target Date: Post-POC`). An OQ without them floats forever.

## Markers

| Marker | Meaning | What the user does |
|---|---|---|
| `[需確認]` | Something you inferred or filled in | **Glance and confirm**, or correct it |
| `[待拍板]` | Two reasonable answers, or missing information | **Choose**, or supply the information |

For example:

- `成功率目標 95% [需確認]` — your inferred value; the user confirms or changes it
- `同名處理策略 [待拍板]：(a) 拒絕 (b) Modal 選擇 (c) 自動覆蓋` — the user picks one

### Marker lifecycle

Markers are a tool for the review conversation. **A file on disk carries none.**

Every marker leaves by one of exactly two doors — deleted, or converted to a `D-NNNN` reference. An item that has been through neither door is not ready to be written; resolve it first. §7.2 is the single place an unresolved item persists, so no other file — the README included — becomes a second home for them.

- The user confirms an item, with or without corrections → **delete that item's `[需確認]` / `[待拍板]` before writing to disk**
- The user says the whole document is fine without going item by item → treat everything as confirmed and delete all markers
- A `[待拍板]` the user defers → **assign the next D-NNNN right then** (create `decisions/NNNN-*.md`, Status: Proposed, with Owner and Target Date) and rewrite the spot as a reference: 「保留策略：待定，見 D-0011」. §7 later collects those Proposed entries into the §7.2 index without renumbering.

A written document may only carry references pointing at §7.2 open questions. Check 5 of the full-spec review tests exactly this — a bare marker left in a file is an Error.

## Amending earlier documents

Whenever the user says they want to change §X, accept it and do two things: re-derive §X, then scan for what it affects.

Common propagation chains:

- §0.4 persona (where §0 ran) → §1.3 target personas, the Persona column of §2.1 FRs, §5.2 user stories
- §0.6 differentiation opportunity → §2 FR priorities, §1.4 success criteria
- §1.3 persona → the Persona column of §2.1 FRs, §5.2 user stories
- §3.2 entity fields → §6.2 API request/response schemas, §8 AC
- §3.3 state machine → the state transitions described in §4.1 SFs, §8.2 AC for state

### Propagation

After amending an earlier section, scan forward and lay the impact out:

```
我修改了 §1.3 的 persona「PM」為「PM / 流程設計者」。
這影響以下後續節：
- §2.1 FR-1, FR-2 的 Persona 欄位
- §5.2 user stories 的分組

要我幫你同步更新嗎？
```

Update everything affected in one pass once the user confirms.

### Two-way propagation: §1.5.1 POC table ↔ §7 ADR

The `§1.5.1` POC trade-off table is **a scannable view for humans**; the matching `§7` ADR is **the full decision record for AI and engineers**. Two renderings of one thing, kept in sync.

1. **§7 ADR is the source of truth** — rationale, alternatives and consequences all live there
2. **§1.5.1 is the condensed view** — issue / current decision / future direction / related ADR only
3. **Not every §1.5.1 row becomes an ADR** — apply the ADR threshold in the §7 guide
4. **A change to a §7 ADR propagates back to §1.5.1 automatically**: title changes → the 議題 column; decision changes → the 當前決定 column; a new ADR → check whether §1.5.1 needs a row; a superseded ADR → strike the row and reference the replacement
5. **A §1.5.1 row with no ADR** (too minor to expand) → leave `Related ADR` as `—`

## Full-spec review

After the last document lands (§9, or §8 when §9 is skipped), **offer to run a full-spec review** — the cross-document pass that catches what per-document work cannot: numbered references that don't resolve, one concept described two ways, orphans, omissions.

The wording, the seven checks (0–6, opening with a mechanical grep pass) and the result bucketing all live in `references/full-spec-review.md`. Read it when you get there, not before — it is a third of this file's weight and it earns nothing until the spec is complete.
