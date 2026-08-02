# Reference Guide: 0-market-research.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/0-market-research.template.md`.
> Instructions here are English; the quoted blocks are scripts spoken to the user — use them as written.
>
> ⚠️ This document differs from the other nine in one fundamental way: **it runs on research, not on derivation from the user's description.** The others unfold from that one sentence; §0 goes out and finds data, and eats whatever data the user supplies, before synthesizing. Its core actions are **web research, data digestion, sourcing and confidence levels** — never generation from thin air.

## Purpose

Before §1 problem-scope is written, answer: **what does this market look like, who is in it, how do others solve this, and where is our angle?**

The research feeds the rest of the spec:

- §0.4 personas → §1.3 target personas, now research-backed rather than reverse-engineered from one sentence
- §0.6 differentiation opportunities → §2 FR priority, §1.4 success criteria benchmarks
- §0.1 sizing → whether §1.4's quantitative targets are plausible

> Positioning: this is **market research inside a feature-design flow**, not a business plan. Even at full PM depth (TAM/SAM/SOM + segments + competitors + personas + sentiment + differentiation), the point remains **how these findings change the feature we're about to design**. Every section closes by answering "so what — what does this imply for §1 and §2?"

## This document is optional

Offer §0 unprompted; it can still be skipped. Three cases:

1. **The user wants it** → run the full §0 (or the compressed POC version below).
2. **The user already has research** (「我們已經做過市場調研了」, 「我貼給你」) → don't start from scratch. Eat their data, fill the gaps, structure the known competitors, personas and figures into §0 format.
3. **The user explicitly skips** (「不用市調，我很清楚市場」, 「這是純內部工具」) → skip §0, mark the README row `⏭️ 跳過（原因）`, go straight to §1. §1.3 personas fall back to derive-plus-`[需確認]`.

> How to raise it in the opening: see `Opening` in `0-skill-mode.md`, which already includes the §0 question.

## Research method

### Two sources — use whichever exists

| Source | How to use it |
|---|---|
| **Data the user provides** | CSV, surveys, interview transcripts, support tickets, competitor pricing tables, existing market reports → read and analyse directly (via `Read` and similar). This is **first-hand and highest-confidence**; use it first. |
| **Web research** | `WebSearch` / `WebFetch` for competitor sites, pricing pages, reviews (G2 / Capterra / Reddit / communities), industry reports, market figures. **Second-hand** — needs a source and a confidence level. |

> With no web tools available, or the user offline / headless → degrade to **hypotheses from existing knowledge, marked `[需確認]`, with a note on how to verify them**. Never pretend to have looked something up.

### Iron rule: research content carries a source and a confidence level

§0's biggest risk is **inventing numbers**. So:

- Every market figure and competitor fact **carries a source** (listed in §0.8, cited inline as `[來源: ...]`)
- What can't be found and is estimated instead is marked `[估算]` with its reasoning shown, **never written as though verified**
- Three confidence levels: `高` (multiple agreeing sources, or first-hand data) / `中` (single source, or a reasonable estimate) / `低` (hypothesis from experience)
- The spec-wide markers still apply: inferences the user should verify take `[需確認]`; genuinely two-way readings take `[待拍板]` with options and a recommendation

> In one line: **better to say 「這條信心度低，建議你找 X 驗證」 than to hand over a confident-looking guess.**

## Research and derivation guide

| Section | Output | Main source | Notes |
|---|---|---|---|
| §0.1 Market Sizing | TAM / SAM / SOM, top-down cross-checked against bottom-up | Web industry reports + bottom-up unit economics | Where the feature **can't be monetized independently** (most internal features), switch to **demand sizing**: how many of our users or workspaces hit this problem, and how often. See "Two sizing modes" below |
| §0.2 Market Segments | 3–5 segments (`MS-N`): demographic/firmographic, JTBD, pain, product fit, size | Web + user data | Segments must be distinguishable and non-overlapping |
| §0.3 Competitive Scan | 5 competitors or analogues (`CMP-N`): positioning, strengths, weaknesses/gaps, pricing model, how they solve this | Web (sites/pricing/reviews) + competitor data from the user | Where an internal feature has no "competitors", find **analogous features** — how other products handle import/export, or this class of problem |
| §0.4 Personas | 3 research-backed personas (`PER-N`): JTBD, top 3 pains, top 3 gains, one surprising insight, share | User data > web > hypothesis | **Feeds §1.3 directly.** Every persona must be able to swing a product decision; decorative ones don't belong |
| §0.5 Sentiment & Demand | With feedback data: per-segment sentiment score (−1 to +1), positive and negative themes, quotes. Without: web demand signals (review complaints, forums, search interest) | User feedback data / web | A small sample gets an honest 「樣本少，是假說不是結論」 |
| §0.6 Differentiation & Opportunity | Opportunity list (`OPP-N`): shared competitor gaps, ignored segments, JTBDs nobody solves well, where we can win | Synthesis of §0.2–§0.5 | **Feeds §2 priority and §1.4 directly.** Every OPP points at something actionable |
| §0.7 Implications for Spec | Explicit bullets: which personas go into §1.3, which problem framing into §1.1, which OPPs into §2, which benchmarks into §1.4 | Whole-document synthesis | The §0→§1 handoff bridge, analogous to §5.9 design handoff |
| §0.8 Sources & Confidence | Source list, confidence per major claim, items still to verify | — | Closing section |

### Two sizing modes — §0.1 is easy to get wrong

Decide which kind of feature this is and **size it the matching way**:

- **Independently monetizable** — the feature is itself a sellable product or module (a template marketplace, a paid API) → standard **TAM/SAM/SOM** (annual revenue opportunity), top-down (carved from the industry total) cross-checked against bottom-up (customers × price × frequency).
- **Internal or supporting** — the common case, a feature that makes the existing product better → skip the forced revenue TAM and do **demand sizing**:
  - How many of our current users or workspaces would use it?
  - What share hit the pain of not having it, and how often?
  - Which existing metric does shipping it move — retention, activation, support volume?
  - A "if this were monetized separately" TAM hypothesis can still be attached, marked `[估算]` with its premises stated.

> The cost of picking wrong: forcing TAM/SAM/SOM onto a small internal tool produces big numbers nobody believes, and takes the credibility of the whole of §0 with them.

## Opening

```
要不要先做一份市場研究再開始設計？

我可以幫你查：市場有多大、有哪些競品 / 類似做法、別人的強弱項在哪、
使用者真正在抱怨什麼，最後整理出「我們的切入點」。這份會餵給後面的
problem、persona、需求優先級。

幾個問題幫我抓方向：
1. 你手上有沒有現成資料可以給我？（問卷 / 訪談 / 客服單 / 競品定價 / 既有市場報告）
2. 鎖定哪個市場 / 地區 / 客群？還是先不設限？

（競品名單我會在下一步「研究計畫」一次提給你、你再增刪 —— 這裡不先問，避免你講兩次。）

（如果你已經很清楚市場、想直接進設計，跟我說一聲就跳過這份。）
```

For a POC, add: 「這是 POC 的話，我會做精簡版 — 3 個競品、概略規模、重點放在差異化切入點，要更深再說」.

### Direction check before the run — the one gate, always do it

After the opening questions and **before any web research begins**, state your plan in **one sentence**, get it confirmed, then go.

Why: §0 is the only document in the spec that reaches outward for new facts — research is both expensive (many searches) and easy to point the wrong way (wrong competitor set, wrong market frame, wrong segmentation axis). Discovering that after the full text is written wastes the entire run. This gate costs almost nothing — nothing has been searched yet — and prevents exactly that.

Say it like a colleague, not a form:

```
我打算這樣查：競品先看 Fathom / Fireflies / Otter / Granola / Read AI 這幾家；
這個用 demand-sizing 看（它是既有產品的附加功能，不是獨立市場）；
主軸抓「行動項目最後沒變成被追蹤的任務」這個痛點。這樣對嗎？要加減競品或換角度都說。
```

「Otter 拿掉、加 Fellow」 or 「直接跑」 is all you need. **Confirmed means run to the end without interrupting**; results come afterwards, through the display format below.

**This gate is also the only place the competitor list is settled** — the opening deliberately doesn't ask. Take whatever competitors the user mentioned in passing in their feature description or opening answers, add the ones you found or know, and offer the combined shortlist for them to edit. Don't make them say it twice.

**Scale the gate to the data they brought**:

- Full market report or competitor table supplied → degrade to the light version: 「我把你的資料結構化，再用搜尋補這幾個洞：{列洞}，OK？」
- Nothing supplied → use the full planning sentence above (competitor list + sizing mode + main thread).

**The shape of this gate is one sentence, one confirmation, then silence until it's done.** State the whole research plan in a sentence, take one direction check, and don't interrupt again until it lands. Turning it into a form (「請確認以下 N 項研究參數」) or a multi-stage confirmation (competitors → segments → personas…) falls back into asking section by section, which is more annoying than making the user wait.

> Using AskUserQuestion, this gate is **one question at most** (「這個研究方向對嗎？」 with options: run it / adjust competitors or angle). Keep it light; a plain sentence works too.
> In POC mode, **this gate is §0's only hard stop** — nothing interrupts again after the document is written.

## Questions you must ask

Most of §0 is research, but a few directional things need the user:

- **Market and geographic bounds** — global? A region? An industry vertical? (Sets §0.1's denominator)
- **Sizing mode** — is this feature monetized independently, or supporting the existing product? (Decides TAM vs demand sizing. You can usually judge it from the feature's nature and mark `[需確認]`; ask only when unsure)
- **Known competitors** — the list already in the user's head, folded into §0.3 before you search outward

Ask in everyday language, **3 at a time, maximum**. Everything else — how to cut segments, what the personas look like, where the opportunity is — is research and synthesis, shown for verification rather than handed back as a question.

## Open question candidates

- Two reasonable segmentation axes (by role vs by company size) → `[待拍板]` with a recommendation
- Sizing mode uncertain (internal feature or a monetizable one) → `[待拍板]`, or ask
- A critical competitor fact that can't be found (a rival's real pricing) → `[需確認]` plus how to verify it
- Data too thin to make the personas more than hypotheses → mark the whole section 低 confidence and list it in §0.8

## Display format

§0 usually runs past ~150 lines (competitors, segments and personas all expanded) → apply the **large-document rule**: give **summary, open decisions and a confidence note** in conversation, write the full text to disk, have the user open the file.

### Step 1: summary

```
市場研究做完了，重點如下：

- 市場規模：[一句話 + 信心度]
- 競品格局：[一句話，誰是領先 / 誰有缺口]
- 主要客群：[2-3 個 segment 一句話]
- 使用者最痛的點：[1-2 條]
- 我們的切入點：[1-2 條 differentiation]

→ 對接下來的影響：persona 我會用 PER-X 餵進 §1.3，
  差異化機會 OPP-X 會影響 §2 的需求優先級。

有 [N] 個地方信心度偏低 / 需要你確認（列關鍵詞）。
全文已落盤到 0-market-research.md，你可以開檔看細節。
```

### Step 2: write the full text

Fill §0.1–§0.8 against the template and write it out, with sources and confidence levels marked inline where they belong.

### Step 3: the decisions

```
幾件事想跟你確認：

1. 市場規模我用 [估算] 推到 [數字]，基於 [前提] —— 這個前提合理嗎？
2. 競品我列了 5 家（A/B/C/D/E），你心中還有沒有該列進來的？
3. 我推出的切入點是 [OPP-1]，你認同這是主打方向嗎？
```

## Where you'll get stuck

### The user has no data and can't name a competitor

Don't stall. Work backwards from the problem the feature solves: search 「<問題> software」, 「<類比功能> tool」 for analogous solutions, and mine the reviews for pain points. Mark confidence throughout and list 「建議補做的研究」 in §0.8.

### No reliable market figure exists

Don't invent one. Give a bottom-up estimate (unit economics multiplied up) with explicit premises, marked `[估算]`, and write in §0.8 that confidence is low with a specific way to verify — a report to find, someone to interview.

### It's a pure internal tool and "market" / "competitor" feel wrong

Convert to **analogues plus demand sizing**: the competitive scan becomes 「別的產品 / 我們其他模組怎麼處理這類事」; sizing becomes demand sizing (how many internal users, which existing pain it removes). No external market is not a reason to leave the section blank.

### The user dumps a large pile of feedback data

This is the best possible fuel for §0.5 sentiment. Split by segment, score sentiment, extract positive and negative themes, attach representative quotes. A small sample gets an honest 「N 筆，是訊號不是定論」.

### The user amends §0 and it needs to propagate

§0 is the head of the chain, so the blast radius is large. Follow `Amending earlier documents` in `0-skill-mode.md`, sweeping in particular:

- §0.4 persona changed → §1.3 target personas, the Persona column of §2.1 FRs, §5.2 user stories
- §0.6 opportunity changed → §2 FR priority, §1.4 success criteria
- §0.1 sizing changed → §1.4 quantitative targets

## Reflection check, before §1

- [ ] Every market figure carries a source or is marked `[估算]` — no bare numbers
- [ ] §0.1 uses the right sizing mode (monetizable → TAM/SAM/SOM; internal → demand sizing)
- [ ] §0.3 competitors list weaknesses and gaps **as well as** strengths — strengths alone isn't analysis
- [ ] Every §0.4 persona has a JTBD, pains and one surprising insight, and maps to a downstream product decision
- [ ] Every §0.6 OPP points at something actionable, not a vague 「做得更好」
- [ ] §0.7 explicitly states which findings feed which parts of §1 and §2
- [ ] Every low-confidence item is in the §0.8 to-verify list
- [ ] Marker lifecycle done: confirmed markers deleted, surviving `[待拍板]` carry options and a recommendation, deferred ones converted to a D-NNNN reference

## Closing summary

```
§0 market-research 完成！摘要：

- 市場規模：[一句話 + 信心度]
- 競品格局：[一句話]
- 鎖定客群：[segment 列表]
- 使用者最痛：[1-2 條]
- 切入點：[OPP 列表]
- 餵給 §1 的 persona：PER-1 / PER-2 / PER-3
- 待驗證（信心度低）：[列項]

接下來進入 §1 problem-scope。我會用 §0 的發現當底 —— persona 直接接 §0.4，
problem statement 帶上你最痛的點，success criteria 對標競品。一樣是我先推導、你再確認。

要進嗎？
```
