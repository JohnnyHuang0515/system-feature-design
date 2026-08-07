---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose" or "debug this", or reports something broken, throwing, failing, or slow — especially a bug that resisted a first glance, an intermittent flake, or a regression between two known-good states.
---

# Diagnosing Bugs

A discipline for hard bugs. Skip a phase only with an explicit reason.

Read the relevant `.claude/rules/` files for the area you're touching, and `.claude/rules/codebase-design.md` for the seam vocabulary Phase 5 uses.

## Phase 1 — Build a feedback loop

**This is the skill.** Everything after it is mechanical. With a **tight** pass/fail signal that goes red on *this* bug, you will find the cause — bisection, hypothesis testing and instrumentation all just consume it. Without one, no amount of reading code will save you.

Spend disproportionate effort here. Be aggressive, be creative, refuse to give up.

### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM, console, network.
5. **Replay a captured trace.** Save a real request, payload or event log to disk and replay it through the code path in isolation.
6. **Throwaway harness.** A minimal subset of the system — one service, mocked deps — that hits the bug path in a single function call.
7. **Property / fuzz loop.** For "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If it appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so `git bisect run` can drive it.
9. **Differential loop.** Same input through old vs new version, or two configs, and diff the outputs.
10. **Human-in-the-loop script.** Last resort, when a human must click. Drive *them* from a script so the loop stays structured, and feed the captured output back.

Build the right loop and the bug is 90% fixed.

### Tighten it

Treat the loop as a product. Once you have *a* loop:

- Faster? Cache setup, skip unrelated init, narrow the test scope.
- Sharper signal? Assert on the specific symptom, not "didn't crash".
- More deterministic? Pin time, seed the RNG, isolate the filesystem, freeze the network.

A 30-second flaky loop is barely better than none. A 2-second deterministic one is a superpower.

### Non-deterministic bugs

The goal isn't a clean repro, it's a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; a 1% one isn't — keep raising the rate until it is.

### When you genuinely cannot build one

Stop and say so. List what you tried, and ask for one of: access to an environment that reproduces it, a captured artifact (HAR file, log dump, core dump, timestamped screen recording), or permission to add temporary production instrumentation. Hypothesising without a loop is the failure this skill exists to prevent.

### Completion criterion

Phase 1 is done when you can name **one command** that you have **already run at least once** — paste the invocation and its output, **redacted** — and that is:

- [ ] **Red-capable** — it drives the actual bug path and asserts the user's exact symptom, so it goes red on this bug and green once fixed. "Runs without erroring" is not red-capable.
- [ ] **Deterministic** — same verdict every run (for flaky bugs, a pinned high reproduction rate).
- [ ] **Fast** — seconds, not minutes.
- [ ] **Agent-runnable** — runnable unattended.

Catching yourself reading code to build a theory before this command exists means **stop**. No red-capable command, no Phase 2.

### Redact first

This skill works by **showing things** — the invocation, its output, the artifact you captured. Every one of those is a place a live credential leaves the machine, and the moment it lands in a transcript it is out of your hands.

So redaction is the first move on each, not a tidy-up afterwards:

- **A secret you have to name** → write `<REDACTED>` in its place.
- **A loop that needs a credential** → build it against an env var, so the value stays in the environment rather than in what you show. `curl -H "Authorization: Bearer $API_TOKEN"` is showable; the token pasted inline is not.
- **A captured artifact** — a HAR, a request log, a database dump → quote only the lines that carry the signal. Attaching the whole file to prove one header is wrong hands over everything else in it.

This holds for what you show the user as much as what you write to a file. A redacted paste is still a complete Phase 1 exhibit — the reader needs the *shape* of the request, not its bearer token.

## Phase 2 — Reproduce and minimise

Run the loop and watch it go red. Confirm:

- [ ] The failure mode is the one **the user** described, not a different one that happens to live nearby. Wrong bug, wrong fix.
- [ ] It reproduces across runs (or at a high enough rate to debug against).
- [ ] The exact symptom is captured — error message, wrong output, timing — so later phases can verify the fix addresses it.

Then **minimise**: shrink to the smallest scenario that still goes red. Cut inputs, callers, config, data and steps **one at a time**, re-running after each cut. Done when every remaining element is load-bearing — removing any one turns the loop green.

A minimal repro shrinks the hypothesis space in Phase 3 and becomes the clean regression test in Phase 5. Reproduce *and* minimise before moving on.

## Phase 3 — Hypothesise

Generate **3–5 ranked hypotheses before testing any of them** — generating one at a time anchors you on the first plausible idea.

Each must be **falsifiable**, stated as its prediction:

> "If X is the cause, then changing Y makes the bug disappear / changing Z makes it worse."

A hypothesis with no prediction is a vibe. Sharpen it or drop it.

**Show the ranked list to the human before testing.** They often re-rank it instantly ("we deployed a change to #3 last week") or have already ruled something out. Cheap checkpoint, big saving. Don't block on it — proceed with your ranking if they're away.

## Phase 4 — Instrument

Every probe maps to a specific prediction from Phase 3. **Change one variable at a time.**

Tool order: a debugger or REPL where the environment supports it — one breakpoint beats ten logs — then targeted logs at the boundaries that distinguish hypotheses. "Log everything and grep" is not a step.

**Tag every debug log with a unique prefix**, e.g. `[DEBUG-a4f2]`, so cleanup is a single grep. Untagged logs survive the fix; tagged ones die with it.

**Performance branch.** For a regression, logs are usually the wrong tool. Establish a baseline measurement first — timing harness, profiler, query plan — then bisect. Measure first, fix second.

## Phase 5 — Fix and regression test

Write the regression test **before the fix** — if there is a **correct seam** for it.

A correct seam exercises the real bug pattern as it occurs at the call site. Where the only available seam is too shallow — a single-caller test for a bug that needs several callers, a unit test that can't replicate the chain that triggered it — a test there gives false confidence.

**No correct seam is itself the finding.** Note it: the architecture is preventing this bug from being locked down.

With a correct seam: turn the minimised repro into a failing test there, watch it fail, apply the fix, watch it pass, then re-run the Phase 1 loop against the original un-minimised scenario.

## Phase 6 — Cleanup and post-mortem

Before declaring done:

- [ ] The original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] The regression test passes, or the absence of a seam is documented
- [ ] All `[DEBUG-...]` instrumentation is removed — grep the prefix
- [ ] Throwaway harnesses are deleted, or moved somewhere clearly marked
- [ ] The hypothesis that turned out correct is stated in the commit or PR message, so the next person debugging learns from it

**Then ask what would have prevented this bug.** Where the answer is architectural — no good test seam, tangled callers, hidden coupling — record it against `.claude/rules/codebase-design.md`'s deletion test and hand the specifics on. Make that recommendation **after** the fix is in: you know more now than when you started.
