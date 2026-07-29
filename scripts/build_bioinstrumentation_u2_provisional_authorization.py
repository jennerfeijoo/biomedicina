#!/usr/bin/env python3
"""Synchronize the central package and readiness document for provisional U2 authoring."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / "data/course_plan_packages/package-04-bioinstrumentation-excellence-pilot.json"
READINESS_PATH = ROOT / "docs/pilots/bioinstrumentacion/unit-02/AUTHORING_READINESS.md"
AUTH_PATH = ROOT / "data/authoring_authorizations/bioinstrumentacion-unit-02-provisional.json"
DOC_PATH = ROOT / "docs/pilots/bioinstrumentacion/unit-02/PROVISIONAL_AUTHORING_AUTHORIZATION.md"
VALIDATOR_PATH = ROOT / "scripts/validate_bioinstrumentation_u2_provisional_authorization.py"
BASIS_COMMIT = "a29fcedce078de03976970cdb8ce21a10b300245"


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


def authorization_section() -> dict[str, Any]:
    return {
        "status": "authorized_for_controlled_drafting_provisionally",
        "record": str(AUTH_PATH.relative_to(ROOT)),
        "document": str(DOC_PATH.relative_to(ROOT)),
        "validation": str(VALIDATOR_PATH.relative_to(ROOT)),
        "authority": "project_owner_continuation_override",
        "authorization_basis_commit": BASIS_COMMIT,
        "operational_issue": 161,
        "assistant_review_accepted_provisionally": True,
        "controlled_authoring_authorized": True,
        "full_theory_drafting_authorized_provisionally": True,
        "authoral_unit_present_in_authorization_block": False,
        "external_professional_review_status": "pending_human_review",
        "professional_endorsement_present": False,
        "student_cognitive_test": "pending_human_execution",
        "feedback_usability_review": "pending_human_execution",
        "inter_rater_round": "pending_human_execution",
        "public_release_authorized": False,
        "unit_developed": False,
        "course_state": "pending",
        "editorial_effect": "controlled_authoring_only",
    }


def update_package() -> None:
    package = load_object(PACKAGE_PATH)
    if package.get("schema_version") != "2.0":
        raise ValueError("central package schema must remain 2.0")

    package = insert_after(
        package,
        "unit_02_assessment_workstream",
        "unit_02_provisional_authoring_workstream",
        "unit_02_controlled_authoring_authorized_provisionally",
    )
    package["purpose"] = (
        "Validar un modelo de curso trazable, recuperable y revisable antes de escalarlo al resto de la plataforma. "
        "El paquete contiene un borrador autoral interno de la Unidad 1 y autoriza provisionalmente la autoría controlada "
        "de la Unidad 2 después de prácticas, evaluaciones y auditoría interna; no autoriza declarar unidades desarrolladas, "
        "publicarlas ni afirmar validación profesional externa."
    )
    shared = package.get("shared_unit_contract")
    if not isinstance(shared, dict):
        raise ValueError("shared unit contract is missing")
    shared["editorial_notice"] = (
        "Existen trabajo autoral interno en la Unidad 1 y autorización provisional de autoría controlada para la Unidad 2. "
        "La revisión disciplinar externa y la evidencia humana continúan pendientes; ningún artefacto representa una unidad "
        "desarrollada, publicada o profesionalmente validada."
    )

    package = insert_after(
        package,
        "unit_02_assessment_implementation",
        "unit_02_provisional_authoring_authorization",
        authorization_section(),
    )
    PACKAGE_PATH.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"{label}: expected one replacement target, found {count}")
    return text.replace(old, new, 1)


def update_readiness() -> None:
    text = READINESS_PATH.read_text(encoding="utf-8")

    state_old = """scientific_editorial_audit: passed_with_corrections_applied
unresolved_critical_findings: 0
unresolved_major_findings: 0
```"""
    state_new = """scientific_editorial_audit: passed_with_corrections_applied
unresolved_critical_findings: 0
unresolved_major_findings: 0
provisional_authoring_authorized: true
authoring_authorization_status: controlled_authoring_authorized
full_theory_drafting_authorized_provisionally: true
external_professional_review: pending_human_review
```"""
    if "provisional_authoring_authorized: true" not in text:
        text = replace_once(text, state_old, state_new, "state block")

    material_old = "- gates permanentes con fixtures de dominio y diagnóstico."
    material_new = (
        "- gates permanentes con fixtures de dominio y diagnóstico;\n"
        "- auditoría científica-editorial interna con seis hallazgos resueltos;\n"
        "- autorización provisional separada para autoría controlada de la Unidad 2."
    )
    if "autorización provisional separada para autoría controlada" not in text:
        text = replace_once(text, material_old, material_new, "material inventory")

    handoff_heading = "## Handoff disciplinar"
    authorization_section_text = """## Autorización provisional de autoría controlada

El propietario indicó continuar después de la auditoría interna y autorizó provisionalmente la producción de un borrador autoral controlado. El registro autoritativo es:

```text
data/authoring_authorizations/bioinstrumentacion-unit-02-provisional.json
```

La documentación y el gate permanente son:

```text
docs/pilots/bioinstrumentacion/unit-02/PROVISIONAL_AUTHORING_AUTHORIZATION.md
scripts/validate_bioinstrumentation_u2_provisional_authorization.py
```

La autorización permite crear el directorio fuente modular, redactar la teoría completa, integrar prácticas y evaluaciones existentes, construir `unit-02.json` como borrador interno y ejecutar validación determinista. Se limita al commit `a29fcedce078de03976970cdb8ce21a10b300245` y a las seis correcciones de auditoría.

Esta autorización es un `project_owner_continuation_override`: no constituye revisión profesional, evidencia humana, autorización de publicación ni cambio del estado externo `pending_human_review`.

"""
    if "## Autorización provisional de autoría controlada" not in text:
        text = replace_once(text, handoff_heading, authorization_section_text + handoff_heading, "authorization section")

    authorized_old = """## Qué está autorizado

- ejecutar y revisar U2-P1, U2-P2 y U2-P3;
- ejecutar U2-A2, U2-A3 y U2-A4 sobre respuestas estructuradas;
- aplicar rúbricas humanas de U2-A1 y U2-A5;
- regenerar salidas en `build/` o directorios temporales;
- mejorar reproducibilidad, controles negativos, feedback y documentación;
- preparar una auditoría científica y editorial conjunta de prácticas y evaluaciones.
"""
    authorized_new = """## Qué está autorizado

- ejecutar y revisar U2-P1, U2-P2 y U2-P3;
- ejecutar U2-A2, U2-A3 y U2-A4 sobre respuestas estructuradas;
- aplicar rúbricas humanas de U2-A1 y U2-A5;
- regenerar salidas en `build/` o directorios temporales;
- crear `data/course_redevelopment/bioinstrumentacion/unit-02-source`;
- crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json` como borrador interno;
- redactar la teoría completa con fuentes localizadas, supuestos y límites;
- integrar prácticas, evaluaciones, feedback y recuperación;
- crear un constructor determinista y un validador autoral específico;
- corregir el borrador mediante gates internos sin publicarlo ni promover el curso.
"""
    if "crear `data/course_redevelopment/bioinstrumentacion/unit-02-source`;" not in text:
        text = replace_once(text, authorized_old, authorized_new, "authorized scope")

    prohibited_old = """## Qué no está autorizado

- crear `data/course_redevelopment/bioinstrumentacion/units/unit-02.json`;
- redactar la teoría completa;
- publicar una página nueva;
- promover el curso a `developed` o `complete`;
- usar datos de personas, muestras o conexión de sensores a sujetos;
- operar equipos clínicos;
- puntuar automáticamente razonamientos abiertos;
- presentar especificaciones de fabricante como validación de una cadena;
- declarar utilidad clínica, conformidad normativa, seguridad o aprobación profesional.
"""
    prohibited_new = """## Qué no está autorizado

- publicar una página nueva o exponer el borrador como contenido completado;
- promover el curso a `developed` o `complete`;
- usar datos de personas, muestras o conexión de sensores a sujetos;
- operar equipos clínicos;
- puntuar automáticamente razonamientos abiertos;
- distribuir claves de evaluación en recursos públicos;
- presentar especificaciones de fabricante como validación de una cadena;
- declarar utilidad clínica, conformidad normativa, seguridad o aprobación profesional;
- fabricar prueba cognitiva, revisión de usabilidad, concordancia o revisión profesional.
"""
    if "distribuir claves de evaluación en recursos públicos;" not in text:
        text = replace_once(text, prohibited_old, prohibited_new, "prohibited scope")

    gate_old = """## Gate antes de autoría completa

Aún se requiere:

- mantener vigentes las correcciones y el gate de auditoría científica y editorial;
- ejecutar una prueba cognitiva con estudiantes;
- revisar usabilidad del feedback y concordancia entre revisores;
- revisar continuidad pedagógica y suficiencia de fuentes;
- obtener una autorización separada para redacción controlada;
- mantener bloqueadas publicación y promoción;
- completar revisión profesional externa mediante evidencia humana válida.

## Próximo bloque recomendado

Preparar una autorización provisional separada para autoría controlada de la Unidad 2, limitada por el contrato técnico y por las correcciones de auditoría. La teoría completa no queda autorizada por esta auditoría; la publicación, la promoción del curso y la revisión profesional continúan bloqueadas.
"""
    gate_new = """## Gates posteriores a la autoría controlada

Antes de declarar la unidad desarrollada o publicarla todavía se requiere:

- mantener vigentes las correcciones y el gate de auditoría científica y editorial;
- auditar científicamente el borrador autoral completo;
- ejecutar una prueba cognitiva con estudiantes;
- revisar usabilidad del feedback y concordancia entre revisores;
- revisar continuidad pedagógica y suficiencia de fuentes;
- mantener bloqueadas publicación y promoción;
- completar revisión profesional externa mediante evidencia humana válida.

## Próximo bloque recomendado

Crear el borrador autoral modular de la Unidad 2, su constructor determinista y su validador permanente. El resultado debe permanecer interno, con el curso en `pending`, sin publicación ni afirmaciones de validación profesional.
"""
    if "## Gates posteriores a la autoría controlada" not in text:
        text = replace_once(text, gate_old, gate_new, "post-authoring gates")

    READINESS_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    update_package()
    update_readiness()
    print(PACKAGE_PATH.relative_to(ROOT))
    print(READINESS_PATH.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
