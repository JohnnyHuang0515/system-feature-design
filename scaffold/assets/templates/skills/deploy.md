---
name: deploy
description: Deploy {{PROJECT_NAME}} to {{DEPLOY_TARGET}}. Use when the user asks to deploy, release, ship, or push to production/staging. Covers the full pre-flight check, deployment steps, and post-deploy verification.
---

# Deploy

Workflow for deploying {{PROJECT_NAME}} to {{DEPLOY_TARGET}}.

## Pre-flight checklist

Before deploying anything, verify:

- [ ] All tests pass: `{{TEST_CMD}}`
- [ ] Linter is clean: `{{LINT_CMD}}`
- [ ] Local branch is up to date with `main` (or release branch).
- [ ] No uncommitted changes (`git status` is clean).
- [ ] The change has been reviewed — either a merged PR, or explicit user approval for direct deploys.
- [ ] Required secrets and config are present in the target environment.
- [ ] Any database migrations have been applied (or are included in the deploy).

If **any** of these fail, stop and surface the issue. Don't deploy past a failure.

## Deployment steps

<!-- TODO: Fill in the concrete steps for your setup. Example for a generic setup:

1. Build: `{{BUILD_CMD}}`
2. Tag the release: `git tag -a vX.Y.Z -m "release notes"`
3. Push: `git push && git push --tags`
4. Trigger deploy: `{{DEPLOY_CMD}}`
5. Wait for CI/CD to report success.
-->

## Post-deploy verification

After the deploy completes:

- [ ] Smoke test — name the endpoints you hit and paste each status code. "tested it" with nothing beside it is not a smoke test.
- [ ] Error monitoring — **zero new error signatures since the deploy timestamp**. Some errors is not a passing bar; state the count and the window you looked at.
- [ ] Platform health indicators green, named one by one.
- [ ] Where a migration shipped, the schema diff against expected is **empty** — show it.

The pre-flight list above is nearly all runnable commands; this list guards a change that is already live, so it earns the same treatment. A deploy that reports success while broken is exactly what these four are for.

If something's wrong, follow the rollback procedure:

<!-- TODO: Document rollback. Example:
- Vercel: `vercel rollback`
- Fly.io: `fly releases list` + `fly deploy --image <previous>`
- Manual: revert the commit and redeploy.
-->

## What to report to the user

When the deploy finishes, report:
1. What was deployed (commit SHA, branch, version tag).
2. What environment it went to.
3. Any warnings from the pre-flight or post-deploy checks.
4. Link to the deploy dashboard if available.

## Hard rules

- **Deploy with the day ahead of you** — morning, mid-week, with time to watch it.
- **A green suite gates the deploy.**
- **Run the post-deploy verification**; a deploy that reports success can still be broken.
- **Stay for a few minutes of monitoring** after it lands.
