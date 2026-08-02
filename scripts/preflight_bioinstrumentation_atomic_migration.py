#!/usr/bin/env python3
"""Preflight determinista para la migración atómica de Bioinstrumentación.

Este control no modifica contenido. Verifica que el repositorio siga en el estado
legacy esperado antes de iniciar la migración 6→10 y que el manifiesto contenga
las decisiones mínimas de identidad, preservación y rollback.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "course_migrations" / "bioinstrumentacion-numbering-v1.json"
UNITS = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units"
PLAN = ROOT / "docs" / "audits" / "bioinstrumentacion" / "ATOMIC_MIGRATION_PLAN.md"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def load_manifest() -> dict:
    if not MANIFEST.exists():
        fail(f"falta {MANIFEST.relative_to(ROOT)}")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("el manifiesto debe ser un objeto JSON")
    return data


def validate_manifest(data: dict) -> None:
    if data.get("migration_id") != "bioinstrumentacion-numbering-v1":
        fail("migration_id inesperado")
    if data.get("status") not in {"planned_not_executed", "ready_for_execution"}:
        fail("estado de migración incompatible con preflight")

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
        fail("la publicación no debe estar autorizada en preflight")
    if data.get("disciplinary_review_complete") is not False:
        fail("no puede declararse revisión disciplinar completa")


def validate_repository_state() -> None:
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

    expected = [UNITS / f"unit-{number:02d}.json" for number in range(1, 7)]
    missing = [path.relative_to(ROOT).as_posix() for path in expected if not path.exists()]
    if missing:
        fail(f"faltan unidades legacy: {missing}")

    premature = [UNITS / f"unit-{number:02d}.json" for number in range(7, 11)]
    existing = [path.relative_to(ROOT).as_posix() for path in premature if path.exists()]
    if existing:
        fail(f"la migración parece parcialmente ejecutada: {existing}")


def main() -> int:
    manifest = load_manifest()
    validate_manifest(manifest)
    validate_repository_state()
    print("OK: preflight de migración atómica de Bioinstrumentación superado")
    print("Estado esperado: 6 unidades legacy, migración 6→10 aún no ejecutada")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
