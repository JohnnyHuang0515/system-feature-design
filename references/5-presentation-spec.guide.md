# Reference Guide: 5-presentation-spec.md

> Runs on the `Derive → Show → Verify` model in `0-skill-mode.md`. Pairs with `templates/5-presentation-spec.template.md`.
> Instructions here are English; the quoted blocks are scripts spoken to the user — use them as written.

## Purpose

Describe how the feature presents itself — the manual for frontend and UX engineers. Visual detail belongs to the Design System; this document says **which component, on which page, along which flow**.

## Opening

```
進入第五份:呈現規格。

這份描述 feature 怎麼對外呈現給使用者 — 不一定是 UI,
也可能是 API only / Background Job / CLI / Notification。

我會先推導,你確認 / 修正。
```

## Derivation

### Presentation type

Infer it from §1 and §2:

- The user describes 「點按鈕、看畫面」 → GUI
- Pure API integration → API Only
- Scheduled task or system behaviour → Background Job
- Command-line tool → CLI
- Notification, email, push → Notification

**The test is how the user touches the feature, not what domain it's in.** Notification as a type means the delivery channel itself — the triggering and content of email or push — **not** "the feature is notification-related". An in-app notification centre with a bell, a panel and a settings page is primarily GUI, with Notification as a secondary type. When unsure: if the user will look at a screen and click things, there's a GUI component, and §5.4–5.9 get written.

Mark the inferred type `[需確認]` — a feature can have several.

### What follows, by type

| Type | 5.2 | 5.3 | 5.4–5.9 |
|---|---|---|---|
| GUI | User Story | User Flow | write |
| API Only | Consumer Story | Consumer Flow | skip |
| Background Job | Trigger Story | Execution Flow | skip |
| CLI | Command Story | Command Flow | skip |
| Notification | Recipient Story | Trigger Flow | skip |

> §5.4 User Journey and §5.9 Design Handoff are GUI-only. For other types the "journey" is already carried by §5.3's consumer or execution flow, and with no visual artefact there is nothing for §5.9 to hand off.

### User stories

From §1.3 personas plus §2.1 FRs: pair each persona with the FRs they'd use, in the 「作為 X,我想要 Y,以便 Z」 form. A persona usually gets 1–3 stories.

### User flows

Reverse the §4.1 SFs into the user's point of view. An SF says what the system does; a UF says what the user sees and does. Each SF maps to 1–N UFs, written step by step, with no system internals.

### User journey (§5.4, GUI only)

Once the UFs exist, **lift them one level** into a journey. This isn't rewriting the UFs — it's stringing the scattered UFs into the complete arc of the user reaching their goal.

- **Stages**: 3–6, induced from the §1 persona's goal and the UF order — awareness/entry → operation → completion/follow-up
- **Per stage**: what the user is trying to finish, which UFs and Pages it touches, where they might stall (aligned to §4 EF / EC), and what matters experientially
- **Multiple personas**: one journey per major persona; secondary or one-off personas can be omitted
- The journey **gets no IDs of its own** — use stage names plus references to existing UF-N / P-N

Why the extra layer: a UF is step-by-step operation, a journey is the shape of the whole experience. Frontend and UX read the journey to see which stage most needs to be smooth and where users drop off — neither is visible reading UFs one at a time.

### Components and pages (§5.6 / §5.7, GUI only)

From the user flows: the UI elements a step touches → components (C-N); the screen a step happens on → pages (P-N); a page's layout blocks → sections (T-N).

### Design handoff (§5.9, GUI only)

§5 carries structure and interaction. **Visuals — mockups, colour, type scale — are downstream and out of this spec.** §5.9 turns that boundary from a silent hole into an explicit gap with directions:

- **Design System status** (aligned with the §5.5 decision): exists → record the source link; **absent → flag it as a prerequisite for frontend work**, recommend a tool or skill to produce one (ckm-design-system / ui-ux-pro-max / design-taste-frontend / Pencil MCP), and log an OQ or ADR in §7 with Owner and Target Date
- **How mockups get made**: feed §5.6 components + §5.7 pages (ASCII layout) + §5.8 interaction decisions to the design tool for hi-fi output. The tool's output is authoritative for visuals; on conflict, sync the spec back
- **Prerequisite list**: Design System, mockups or visual references, responsive breakpoints (aligned to §5.8), microcopy source — tick each, and flag what's missing

The dividing line: this skill doesn't turn itself into a design tool and produce mockups — the environment has dedicated design skills. §5.9's job is **handoff**, not **output**.

### Backfill §4

After §5.3's UFs are written, **go back and fill each §4 SF's "Related UF" column** with the matching UF-N.

## Frontend experience checklist (GUI only, always run)

> This is §5's core set of questions. Structure — which components and pages exist — is yours to derive. What they look like, how they behave, and what happens on failure are experience decisions: you propose a value, the user decides.
> The common failure: finish the structure and move on, never asking a single frontend question, so the user only discovers the mismatch when the spec lands.

Once GUI is confirmed, walk all 8 dimensions:

| # | Dimension | How to ask it | Common options |
|---|---|---|---|
| 1 | Entry point and navigation | 「使用者要從哪裡進到這個功能?」 | 側欄新項目 / 既有頁面加按鈕 / 既有選單加項目 / 設定頁 |
| 2 | Container | 「主要操作開獨立頁、彈窗,還是側邊抽屜?」 | 獨立頁 / Modal / Drawer / 就地展開 |
| 3 | Interaction mode | 「資料一頁填完,還是分步驟引導?可以在列表上直接改嗎?」 | 單頁表單 / 分步精靈 / inline 編輯 |
| 4 | Empty state and first run | 「第一次進來、一筆資料都沒有時,使用者看到什麼?」 | 引導文案 + CTA / 空表格 / 範例資料 |
| 5 | Errors and partial success | 「操作失敗時使用者看到什麼?能在原地重試嗎?10 筆裡成功 8 筆要怎麼顯示?」 | 整批失敗 + 訊息 / 部分成功 + 結果清單 / 原地重試 |
| 6 | Feedback and safeguards | 「成功後怎麼告訴使用者?危險操作(刪除 / 覆蓋)要不要再確認一次?要能反悔嗎?」 | Toast / Banner / 確認 Modal / Undo |
| 7 | Data volume | 「列表長到幾百筆時怎麼辦?要搜尋、篩選嗎?預設怎麼排?」 | 分頁 / 無限捲動 / 搜尋 + 篩選 / 固定上限 |
| 8 | Device and liveness | 「手機要不要能用?同一筆資料會被別人同時改嗎 — 畫面要自動更新嗎?」 | 桌機 only / RWD;手動刷新 / 輪詢 / 即時推送 |

### How to run it

1. **Filter first.** Decide which dimensions this feature actually has — a pure display feature has no "interaction mode" question; a single-user tool has no "liveness" question. Skip the rest with a one-line note: 「維度 X 不適用,因為…」
2. **Derive a recommended value per dimension** from §1 personas, §2 FR/NFR and §4 EF/EC, each with a one-line reason.
3. **Package the decisions**:
   - Non-POC: follow `0-skill-mode.md`'s AskUserQuestion rule — 2–3 per round
   - POC fast mode: **not silent defaults** — use a **one-shot confirmation pack**, listing every relevant dimension's recommended value at once: 「前端體驗我建議這樣:(清單)。有要改的嗎?都 OK 我就照這個寫」. The whole pack counts as one hard stop
4. **Write it down.** Results go into the §5.8 decision table (N/A plus a reason for the dimensions that don't apply). Anything shaping the data model or irreversible — a partial-success strategy that drives API design, say — is escalated to an ADR.

### Why silent defaults don't work for the frontend

The frontend is the only part the user sees directly. A wrong backend structure is only discovered by reading the document; a wrong frontend experience is rejected on sight — by which point it's already been built. One extra confirmation round in §5 is far cheaper than rebuilding after implementation.

## Questions you must ask

1. **Confirm the presentation type** after inferring it
2. **The frontend experience checklist** (GUI only) — see above: recommended value per relevant dimension, packaged for decision
3. **Whether a Design System exists** (GUI only) — the pivotal §5.5 / §5.9 call: reuse an existing one (ask for the source) or none yet (flag the prerequisite). Phrasing below
4. **Component visual detail** — ask where the user has a specific requirement (a node card that must be 160×140)

## Open question candidates

- Uncertain presentation type (several mixed)
- Several reasonable component splits (one large vs several small)
- Several reasonable page layouts (own page vs Modal vs Drawer)
- Several reasonable renderings of empty state or partial success
- Device support unstated (desktop only vs RWD)
- No Design System yet, with who and what tool undecided (§5.9 prerequisite)

## Display format

### Step 1: confirm the presentation type

```
我從前面文件推測這個 feature 主要透過 GUI 呈現給使用者。對嗎?
還是有其他形式(例如後台 cron job)我漏了?
```

### Step 2: summary

```
我推導出:

- Presentation type:{類型}
- User stories:{N 個} (覆蓋 {M} 個 persona)
- User flows:UF-1 ~ UF-{N}
- User journey(若 GUI):{N} 個階段
- Components(若 GUI):C-1 ~ C-{N}
- Pages(若 GUI):P-1 ~ P-{N}

需要你拍板:[N 個]
```

### Step 3: section by section

For GUI: user stories first (fast), then user flows (medium), then the user journey (stringing UFs into stages, fast), then components and pages (slow — needs visual confirmation), and finally the design handoff (Design System status plus the prerequisite list).

### Step 4: the decisions, led by the frontend checklist

```
前端體驗有 5 個維度需要你拍板(另外 3 個維度不適用,我列在最後):

1. 進入點:我建議放在模板列表頁的「建立」選單裡,不另開側欄項目。OK 嗎?
2. 容器形式:匯入預覽我建議獨立頁(P-5),不是 Modal。可以嗎?
   (考量:預覽內容多,Modal 會擠;但獨立頁多一次跳轉)
3. 失敗呈現:驗證失敗停在原頁 + 錯誤訊息,不做「部分匯入」。對嗎?

(下一輪再問:操作回饋方式、資料量呈現)
不適用維度:操作模式(無多步驟表單)、即時性(單人編輯)、…
```

Use AskUserQuestion where available, 2–3 per round.

## Where you'll get stuck

### The user has never written a UI spec

Say it plainly: 「我們不寫實作層(props、event handler 等),只寫:這個 component 角色是什麼、有哪些狀態、用在哪些 page。視覺細節歸 Design System。」

### Confirming whether a Design System exists (§5.5 / §5.9, mandatory)

Never assume there is one. Ask in everyday language:

```
✅ 「你們現在有沒有一套共用的設計規範 / 元件庫?(例:Figma 上的 design system、
    或程式裡共用的 UI component 庫)還是這個功能要從零刻 UI?」
```

- **Yes** → ask for the source (Figma / Storybook / code library), record the reference in §5.5, mark §5.9 as reusing it
- **No** → this is not a small thing. **A baseline design system has to exist before frontend work starts**, or every screen gets its own. Flag it as a prerequisite in §5.9, log an OQ or ADR in §7 with Owner and Target Date, and recommend a tool or skill to produce it
- **Ask on a POC too** — deciding 「POC 先用最小 token 集,正式再補」 is fine, but the decision has to be said out loud rather than skipped

### The user wants to hand over a Figma link

Take it. Write the reference as 「視覺以 Figma 為準([連結]),本 spec 只描述結構 + 互動」, and record that Figma as §5.9's Design System source.

### The user's UI description stays abstract

Propose: 「我幫你列幾個可能的 component:[列舉]。看哪些符合你想的,哪些不在範圍。」

### The user wants to use a design tool (Fable / Pencil MCP / a ui-ux skill) for visuals

§5 only carries structure (C-N / P-N / UF-N) and visuals belong to implementation anyway, so wanting a design tool is a reasonable move — don't stall on it:

- **Settle the split first**: keep writing structure, or stop now and produce mockups? Recommend finishing the document and leaving visuals to implementation — pick reversible, sensible defaults for layout-shaped decisions and note that 「視覺與版面由 {工具} 於實作階段定案」
- If mockups are wanted now: feed the settled C-N / P-N / layout ASCII to the tool as input, and fold the design result back into §5 so spec and design stay aligned
- If the tool is unavailable (MCP down, etc.) → finish the spec on defaults. The flow doesn't stop on a tool.

## Reflection check, before §6

- [ ] Presentation type is confirmed
- [ ] Every user story maps to at least one persona and one FR
- [ ] Every user flow maps to an SF (GUI)
- [ ] Every user journey stage references real UFs and Pages, with stall points aligned to §4 EF / EC (GUI)
- [ ] Every §4 SF's "Related UF" column is backfilled
- [ ] Every component a page uses is defined in §5.6 (GUI)
- [ ] Every component appears on at least one page — no orphans (GUI)
- [ ] All 8 frontend dimensions were reviewed: the relevant ones decided, the rest marked N/A (GUI)
- [ ] Decisions are written into the §5.8 table, with major ones escalated to ADRs (GUI)
- [ ] Design System status is decided — reuse existing, or none yet → §5.9 prerequisite + §7 OQ (GUI)
- [ ] The §5.9 handoff list is filled, with missing prerequisites explicitly flagged (GUI)

## Closing summary

```
§5 presentation-spec 完成!

- Presentation type:{類型}
- User stories:{N 個}
- User flows:UF-1 ~ UF-{N}
- User journey:{N} 個階段(若 GUI)
- Components:C-1 ~ C-{N}(若 GUI)
- Pages:P-1 ~ P-{N}(若 GUI)
- 前端體驗決策:{M} 個維度已拍板,{K} 個不適用(§5.8)(若 GUI)
- Design System:{沿用既有 / 尚無—已列前置條件}(若 GUI)
- §4 SF 的 "Related UF" 已回填

接下來進入 §6 interfaces,我會推導對外 API、events、整合點。要進嗎?
```
