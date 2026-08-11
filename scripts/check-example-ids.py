#!/usr/bin/env python3
"""Verify that every ID referenced in a spec folder resolves to a definition.

The spec's whole discipline is that IDs chain across documents — FR-3 in §2 has
AC-3.x in §8, EF-2 in §4 has an AC in §8.4, a ticket cites the FR it implements.
A reference with no definition is the failure Check 1 of the full-spec review
looks for, and it is easy to introduce while restructuring.

Run this after changing any §N structure, and against the shipped example after
editing it — that example exists to demonstrate the discipline, so a dangling
reference inside it teaches the opposite of the intended lesson.

    python3 scripts/check-example-ids.py examples/automation-template-export
    python3 scripts/check-example-ids.py path/to/some-feature   # a real spec too

Exit 0 when every reference resolves, 1 otherwise.
"""
from __future__ import annotations

import collections
import pathlib
import re
import sys

# Which document owns the definition of each ID prefix.
OWNER = {
    "MS": "0-market-research.md",
    "CMP": "0-market-research.md",
    "PER": "0-market-research.md",
    "OPP": "0-market-research.md",
    "FR": "2-requirements.md",
    "NFR": "2-requirements.md",
    "BR": "3-domain-model.md",
    "SF": "4-flows.md",
    "EF": "4-flows.md",
    "EC": "4-flows.md",
    "UF": "5-presentation-spec.md",
    "C": "5-presentation-spec.md",
    "P": "5-presentation-spec.md",
}

# §5.7's T-N is **page-local** — every page starts again at T-1, so there is no
# global T-3 to resolve. Owning it here only appeared to work because the
# template's bullet layout (`- **T-1 …**`) reads as a definition; write the same
# page in a table and every T-N dangles against a document that is perfectly fine.
REF = re.compile(r"\b(MS|CMP|PER|OPP|FR|NFR|BR|SF|EF|EC|UF|C|P)-(\d+)\b|\b(D)-(\d{4})\b")

# `AC-N.M` is dotted, so it needs its own pattern — and it needs one, because a
# ticket's cited ACs are its entire verification surface. Left out, a ticket could
# cite `AC-99.9` and the checker would call the spec clean.
AC_OWNER = "8-acceptance.md"
# §8.2 numbers state ACs `AC-S.N`, so the segment is alphanumeric, not just digits.
AC_REF = re.compile(r"\bAC-([A-Z0-9]+\.\d+)\b")
AC_DEF = re.compile(r"^[#|*\-> ]*\**AC-([A-Z0-9]+\.\d+)\b")

# An ID is defined where it opens a heading, a table row, or a bold label —
# the conventions the templates use.
DEF_AT_LINE_START = r"^[#|*\-> ]*\**{pfx}-0*{num}\b"

# A retired ID is declared, not defined: the number stays reserved so it is
# never reused, and references to the declaration are legitimate.
RETIRED_HINT = re.compile(r"保留不重用|retired|not reused", re.I)

# A fenced block is example text, not the document speaking. Reading it let a line
# inside a ```block``` stand in as a definition — §4 could cite `UF-3` that exists
# nowhere but a display-format example, and every reference still "resolved".
FENCE = re.compile(r"^\s*(?:```|~~~)")


def unfenced(text: str):
    """The document's own lines, with fenced blocks dropped."""
    fenced = False
    for line in text.split("\n"):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            yield line

# Prose that explains the notation cites IDs illustratively — 「後面的文件會引用
# 前面的 ID（如 FR-3、SF-1）」 names no real FR-3. Treat such a line as notation,
# not as a reference; a false positive here trains the reader to ignore the check.
ILLUSTRATIVE = re.compile(r"(?:如|例如|例:|e\.g\.|such as|for example)", re.I)

# Chains the spec's own review requires, expressed as "every X defined here must
# be picked up over there". Existence alone is not enough: a component is not
# orphaned because it appears in its own definition line, and an FR is not
# covered because it appears in §2. These are the Check 2 / Check 3 items that a
# reader will otherwise assert as passing without doing the cross-referencing.
CHAINS = [
    ("FR", "8-acceptance.md", None, "every FR needs an AC (Check 2)"),
    ("NFR", "8-acceptance.md", None, "every NFR needs an AC (Check 2)"),
    ("BR", "8-acceptance.md", None, "every BR needs an AC or a reference (Check 2)"),
    ("EF", "8-acceptance.md", None, "every error flow needs an AC (Check 2)"),
    ("EC", "8-acceptance.md", None, "every edge case needs an AC (Check 2)"),
    # C-N is defined in §5.6, so its own definition line must not count as usage —
    # the target is the rest of §5, wherever a component legitimately gets picked
    # up: a page (§5.7), a journey stage (§5.4), an interaction decision (§5.8).
    ("C", "5-presentation-spec.md", "!5.6", "every component must be used somewhere (Check 3)"),
]

# Templates abbreviate a run of IDs as a range — `EC-1 ~ EC-7`, `AC-1.1 – AC-1.3`.
# Reading only the endpoints makes the middle look absent, so expand them.
RANGE = re.compile(r"\b([A-Z]{1,3})-(\d+)\s*(?:~|～|–|—|-{1,2}|to)\s*(?:[A-Z]{1,3}-)?(\d+)\b")


def collect(root: pathlib.Path) -> tuple[dict[str, str], set[str]]:
    files: dict[str, str] = {}
    for p in sorted(root.glob("*.md")):
        files[p.name] = p.read_text(encoding="utf-8")
    for sub in ("issues", "decisions"):
        for p in sorted((root / sub).glob("*.md")):
            files[f"{sub}/{p.name}"] = p.read_text(encoding="utf-8")
    adrs = {
        f"D-{p.name[:4]}"
        for p in (root / "decisions").glob("[0-9][0-9][0-9][0-9]-*.md")
    }
    return files, adrs


def is_definition_line(line: str, prefix: str, num: str) -> bool:
    if prefix == "AC":
        return bool(AC_DEF.match(line))
    return bool(re.match(DEF_AT_LINE_START.format(pfx=prefix, num=num), line))


def references(text: str, exclude_definitions: bool = False) -> set[str]:
    """IDs this text cites.

    `exclude_definitions` drops the ID's own defining line — `### UF-2: 匯出模板`
    cites nothing, it declares. Counting it as a citation is what made the orphan
    pass unfireable: every defined ID appeared in `referenced` by construction, so
    `defined - referenced` was empty no matter how orphaned the ID really was.
    """
    out = set()
    for line in unfenced(text):
        if ILLUSTRATIVE.search(line):
            continue
        if exclude_definitions:
            defines = AC_DEF.match(line) or any(
                m.group(1) and is_definition_line(line, m.group(1), m.group(2))
                for m in REF.finditer(line)
            )
            if defines:
                continue
        for m in REF.finditer(line):
            if m.group(1):
                out.add(f"{m.group(1)}-{int(m.group(2))}")
            else:
                out.add(f"D-{m.group(4)}")
        for m in AC_REF.finditer(line):
            out.add(f"AC-{m.group(1)}")
        for m in RANGE.finditer(line):
            prefix, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
            if prefix in OWNER and lo < hi <= lo + 50:
                out.update(f"{prefix}-{n}" for n in range(lo, hi + 1))
    return out


def definitions(files: dict[str, str], adrs: set[str]) -> tuple[set[str], set[str]]:
    defined = set(adrs)
    mentioned_as_retired = set()
    for prefix, owner in OWNER.items():
        text = files.get(owner)
        if not text:
            continue
        for line in unfenced(text):
            for m in re.finditer(rf"\b{prefix}-(\d+)\b", line):
                ident = f"{prefix}-{int(m.group(1))}"
                if is_definition_line(line, prefix, m.group(1)):
                    defined.add(ident)
                elif RETIRED_HINT.search(line):
                    mentioned_as_retired.add(ident)

    for line in unfenced(files.get(AC_OWNER, "")):
        m = AC_DEF.match(line)
        if m:
            defined.add(f"AC-{m.group(1)}")

    # A retirement note names two IDs — the one withdrawn and the one it merged
    # into: 「P-4 已於設計過程中併入 P-3，編號保留不重用」. Only P-4 is retired.
    # Sweeping both in excused the live one from every coverage chain, silently,
    # for as long as the note existed. An ID with a definition line is alive.
    retired = mentioned_as_retired - defined
    return defined, retired


def section(text: str, number: str) -> str:
    """The slice of a document belonging to one §N.M section, by its heading."""
    lines = text.split("\n")
    start = next(
        (i for i, l in enumerate(lines) if re.match(rf"^#+ +§?{re.escape(number)}\b", l)),
        None,
    )
    if start is None:
        return ""
    depth = len(lines[start]) - len(lines[start].lstrip("#"))
    end = next(
        (
            j
            for j in range(start + 1, len(lines))
            if lines[j].startswith("#" * depth + " ")
        ),
        len(lines),
    )
    return "\n".join(lines[start:end])


def chain_gaps(files: dict[str, str], defined: set[str], retired: set[str]) -> list[str]:
    """IDs that exist but are never picked up where the review says they must be."""
    gaps = []
    for prefix, target_file, target_section, why in CHAINS:
        owner = OWNER.get(prefix)
        if owner not in files or target_file not in files:
            continue  # a skipped document is not a gap
        target = files[target_file]
        if target_section and target_section.startswith("!"):
            excluded = section(target, target_section[1:])
            target = target.replace(excluded, "") if excluded else target
        elif target_section:
            target = section(target, target_section)
            if not target:
                continue
        picked_up = {i for i in references(target) if i.startswith(prefix + "-")}
        mine = {
            i
            for i in defined
            if i.startswith(prefix + "-") and i not in retired
        }
        missing = sorted(mine - picked_up, key=lambda s: int(s.split("-")[1]))
        if missing:
            if not target_section:
                where = target_file
            elif target_section.startswith("!"):
                where = f"{target_file} outside §{target_section[1:]}"
            else:
                where = f"§{target_section} of {target_file}"
            gaps.append(f"{', '.join(missing)} — absent from {where}: {why}")
    return gaps


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    root = pathlib.Path(sys.argv[1])
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    files, adrs = collect(root)
    if not files:
        print(f"no markdown found under {root}", file=sys.stderr)
        return 2

    defined, retired = definitions(files, adrs)
    referenced: dict[str, set[str]] = collections.defaultdict(set)
    cited: set[str] = set()
    for name, text in files.items():
        for ident in references(text):
            referenced[ident].add(name)
        cited |= references(text, exclude_definitions=True)

    dangling = {
        i: s for i, s in referenced.items() if i not in defined and i not in retired
    }
    # Two prefixes are terminal by design. `CMP-N` is research context shaping §0.6,
    # not something later documents cite. `AC-*` is the end of every chain — the
    # coverage that matters (FR/NFR/BR/EF/EC → AC) is already enforced above, from
    # the other direction, and an AC no ticket happens to cite is normal.
    orphans = sorted(
        i for i in defined - cited - adrs
        if not i.startswith(("CMP-", "AC-"))
    )

    lines = sum(len(t.splitlines()) for t in files.values())
    print(f"{root}: {len(files)} files, {lines} lines, {len(adrs)} ADRs")
    print(f"  defined {len(defined)}  referenced {len(referenced)}  retired {len(retired)}")

    if orphans:
        print(f"  ⚠ defined but never referenced ({len(orphans)}): {', '.join(orphans)}")

    failed = False

    if dangling:
        failed = True
        print(f"  ✗ dangling references: {len(dangling)}")
        for ident, srcs in sorted(dangling.items()):
            print(f"      {ident:<10} cited by {', '.join(sorted(srcs))}")

    gaps = chain_gaps(files, defined, retired)
    if gaps:
        failed = True
        print(f"  ✗ coverage gaps: {len(gaps)}")
        for g in gaps:
            print(f"      {g}")

    if failed:
        return 1

    print("  ✓ every referenced ID resolves, and every chain the review requires is complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
