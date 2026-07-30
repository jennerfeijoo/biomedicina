#!/usr/bin/env python3
"""Build the canonical Bioinstrumentation Unit 2 authoral JSON deterministically."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "unit-02-source"
DEFAULT_OUTPUT = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-02.json"

EXPECTED_FILES = {
    "metadata.json",
    "theory-01.json",
    "theory-02.json",
    "theory-03.json",
    "theory-04.json",
    "theory-05.json",
    "theory-06.json",
    "conceptual-model.json",
    "glossary-01.json",
    "glossary-02.json",
    "examples.json",
    "activities.json",
    "common-errors.json",
    "self-assessment.json",
    "biomedical-connections.json",
    "executable-practices.json",
    "assessment-feedback.json",
    "sources.json",
    "review-and-traceability.json",
}


class BuildError(ValueError):
    """Raised when source fragments cannot produce one unambiguous unit."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BuildError(f"missing source fragment: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BuildError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BuildError(f"{path} must contain a JSON object")
    return value


def add_unique(target: dict[str, Any], payload: dict[str, Any], source: Path) -> None:
    overlap = sorted(set(target) & set(payload))
    if overlap:
        raise BuildError(f"duplicate top-level fields from {source.name}: {', '.join(overlap)}")
    target.update(payload)


def build_unit(source_dir: Path = DEFAULT_SOURCE) -> dict[str, Any]:
    if not source_dir.is_dir():
        raise BuildError(f"source directory is missing: {source_dir}")
    actual = {path.name for path in source_dir.glob("*.json")}
    if actual != EXPECTED_FILES:
        missing = sorted(EXPECTED_FILES - actual)
        extra = sorted(actual - EXPECTED_FILES)
        raise BuildError(f"source fragment inventory mismatch; missing={missing}, extra={extra}")

    unit = load_object(source_dir / "metadata.json")
    theory_sections: list[dict[str, Any]] = []
    for index in range(1, 7):
        fragment = load_object(source_dir / f"theory-{index:02d}.json")
        if set(fragment) != {"heading", "paragraphs", "key_points", "equations", "source_links"}:
            raise BuildError(f"theory-{index:02d}.json has an unexpected schema")
        theory_sections.append(fragment)
    unit["theory_sections"] = theory_sections

    add_unique(unit, load_object(source_dir / "conceptual-model.json"), source_dir / "conceptual-model.json")

    glossary: list[dict[str, Any]] = []
    for name in ("glossary-01.json", "glossary-02.json"):
        fragment = load_object(source_dir / name)
        if set(fragment) != {"glossary"} or not isinstance(fragment["glossary"], list):
            raise BuildError(f"{name} must contain one glossary list")
        glossary.extend(fragment["glossary"])
    unit["glossary"] = glossary

    for name in (
        "examples.json",
        "activities.json",
        "common-errors.json",
        "self-assessment.json",
        "biomedical-connections.json",
        "executable-practices.json",
        "assessment-feedback.json",
        "sources.json",
        "review-and-traceability.json",
    ):
        add_unique(unit, load_object(source_dir / name), source_dir / name)
    return unit


def canonical_bytes(unit: dict[str, Any]) -> bytes:
    return (json.dumps(unit, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    unit = build_unit(args.source_dir)
    expected = canonical_bytes(unit)
    if args.check:
        if not args.output.is_file():
            raise SystemExit(f"ERROR: canonical unit is missing: {args.output}")
        if args.output.read_bytes() != expected:
            raise SystemExit(f"ERROR: canonical unit is out of sync: {args.output}")
        print(f"OK canonical Bioinstrumentation U2: {args.output.relative_to(ROOT)}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(expected)
    print(f"Built {args.output.relative_to(ROOT)} ({len(expected)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
