#!/usr/bin/env python3
"""
Scaffold a Claude Code project structure from a config JSON.

Usage:
    python scaffold.py --config config.json [--target .] [--dry-run]

The config JSON should have the shape shown in the example below.
Example config (single language):
    {
        "project_name": "orderflow",
        "project_description": "Internal order management API",
        "stack": "Python 3.12 + FastAPI + PostgreSQL",
        "languages": ["python"],
        "test_frameworks": ["pytest"],
        "entry_point": "src/orderflow/main.py",
        "install_cmd": "uv sync",
        "test_cmd": "pytest",
        "lint_cmd": "ruff check .",
        "dev_cmd": "uvicorn src.orderflow.main:app --reload",
        "deploy_target": "Fly.io",
        "agents": ["planner", "tester", "implementer", "reviewer", "researcher"],
        "gitignore_plans": true
    }

Example config (multi-language: Node backend + Python ML):
    {
        "project_name": "myapp",
        "project_description": "Node API with Python ML service",
        "stack": "Node.js + Express + Python + FastAPI",
        "languages": ["typescript", "python"],
        "test_frameworks": ["jest", "pytest"],
        "entry_point": "src/index.ts",
        "install_cmd": "npm install && uv sync",
        "test_cmd": "npm test && pytest",
        "lint_cmd": "eslint . && ruff check .",
        "dev_cmd": "npm run dev"
    }

All fields are required except:
    - deploy_target (optional; omit to skip the deploy skill)
    - build_cmd / deploy_cmd (only read by the deploy skill; each renders as a
      TODO line when omitted, so ask for both whenever deploy_target is set)
    - agents (defaults to all five; the four pipeline roles ship together)
    - gitignore_plans (defaults to true)

Backward compat: "language" (string) and "test_framework" (string) still work,
and are automatically converted to single-element lists.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

# Map language -> code-style template filename.
LANG_TEMPLATES = {
    "python": "code-style-python.md",
    "typescript": "code-style-typescript.md",
    "javascript": "code-style-typescript.md",  # close enough
    "go": "code-style-go.md",
}

# Map test framework -> testing template filename.
TEST_TEMPLATES = {
    "pytest": "testing-pytest.md",
    "jest": "testing-jest.md",
    "vitest": "testing-jest.md",
    "mocha": "testing-jest.md",
}

DEFAULT_AGENTS = ["planner", "tester", "implementer", "reviewer", "researcher"]

# The four that hand off to each other. CLAUDE.md, `grilling`, `plan-schema.md`
# and `testing-tdd.md` all name them by role and route work between them, so a
# config that installs three of the four writes a repo whose own instructions
# dispatch an agent that isn't there. `researcher` stands alone and is optional.
PIPELINE_AGENTS = ["planner", "tester", "implementer", "reviewer"]

GITIGNORE_CLAUDE_BLOCK = """\
# Claude Code personal overrides
CLAUDE.local.md
.claude/settings.local.json
"""

GITIGNORE_PLANS_BLOCK = """\
# Working documents from agent pipeline
PLAN.md
FIX_PLAN.md
"""


def log(msg: str, level: str = "info") -> None:
    """Simple colored logger."""
    prefix = {
        "info": "  ",
        "ok": "✓ ",
        "warn": "⚠ ",
        "err": "✗ ",
        "step": "▸ ",
    }.get(level, "  ")
    print(f"{prefix}{msg}", file=sys.stderr)


def load_config(path: Path) -> dict:
    """Load and lightly validate the config JSON."""
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with path.open() as f:
        cfg = json.load(f)

    # Backward compat: "language"/"test_framework" (strings) → lists.
    if "language" in cfg and "languages" not in cfg:
        cfg["languages"] = [cfg.pop("language")]
    if "test_framework" in cfg and "test_frameworks" not in cfg:
        cfg["test_frameworks"] = [cfg.pop("test_framework")]

    required = [
        "project_name", "project_description", "stack", "languages",
        "test_frameworks", "entry_point",
        "install_cmd", "test_cmd", "lint_cmd", "dev_cmd",
    ]
    missing = [k for k in required if k not in cfg or not cfg[k]]
    if missing:
        raise ValueError(f"Config missing required fields: {missing}")

    # Normalise to lowercase lists.
    cfg["languages"] = [l.lower() for l in cfg["languages"]]
    cfg["test_frameworks"] = [f.lower() for f in cfg["test_frameworks"]]

    cfg.setdefault("agents", DEFAULT_AGENTS)
    cfg.setdefault("gitignore_plans", True)
    cfg.setdefault("deploy_target", None)

    # Validate agent names.
    unknown = set(cfg["agents"]) - set(DEFAULT_AGENTS)
    if unknown:
        raise ValueError(f"Unknown agent names: {unknown}. "
                         f"Valid: {DEFAULT_AGENTS}")

    # The pipeline ships whole or not at all.
    chosen = set(cfg["agents"])
    partial = chosen & set(PIPELINE_AGENTS)
    if partial and partial != set(PIPELINE_AGENTS):
        missing = [a for a in PIPELINE_AGENTS if a not in chosen]
        raise ValueError(
            f"The pipeline agents ship together: missing {missing}. "
            f"CLAUDE.md and the shipped rules route work through all four "
            f"({', '.join(PIPELINE_AGENTS)}), so installing a subset writes a repo "
            f"that dispatches agents it does not have. Take all four, or drop to "
            f"['researcher'] alone."
        )

    return cfg


def build_replacements(cfg: dict) -> dict:
    """Build the {{PLACEHOLDER}} -> value mapping."""
    deploy_target = cfg.get("deploy_target")
    languages = cfg["languages"]
    primary_lang = languages[0]  # 用第一個語言決定 indent 等風格

    return {
        "PROJECT_NAME": cfg["project_name"],
        "PROJECT_DESCRIPTION": cfg["project_description"],
        "STACK": cfg["stack"],
        "TEST_FRAMEWORK": ", ".join(cfg["test_frameworks"]),
        "ENTRY_POINT": cfg["entry_point"],
        "INSTALL_CMD": cfg["install_cmd"],
        "TEST_CMD": cfg["test_cmd"],
        "LINT_CMD": cfg["lint_cmd"],
        "DEV_CMD": cfg["dev_cmd"],
        "LANGUAGE": ", ".join(languages),
        "DEPLOY_TARGET": deploy_target or "",
        # Defaulting build to install put `npm install` under a "Build:" heading in
        # every deploy-enabled repo. A TODO is read as a gap; a wrong command isn't.
        "BUILD_CMD": cfg.get("build_cmd", "# TODO: fill in build command"),
        "DEPLOY_CMD": cfg.get("deploy_cmd", "# TODO: fill in deploy command"),
        # Only stated where the agents it routes through are actually installed.
        "PIPELINE_LINE": (
            "**The pipeline**, for non-trivial work: **`grilling`** until the decision "
            "tree is settled → `planner` → human approves → then **`tester` and "
            "`implementer` alternate one vertical slice at a time** (one failing test → "
            "make it green → next slice) → review the whole diff by **dispatching "
            "`reviewer` twice in parallel, once with `axis: Standards` and once with "
            "`axis: Spec`**, and present both reports one after the other under their own "
            "`## Standards` / `## Spec` headings, each keeping its own verdict. Trivial "
            "changes skip the pipeline. Reconciling the two axes is the human's call, "
            "not a combined verdict."
            if set(PIPELINE_AGENTS) <= set(cfg["agents"])
            else "**Skills:** see `.claude/skills/` — each says when it applies."
        ),
        "TEST_ONE_CMD": f"{cfg['test_cmd']} <path>",
        "COVERAGE_CMD": (
            f"{cfg['test_cmd']} --cov"
            if "pytest" in cfg["test_cmd"]
            else f"{cfg['test_cmd']} -- --coverage"
        ),
        "FUNCTION_NAMING": "see existing code",
        "TYPE_NAMING": "see existing code",
        "CONSTANT_NAMING": "see existing code",
        "FILE_NAMING": "see existing code",
        "FORMATTER": "see existing code",
        "LINE_LENGTH": "100",
        "INDENT": "4 spaces" if primary_lang == "python" else "2 spaces",
    }


def substitute(text: str, replacements: dict) -> str:
    """Replace all {{KEY}} markers with values from replacements dict."""
    def repl(match: re.Match) -> str:
        key = match.group(1)
        return replacements.get(key, match.group(0))  # keep unknown as-is
    return re.sub(r"\{\{(\w+)\}\}", repl, text)


def find_unreplaced_placeholders(text: str) -> list[str]:
    """Return any {{FOO}} markers still present."""
    return re.findall(r"\{\{(\w+)\}\}", text)


def check_replacements_reach_a_template(replacements: dict, templates_dir: Path) -> None:
    """Every computed replacement has a `{{KEY}}` waiting for it somewhere.

    The reverse direction — a `{{KEY}}` with no value — already surfaces as an
    unreplaced placeholder in the output. This direction is silent: a value
    computed for nobody writes nothing and reports nothing, so `entry_point`
    stayed a required config field for as long as it took someone to grep.
    A required field the interview asks for and the scaffold discards is worse
    than a missing one — the user answered it.
    """
    used: set[str] = set()
    for p in templates_dir.rglob("*"):
        if p.is_file():
            used |= set(re.findall(r"\{\{(\w+)\}\}", p.read_text(encoding="utf-8", errors="ignore")))
    orphans = sorted(set(replacements) - used)
    if orphans:
        raise ValueError(
            f"Replacements no template uses: {orphans}. "
            f"Put a {{{{KEY}}}} where each belongs, or stop computing it — "
            f"and where it came from a required config field, stop asking for it too."
        )


RETIRED_DIRS = ("in-progress", "deprecated")


def check_skill_lifecycle(skills_dir: Path, shipped: list[str], known: list[str]) -> None:
    """Skill templates live in one of three states, and the folder is which.

    Top level ships. `in-progress/` is drafted but not ready; `deprecated/` is
    retired and kept for reference. Neither subfolder ever reaches a target repo,
    so a name in both places is a contradiction rather than a preference — this
    raises instead of guessing which one was meant.
    """
    for state in RETIRED_DIRS:
        d = skills_dir / state
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            if f.stem in shipped:
                raise ValueError(
                    f"'{f.stem}' is in skills/{state}/ but the scaffold still ships it. "
                    f"Move it out of {state}/, or take it off the shipped list."
                )

    orphans = sorted(
        f.stem for f in skills_dir.glob("*.md") if f.stem not in known
    )
    if orphans:
        raise ValueError(
            "Skill templates nothing ships: " + ", ".join(orphans) + ". "
            "Add each to the shipped list, or move it to skills/in-progress/."
        )


def copy_template(
    src: Path, dst: Path, replacements: dict, dry_run: bool,
) -> list[str]:
    """Copy a template with substitution. Returns any unreplaced placeholders."""
    if not src.exists():
        raise FileNotFoundError(f"Template not found: {src}")

    text = src.read_text(encoding="utf-8")
    text = substitute(text, replacements)
    leftover = find_unreplaced_placeholders(text)

    if dry_run:
        log(f"[DRY-RUN] Would write {dst}", "info")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
        log(f"Wrote {dst}", "ok")

    return leftover


def update_gitignore(
    target: Path, include_plans: bool, dry_run: bool,
) -> None:
    """Append Claude-related entries to .gitignore without duplicating."""
    gitignore = target / ".gitignore"
    existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""

    # Per entry, not per block. A repo that already ignores CLAUDE.local.md on its
    # own would otherwise skip the whole block and never ignore settings.local.json.
    #
    # Compare against *rule lines*, not `existing.split()`. Splitting on whitespace
    # turns every word of every comment into a token, so a repo whose .gitignore says
    # `# CLAUDE.local.md stays local` was read as already ignoring it — the file then
    # shipped un-ignored while the run reported it ignored.
    already = {
        l.strip() for l in existing.splitlines()
        if l.strip() and not l.lstrip().startswith("#")
    }

    def missing(block: str) -> str:
        wanted = [
            l for l in block.splitlines()
            if l.strip() and not l.startswith("#") and l.strip() not in already
        ]
        if not wanted:
            return ""
        header = next((l for l in block.splitlines() if l.startswith("#")), "")
        return "\n".join(([header] if header else []) + wanted) + "\n"

    lines_to_add = [b for b in (missing(GITIGNORE_CLAUDE_BLOCK),) if b]

    if include_plans:
        plans = missing(GITIGNORE_PLANS_BLOCK)
        if plans:
            lines_to_add.append(plans)

    if not lines_to_add:
        log(".gitignore already up to date", "info")
        return

    new_content = existing
    if existing and not existing.endswith("\n"):
        new_content += "\n"
    if existing:
        new_content += "\n"
    new_content += "\n".join(lines_to_add)

    if dry_run:
        log(f"[DRY-RUN] Would update {gitignore}", "info")
    else:
        gitignore.write_text(new_content, encoding="utf-8")
        log(f"Updated {gitignore}", "ok")


def check_existing_files(target: Path) -> list[Path]:
    """Return list of paths we're about to write that already exist.

    Only flags paths that THIS script produces — not other things that may
    live under .claude/ (e.g., settings.local.json, which Claude Code itself
    creates and which is unrelated to our scaffolding).
    """
    candidates = [
        target / "CLAUDE.md",
        target / "CLAUDE.local.md",
        target / ".claude" / "agents",
        target / ".claude" / "rules",
        target / ".claude" / "skills",
        target / ".claude" / "references",
    ]
    return [p for p in candidates if p.exists()]


def scaffold(
    skill_dir: Path, target: Path, cfg: dict, dry_run: bool = False,
    force: bool = False,
) -> None:
    """Main scaffolding logic."""
    log(f"Scaffolding {cfg['project_name']} at {target}", "step")

    # 1. Safety check.
    existing = check_existing_files(target)
    if existing and not force:
        log("Existing Claude files detected:", "warn")
        for p in existing:
            log(f"  - {p.relative_to(target)}", "warn")
        log("Pass --force to overwrite, or delete them first.", "err")
        raise SystemExit(2)

    templates_dir = skill_dir / "assets" / "templates"
    if not templates_dir.is_dir():
        raise FileNotFoundError(f"Templates directory missing: {templates_dir}")

    replacements = build_replacements(cfg)
    check_replacements_reach_a_template(replacements, templates_dir)
    all_leftover: dict[Path, list[str]] = {}

    # 2. Copy core files.
    jobs: list[tuple[Path, Path]] = [
        (templates_dir / "CLAUDE.md", target / "CLAUDE.md"),
        (templates_dir / "CLAUDE.local.md", target / "CLAUDE.local.md"),
        (templates_dir / "rules" / "api-conventions.md",
         target / ".claude" / "rules" / "api-conventions.md"),
        (templates_dir / "rules" / "codebase-design.md",
         target / ".claude" / "rules" / "codebase-design.md"),
    ]

    # 3. Language-specific code-style — one file per language.
    for lang in cfg["languages"]:
        style_template = LANG_TEMPLATES.get(lang, "code-style-generic.md")
        # Single language → code-style.md, multi → code-style-python.md etc.
        if len(cfg["languages"]) == 1:
            dst_name = "code-style.md"
        else:
            dst_name = f"code-style-{lang}.md"
        jobs.append((
            templates_dir / "rules" / style_template,
            target / ".claude" / "rules" / dst_name,
        ))

    # 4. Framework-specific testing rules — one file per framework.
    for framework in cfg["test_frameworks"]:
        test_template = TEST_TEMPLATES.get(framework, "testing-generic.md")
        if len(cfg["test_frameworks"]) == 1:
            dst_name = "testing.md"
        else:
            dst_name = f"testing-{framework}.md"
        jobs.append((
            templates_dir / "rules" / test_template,
            target / ".claude" / "rules" / dst_name,
        ))

    # 5. Bundled skills — always-on set, then the conditional ones.
    ALWAYS_SKILLS = [
        "grilling",
        "security-review",
        "diagnosing-bugs",
        "improve-codebase-architecture",
        "domain-glossary",
        "prototype",
        "handoff",
        "resolving-merge-conflicts",
    ]
    CONDITIONAL_SKILLS = ["deploy"]  # ships only when its config key is set
    shipped = list(ALWAYS_SKILLS)
    if cfg.get("deploy_target"):
        shipped.append("deploy")
    check_skill_lifecycle(
        templates_dir / "skills", shipped, ALWAYS_SKILLS + CONDITIONAL_SKILLS,
    )
    for skill_name in shipped:
        jobs.append((
            templates_dir / "skills" / f"{skill_name}.md",
            target / ".claude" / "skills" / skill_name / "SKILL.md",
        ))

    # 6. Agents.
    for agent_name in cfg["agents"]:
        jobs.append((
            templates_dir / "agents" / f"{agent_name}.md",
            target / ".claude" / "agents" / f"{agent_name}.md",
        ))

    # 7. References — shared docs that agents read at runtime.
    # Only copy files that agents actually need during work (not human-facing docs).
    AGENT_REFERENCES = ["plan-schema.md", "testing-tdd.md", "review-lenses.md"]
    references_dir = skill_dir / "references"
    # Not `if it exists` — the shipped rules and three of the five agents name these
    # files by path. Skipping a missing one writes a repo whose own instructions point
    # at nothing, and reports success while doing it.
    missing_refs = [
        n for n in AGENT_REFERENCES if not (references_dir / n).exists()
    ]
    if not references_dir.is_dir() or missing_refs:
        raise FileNotFoundError(
            f"Agent references missing: {missing_refs or [str(references_dir)]}. "
            f"The skill's own files are incomplete — reinstall rather than scaffold "
            f"a repo that points at documents it does not have."
        )
    for ref_name in AGENT_REFERENCES:
        jobs.append((
            references_dir / ref_name,
            target / ".claude" / "references" / ref_name,
        ))

    # 7. Execute jobs.
    for src, dst in jobs:
        leftover = copy_template(src, dst, replacements, dry_run)
        if leftover:
            all_leftover[dst] = leftover

    # 8. .gitignore update.
    update_gitignore(target, cfg["gitignore_plans"], dry_run)

    # 9. Final validation.
    if all_leftover:
        log("", "info")
        log("VALIDATION FAILED — unreplaced placeholders found:", "err")
        for path, markers in all_leftover.items():
            log(f"  {path}: {set(markers)}", "err")
        log("", "info")
        log("The files were still written, but you should review and fix these.", "warn")
        raise SystemExit(1)

    # 10. Name what an earlier run left behind.
    #
    # `--force` overwrites; it never deletes. Re-scaffolding a Rust project over an
    # earlier Python + Go + TypeScript one leaves those style rules sitting beside a
    # CLAUDE.md that no longer mentions them, and re-scaffolding without the pipeline
    # leaves all five agent files next to a CLAUDE.md saying there is no pipeline.
    # Deleting is not this script's call — a repo's `.claude/` also holds work the
    # user put there. Naming it is.
    if not dry_run:
        wrote = {dst.resolve() for _, dst in jobs}
        stale = sorted(
            p for d in ("rules", "skills", "agents", "references")
            for p in (target / ".claude" / d).rglob("*.md")
            if p.resolve() not in wrote
        )
        if stale:
            log("", "info")
            log(f"{len(stale)} file(s) here are from an earlier run, not this one:", "warn")
            for p in stale:
                log(f"  {p.relative_to(target)}", "warn")
            log("This config did not ask for them. Delete what no longer applies.", "warn")

    log("", "info")
    log(f"Scaffolding complete. Files written under: {target}", "ok")
    if not dry_run:
        log("Next: review CLAUDE.md (especially the Project overview section).", "info")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a Claude Code project structure.",
    )
    parser.add_argument(
        "--config", type=Path, required=True,
        help="Path to config JSON file.",
    )
    parser.add_argument(
        "--target", type=Path, default=Path("."),
        help="Target directory (default: current).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print actions without writing files.",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Overwrite existing Claude files without asking.",
    )
    args = parser.parse_args()

    # The script expects to live at <skill>/scripts/scaffold.py
    skill_dir = Path(__file__).resolve().parent.parent

    cfg = load_config(args.config)
    scaffold(skill_dir, args.target.resolve(), cfg, args.dry_run, args.force)


if __name__ == "__main__":
    main()
