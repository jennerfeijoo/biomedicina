#!/usr/bin/env python3
"""Audit whether advanced unit JSON is represented in public static pages.

Generated lessons must contain the advanced renderer marker and representative
source content. Explicitly registered authored lessons are preserved when they
meet independent structural and density checks. This distinction prevents a
manual page from being overwritten merely because its wording differs from the
advanced JSON while still blocking thin or unregistered exceptions.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = ROOT / "data" / "citonauta_curriculum.json"
ADVANCED_UNIT_ROOT = ROOT / "data" / "generated_units"
AUTHORED_OVERRIDES_PATH = ROOT / "data" / "authored_unit_overrides.json"
ADVANCED_MARKER = "<!-- advanced-unit-renderer:v1 -->"
GENERATED_MARKER = 'data-generated="citonauta-unit"'
GENERIC_PHRASES = (
    "tema de ",
    "que organiza entidades, relaciones o procedimientos propios de",
    "su significado operativo se fija indicando qué representa",
)
TAG_RE = re.compile(r"<[^>]+>")
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)


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


def authored_override_keys() -> tuple[set[tuple[str, int]], list[str]]:
    errors: list[str] = []
    if not AUTHORED_OVERRIDES_PATH.exists():
        return set(), ["falta data/authored_unit_overrides.json"]
    data = load_json(AUTHORED_OVERRIDES_PATH)
    if data.get("schema_version") != "1.0":
        errors.append("authored_unit_overrides.json debe usar schema_version 1.0")
    keys: set[tuple[str, int]] = set()
    for index, entry in enumerate(data.get("overrides", []), start=1):
        if not isinstance(entry, dict):
            errors.append(f"override {index}: debe ser un objeto")
            continue
        subject_id = str(entry.get("subject_id", "")).strip()
        rationale = str(entry.get("rationale", "")).strip()
        units = entry.get("units")
        if not subject_id:
            errors.append(f"override {index}: falta subject_id")
        if len(rationale) < 80:
            errors.append(f"override {index}: la justificación editorial es insuficiente")
        if not isinstance(units, list) or not units:
            errors.append(f"override {index}: units debe ser una lista no vacía")
            continue
        for raw_unit in units:
            try:
                unit_number = int(raw_unit)
            except (TypeError, ValueError):
                errors.append(f"override {index}: número de unidad inválido: {raw_unit}")
                continue
            key = (subject_id, unit_number)
            if key in keys:
                errors.append(f"override duplicado: {subject_id}/unidad-{unit_number:02d}")
            keys.add(key)
    return keys, errors


def expected_static_page(course_path: Path, unit_number: int) -> Path:
    return course_path.parent / "unidades" / f"unidad-{unit_number:02d}.html"


def representative_markers(unit: dict[str, Any]) -> list[str]:
    markers: list[str] = []
    for key in ("title", "purpose"):
        value = str(unit.get(key, "")).strip()
        if value:
            markers.append(value)
    for section in unit.get("theory_sections", []):
        if isinstance(section, dict):
            heading = str(section.get("heading") or section.get("title") or "").strip()
            if heading:
                markers.append(heading)
                break
    examples = unit.get("worked_examples") or unit.get("worked_example") or []
    if isinstance(examples, dict):
        examples = [examples]
    if isinstance(examples, list) and examples and isinstance(examples[0], dict):
        title = str(examples[0].get("title", "")).strip()
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


def visible_word_count(page: str) -> int:
    visible = html.unescape(TAG_RE.sub(" ", page))
    return len(WORD_RE.findall(visible))


def authored_quality_errors(page: str, unit: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    title = str(unit.get("title", "")).strip()
    if title and not marker_present(page, title):
        errors.append("el título no coincide con el JSON avanzado")
    section_count = page.casefold().count("<section")
    if section_count < 5:
        errors.append(f"solo contiene {section_count} secciones; se requieren al menos 5")
    words = visible_word_count(page)
    if words < 700:
        errors.append(f"solo contiene {words} palabras visibles; se requieren al menos 700")
    if "autoevaluación" not in page.casefold() and "autoevaluacion" not in page.casefold():
        errors.append("no contiene una sección de autoevaluación")
    if all(phrase in page.casefold() for phrase in GENERIC_PHRASES[1:]):
        errors.append("conserva el fallback conceptual genérico")
    return errors


def audit() -> dict[str, Any]:
    paths = course_paths()
    overrides, override_errors = authored_override_keys()
    missing_course_paths: list[str] = []
    missing_pages: list[str] = []
    generic_pages: list[str] = []
    unsynchronized_pages: list[str] = []
    malformed_units: list[str] = []
    authored_pages: list[str] = []
    authored_quality_failures: list[str] = []
    unregistered_authored_pages: list[str] = []
    advanced_units = 0
    seen_override_keys: set[tuple[str, int]] = set()

    if not ADVANCED_UNIT_ROOT.exists():
        return {
            "advanced_units": 0,
            "missing_course_paths": [],
            "missing_pages": [],
            "generic_pages": [],
            "unsynchronized_pages": [],
            "malformed_units": [],
            "authored_pages": [],
            "authored_quality_failures": [],
            "unregistered_authored_pages": [],
            "override_errors": override_errors,
            "unused_overrides": [],
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
        relative_page = static_path.relative_to(ROOT).as_posix()
        key = (subject_id, unit_number)
        is_generated = GENERATED_MARKER in page

        if is_generated:
            if key in overrides:
                override_errors.append(f"override innecesario para página generada: {relative_page}")
                seen_override_keys.add(key)
            if ADVANCED_MARKER not in page:
                unsynchronized_pages.append(relative_page)
            if all(phrase in page_folded for phrase in GENERIC_PHRASES[1:]):
                generic_pages.append(relative_page)
            markers = representative_markers(unit)
            if markers and not any(marker_present(page, marker) for marker in markers):
                unsynchronized_pages.append(relative_page)
        else:
            if key not in overrides:
                unregistered_authored_pages.append(relative_page)
                continue
            seen_override_keys.add(key)
            authored_pages.append(relative_page)
            quality_errors = authored_quality_errors(page, unit)
            authored_quality_failures.extend(
                f"{relative_page}: {error}" for error in quality_errors
            )

    unused_overrides = [
        f"{subject_id}/unidad-{unit_number:02d}"
        for subject_id, unit_number in sorted(overrides - seen_override_keys)
    ]
    return {
        "advanced_units": advanced_units,
        "missing_course_paths": sorted(set(missing_course_paths)),
        "missing_pages": sorted(set(missing_pages)),
        "generic_pages": sorted(set(generic_pages)),
        "unsynchronized_pages": sorted(set(unsynchronized_pages)),
        "malformed_units": sorted(set(malformed_units)),
        "authored_pages": sorted(set(authored_pages)),
        "authored_quality_failures": sorted(set(authored_quality_failures)),
        "unregistered_authored_pages": sorted(set(unregistered_authored_pages)),
        "override_errors": sorted(set(override_errors)),
        "unused_overrides": unused_overrides,
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
        help="Devuelve error ante páginas ausentes, genéricas, desincronizadas o excepciones autorales inválidas.",
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
    print_section("Páginas generadas con fallback genérico", report["generic_pages"])
    print_section("Páginas generadas desincronizadas", report["unsynchronized_pages"])
    print_section("Unidades JSON malformadas", report["malformed_units"])
    print_section("Páginas autorales registradas", report["authored_pages"])
    print_section("Páginas autorales que no superan calidad", report["authored_quality_failures"])
    print_section("Páginas autorales no registradas", report["unregistered_authored_pages"])
    print_section("Errores del registro de overrides", report["override_errors"])
    print_section("Overrides sin página avanzada correspondiente", report["unused_overrides"])

    finding_keys = (
        "missing_course_paths",
        "missing_pages",
        "generic_pages",
        "unsynchronized_pages",
        "malformed_units",
        "authored_quality_failures",
        "unregistered_authored_pages",
        "override_errors",
        "unused_overrides",
    )
    findings = sum(len(report[key]) for key in finding_keys)
    print(f"\nHallazgos totales: {findings}")
    if args.strict and findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
