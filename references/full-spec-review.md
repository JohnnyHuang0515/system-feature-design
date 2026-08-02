# Full-spec review

> Disclosed reference, reached only when the spec is finished. `0-skill-mode.md` points here from its closing step.
> Instructions are English; the quoted blocks are scripts spoken to the user — use them as written.

After the last document lands (§9, or §8 when §9 is skipped), **offer to run a full-spec review**.

Working document by document, each one is only seen on its own. Cross-document problems appear only when they sit together: whether numbered references resolve, whether one concept is described consistently across files, whether anything is orphaned, whether anything is missing.

### How to offer it

```
所有文件都完成了！

要不要跑一次完整 spec 的總 review？
我會檢查跨文件的一致性，例如：
- 所有 FR 是否都有對應的驗收條件
- 編號 reference 是否全部對得上
- 同一個概念在不同文件描述是否一致
- 有沒有遺漏或孤兒內容

要跑嗎？
```

### If the user says yes

Preconditions:

- §5 Presentation Type is not GUI → skip everything touching §5.4–5.9 (user journey / component / page / T-N / interaction decision table / design handoff)
- §9 was skipped → skip §9 items, but check in reverse that §1–§8 carry no leftover references to §9
- §0 was skipped → skip all §0 items (MS / CMP / PER / OPP references, persona sourcing, sourcing discipline) and check in reverse that §1.3 points at no non-existent PER-N

#### Check 0: mechanical pass, before the eyeballs

Most of Check 1 and Check 5 scans more reliably by command than by reading. Run these first:

```bash
# Check 1：跨文件 ID 解析。掃完整份 spec（含 issues/ 與 decisions/），
# 列出「被引用但沒定義」的 ID。乾淨時 exit 0。
python3 <skill-path>/scripts/check-example-ids.py .

# Check 5：殘留標記（結果應為空）。用 bracket pattern，避免誤命中純中文敘述與 JTBD
grep -rn "\[需確認\|\[待拍板\|\[TBD\]" --include="*.md" .

# Check 1 續：§6.2 用到的 error code vs §6.5 catalog（兩份清單應一致）
grep -oE "(4[0-9]{2}|500) [A-Z_]+" 6-interfaces.md | sort -u
grep -oE "\| (4[0-9]{2}|500) \| [A-Z_]+" 6-interfaces.md | sort -u
```

The ID script does the bulk of Check 1 better than reading can — it knows which document owns each prefix, treats a retired ID (`編號保留不重用`) as declared rather than missing, and skips IDs cited illustratively in prose about the notation. It also reports IDs **defined but never referenced**, which is Check 3's orphan pass. Read its output before starting Check 1 by eye; whatever it clears, you don't re-check.

⚠️ Traps:

- Scanning for leftover §9 references, `grep "§9"` also hits `FR-9`, `SF-9`, `AC-9.x` — judge each hit on whether it really points at the rollout document.
- Leftover markers **must be matched with the bracket pattern** (`\[需確認`). Bare `TBD` collides with **JTBD**, which appears throughout §0 and personas; bare `需確認` collides with ordinary prose like 「…前需確認」. A `JTBD` hit or a prose hit is not a leftover marker.
- §0's `[估算]` / `[來源]` / confidence levels are **permanent annotations** (sourcing discipline), not leftover markers.

With the mechanical pass done, spend your attention on what a machine can't do — Check 4 conceptual consistency and Check 2 coverage semantics.

#### Check 1: cross-document ID references

Scan every numbered usage and confirm it resolves:

- PER-N cited by §1.3 personas (where §0 ran) → exists in §0.4
- PER-N / OPP-N / MS-N cited by the §0.7 Implications table → exists
- OPP-N cited by §2 FR priorities or §1.4 → exists in §0.6
- The Persona column of §2.1 FRs → maps to a persona listed in §1.3
- §3.2 entity references → all exist
- The Scope column of §3.4 BRs → maps to a real entity
- Related FR of §4.1 SFs → FR-N exists
- Related UF of §4.1 SFs → UF-N exists in §5.3
- "Triggers in" of §4.2 EFs → the SF step exists
- UF-N / P-N cited by §5.4 user journey stages → exist
- "Used in" of §5.6 components → P-N exists in §5.7
- "Entry from" of §5.7 pages → UF-N exists
- Related FR of §6.2 endpoints → FR-N exists
- Errors of §6.2 endpoints → the error code is registered in the §6.5 catalog
- §6.4.1 published events → listed in §3.5
- The Affects column of §7 ADRs → correct
- Every §8 AC's FR / state / BR / EF / EC / NFR → exists
- Every reference to §9 → §9 exists (rewritten or removed if §9 was skipped)

#### Check 2: required coverage

- Every FR has an AC (§8.1)
- Every state transition has both a legal and a violation AC (§8.2); where no interface can trigger the violation, an explicit 「不適用 + 原因」 note
- Every BR has an AC or a reference (§8.3)
- Every EF and EC has an AC (§8.4)
- Every NFR has an AC (§8.5)
- Every component a page uses is defined in §5.6
- Every dimension of the §5.8 interaction decision table has a decision (or 「N/A + 原因」), and major decisions have an ADR
- Where §5.9 Design System reads 「尚無」, §7 carries a matching OQ or ADR with Owner and Target Date
- Every §6.2 endpoint has at least one happy path plus its error responses
- Every §9.4 alert has a §9.5 runbook

#### Check 3: orphans

Scan in reverse for anything defined but never used:

- Every §0.4 PER-N (where §0 ran) is adopted by §1.3, or explicitly noted as researched but out of this feature's target
- Every §0.6 OPP-N flows into §0.7 or §2 — an opportunity that feeds nothing was wasted work
- Every §3.2 entity is used by at least one FR / SF / API
- Every §5.6 component appears on at least one page
- Every §6.5 error code is used by at least one endpoint
- Every §3.5 domain event has a producer and a (potential) consumer

#### Check 4: conceptual consistency

- §0.4 persona JTBD and pain points (where §0 ran) vs the §1.3 persona description — §1.3 shouldn't contradict §0.4
- Impact claimed by §0.7 Implications vs what downstream actually says (§0.7 says OPP-1 raises some FR's priority — does §2 reflect it?)
- §3.3 state machine states vs the transitions described in §4.1 SFs
- §3.4 BR rules vs §6.5 error code meanings
- §1.3 persona pain points vs §2.1 FR descriptions
- §1.5 in scope vs §2.1 FRs — every FR is inside scope
- §1.5.1 POC table vs §7 ADRs — everything that should be expanded, is
- §5.4 user journey stages vs §5.3 UFs — the journey is genuinely strung from UFs, with no invented stages
- §5.5 Design System status vs §5.9 handoff content — both describe the same "have / haven't"

#### Check 5: unresolved decisions

- Every §7.2 open question has Owner and Target Date
- No unresolved `[需確認]` / `[待拍板]` markers remain (nor non-standard leftovers like `[TBD]` / `[Open Question]`)

#### Check 6: §0 research discipline (only where §0 ran)

- Every market figure and competitor fact in §0 carries a **source** or is marked `[估算]` — a bare number reads as verified when it isn't
- Every low-confidence or unverified item is collected into §0.8 「建議補做的研究」
- §0.1 uses the right sizing mode — independently monetizable → TAM/SAM/SOM; internal feature → demand sizing

### Presenting the results

```
總 review 完成！結果如下：

✅ Pass 項目（無需處理）：
- 所有 FR 都有對應 AC（FR-1 ~ FR-9 → AC-1.1 ~ AC-9.3）
- 編號 reference 全部對得上
- ...

⚠️ Warning 項目（建議處理）：
- §3.5 列了 TemplateActivated 事件但沒有任何 consumer
- §5.6 C-9 (Toast) 沒有明確被任何 page 引用（但實際使用上隱含）
- ...

❌ Error 項目（建議必修）：
- §6.2 POST /api/templates/import 提到 401 UNAUTHORIZED，但 §6.5 catalog 沒列
- §8.1 AC-3.2 沒寫，但 FR-3 有對應的 AC-3.1, AC-3.3
- ...

要我幫你修正 Error 項目嗎？Warning 項目要看哪些？
```

### If the user says no

Deliver the finished spec with:

- The spec's file tree
- A one-line summary per document
- A suggested role-to-section map (PM / backend / frontend / QA / SRE)
- An invitation: 「未來如果想跑總 review，隨時告訴我」
