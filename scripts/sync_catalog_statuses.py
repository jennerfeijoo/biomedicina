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
import audit_generic_content  # noqa: E402
import validate_scientific_traceability  # noqa: E402

DEFAULT_OUTPUT = ROOT / "data" / "catalog_statuses.json"


def traced_subjects() -> list[str]:
    subjects: list[str] = []
    directory = ROOT / "data" / "claim_registry"
    for path in sorted(directory.glob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        claims = payload.get("claims") if isinstance(payload, dict) else None
        if claims and not validate_scientific_traceability.validate_repository_registry(
            payload, path.relative_to(ROOT).as_posix()
        ):
            subjects.append(str(payload.get("subject_id")))
    return sorted(set(subjects))


def ai_validated_subjects() -> list[str]:
    subjects: list[str] = []
    for path in sorted((ROOT / "data" / "subjects").glob("*/*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        metadata = payload.get("generation_metadata") or {}
        if (
            payload.get("status") == "complete"
            and metadata.get("review_state") == "ai_review_validated"
            and metadata.get("reviewer_validation_id")
        ):
            subjects.append(str(payload.get("id") or path.stem))
    return sorted(set(subjects))


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
    generic_report = audit_generic_content.audit()
    template_detected = sorted(
        set(generic_report["template_detected"]).intersection(developed)
    )
    screened = sorted(set(developed) - set(template_detected))
    source_traced = traced_subjects()
    ai_validated = ai_validated_subjects()
    return {
        "schema_version": "2.0",
        "generated_from": [
            "scripts/audit_course_completion.py",
            "scripts/audit_developed_courses.py",
            "scripts/audit_generic_content.py",
            "scripts/validate_scientific_traceability.py",
        ],
        "definitions": {
            "material_available": "Existen páginas y actividades; no implica especificidad ni validez.",
            "screened_no_known_template_marker": (
                "No se detectó un marcador de plantilla conocido; no equivale a validación científica."
            ),
            "template_detected": "El contenido conserva texto genérico y requiere reconstrucción disciplinar.",
            "claim_traceability_present": "Existe un registro válido de afirmaciones con localizadores.",
            "ai_review_validated": "La revisión IA coincide con un registro de validez vigente para su alcance.",
            "pilot_evaluated": "Existe evidencia educativa versionada de un piloto con estudiantes.",
        },
        "counts": {
            "catalog_courses": len(catalog_subjects),
            "material_available": len(developed),
            "screened_no_known_template_marker": len(screened),
            "template_detected": len(template_detected),
            "claim_traceability_present": len(source_traced),
            "ai_review_validated": len(ai_validated),
            "pilot_evaluated": 0,
            # Compatibilidad temporal con validadores históricos.
            "developed": len(developed),
            "complete": len(complete),
            "pending": len(pending),
        },
        "dimensions": {
            "material": {
                "available": developed,
                "missing": pending,
            },
            "specificity": {
                "screened_no_known_template_marker": screened,
                "template_detected": template_detected,
            },
            "source_traceability": {
                "claim_traceability_present": source_traced,
            },
            "review": {
                "ai_review_validated": ai_validated,
            },
            "educational_evidence": {
                "pilot_evaluated": [],
            },
        },
        "legacy_compatibility": {
            "deprecated": True,
            "reason": (
                "Se conserva temporalmente para validadores históricos. La interfaz pública usa dimensions."
            ),
            "top_level_fields": ["developed", "complete", "pending"],
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
        f"{counts['material_available']} con material, "
        f"{counts['template_detected']} con plantilla detectada, "
        f"{counts['claim_traceability_present']} con trazabilidad de afirmaciones y "
        f"{counts['ai_review_validated']} con revisión IA validada"
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
