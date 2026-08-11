#!/usr/bin/env python3
"""Verify that a written document's numbered sections match its template's.

A document grows sections. Asked for §7, an agent writes 7.1 and 7.2 from the
template and then keeps going — 7.3 Architecture Decision Records with two ADR
bodies inline, 7.4 Constraints restating §1.6, 7.7 Risk Register invented whole.
Every other check passes: an ADR that was never given an ID has no reference to
dangle, and a duplicated section carries no marker.

The template is the spine. This compares the two by **section number** — titles
drift legitimately (`5.2 User Stories` for `5.2 User Stories / Consumer
Stories`), and unnumbered headings are the document's own content (`### SF-1:`,
`### POST /api/templates/import`, `### Active Decisions`), not spine.

    python3 scripts/check-sections.py path/to/some-feature/7-decisions.md
    python3 scripts/check-sections.py path/to/some-feature     # every §N in it
    python3 scripts/check-sections.py examples/automation-template-export

Three ways to fail, all of them hard:

- a numbered section the template does not have
- a non-optional template section the document dropped — one that genuinely does
  not apply keeps its heading and says why beneath it, as the shipped example does
  for §6.3
- two headings at one number — `## 7.1 Decision Index` and `## 7.1 Details` in the
  same file, which reusing an existing number let slip past an earlier version

Optional means the template marked it 選填, plus §5.4–5.9 where §5.1 selected
something other than GUI.

Exit 0 when every document's sections match its template's, 1 otherwise.
"""
from __future__ import annotations

import pathlib
import re
import sys

HEADING = re.compile(r"^(#{1,6})\s+§?(\d+(?:\.\d+)+)(?=[\s:.、（(]|$)")

# ``` or ~~~, with or without a language tag, and tolerating indentation.
FENCE = re.compile(r"^\s*(?:```|~~~)")

# A template section the author may legitimately leave out. The templates declare
# this one way: `（選填）` in the heading, or a note **opening** with 選填.
#
# Match it anywhere in the note instead and ordinary prose starts silencing whole
# subtrees — §1.3's note says 「若有做 §0 market research」 about its *content*, and
# a loose pattern reads that as permission to skip §1.3 entirely. The failure mode
# is silence, so the pattern has to be anchored.
OPTIONAL_HEADING = re.compile(r"[（(](?:選填|optional)[）)]", re.I)
OPTIONAL_NOTE = re.compile(r"^>?\s*(?:選填|Optional)\b|^>?\s*選填[。，：:]")

DOC = re.compile(r"^(\d+)-")

# Two sections are marked 選填 with a condition attached — 「FR + NFR 合計 > 10 條」.
# The optional regexes read only the 選填 half, so the condition was unenforceable and
# a 20-FR spec could drop both summary views and exit 0. This counts the gate.
#
# Every other conditional section (§1.5.1 POC, §3.5 events, §6.6 versioning, §9.3.3
# tracing) turns on a judgment no script can make, so those keep their heading and
# say 「不適用 + 原因」 instead of being droppable — the convention SKILL.md already sets.
GATED_ON_ITEM_COUNT = {"2.4", "8.6"}
ITEM_COUNT_GATE = 10
ITEM_DEF = re.compile(r"^[#|*\-> ]*\**((?:FR|NFR)-\d+)\b")


def item_count(folder: pathlib.Path) -> int | None:
    """FR + NFR defined in this spec, or None when §2 is not on disk to count.

    None means the gate cannot be evaluated — checking a single file rather than the
    folder. The closing bar runs `check-sections.py .`, so the folder is the norm.
    """
    reqs = folder / "2-requirements.md"
    if not reqs.is_file():
        return None
    found = set()
    fenced = False
    for line in reqs.read_text(encoding="utf-8").split("\n"):
        if FENCE.match(line):
            fenced = not fenced
            continue
        m = ITEM_DEF.match(line)
        if m and not fenced:
            found.add(m.group(1))
    return len(found)


# §5.4–5.9 describe a graphical interface. Where §5.1 selected something else,
# they are not omissions — full-spec-review skips them for the same reason.
GUI_ONLY = {"5.4", "5.5", "5.6", "5.7", "5.8", "5.9"}
# `\s` crosses newlines, so a blank value let this run on and capture the next
# heading as the selected type. Horizontal whitespace only.
SELECTED_TYPE = re.compile(r"\*\*Selected type\*\*[ \t]*[:：][ \t]*(.*)")


def spine(text: str, doc: str) -> tuple[list[str], dict[str, str], dict[str, str], list[tuple[str, str]]]:
    """Numbered headings belonging to this document, in order, with title and note.

    A heading numbered for another document — `## §5.8 的補充` inside §7 — is a
    cross-reference in heading clothing, not a section of this document.

    The note is the blockquote directly under a heading, where a template says
    things like 「選填」 or 「不是每個分類都需要填」 about the section it opens.
    """
    order: list[str] = []
    titles: dict[str, str] = {}
    notes: dict[str, str] = {}
    dupes: list[tuple[str, str]] = []
    lines = text.split("\n")
    fenced = False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            fenced = not fenced
            continue
        # A heading inside a fence is an example of markdown, not a section. Counting
        # them let a §8 whose five required headings existed only inside a ```markdown
        # block — with no acceptance criteria anywhere — pass on exit 0.
        if fenced:
            continue
        m = HEADING.match(line)
        if not m or m.group(2).split(".")[0] != doc:
            continue
        number = m.group(2)
        if number in titles:
            # Keying by number alone let a document invent a section as long as it
            # reused a number the template already has — `## 7.1 Decision Index` and
            # `## 7.1 Details` in one file both resolved to §7.1.
            dupes.append((number, line[m.end():].strip()))
            continue
        order.append(number)
        titles[number] = line[m.end():].strip()
        note = []
        for nxt in lines[i + 1:]:
            if not nxt.strip():
                if note:
                    break
                continue
            if not nxt.startswith(">"):
                break
            note.append(nxt)
        notes[number] = "\n".join(note)
    return order, titles, notes, dupes


# A `{...}` slot the template ships for the author to replace. Surviving into a
# written document, it is the loudest possible sign the section was never filled —
# and the quietest to every other check: an `8-acceptance.md` that was a byte-for-byte
# copy of its template, twelve literal `...` bodies and not one real criterion,
# satisfied every FR / BR / EF / EC / NFR → AC chain and exited 0, because the
# template ships those chains' own `### FR-1:` headings prefilled.
PLACEHOLDER = re.compile(r"\{[^{}\n]{1,60}\}")

# `{由運維補：…}` is the one slot instructed to survive — §9.5 runbooks ship as a
# skeleton whose escalation steps need real operational knowledge, and leaving the
# gap visible beats inventing it. 9-rollout.guide.md says so explicitly.
PLACEHOLDER_BY_DESIGN = re.compile(r"由運維補|由維運補")

# `{N}` inside `已有 {N} 個未指派` is a runtime interpolation slot in UI copy, not an
# unfilled field. Code spans and fences are where that copy lives, so read neither.
CODE_SPAN = re.compile(r"`[^`\n]*`")


def unfilled(text: str, template_text: str) -> list[tuple[int, str]]:
    """Placeholders this document inherited from its template and never replaced."""
    slots = set(PLACEHOLDER.findall(template_text))
    if not slots:
        return []
    out = []
    fenced = False
    for i, line in enumerate(text.split("\n"), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        for m in PLACEHOLDER.finditer(CODE_SPAN.sub("", line)):
            tok = m.group(0)
            if tok in slots and not PLACEHOLDER_BY_DESIGN.search(tok):
                out.append((i, tok))
    return out


def template_for(path: pathlib.Path, templates: pathlib.Path) -> pathlib.Path | None:
    m = DOC.match(path.name)
    if not m:
        return None
    found = sorted(templates.glob(f"{m.group(1)}-*.template.md"))
    return found[0] if found else None


def check(path: pathlib.Path, templates: pathlib.Path) -> tuple[bool, list[str]]:
    """(invented_anything, report lines) for one document."""
    tpl = template_for(path, templates)
    if tpl is None:
        return False, []
    doc = DOC.match(path.name).group(1)

    want_order, want_titles, want_notes, _ = spine(tpl.read_text(encoding="utf-8"), doc)

    text = path.read_text(encoding="utf-8")
    # §5.4–5.9 are exempt only on an *affirmative* non-GUI selection. Missing, blank,
    # or still the template's `{勾選}` placeholder all mean the author has not chosen —
    # and the template ships that placeholder, so a §5 that never edited line 23 would
    # otherwise have its whole frontend half exempted silently, on exit 0.
    gui = True
    if doc == "5":
        m = SELECTED_TYPE.search(text)
        if m:
            selected = m.group(1).strip()
            resolved = selected and "{" not in selected and "}" not in selected
            gui = not resolved or "GUI" in selected.upper()
    got_order, got_titles, _, got_dupes = spine(text, doc)
    want, got = set(want_order), set(got_order)

    def optional(number: str) -> bool:
        """A section the template says may be left out, inherited down the tree.

        A parent marked 選填 makes its subsections optional too — skipping §9.2
        skips everything under it.
        """
        if not gui and number in GUI_ONLY:
            return True
        if number in GATED_ON_ITEM_COUNT:
            n = item_count(path.parent)
            if n is not None and n > ITEM_COUNT_GATE:
                return False
        parts = number.split(".")
        return any(
            OPTIONAL_HEADING.search(want_titles.get(anc, ""))
            or OPTIONAL_NOTE.search(want_notes.get(anc, ""))
            for anc in (".".join(parts[:i]) for i in range(1, len(parts) + 1))
        )

    out = [f"{path.name}: {len(got)} numbered sections, template has {len(want)}"]
    extra = sorted(got - want, key=version)
    missing = [n for n in want_order if n not in got and not optional(n)]

    # Both directions fail. Warning-only on omission let the two worst real cases
    # through: dropping §6.5.1/.2 severs the error-code source of truth, and
    # flattening §8.1–§8.5 broke 38 coverage chains. Both exited 0 under the old split.
    for n in missing:
        out.append(
            f"  ✗ §{n} {want_titles[n]} — in the template, missing here. "
            f"Put the heading back and write why it does not apply"
        )
    for n in extra:
        out.append(
            f"  ✗ §{n} {got_titles[n]} — not in {tpl.name}. Give it an unnumbered "
            f"heading under the section that owns it"
        )
    for n, title in got_dupes:
        out.append(
            f"  ✗ §{n} {title} — §{n} already has a heading. One number, one section"
        )
    left = unfilled(text, tpl.read_text(encoding="utf-8"))
    for line_no, tok in left[:8]:
        out.append(f"  ✗ line {line_no}: {tok} — still the template's placeholder")
    if len(left) > 8:
        out.append(f"  ✗ … and {len(left) - 8} more placeholders never filled in")
    if not extra and not missing and not got_dupes and not left:
        out.append("  ✓ matches the template")
    return bool(extra or missing or got_dupes or left), out


def version(number: str) -> tuple[int, ...]:
    return tuple(int(p) for p in number.split("."))


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    root = pathlib.Path(sys.argv[1])
    templates = pathlib.Path(
        sys.argv[2] if len(sys.argv) > 2
        else pathlib.Path(__file__).resolve().parent.parent / "templates"
    )
    if not templates.is_dir():
        print(f"no templates directory: {templates}", file=sys.stderr)
        return 2

    if root.is_file():
        targets = [root]
    elif root.is_dir():
        targets = sorted(
            p for p in root.glob("*.md") if template_for(p, templates) is not None
        )
    else:
        print(f"not found: {root}", file=sys.stderr)
        return 2

    if not targets:
        print(f"no numbered documents under {root}", file=sys.stderr)
        return 2

    failed = False
    for p in targets:
        drifted, lines = check(p, templates)
        failed |= drifted
        print("\n".join(lines))

    print()
    if failed:
        print("✗ sections differ from the template. Each line above names its fix.")
        return 1
    print(f"✓ {len(targets)} document(s) match their template")
    return 0


if __name__ == "__main__":
    sys.exit(main())
