#!/usr/bin/env python3
"""Audit whether advanced unit JSON is represented in public static unit pages.

The course pages can enhance unit cards in the browser from ``data/generated_units``.
Dedicated unit pages are generated through a different path. This audit exposes cases
where an advanced JSON unit exists but its public HTML page still contains only the
generic fallback representation.

The command is informational by default. Use ``--strict`` after the static renderer has
been migrated to the advanced unit schema.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = ROOT / "data" / "citonauta_curriculum.json"
ADVANCED_UNIT_ROOT = ROOT / "data" / "generated_units"
GENERIC_PHRASES = (
    "tema de ",
    "que organiza entidades, relaciones o procedimientos propios de",
    "su significado operativo se fija indicando qué representa",
)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)}: la raíz JSON debe ser un objeto")
    return data


def course_paths() -> dict[str, Path]:
    curriculum = load_json(CURRICULUM_PATH)
    result: dict[str, Path] = {}
    for area in curriculum.get("areas", []):
        for subject in area.get("subjects", []):
            subject_id = str(subject.get("id", "")).strip()
            public_path = str(subject.get("path", "")).strip()
            if subject_id and public_path:
                result[subject_id] = ROOT / public_path
    return result


def expected_static_page(course_path: Path, unit_number: int) -> Path:
    return course_path.parent / "unidades" / f"unidad-{unit_number:02d}.html"


def representative_markers(unit: dict[str, Any]) -> list[str]:
    markers: list[str] = []
    purpose = str(unit.get("purpose", "")).strip()
    if purpose:
        markers.append(purpose)

    for section in unit.get("theory_sections", []):
        if not isinstance(section, dict):
            continue
        heading = str(section.get("heading", "")).strip()
        if heading:
            markers.append(heading)
            break

    examples = unit.get("worked_examples", [])
    if isinstance(examples, list) and examples:
        first = examples[0]
        if isinstance(first, dict):
            title = str(first.get("title", "")).strip()
            if title:
                markers.append(title)

    return markers


def marker_present(page: str, marker: str) -> bool:
    candidates = {
        marker.casefold(),
        html.escape(marker, quote=True).casefold(),
        html.escape(marker, quote=False).casefold(),
    }
    page_folded = page.casefold()
    return any(candidate and candidate in page_folded for candidate in candidates)


def audit() -> dict[str, Any]:
    paths = course_paths()
    missing_course_paths: list[str] = []
    missing_pages: list[str] = []
    generic_pages: list[str] = []
    unsynchronized_pages: list[str] = []
    malformed_units: list[str] = []
    advanced_units = 0

    if not ADVANCED_UNIT_ROOT.exists():
        return {
            "advanced_units": 0,
            "missing_course_paths": [],
            "missing_pages": [],
            "generic_pages": [],
            "unsynchronized_pages": [],
            "malformed_units": [],
        }

    for unit_path in sorted(ADVANCED_UNIT_ROOT.glob("*/unit-*.json")):
        advanced_units += 1
        subject_id = unit_path.parent.name
        relative_unit = unit_path.relative_to(ROOT).as_posix()
        try:
            unit = load_json(unit_path)
            unit_number = int(unit.get("unit", 0))
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            malformed_units.append(f"{relative_unit}: {error}")
            continue

        course_path = paths.get(subject_id)
        if course_path is None:
            missing_course_paths.append(subject_id)
            continue

        static_path = expected_static_page(course_path, unit_number)
        if not static_path.exists():
            missing_pages.append(static_path.relative_to(ROOT).as_posix())
            continue

        page = static_path.read_text(encoding="utf-8", errors="replace")
        page_folded = page.casefold()
        has_generic_fallback = all(phrase in page_folded for phrase in GENERIC_PHRASES[1:])
        if has_generic_fallback:
            generic_pages.append(static_path.relative_to(ROOT).as_posix())

        markers = representative_markers(unit)
        if markers and not any(marker_present(page, marker) for marker in markers):
            unsynchronized_pages.append(static_path.relative_to(ROOT).as_posix())

    return {
        "advanced_units": advanced_units,
        "missing_course_paths": sorted(set(missing_course_paths)),
        "missing_pages": sorted(set(missing_pages)),
        "generic_pages": sorted(set(generic_pages)),
        "unsynchronized_pages": sorted(set(unsynchronized_pages)),
        "malformed_units": sorted(set(malformed_units)),
    }


def print_section(title: str, entries: list[str]) -> None:
    print(f"\n{title}: {len(entries)}")
    for entry in entries:
        print(f"- {entry}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audita la alineación entre unidades JSON avanzadas y páginas HTML públicas."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Devuelve error cuando existen páginas ausentes, genéricas o desincronizadas.",
    )
    parser.add_argument("--json-output", help="Ruta opcional para guardar el informe JSON.")
    args = parser.parse_args()

    report = audit()
    if args.json_output:
        output = ROOT / args.json_output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("AUDITORÍA DE ALINEACIÓN DE UNIDADES PÚBLICAS")
    print(f"Unidades JSON avanzadas: {report['advanced_units']}")
    print_section("Asignaturas sin ruta curricular", report["missing_course_paths"])
    print_section("Páginas de unidad ausentes", report["missing_pages"])
    print_section("Páginas que conservan fallback genérico", report["generic_pages"])
    print_section("Páginas sin marcadores del contenido avanzado", report["unsynchronized_pages"])
    print_section("Unidades JSON malformadas", report["malformed_units"])

    findings = sum(
        len(report[key])
        for key in (
            "missing_course_paths",
            "missing_pages",
            "generic_pages",
            "unsynchronized_pages",
            "malformed_units",
        )
    )
    print(f"\nHallazgos totales: {findings}")
    if args.strict and findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
