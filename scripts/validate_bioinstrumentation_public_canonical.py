#!/usr/bin/env python3
"""Valida la capa pública canónica de diez unidades de Bioinstrumentación.

La migración pública no reescribe los borradores autorales históricos. Este
control comprueba que overlay, descriptor generado, unidades avanzadas y
manifiesto de migración representan la misma secuencia, y que el estado
editorial no atribuye revisiones o conformidades inexistentes.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "bioinstrumentacion.json"
GENERATED_COURSE = ROOT / "data" / "generated_courses" / "bioinstrumentacion.json"
GENERATED_UNITS = ROOT / "data" / "generated_units" / "bioinstrumentacion"
MIGRATION = ROOT / "data" / "course_migrations" / "bioinstrumentacion-public-canonical-v1.json"
LEGACY_UNITS = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units"

EXPECTED_TITLES = {
    1: "Mensurando, sistema de medición y cadena de trazabilidad",
    2: "Sensores, transductores y modelos estáticos y dinámicos",
    3: "Biopotenciales, electrodos e interfaz electrodo-tejido",
    4: "Acondicionamiento analógico, ruido y rechazo de interferencias",
    5: "Muestreo, conversión y adquisición digital",
    6: "Sensores mecánicos, térmicos, de flujo y ópticos",
    7: "Aislamiento, seguridad eléctrica y compatibilidad electromagnética",
    8: "Caracterización de desempeño, calibración e incertidumbre",
    9: "Verificación, validación, riesgo y aptitud para el uso",
    10: "Integración y expediente reproducible",
}
EXPECTED_ORIGINS = {
    1: "legacy_unit_1",
    2: "legacy_unit_2",
    3: "legacy_unit_3",
    4: "new",
    5: "legacy_unit_4",
    6: "legacy_unit_5",
    7: "legacy_unit_6",
    8: "new",
    9: "new",
    10: "new",
}
PROHIBITED_PUBLIC_DURATION_PATTERNS = (
    re.compile(r"\b\d+\s*(?:horas?|semanas?|meses?|semestres?)\b", re.IGNORECASE),
    re.compile(r"\bduración\s+(?:estimada|del curso|de la unidad)\b", re.IGNORECASE),
)


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def load_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"falta {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"JSON inválido en {path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} debe contener un objeto JSON")
    return data


def require_text(data: dict[str, Any], key: str, path: Path) -> str:
    value = str(data.get(key) or "").strip()
    if not value:
        fail(f"{path.relative_to(ROOT)}: falta texto en {key}")
    return value


def require_list(data: dict[str, Any], key: str, path: Path, minimum: int = 1) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or len(value) < minimum:
        fail(f"{path.relative_to(ROOT)}: {key} debe contener al menos {minimum} elementos")
    return value


def scan_public_duration(data: Any, path: Path) -> None:
    serialized = json.dumps(data, ensure_ascii=False)
    for pattern in PROHIBITED_PUBLIC_DURATION_PATTERNS:
        match = pattern.search(serialized)
        if match:
            fail(
                f"{path.relative_to(ROOT)} contiene una referencia pública de duración no permitida: "
                f"{match.group(0)!r}"
            )


def validate_overlay() -> dict[str, Any]:
    data = load_object(OVERLAY)
    if data.get("id") != "bioinstrumentacion":
        fail("el overlay usa un id de asignatura incorrecto")
    if data.get("area_id") != "ingenieria-biomedica":
        fail("el overlay usa un area_id incorrecto")
    if data.get("status") != "review":
        fail("Bioinstrumentación debe permanecer en estado review")
    for key in (
        "title",
        "description",
        "level",
        "biomedical_connection",
    ):
        require_text(data, key, OVERLAY)
    for key, minimum in (
        ("prerequisites", 4),
        ("course_competencies", 6),
        ("learning_objectives", 6),
        ("learning_outcomes", 6),
        ("modules", 10),
        ("assessment", 3),
    ):
        require_list(data, key, OVERLAY, minimum)

    units = require_list(data, "detailed_units", OVERLAY, 10)
    if len(units) != 10 or not all(isinstance(item, dict) for item in units):
        fail("el overlay debe declarar exactamente diez unidades como objetos")
    numbers = [int(item.get("unit", 0)) for item in units]
    if numbers != list(range(1, 11)):
        fail(f"secuencia inválida en overlay: {numbers}")
    for item in units:
        number = int(item["unit"])
        if str(item.get("title") or "").strip() != EXPECTED_TITLES[number]:
            fail(f"título incorrecto en overlay para unidad {number}")
        for key in ("description",):
            if not str(item.get(key) or "").strip():
                fail(f"overlay unidad {number}: falta {key}")
        for key in ("topics", "learning_outcomes", "biomedical_applications"):
            value = item.get(key)
            if not isinstance(value, list) or not value:
                fail(f"overlay unidad {number}: falta contenido en {key}")

    weights = []
    for component in data["assessment"]:
        if not isinstance(component, dict):
            fail("assessment contiene un elemento no estructurado")
        match = re.search(r"\d+(?:[.,]\d+)?", str(component.get("weight") or ""))
        if not match:
            fail("assessment contiene una ponderación inválida")
        weights.append(float(match.group(0).replace(",", ".")))
    if abs(sum(weights) - 100.0) > 1e-9:
        fail(f"las ponderaciones del overlay suman {sum(weights):g} %, no 100 %")
    scan_public_duration(data, OVERLAY)
    return data


def validate_generated_course() -> dict[str, Any]:
    data = load_object(GENERATED_COURSE)
    if str(data.get("schema_version")) != "2.0":
        fail("generated course debe usar schema_version 2.0")
    if data.get("subject_id") != "bioinstrumentacion":
        fail("generated course usa subject_id incorrecto")
    if data.get("status") != "review":
        fail("generated course debe permanecer en review")
    for key, minimum in (
        ("prerequisites", 4),
        ("course_competencies", 6),
        ("learning_outcomes", 6),
        ("assessment_plan", 3),
        ("study_method", 4),
    ):
        require_list(data, key, GENERATED_COURSE, minimum)
    sequence = require_list(data, "curriculum_sequence", GENERATED_COURSE, 10)
    if len(sequence) != 10 or not all(isinstance(item, dict) for item in sequence):
        fail("curriculum_sequence debe contener exactamente diez objetos")
    for expected_number, item in enumerate(sequence, start=1):
        if int(item.get("unit", 0)) != expected_number:
            fail("curriculum_sequence no es contigua")
        if str(item.get("title") or "").strip() != EXPECTED_TITLES[expected_number]:
            fail(f"generated course: título incorrecto en unidad {expected_number}")
    total = sum(float(item.get("weight_percent", 0)) for item in data["assessment_plan"])
    if abs(total - 100.0) > 1e-9:
        fail(f"assessment_plan suma {total:g} %, no 100 %")
    migration = data.get("migration")
    if not isinstance(migration, dict):
        fail("generated course no declara migration")
    if migration.get("public_layer") != "canonical_ten_unit_sequence":
        fail("generated course no declara la capa pública canónica")
    for key in ("human_review_executed", "disciplinary_review_complete"):
        if migration.get(key) is not False:
            fail(f"generated course declara indebidamente {key}")
    scan_public_duration(data, GENERATED_COURSE)
    return data


def validate_units() -> list[dict[str, Any]]:
    if not GENERATED_UNITS.is_dir():
        fail(f"falta {GENERATED_UNITS.relative_to(ROOT)}")
    paths = sorted(GENERATED_UNITS.glob("unit-*.json"))
    expected_names = [f"unit-{number:02d}.json" for number in range(1, 11)]
    actual_names = [path.name for path in paths]
    if actual_names != expected_names:
        fail(f"unidades generadas {actual_names}; se esperaba {expected_names}")

    units: list[dict[str, Any]] = []
    slugs: set[str] = set()
    for number, path in enumerate(paths, start=1):
        unit = load_object(path)
        if str(unit.get("schema_version")) != "2.0":
            fail(f"{path.relative_to(ROOT)}: schema_version debe ser 2.0")
        if unit.get("subject_id") != "bioinstrumentacion":
            fail(f"{path.relative_to(ROOT)}: subject_id incorrecto")
        if unit.get("area_id") != "ingenieria-biomedica":
            fail(f"{path.relative_to(ROOT)}: area_id incorrecto")
        if int(unit.get("unit", 0)) != number:
            fail(f"{path.relative_to(ROOT)}: número de unidad inconsistente")
        if unit.get("status") != "review":
            fail(f"{path.relative_to(ROOT)}: status debe ser review")
        if require_text(unit, "title", path) != EXPECTED_TITLES[number]:
            fail(f"{path.relative_to(ROOT)}: título canónico incorrecto")
        slug = require_text(unit, "slug", path)
        if slug in slugs:
            fail(f"slug duplicado: {slug}")
        slugs.add(slug)
        require_text(unit, "purpose", path)
        for key, minimum in (
            ("learning_objectives", 4),
            ("theory_sections", 3),
            ("worked_examples", 1),
            ("guided_activities", 1),
            ("common_errors", 3),
            ("self_assessment", 3),
            ("biomedical_connections", 2),
            ("sources", 2),
        ):
            require_list(unit, key, path, minimum)
        for section in unit["theory_sections"]:
            if not isinstance(section, dict):
                fail(f"{path.relative_to(ROOT)}: theory_sections contiene un elemento inválido")
            if not str(section.get("heading") or "").strip():
                fail(f"{path.relative_to(ROOT)}: sección sin heading")
            paragraphs = section.get("paragraphs")
            if not isinstance(paragraphs, list) or len(paragraphs) < 2:
                fail(f"{path.relative_to(ROOT)}: cada sección requiere al menos dos párrafos")
        for source in unit["sources"]:
            if not isinstance(source, dict):
                fail(f"{path.relative_to(ROOT)}: fuente no estructurada")
            for key in ("title", "organization", "url", "role", "verification_status"):
                if not str(source.get(key) or "").strip():
                    fail(f"{path.relative_to(ROOT)}: fuente sin {key}")
            if not str(source["url"]).startswith("https://"):
                fail(f"{path.relative_to(ROOT)}: fuente sin URL HTTPS")
        scan_public_duration(unit, path)
        units.append(unit)
    return units


def validate_migration(units: list[dict[str, Any]]) -> None:
    data = load_object(MIGRATION)
    if data.get("migration_id") != "bioinstrumentacion-public-canonical-v1":
        fail("migration_id público incorrecto")
    if data.get("status") != "implemented_public_layer":
        fail("la migración pública no está marcada como implementada")
    sequence = require_list(data, "canonical_public_sequence", MIGRATION, 10)
    if len(sequence) != 10 or not all(isinstance(item, dict) for item in sequence):
        fail("canonical_public_sequence debe contener exactamente diez unidades")
    for number, item in enumerate(sequence, start=1):
        if int(item.get("canonical_unit", 0)) != number:
            fail("canonical_public_sequence no es contigua")
        if item.get("origin") != EXPECTED_ORIGINS[number]:
            fail(f"origen incorrecto en manifiesto para unidad {number}")
        if str(item.get("title") or "").strip() != EXPECTED_TITLES[number]:
            fail(f"título incorrecto en manifiesto para unidad {number}")
        if str(item.get("slug") or "").strip() != units[number - 1]["slug"]:
            fail(f"slug inconsistente en manifiesto para unidad {number}")
    legacy_map = {
        int(item["canonical_unit"]): int(item["legacy_unit"])
        for item in sequence
        if "legacy_unit" in item
    }
    if legacy_map != {5: 4, 6: 5, 7: 6}:
        fail(f"crosswalk legacy incorrecto: {legacy_map}")

    state = data.get("publication_state")
    if not isinstance(state, dict) or state.get("educational_publication") != "review":
        fail("publication_state debe declarar publicación educativa review")
    false_claims = (
        "human_review_executed",
        "disciplinary_review_complete",
        "professional_approval_claimed",
        "clinical_validity_claimed",
        "safety_conformity_claimed",
        "emc_conformity_claimed",
        "regulatory_conformity_claimed",
        "accreditation_claimed",
    )
    for key in false_claims:
        if state.get(key) is not False:
            fail(f"publication_state declara indebidamente {key}")
    require_list(data, "acceptance_gates", MIGRATION, 8)
    require_list(data, "remaining_external_gates", MIGRATION, 3)


def validate_legacy_preservation() -> None:
    expected = [LEGACY_UNITS / f"unit-{number:02d}.json" for number in range(1, 7)]
    missing = [path.relative_to(ROOT).as_posix() for path in expected if not path.exists()]
    if missing:
        fail(f"faltan fuentes autorales legacy preservadas: {missing}")
    unexpected = [LEGACY_UNITS / f"unit-{number:02d}.json" for number in range(7, 11)]
    present = [path.relative_to(ROOT).as_posix() for path in unexpected if path.exists()]
    if present:
        fail(
            "la migración pública no debe crear una segunda secuencia autoral parcial en "
            f"course_redevelopment: {present}"
        )


def main() -> int:
    overlay = validate_overlay()
    generated = validate_generated_course()
    units = validate_units()
    validate_migration(units)
    validate_legacy_preservation()

    overlay_titles = [item["title"] for item in overlay["detailed_units"]]
    generated_titles = [item["title"] for item in generated["curriculum_sequence"]]
    unit_titles = [item["title"] for item in units]
    expected_titles = [EXPECTED_TITLES[number] for number in range(1, 11)]
    if not (overlay_titles == generated_titles == unit_titles == expected_titles):
        fail("los títulos no están sincronizados entre las tres capas públicas")

    print("OK: Bioinstrumentación dispone de una capa pública canónica de diez unidades")
    print("Estado editorial: review; revisión humana y disciplinar continúan pendientes")
    print("Fuentes autorales legacy 1–6 preservadas sin reescritura histórica")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
