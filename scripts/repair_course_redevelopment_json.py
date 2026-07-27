#!/usr/bin/env python3
"""Repair narrowly defined JSON syntax defects in redevelopment unit files.

The tool is intentionally conservative. It only:

1. normalizes single backslashes inside values assigned to ``latex`` so every
   LaTeX command survives JSON decoding as a literal backslash;
2. closes a final object immediately before an array terminator when that
   object starts with ``{`` and is missing its closing ``}``;
3. validates every unit with ``json.loads`` and rejects control characters in
   decoded LaTeX values before writing any file.

It does not reformat JSON or change academic prose.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REDEVELOPMENT_ROOT = ROOT / "data" / "course_redevelopment"
LATEX_VALUE_RE = re.compile(r'("latex"\s*:\s*")((?:[^"\\]|\\.)*)(")')
OBJECT_ARRAY_KEYS = {"common_errors", "biomedical_connections"}
FORBIDDEN_LATEX_CONTROLS = {"\b", "\f", "\n", "\r", "\t"}


def normalize_latex_payload(payload: str) -> str:
    """Double every single LaTeX backslash while preserving JSON pairs.

    A lexical pair ``\\\\`` already represents one literal backslash after JSON
    decoding and is kept unchanged. An escaped quote is also preserved. Any
    other single backslash is doubled, including sequences such as ``\\frac``,
    ``\\nabla`` and ``\\tau`` that JSON would otherwise decode as control
    escapes when their first letter happens to be ``f``, ``n`` or ``t``.
    """
    output: list[str] = []
    index = 0
    while index < len(payload):
        character = payload[index]
        if character != "\\":
            output.append(character)
            index += 1
            continue

        if index + 1 < len(payload) and payload[index + 1] in {"\\", '"'}:
            output.extend((payload[index], payload[index + 1]))
            index += 2
            continue

        output.extend(("\\", "\\"))
        index += 1

    return "".join(output)


def repair_latex_values(text: str) -> str:
    return LATEX_VALUE_RE.sub(
        lambda match: (
            match.group(1)
            + normalize_latex_payload(match.group(2))
            + match.group(3)
        ),
        text,
    )


def repair_truncated_final_objects(text: str) -> str:
    """Close a final one-line object immediately before ``]`` in known arrays."""
    lines = text.splitlines(keepends=True)
    active_key: str | None = None
    bracket_depth = 0

    for index, line in enumerate(lines):
        stripped = line.strip()
        key_match = re.match(r'^"([^"]+)"\s*:\s*\[$', stripped)
        if key_match and key_match.group(1) in OBJECT_ARRAY_KEYS:
            active_key = key_match.group(1)
            bracket_depth = 1
            continue

        if active_key is None:
            continue

        bracket_depth += stripped.count("[") - stripped.count("]")
        if bracket_depth <= 0:
            active_key = None
            bracket_depth = 0
            continue

        if not stripped.startswith("{"):
            continue
        if stripped.endswith("},") or stripped.endswith("}"):
            continue

        next_index = index + 1
        while next_index < len(lines) and not lines[next_index].strip():
            next_index += 1
        if next_index >= len(lines) or lines[next_index].strip() != "],":
            continue

        newline = "\n" if line.endswith("\n") else ""
        body = line[:-1] if newline else line
        lines[index] = body + "}" + newline

    return "".join(lines)


def repair_text(text: str) -> str:
    return repair_truncated_final_objects(repair_latex_values(text))


def iter_latex_values(value: Any, location: str = "root"):
    if isinstance(value, dict):
        for key, item in value.items():
            child_location = f"{location}.{key}"
            if key == "latex" and isinstance(item, str):
                yield child_location, item
            yield from iter_latex_values(item, child_location)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_latex_values(item, f"{location}[{index}]")


def validate_json(path: Path, text: str) -> None:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: {exc}") from exc

    for location, latex in iter_latex_values(data):
        controls = sorted({character for character in latex if character in FORBIDDEN_LATEX_CONTROLS})
        if controls:
            names = ", ".join(repr(character) for character in controls)
            raise ValueError(
                f"{path}: {location} contiene controles JSON incompatibles con LaTeX: {names}"
            )


def process(subject_id: str, write: bool) -> tuple[list[Path], list[str]]:
    units_dir = REDEVELOPMENT_ROOT / subject_id / "units"
    if not units_dir.exists():
        raise FileNotFoundError(f"No existe {units_dir}")

    changed: list[Path] = []
    errors: list[str] = []
    candidates: dict[Path, str] = {}

    for path in sorted(units_dir.glob("unit-*.json")):
        original = path.read_text(encoding="utf-8")
        repaired = repair_text(original)
        try:
            validate_json(path, repaired)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        candidates[path] = repaired
        if repaired != original:
            changed.append(path)

    if errors:
        return changed, errors

    if write:
        for path in changed:
            path.write_text(candidates[path], encoding="utf-8")

    return changed, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", default="biologia-desarrollo")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--require-clean", action="store_true")
    args = parser.parse_args()

    try:
        changed, errors = process(args.subject_id, args.write)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 2

    for path in changed:
        action = "repaired" if args.write else "would_repair"
        print(f"{action}: {path.relative_to(ROOT)}")

    if args.require_clean and changed:
        print(
            f"ERROR: {len(changed)} archivos requieren reparación",
            file=sys.stderr,
        )
        return 1

    unit_count = len(
        list((REDEVELOPMENT_ROOT / args.subject_id / "units").glob("unit-*.json"))
    )
    print(f"validated_units: {unit_count}")
    print(f"changed_units: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
