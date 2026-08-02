---
name: resolving-merge-conflicts
description: Work through an in-progress git merge or rebase conflict hunk by hunk, resolving by intent traced to each side's primary source, then finish the operation. Use when the user is mid-merge or mid-rebase and has conflicts to resolve.
---

# Resolving Merge Conflicts

1. **See the current state.** Check the git history and the conflicting files. Know which operation is in progress — merge or rebase — and what it is trying to achieve.

2. **Find the primary source for each conflict.** Understand why each side made its change and what the original intent was: read the commit messages, the PRs, the originating issues or tickets. A conflict resolved from the diff alone is a guess.

3. **Resolve each hunk.** Preserve both intents where they can coexist. Where they genuinely can't, take the one matching the merge's stated goal and note the trade-off. Invent no new behaviour — a resolution is a choice between existing intents, not a third design.

   **Always resolve. Never `--abort`.** Aborting throws away the understanding you just built and leaves the same conflict for next time.

4. **Run the project's automated checks** — discover them rather than assuming: typically typecheck, then tests, then format. Fix whatever the merge broke.

5. **Finish the operation.** Stage everything and commit; if rebasing, continue until every commit is rebased.
