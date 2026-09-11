#!/usr/bin/env python3
"""Static checks for a hand-authored .tldr file, before you try to open it in tldraw.

The PNG renderer is NOT an import test. It runs tldraw v3 and builds the document via
`editor.createShapes`, which never validates index keys and recomputes note font scaling
itself. A file can render perfectly and still be rejected by tldraw.com — silently, as an
empty document with no error message.

This script catches the failures that are decidable without a browser. It is a gate, not a
guarantee: the authoritative test is opening the file in the target app (see SKILL.md,
"Validate against the target").

Usage:  uv run python validate_tldr.py <file.tldr> [more.tldr ...]
Findings are split in two: ERRORS make tldraw reject the file outright, HINTS are things
that import fine but look wrong once open.

Exit code 0 = no errors, 1 = errors, 2 = file unreadable. Hints never change the exit code.
"""

import json
import pathlib
import sys

# tldraw's fractional index alphabet (see the `fractional-indexing` package).
B62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# Length of the integer part, keyed by its leading character. Only the 'a'..'z' /
# 'A'..'Z' heads matter for hand-authored files; 'a' means "one digit follows".
INTEGER_LENGTHS = {c: i + 2 for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")}
INTEGER_LENGTHS.update({c: 27 - i for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")})

SHAPES_WITH_RICHTEXT = {"geo", "text", "note", "arrow"}


def index_problem(key):
    """Return a reason string if `key` is not a valid tldraw index key, else None."""
    if not isinstance(key, str) or not key:
        return "not a non-empty string"
    head = key[0]
    if head not in INTEGER_LENGTHS:
        return f"leading character {head!r} is not a valid integer-part head"
    int_len = INTEGER_LENGTHS[head]
    if len(key) < int_len:
        return f"integer part needs {int_len} characters, got {len(key)}"
    body = key[1:]
    if any(c not in B62 for c in body):
        return "contains characters outside the base62 alphabet"
    fraction = key[int_len:]
    # tldraw rejects a fractional part with a trailing zero — it is not a canonical key.
    # This is what turns a plain counter ("a1".."a41") into an invalid file at "a10".
    if fraction.endswith("0"):
        return "fractional part must not end in '0' (a plain counter produces a10, a20, ...)"
    return None


def check(path):
    findings = []   # hard errors: tldraw refuses the file
    hints = []      # imports fine, but probably not what you meant

    try:
        doc = json.loads(pathlib.Path(path).read_text())
    except Exception as exc:
        return None, [f"file could not be parsed: {exc}"], []

    records = doc.get("records")
    if not isinstance(records, list):
        return None, ["no 'records' array at the top level"], []

    shapes = [r for r in records if r.get("typeName") == "shape"]
    bindings = [r for r in records if r.get("typeName") == "binding"]
    shape_ids = {r.get("id") for r in shapes}
    page_ids = {r.get("id") for r in records if r.get("typeName") == "page"}

    if sum(1 for r in records if r.get("typeName") == "document") != 1:
        findings.append("there must be exactly one 'document' record")
    if not page_ids:
        findings.append("no 'page' record")

    # --- index keys: valid, and unique per parent ---------------------------------
    seen = {}
    for s in shapes:
        key, parent = s.get("index"), s.get("parentId")
        problem = index_problem(key)
        if problem:
            findings.append(f"{s.get('id')}: invalid index {key!r} — {problem}")
        if (parent, key) in seen:
            findings.append(
                f"{s.get('id')}: index {key!r} already used by {seen[(parent, key)]} "
                f"under the same parent {parent!r}"
            )
        seen[(parent, key)] = s.get("id")

    # --- parents must exist --------------------------------------------------------
    frame_ids = {s.get("id") for s in shapes if s.get("type") == "frame"}
    for s in shapes:
        parent = s.get("parentId")
        if parent not in page_ids and parent not in frame_ids:
            findings.append(f"{s.get('id')}: parentId {parent!r} is neither a page nor a frame")

    # --- bindings must point at real shapes ----------------------------------------
    for b in bindings:
        for field in ("fromId", "toId"):
            if b.get(field) not in shape_ids:
                findings.append(f"{b.get('id')}: {field} {b.get(field)!r} is not an existing shape")

    for s in shapes:
        sid, stype, props = s.get("id"), s.get("type"), s.get("props") or {}

        # --- note font scaling ------------------------------------------------------
        # fontSizeAdjustment is a SCALE FACTOR, not a pixel size. tldraw computes it in
        # onBeforeCreate; loading a finished snapshot skips that, so a stored 0 renders
        # the text at zero size — the note shows up blank with its text still in the file.
        if stype == "note" and props.get("fontSizeAdjustment") in (0, None):
            findings.append(
                f"{sid}: note has fontSizeAdjustment {props.get('fontSizeAdjustment')!r} — "
                "use 1; 0 renders the label invisible"
            )

        # --- text shapes need an explicit width -------------------------------------
        # Only a hint: tldraw itself writes autoSize:true and computes w/h when the shape is
        # created interactively, so genuine exports are full of it. It bites hand-authored
        # files, where nothing recomputes the size and the text ends up clipped to one line.
        if stype == "text" and props.get("autoSize") is True:
            hints.append(
                f"{sid}: text with autoSize:true — fine in a tldraw export, but in a "
                "hand-authored file nothing recomputes w/h and the text gets clipped to one "
                "line; prefer autoSize:false with an explicit w"
            )

        # --- arrow kind --------------------------------------------------------------
        if stype == "arrow" and props.get("kind") not in ("elbow", "arc"):
            findings.append(
                f"{sid}: arrow kind {props.get('kind')!r} — only 'elbow' and 'arc' exist"
            )

        # --- rich text shape ----------------------------------------------------------
        if stype in SHAPES_WITH_RICHTEXT and "richText" in props:
            rt = props["richText"]
            if not isinstance(rt, dict) or rt.get("type") != "doc" or "content" not in rt:
                findings.append(f"{sid}: richText is not a ProseMirror doc with 'content'")

    return len(shapes), findings, hints


def main(argv):
    paths = argv[1:]
    if not paths:
        print(__doc__)
        return 2

    worst = 0
    for path in paths:
        count, findings, hints = check(path)
        name = pathlib.Path(path).name
        if count is None:
            print(f"{name}: UNREADABLE")
            worst = max(worst, 2)
        elif findings:
            print(f"{name}: {len(findings)} error(s) across {count} shapes")
            worst = max(worst, 1)
        else:
            print(f"{name}: ok — {count} shapes, no errors")
        for f in findings:
            print(f"  ERROR  {f}")
        for h in hints:
            print(f"  hint   {h}")
        if findings:
            print("  Fix the errors, then still open the file in the target app before shipping it.")
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
