---
name: prototype
description: Build a throwaway prototype to answer one design question. Use when the user wants to sanity-check whether a state model or a piece of logic feels right, or to explore what a UI should look like, before committing the decision to a spec or an implementation.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides its shape.

## Pick a branch

Identify the question — from the prompt, the surrounding code, or by asking if the user is around. The two branches produce very different artifacts, and getting it wrong wastes the whole prototype. Genuinely ambiguous and the user is away → match the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top.

### Logic — "does this state model feel right?"

For questions about business logic, state transitions or data shape: the kind of thing that looks reasonable on paper and only feels wrong once real cases run through it. *"Does this handle X then Y?"* *"Can this model even represent the case where…?"*

**Keep the logic pure and portable, with a throwaway shell around it.** Put the part that answers the question behind a small pure interface — a reducer `(state, action) => state`, an explicit state machine when "which actions are even legal right now" is part of the question, a set of pure functions when there's no current state, or a module with a clear method surface when it genuinely owns ongoing state. Pick the shape the *question* needs, not the one easiest to wire up. No I/O, no logging for control flow — the shell imports the logic, never the reverse. That split is what lets the validated logic lift into the real module afterwards while the shell is discarded.

**The shell is one self-contained HTML file** — plain HTML, CSS and JS, no build, no server, no dependencies. The person who owns the decision opens it by double-clicking and drives it themselves, in their own vocabulary. That is the whole point: a prototype they have to watch you operate answers your question about the model, not theirs.

Three parts in the file:

- **A state panel** showing the full relevant state, re-rendered after every action so what changed is visible rather than inferred.
- **Free-play buttons** for every action, always available, so they can wander into the case you didn't think to script.
- **Guided walkthroughs** — tabs, one per scenario, each naming the situation in domain language with the buttons to press underneath in order. This is what lets a non-developer reach the edge case you actually need judged.

Label everything the way *they* say it — 「員工請了半天,主管還沒批」, not `state: PENDING_HALF_DAY`. A panel written in the code's vocabulary tests whether they can read your naming, which is not the question.

### UI — "what should this look like?"

Generate **several radically different variations**, switchable in the browser, so the user flips between them and picks — usually saying *"I want the header from B with the sidebar from C"*, which is the real answer.

**Embed in an existing page wherever possible.** A variant is far easier to judge butting up against the real header, real sidebar, real data and real density; a standalone throwaway route is a vacuum where every variant looks fine. Default to rendering variants on the existing route behind a `?variant=` param, keeping the page's data fetching, params and auth and swapping only what's rendered. Something with no page yet but that would naturally live inside one — a new dashboard section, a new card on settings — still mounts inside its host. Only a genuinely new top-level surface earns its own throwaway route, named so nobody mistakes it for production.

**Three variants by default; cap at five** — past that they stop being radically different and start being noise. Radically different means different layout, different information hierarchy, different primary affordance. Three tweaked card grids is wallpaper, not a prototype; if two drafts come out similar, redo one under an explicit constraint.

**The switcher** is a small fixed bar at the bottom centre: previous arrow, the current variant's key and name (`B — Sidebar layout`), next arrow, both wrapping. Arrows update the URL param through the framework's router so a variant is shareable and survives reload; `←` / `→` do the same, except while an input, textarea or contenteditable has focus. Style it high-contrast so it reads as scaffolding rather than part of the design being judged, and gate it on a non-production check so a stray merge can't ship it.

## Rules for both

1. **Throwaway from day one, and marked as such.** Put it next to the module or page it prototypes for, so the context is obvious, but name it so a casual reader sees it isn't production. Throwaway UI routes follow whatever routing convention the project already uses.
2. **One command to run.** Whatever the project's task runner already supports. The user starts it without thinking.
3. **No persistence by default.** State lives in memory — persistence is usually the thing being checked, not something to depend on. Where the question genuinely involves a database, use a scratch one named to make its fate obvious.
4. **Skip the polish.** No tests, no error handling beyond what makes it runnable, no abstractions. The point is to learn something fast.
5. **Surface the state.** After every action, or on every variant switch, show the full relevant state so the change is visible.
6. **Capture it when done.** Fold the validated decision into the real code, then keep the prototype as a **primary source**: commit it to a throwaway branch off main and leave a pointer to that branch on the implementation issue. Record the verdict and the question it settled. Main keeps only the decision.

   For logic, the validated reducer or state machine lifts into the real module and the HTML shell rides to the branch. For UI, the winner folds into the page and the losing variants plus the switcher come out of main — variant components left behind rot fast and confuse the next reader. Rewrite what you promote: it was written under prototype constraints, with no tests and minimal error handling.

## Anti-patterns

- **Adding tests.** A prototype that needs tests has stopped being one.
- **Wiring to the real database, or to real mutations.** Point at an in-memory store or a stub — unless persistence *is* the question.
- **Generalising.** No "what if we want X later". It answers one question.
- **Blurring the logic into the shell.** A reducer that reaches for `document` is no longer portable.
- **Variants that differ only in colour or copy**, or that share a `<Layout>`. A shared `<Header>` is fine; sharing the layout defeats the point, since each variant should be free to throw it out.

## Feeding the answer back

A prototype that settled a decision more precisely than prose can — a state machine, a reducer, a schema, a type shape — earns an inline snippet in the spec or ticket, noted as coming from a prototype and trimmed to the decision-rich part. That is the one exception to specs and tickets carrying no code.
