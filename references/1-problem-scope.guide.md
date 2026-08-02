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

## Prior art, before deriving

Where there is a codebase or an earlier spec folder, **check whether this already exists** before specifying it. The most expensive failure this document can produce is a complete spec for behaviour that shipped last quarter, and it is only catchable here — §2 onward inherits the premise.

Search **by domain concept, not by the user's wording.** Someone asking for「匯出範本」 will not match `export` if the code calls it `serialize` or `snapshot`; take the entities the request implies and search for those. Read any sibling `{feature-name}/` folders and `.out-of-scope/` (below).

**Report where you looked** — the paths and the terms — alongside what you found. An unreported search is indistinguishable from no search, and a "nothing found" the user can't audit is worth nothing.

Three outcomes:

- **Already built** → say so, point at where it lives, and ask whether the user wants a change to it instead of a new feature. Don't start §1.1 on the assumption they're wrong.
- **Partly built** → name the overlap; it usually belongs in §1.5 Out of Scope with a pointer, not in scope again.
- **Previously declined** → `.out-of-scope/` has a matching entry. Surface it with its reason and ask whether something has changed.

Report the search **whether or not it found anything**. A hit evidences itself; a miss doesn't, and a miss is the case this exists for — 「沒找到類似的功能」 with no terms beside it is the one sentence a model will write without having looked.

Greenfield, or a spec sitting outside any repo, has nothing to search: say the check doesn't apply here, rather than reporting one you didn't run.

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

## `.out-of-scope/` — the declined-request record

A sibling of the spec folders, holding one file per request **a human explicitly turned down**, with the reason. It exists so the same proposal doesn't walk through the whole spec flow again next quarter, and so the prior-art check above has something to find.

**Only a decline the user actually made gets written.** §1.5's 3–5 unprompted out-of-scope entries are *your* proposed scope boundaries — they belong in §1.5 and nowhere else. Writing them here fills the record with speculation within three features and it stops being read, which costs more than not having it.

The test: can you quote the user declining it? Then write it. Otherwise it's a scope line.

```md
# {The request, in the user's own words}

Declined 2026-08-02 · raised during {feature-name}

{Why — one or two sentences. What would have to change for this to come back.}
```

Something already built is **not** an entry here; point at where it lives instead. This record is for what was rejected, not for what exists.

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

## The fog count, at the same moment as the Path

Q-Stage settles the Path — POC, MVP, production — and that is the moment to settle the other fork: **does this run fit one context window, or does it need a Map first?**

Count the **fog** items §1 surfaced. An item is fog when **both** hold:

1. You can name the area of the decision but **cannot write its options** (a)(b)(c), because the options depend on an answer you don't have.
2. **The answer would change something you are about to write.** Name the section it lands in — §3's entities, §6's interfaces, §8's criteria.

Both conditions as written. Condition 2 asks what the answer *changes*, not whether you could produce text without it — you always could. **Writing a section provisionally and reconciling when the answer arrives is condition 2 being met**, not a way past it. If your plan is to design something reasonable now and map the real answer onto it later, that plan is the evidence.

One condition alone is something else, and has a home already:

| What you have | Where it goes |
|---|---|
| Can't write options, but §2–§8 can proceed without it | §7.2 Open Question with a `D-NNNN` — not fog |
| Can write options, and it blocks | A `[待拍板]` you put to the user now |
| Can write options, doesn't block | A `[待拍板]`, or §7.2 if deferred |
| Can't write options **and** it blocks | **Fog** |

**Report the count as a number, and only after you have taken it.** 「fog 檢查:0 項」 is checkable — a reader can ask which decisions you counted. 「沒有卡住後面的未知」 is not, and a reassurance with no number beside it is the sentence this gate is skipped with. The count belongs in the closing summary, which comes *after* the close; a run that announces its fog outcome in the step-1 summary has announced a count it has not taken.

**One or more fog items → chart a Map before §2.** Say so out loud, name the fog items, and switch to `references/map.guide.md`. Zero → §2 opens normally.

**Move into charting.** Which set of documents this run produces is **structural decomposition, which `Derive vs ask` in `0-skill-mode.md` keeps on your side** — the user verifies and corrects, and business decisions are theirs, but this fork is not one of them. You derived it from a count you just took in front of them.

So say it with this script, which asks for the destination rather than for permission:

```
這裡有 [N] 個卡點,在它們解掉之前,後面的文件只能用猜的:

- [fog 項目一] — 會決定 [§X 的什麼]
- [fog 項目二] — 會決定 [§Y 的什麼]

這幾個不是「你還沒想過」,是「要有人去查了才談得下去」,
所以先畫一張決策地圖,一個一個解掉,再回來寫規格。
先寫規格的話,這幾份等資料進來要重寫。

第一件事:這張地圖走到底,你要的產出是什麼?
```

The last line is the Map's first step, so the user is answering a question either way — the difference is which one. 「要畫地圖還是直接寫規格?」 is a menu, and a gate offered as (a) or (b) is answered by whichever option sounds faster. The override below stays available; volunteering it is the user's move, not yours.

**The user's own words close a row.** 「不知道,要查了才知道」、「要先有人把資料撈出來看過才有辦法談」 — a user telling you the answer needs someone to go and *find a fact* has produced fog. Running the spec in parallel while that fact is gathered does not undo it; it means the documents downstream get written from a guess and rewritten when the guess lands, which is the cost this gate exists to avoid. Schedule pressure is not an override — a Map is faster than a spec rewritten twice.

**Calibration, both directions.** Ten decisions you can write options for are ten answerable questions and they fit one window — that is a spec run, however long the list. One 「要查了才知道」 about something §3 or §6 is built on is fog, however reasonable a parallel plan sounds.

What separates them is **what the user needs in order to answer**:

| The user says | It is |
|---|---|
| 「不知道,**要查了才知道**」 | **fog** — a fact has to be found before the question can even be phrased |
| 「沒想過,**你建議呢**」 | a `[待拍板]` — they can decide the moment you put options up |

The count that matters is of what you *can't* phrase, never of what's open.

The user saying 「不用畫地圖,直接寫規格」 closes this — record the fog items as §7.2 Open Questions and carry on, noting that the documents downstream of them are provisional.

**Entering from a cleared Map**, count what remains, never what the map already answered. Its Decisions so far are settled input — they arrive as answers, not as `[待拍板]`, and re-opening them is how a map→spec handoff turns into a loop. A cleared map normally counts zero; anything above zero is fog that surfaced *since* it cleared, which belongs on the map as a new ticket rather than restarting §1.

## Reflection check, before §2

- [ ] Prior art checked where there's a codebase or sibling spec, and the paths and terms searched were reported
- [ ] Fog counted; zero, or a Map charted, or the user waived it
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
- 既有實作:[查過哪些路徑跟關鍵詞,找到什麼;無 codebase 則省略此行]
- 這次走:[POC / MVP / 正式上線],寫 [文件範圍]
- fog 檢查:[N] 項 —— [N=0 寫「都問得出選項,可以直接往下」;N>0 逐項列出,而且這段不會出現,因為要先畫地圖]
- POC 設計表格:[若有,N 條議題]
- Open Questions:[若有,等 §7 拍板]

接下來進入 §2 requirements,把「要做的事」拆成具體功能需求清單(FR)跟非功能需求(NFR)。
我會繼續用同樣模式 — 我先推導,你再確認。

要進嗎?
```
