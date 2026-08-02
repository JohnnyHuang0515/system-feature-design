---
name: handoff
description: Compact the current conversation into a handoff document so a fresh session can continue the work. Use when a thread is getting long, when the work needs to branch off into a separate session, or when the user asks to carry context across a context-window boundary.
---

# Handoff

Write a handoff document summarising the current conversation so a fresh agent can pick the work up. Save it to the OS temporary directory, not the workspace — it is a bridge, not an artifact.

Then **open a new session and reference that file**. A handoff forks; `/compact` continues. Use a handoff when you want a fresh window but need this conversation preserved verbatim somewhere.

## What goes in

- **Where the work stands** — what is done, what is in flight, what is next.
- **Decisions already made**, and the reasoning that would otherwise have to be rediscovered.
- **Dead ends** — what was tried and rejected, so the next session doesn't repeat it.
- **A "suggested skills" section** naming the skills the next agent should reach for.

## What stays out

**Anything already captured in another artifact** — specs, plans, ADRs, issues, commits, diffs. Reference them by path or URL. Duplicating them means the handoff goes stale the moment one of them changes, and a stale handoff is worse than none.

**Secrets.** Redact API keys, passwords, tokens and personally identifiable information before writing.

## When to reach for it

- The thread is approaching the window where the model still reasons sharply — don't push on degraded, hand off.
- The work needs to branch — a prototype session, a separate investigation — and come back. Hand off in both directions.
- A phase boundary where you want the verbatim history preserved rather than summarised in place.

Given an argument describing what the next session is for, tailor the document to that.
