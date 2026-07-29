#!/usr/bin/env python3
"""Genera y valida el manifiesto de estados editoriales del catálogo.

El manifiesto público no se mantiene manualmente. Se deriva de las mismas
auditorías que clasifican desarrollo lectivo y revisión disciplinar, de modo que
el catálogo no pueda confundir una página de respaldo con una asignatura
desarrollada ni la ausencia de provisionales con la finalización del currículo.
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

import audit_course_completion  # noqa: E402
import audit_developed_courses  # noqa: E402

DEFAULT_OUTPUT = ROOT / "data" / "catalog_statuses.json"


def build_manifest(report: dict[str, Any]) -> dict[str, Any]:
    completion = audit_course_completion.audit()
    catalog_subjects = sorted(row["subject_id"] for row in completion["courses"])
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
    pending = sorted(set(catalog_subjects) - set(developed))
    return {
        "schema_version": "1.1",
        "generated_from": [
            "scripts/audit_course_completion.py",
            "scripts/audit_developed_courses.py",
        ],
        "definitions": {
            "developed": (
                "La asignatura dispone de contenido lectivo desarrollado, "
                "aunque puede seguir en revisión académica."
            ),
            "complete": "La asignatura tiene revisión disciplinar documentada.",
            "pending": (
                "La asignatura todavía depende total o parcialmente de unidades de respaldo."
            ),
        },
        "counts": {
            "catalog_courses": len(catalog_subjects),
            "developed": len(developed),
            "complete": len(complete),
            "pending": len(pending),
        },
        "developed": developed,
        "complete": complete,
        "pending": pending,
    }


def serialize(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def status_summary(manifest: dict[str, Any]) -> str:
    counts = manifest["counts"]
    return (
        f"{counts['catalog_courses']} catalogadas, "
        f"{counts['developed']} desarrolladas, "
        f"{counts['pending']} pendientes y "
        f"{counts['complete']} con revisión disciplinar completa"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera o comprueba data/catalog_statuses.json desde las auditorías académicas."
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
        print("Manifiesto editorial sincronizado: " + status_summary(manifest) + ".")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected, encoding="utf-8")
    manifest = json.loads(expected)
    print(f"Actualizado {output.relative_to(ROOT)}: {status_summary(manifest)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
