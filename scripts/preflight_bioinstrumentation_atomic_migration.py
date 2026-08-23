#!/usr/bin/env python3
"""Control determinista de la migración de Bioinstrumentación.

El repositorio conserva dos capas distintas de la migración 6→10:

1. el preflight histórico, anterior a ejecutar la migración pública; y
2. el estado posterior, en el que la secuencia pública de diez unidades y el
   corpus académico canónico ya existen, mientras las seis fuentes autorales
   históricas permanecen inmutables como procedencia.

Este script acepta ambos estados y aplica controles diferentes en cada uno. No
modifica contenido ni convierte la existencia de un corpus canónico en revisión
humana, conformidad o autorización de publicación profesional.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "course_migrations" / "bioinstrumentacion-numbering-v1.json"
PUBLIC_MANIFEST = ROOT / "data" / "course_migrations" / "bioinstrumentacion-public-canonical-v1.json"
UNITS = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units"
CANONICAL_COURSE = ROOT / "data" / "courses" / "bioinstrumentacion" / "course.json"
PLAN = ROOT / "docs" / "audits" / "bioinstrumentacion" / "ATOMIC_MIGRATION_PLAN.md"

PRE_EXECUTION_STATES = {"planned_not_executed", "ready_for_execution"}
POST_BOOTSTRAP_STATE = "canonical_academic_bootstrap_executed"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def load_json(path: Path, label: str) -> dict:
    if not path.exists():
        fail(f"falta {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"{label} debe ser un objeto JSON")
    return data


def load_manifest() -> dict:
    return load_json(MANIFEST, "el manifiesto")


def validate_shared_manifest_contract(data: dict) -> None:
    if data.get("migration_id") != "bioinstrumentacion-numbering-v1":
        fail("migration_id inesperado")

    sequence = data.get("canonical_sequence")
    if not isinstance(sequence, list) or len(sequence) != 10:
        fail("canonical_sequence debe contener exactamente diez unidades")

    numbers = [item.get("canonical_unit") for item in sequence if isinstance(item, dict)]
    if numbers != list(range(1, 11)):
        fail(f"secuencia canónica inválida: {numbers}")

    expected_origins = {
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
    for item in sequence:
        number = item["canonical_unit"]
        if item.get("origin") != expected_origins[number]:
            fail(f"origen incorrecto para unidad {number}")

    findings = {item.get("id") for item in data.get("critical_findings", []) if isinstance(item, dict)}
    for required in {"BN-01", "BN-02", "BN-03", "BN-04"}:
        if required not in findings:
            fail(f"falta hallazgo crítico {required}")

    gates = data.get("atomic_migration_gates")
    if not isinstance(gates, list) or len(gates) < 8:
        fail("faltan gates de migración atómica")

    if data.get("publication_authorized") is not False:
        fail("la publicación profesional no debe declararse autorizada")
    if data.get("disciplinary_review_complete") is not False:
        fail("no puede declararse revisión disciplinar completa")


def validate_legacy_sources_preserved() -> None:
    expected = [UNITS / f"unit-{number:02d}.json" for number in range(1, 7)]
    missing = [path.relative_to(ROOT).as_posix() for path in expected if not path.exists()]
    if missing:
        fail(f"faltan unidades autorales históricas: {missing}")

    # Las posiciones 7–10 no deben crearse dentro del árbol histórico para
    # aparentar que la numeración legacy siempre fue la canónica actual.
    premature = [UNITS / f"unit-{number:02d}.json" for number in range(7, 11)]
    existing = [path.relative_to(ROOT).as_posix() for path in premature if path.exists()]
    if existing:
        fail(f"se reescribió indebidamente la historia autoral: {existing}")


def validate_pre_execution_state(data: dict) -> None:
    if not PLAN.exists():
        fail(f"falta {PLAN.relative_to(ROOT)}")
    plan = PLAN.read_text(encoding="utf-8")
    for token in (
        "atomic_migration_plan: completed",
        "migration_executed: false",
        "next_action: implement_migration_in_single_integrated_pr",
    ):
        if token not in plan:
            fail(f"el plan no contiene el estado requerido: {token}")

    validate_legacy_sources_preserved()


def validate_post_bootstrap_state(data: dict) -> None:
    validate_legacy_sources_preserved()

    public_manifest = load_json(PUBLIC_MANIFEST, "el manifiesto público")
    if public_manifest.get("status") != "implemented_public_layer":
        fail("la capa pública de diez unidades no consta como implementada")
    public_sequence = public_manifest.get("canonical_public_sequence")
    if not isinstance(public_sequence, list) or [item.get("canonical_unit") for item in public_sequence] != list(range(1, 11)):
        fail("la secuencia pública canónica no contiene las diez unidades esperadas")

    bootstrap = data.get("canonical_academic_bootstrap")
    if not isinstance(bootstrap, dict):
        fail("falta canonical_academic_bootstrap")
    if bootstrap.get("course_code") != "BIOINST" or bootstrap.get("unit_count") != 10:
        fail("metadatos del bootstrap académico incompatibles")
    if bootstrap.get("historical_authoral_sources_preserved") is not True:
        fail("el bootstrap debe declarar preservación de fuentes autorales históricas")
    if bootstrap.get("legacy_numbering_rewritten") is not False:
        fail("el bootstrap no puede declarar reescritura de la numeración histórica")
    if bootstrap.get("human_review_executed") is not False:
        fail("el bootstrap no puede inventar revisión humana")
    if bootstrap.get("disciplinary_review_complete") is not False:
        fail("el bootstrap no puede inventar revisión disciplinar")

    course = load_json(CANONICAL_COURSE, "el curso canónico")
    if course.get("code") != "BIOINST":
        fail("código inesperado en el curso canónico")
    unit_files = course.get("unit_files")
    if not isinstance(unit_files, list) or unit_files != [f"units/unit-{number:02d}.json" for number in range(1, 11)]:
        fail("el curso canónico no declara las diez unidades en orden")

    status = course.get("status") or {}
    if status.get("internal_review") != "pending" or status.get("external_review") != "pending":
        fail("el corpus canónico debe conservar la revisión humana como pendiente")
    if status.get("publication") != "published_provisional":
        fail("la publicación canónica debe seguir siendo provisional")


def main() -> int:
    manifest = load_manifest()
    validate_shared_manifest_contract(manifest)
    state = manifest.get("status")

    if state in PRE_EXECUTION_STATES:
        validate_pre_execution_state(manifest)
        print("OK: preflight de migración atómica de Bioinstrumentación superado")
        print("Estado: seis fuentes autorales legacy preservadas; bootstrap académico aún no registrado")
        return 0

    if state == POST_BOOTSTRAP_STATE:
        validate_post_bootstrap_state(manifest)
        print("OK: migración de Bioinstrumentación validada en estado post-bootstrap")
        print("Estado: diez unidades canónicas; seis fuentes autorales históricas preservadas; revisión humana pendiente")
        return 0

    fail(f"estado de migración no reconocido: {state}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
