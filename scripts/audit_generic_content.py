#!/usr/bin/env python3
"""Detecta marcadores conocidos de contenido de plantilla en unidades públicas."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
UNITS_ROOT = ROOT / "data" / "generated_units"
KNOWN_MARKERS = (
    "Concepto de la unidad que debe definirse mediante entidades observables",
)


def audit(units_root: Path = UNITS_ROOT) -> dict[str, Any]:
    courses: dict[str, dict[str, Any]] = {}
    for path in sorted(units_root.glob("*/unit-*.json")):
        subject_id = path.parent.name
        record = courses.setdefault(
            subject_id,
            {"subject_id": subject_id, "units_scanned": 0, "affected_units": [], "matches": 0},
        )
        record["units_scanned"] += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        matches = sum(text.count(marker) for marker in KNOWN_MARKERS)
        if matches:
            record["matches"] += matches
            record["affected_units"].append(path.stem)

    template_detected = sorted(
        subject_id for subject_id, record in courses.items() if record["matches"]
    )
    screened = sorted(set(courses) - set(template_detected))
    affected_units = sum(len(courses[subject_id]["affected_units"]) for subject_id in template_detected)
    occurrences = sum(courses[subject_id]["matches"] for subject_id in template_detected)
    return {
        "schema_version": "1.0",
        "interpretation": (
            "screened_no_known_template_marker significa únicamente que no se detectó un "
            "marcador conocido; no equivale a validación científica."
        ),
        "summary": {
            "courses_scanned": len(courses),
            "template_detected_courses": len(template_detected),
            "screened_no_known_template_marker_courses": len(screened),
            "affected_units": affected_units,
            "marker_occurrences": occurrences,
        },
        "template_detected": template_detected,
        "screened_no_known_template_marker": screened,
        "evidence": [courses[subject_id] for subject_id in template_detected],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument(
        "--fail-on-detected",
        action="store_true",
        help="Falla si queda cualquier unidad con un marcador conocido.",
    )
    args = parser.parse_args()
    report = audit()
    if args.json_output:
        output = args.json_output if args.json_output.is_absolute() else ROOT / args.json_output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return int(args.fail_on_detected and bool(report["template_detected"]))


if __name__ == "__main__":
    raise SystemExit(main())
