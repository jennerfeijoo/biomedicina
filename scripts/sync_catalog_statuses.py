#!/usr/bin/env python3
"""Genera y valida el manifiesto de estados editoriales del catálogo.

El manifiesto público no se mantiene manualmente. Se deriva de la misma auditoría
que clasifica desarrollo lectivo y revisión disciplinar, de modo que el filtro del
catálogo no pueda quedar desactualizado respecto de las fuentes académicas.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_developed_courses  # noqa: E402

DEFAULT_OUTPUT = ROOT / "data" / "catalog_statuses.json"


def build_manifest(report: dict[str, Any]) -> dict[str, Any]:
    developed = sorted(
        row["subject_id"]
        for row in report["developed_courses"]
        if row["developed_units"] > 0 or row["fully_developed"]
    )
    complete = sorted(
        row["subject_id"]
        for row in report["redevelopment_packages"]
        if row["academic_review_complete"] and row["subject_id"] in developed
    )
    return {
        "schema_version": "1.0",
        "generated_from": "scripts/audit_developed_courses.py",
        "definitions": {
            "developed": (
                "La asignatura dispone de contenido lectivo desarrollado, "
                "aunque puede seguir en revisión académica."
            ),
            "complete": "La asignatura tiene revisión disciplinar documentada.",
            "pending": (
                "La asignatura todavía no dispone de desarrollo lectivo completo."
            ),
        },
        "developed": developed,
        "complete": complete,
    }


def serialize(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera o comprueba data/catalog_statuses.json desde la auditoría académica."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="No escribe; falla si el manifiesto registrado no coincide con la auditoría actual.",
    )
    args = parser.parse_args()

    expected = serialize(build_manifest(audit_developed_courses.build_report()))
    output = args.output if args.output.is_absolute() else ROOT / args.output

    if args.check:
        if not output.exists():
            print(f"ERROR: falta {output.relative_to(ROOT)}")
            return 1
        current = output.read_text(encoding="utf-8")
        if current != expected:
            print(
                f"ERROR: {output.relative_to(ROOT)} está desactualizado. "
                "Ejecute: python scripts/sync_catalog_statuses.py"
            )
            return 1
        manifest = json.loads(expected)
        print(
            "Manifiesto editorial sincronizado: "
            f"{len(manifest['developed'])} desarrolladas, "
            f"{len(manifest['complete'])} con revisión disciplinar completa."
        )
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected, encoding="utf-8")
    manifest = json.loads(expected)
    print(
        f"Actualizado {output.relative_to(ROOT)}: "
        f"{len(manifest['developed'])} desarrolladas, "
        f"{len(manifest['complete'])} con revisión disciplinar completa."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
