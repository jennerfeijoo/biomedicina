#!/usr/bin/env python3
"""Synchronize central package and readiness state for the Bioinstrumentation U2 authoral draft."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / "data/course_plan_packages/package-04-bioinstrumentation-excellence-pilot.json"
READINESS_PATH = ROOT / "docs/pilots/bioinstrumentacion/unit-02/AUTHORING_READINESS.md"

SOURCE_DIR = "data/course_redevelopment/bioinstrumentacion/unit-02-source"
CANONICAL_UNIT = "data/course_redevelopment/bioinstrumentacion/units/unit-02.json"
BUILDER = "scripts/build_bioinstrumentation_u2_authoral_unit.py"
VALIDATOR = "scripts/validate_bioinstrumentation_u2_authoral_unit.py"
IMPLEMENTATION_DOC = "docs/pilots/bioinstrumentacion/unit-02/AUTHORAL_UNIT_IMPLEMENTATION.md"
AUTHORIZATION = "data/authoring_authorizations/bioinstrumentacion-unit-02-provisional.json"
AUDIT = "data/course_audits/bioinstrumentacion/UNIT_02_PRACTICES_ASSESSMENT_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def insert_after(mapping: dict[str, Any], anchor: str, key: str, value: Any) -> dict[str, Any]:
    result: dict[str, Any] = {}
    inserted = False
    for current_key, current_value in mapping.items():
        if current_key == key:
            continue
        result[current_key] = current_value
        if current_key == anchor:
            result[key] = value
            inserted = True
    if not inserted:
        raise ValueError(f"anchor not found while inserting {key}: {anchor}")
    return result


def authoral_section() -> dict[str, Any]:
    return {
        "status": "authored_internal_review_pending_external_verification",
        "source_dir": SOURCE_DIR,
        "canonical_unit": CANONICAL_UNIT,
        "builder": BUILDER,
        "validation": VALIDATOR,
        "implementation_document": IMPLEMENTATION_DOC,
        "provisional_authorization": AUTHORIZATION,
        "audit_basis": AUDIT,
        "theory_section_count": 6,
        "minimum_theory_words": 2200,
        "glossary_term_count": 20,
        "worked_example_count": 3,
        "assessment_ids": ["U2-A1", "U2-A2", "U2-A3", "U2-A4", "U2-A5"],
        "practice_ids": ["U2-P1", "U2-P2", "U2-P3"],
        "source_count": 12,
        "internal_authoring_review": "implemented",
        "external_professional_review_status": "pending_human_review",
        "cognitive_test_status": "pending_human_execution",
        "feedback_usability_review": "pending_human_execution",
        "inter_rater_status": "pending_human_execution",
        "public_release_authorized": False,
        "unit_developed": False,
        "course_state": "pending",
        "editorial_effect": "authoral_draft_only",
    }


def update_package() -> None:
    package = load_object(PACKAGE_PATH)
    if package.get("schema_version") != "2.0":
        raise ValueError("central package schema must remain 2.0")

    package = insert_after(
        package,
        "unit_02_provisional_authoring_workstream",
        "unit_02_authoral_unit_workstream",
        "unit_02_authoral_draft_review",
    )
    package["purpose"] = (
        "Validar un modelo de curso trazable, recuperable y revisable antes de escalarlo al resto de la plataforma. "
        "El paquete contiene borradores autorales internos de las Unidades 1 y 2, con prácticas, evaluaciones, feedback "
        "y auditorías reproducibles; no autoriza declarar unidades desarrolladas, publicarlas ni afirmar validación "
        "profesional externa."
    )
    shared = package.get("shared_unit_contract")
    if not isinstance(shared, dict):
        raise ValueError("shared unit contract is missing")
    shared["editorial_notice"] = (
        "Existen borradores autorales internos de las Unidades 1 y 2. La revisión disciplinar externa, la prueba "
        "cognitiva, la revisión de usabilidad y la concordancia continúan pendientes; ningún artefacto representa "
        "una unidad desarrollada, publicada o profesionalmente validada."
    )
    package = insert_after(
        package,
        "unit_02_provisional_authoring_authorization",
        "unit_02_authoral_unit",
        authoral_section(),
    )
    PACKAGE_PATH.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"{label}: expected one replacement target, found {count}")
    return text.replace(old, new, 1)


def update_readiness() -> None:
    text = READINESS_PATH.read_text(encoding="utf-8")

    state_anchor = "external_professional_review: pending_human_review\n```"
    state_insert = (
        "external_professional_review: pending_human_review\n"
        "authoral_source_status: present\n"
        "unit_authoral_file_current: present_internal_review\n"
        "authoral_unit_status: authored_internal_review_pending_external_verification\n"
        "authoral_theory_sections: 6\n"
        "authoral_minimum_theory_words: 2200\n"
        "authoral_glossary_terms: 20\n"
        "authoral_worked_examples: 3\n"
        "authoral_source_count: 12\n"
        "```"
    )
    if "authoral_unit_status: authored_internal_review_pending_external_verification" not in text:
        text = replace_once(text, state_anchor, state_insert, "authoral state block")

    heading = "## Handoff disciplinar"
    section = """## Borrador autoral completo

La fuente modular y el artefacto canónico interno son:

```text
data/course_redevelopment/bioinstrumentacion/unit-02-source
data/course_redevelopment/bioinstrumentacion/units/unit-02.json
```

El constructor, el validador y la documentación de implementación son:

```text
scripts/build_bioinstrumentation_u2_authoral_unit.py
scripts/validate_bioinstrumentation_u2_authoral_unit.py
docs/pilots/bioinstrumentacion/unit-02/AUTHORAL_UNIT_IMPLEMENTATION.md
```

El borrador contiene seis secciones teóricas con al menos 2.200 palabras, veinte términos de glosario, tres ejemplos razonados, cinco actividades alineadas, doce errores conceptuales, doce preguntas de autoevaluación, cinco conexiones biomédicas limitadas, tres prácticas ejecutables y doce fuentes localizadas. Integra las seis correcciones de la auditoría previa y mantiene las claves de evaluación fuera del contenido destinado al estudiante.

La evidencia humana continúa pendiente. El curso permanece `pending`, la publicación continúa bloqueada y el archivo no debe incorporarse a la generación pública mientras no existan revisión profesional, prueba cognitiva, revisión de usabilidad y concordancia documentadas.

"""
    if "## Borrador autoral completo" not in text:
        text = replace_once(text, heading, section + heading, "authoral section")

    old_next = """## Próximo bloque recomendado

Crear el borrador autoral modular de la Unidad 2, su constructor determinista y su validador permanente. El resultado debe permanecer interno, con el curso en `pending`, sin publicación ni afirmaciones de validación profesional.
"""
    new_next = """## Próximo bloque recomendado

Ejecutar una auditoría científica y editorial del borrador autoral completo, verificando teoría, ejemplos, glosario, continuidad pedagógica, trazabilidad y coherencia con las prácticas y evaluaciones. La auditoría seguirá siendo interna y no modificará `pending_human_review`, la publicación ni el estado del curso.
"""
    if old_next in text:
        text = replace_once(text, old_next, new_next, "next gate")
    elif new_next not in text:
        raise ValueError("next gate text is not recognized")

    READINESS_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    update_package()
    update_readiness()
    print(PACKAGE_PATH.relative_to(ROOT))
    print(READINESS_PATH.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
