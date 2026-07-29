#!/usr/bin/env python3
"""Apply and materialize the internal scientific/editorial audit of Bioinstrumentation U2."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT_PATH = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-02.json"
MASTERY_DYNAMIC_PATH = ROOT / "data" / "assessment_fixtures" / "bioinstrumentacion" / "unit-02" / "mastery-dynamic.json"
MASTERY_LOADING_PATH = ROOT / "data" / "assessment_fixtures" / "bioinstrumentacion" / "unit-02" / "mastery-loading.json"
DIAGNOSTIC_LOADING_PATH = ROOT / "data" / "assessment_fixtures" / "bioinstrumentacion" / "unit-02" / "diagnostic-loading.json"
ASSESSMENT_DOC_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "ASSESSMENT_IMPLEMENTATION.md"
READINESS_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "AUTHORING_READINESS.md"
AUDIT_PATH = ROOT / "data" / "course_audits" / "bioinstrumentacion" / "UNIT_02_PRACTICES_ASSESSMENT_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json"
REPORT_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02" / "INTERNAL_SCIENTIFIC_EDITORIAL_AUDIT.md"

AUDIT_RECORD_REL = str(AUDIT_PATH.relative_to(ROOT))
REPORT_REL = str(REPORT_PATH.relative_to(ROOT))


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def indexed_assessments(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = contract.get("machine_scored_assessments")
    if not isinstance(entries, list):
        raise ValueError("machine_scored_assessments must be a list")
    result = {
        str(entry.get("id")): entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("id")
    }
    if set(result) != {"U2-A2", "U2-A3", "U2-A4"}:
        raise ValueError("unexpected machine assessment set")
    return result


def apply_assessment_corrections() -> None:
    contract = load_object(ASSESSMENT_PATH)
    assessments = indexed_assessments(contract)

    static = assessments["U2-A2"]
    static_cases = {str(case.get("id")): case for case in static.get("cases", []) if isinstance(case, dict)}
    if set(static_cases) != {"SC01", "SC02", "SC03", "SC04"}:
        raise ValueError("unexpected static case set")
    static_cases["SC01"]["misconceptions"] = ["linearity-is-intrinsic-global"]

    dynamic = assessments["U2-A3"]
    dynamic["allowed_decisions"] = [
        "accept_first_order_limited",
        "reject_declared_simple_first_order",
    ]
    dynamic_cases = {str(case.get("id")): case for case in dynamic.get("cases", []) if isinstance(case, dict)}
    if set(dynamic_cases) != {"DY01", "DY02", "DY03", "DY04"}:
        raise ValueError("unexpected dynamic case set")
    for case_id in ("DY02", "DY03", "DY04"):
        dynamic_cases[case_id]["expected_decision"] = "reject_declared_simple_first_order"
    dynamic["decision_scope_note"] = (
        "Rechazar significa que el modelo simple declarado, sin retardo ni dinámica adicional, "
        "no es suficiente para la evidencia observada; no excluye modelos compuestos que contengan "
        "un subsistema de primer orden."
    )

    loading = assessments["U2-A4"]
    loading["allowed_perturbed_quantities"] = [
        "bridge_output_voltage",
        "sensor_temperature",
        "structural_deformation_and_dynamics",
        "incident_optical_power_and_photocurrent",
    ]
    loading_claims = {str(claim.get("id")): claim for claim in loading.get("claims", []) if isinstance(claim, dict)}
    if set(loading_claims) != {"LG01", "LG02", "LG03", "LG04"}:
        raise ValueError("unexpected loading claim set")
    loading_claims["LG01"]["expected_perturbed_quantity"] = "bridge_output_voltage"

    contract["evidence_crosswalk"] = {
        "U2-A1": {
            "outcomes": ["U2-LO1"],
            "practice_ids": [],
            "source_claims": ["U2-C1"],
            "artifacts": [
                "docs/pilots/bioinstrumentacion/unit-02/CONCEPT_AND_VISUAL_MODEL.md",
                "docs/pilots/bioinstrumentacion/unit-02/ASSESSMENT_AND_FEEDBACK_BLUEPRINT.md",
            ],
        },
        "U2-A2": {
            "outcomes": ["U2-LO2", "U2-LO3"],
            "practice_ids": ["U2-P1"],
            "source_claims": ["U2-C2", "U2-C5"],
            "artifacts": [
                "data/practice_implementations/bioinstrumentacion-unit-02.json",
                "docs/pilots/bioinstrumentacion/unit-02/STATIC_SYNTHETIC_MODEL_RESOLUTION.md",
            ],
        },
        "U2-A3": {
            "outcomes": ["U2-LO4"],
            "practice_ids": ["U2-P2"],
            "source_claims": ["U2-C4", "U2-C5"],
            "artifacts": [
                "data/practice_implementations/bioinstrumentacion-unit-02.json",
                "docs/pilots/bioinstrumentacion/unit-02/DYNAMIC_FIRST_ORDER_RESOLUTION.md",
            ],
        },
        "U2-A4": {
            "outcomes": ["U2-LO3", "U2-LO5"],
            "practice_ids": ["U2-P3"],
            "source_claims": ["U2-C5", "U2-C6"],
            "artifacts": [
                "data/practice_implementations/bioinstrumentacion-unit-02.json",
                "docs/pilots/bioinstrumentacion/unit-02/LOADING_CASES_RESOLUTION.md",
                "docs/pilots/bioinstrumentacion/unit-02/COMPONENT_SELECTION_SPEC.md",
            ],
        },
        "U2-A5": {
            "outcomes": ["U2-LO1", "U2-LO2", "U2-LO3", "U2-LO4", "U2-LO5"],
            "practice_ids": ["U2-P1", "U2-P2", "U2-P3"],
            "source_claims": ["U2-C1", "U2-C2", "U2-C3", "U2-C4", "U2-C5", "U2-C6"],
            "artifacts": [
                "docs/pilots/bioinstrumentacion/unit-02/ASSESSMENT_AND_FEEDBACK_BLUEPRINT.md",
                "docs/pilots/bioinstrumentacion/unit-02/PRACTICE_IMPLEMENTATION.md",
            ],
        },
    }

    prohibited = list(contract.get("feedback_contract", {}).get("prohibited_output_fields", []))
    contract["answer_key_distribution_policy"] = {
        "storage": "internal_server_side_or_private_evaluation_service",
        "learner_payload_excludes": prohibited,
        "public_client_bundle_authorized": False,
        "requires_separate_release_review": True,
        "reason": (
            "Los campos esperados son necesarios para pruebas internas, pero no pueden enviarse al cliente "
            "del estudiante ni incorporarse a un paquete público antes de una revisión de despliegue separada."
        ),
    }
    contract["internal_scientific_editorial_audit"] = {
        "status": "passed_with_corrections_applied",
        "record": AUDIT_RECORD_REL,
        "report": REPORT_REL,
        "unresolved_critical_findings": 0,
        "unresolved_major_findings": 0,
        "external_professional_review": "pending_human_review",
        "full_theory_drafting_authorized": False,
        "public_release_authorized": False,
    }
    write_json(ASSESSMENT_PATH, contract)


def apply_fixture_corrections() -> None:
    dynamic = load_object(MASTERY_DYNAMIC_PATH)
    responses = dynamic.get("responses")
    if not isinstance(responses, dict):
        raise ValueError("mastery dynamic responses are missing")
    for case_id in ("DY02", "DY03", "DY04"):
        response = responses.get(case_id)
        if not isinstance(response, dict):
            raise ValueError(f"mastery dynamic response missing: {case_id}")
        response["decision"] = "reject_declared_simple_first_order"
    write_json(MASTERY_DYNAMIC_PATH, dynamic)

    mastery_loading = load_object(MASTERY_LOADING_PATH)
    mastery_responses = mastery_loading.get("responses")
    if not isinstance(mastery_responses, dict) or not isinstance(mastery_responses.get("LG01"), dict):
        raise ValueError("mastery loading LG01 response is missing")
    mastery_responses["LG01"]["perturbed_quantity"] = "bridge_output_voltage"
    write_json(MASTERY_LOADING_PATH, mastery_loading)

    diagnostic_loading = load_object(DIAGNOSTIC_LOADING_PATH)
    diagnostic_responses = diagnostic_loading.get("responses")
    if not isinstance(diagnostic_responses, dict) or not isinstance(diagnostic_responses.get("LG02"), dict):
        raise ValueError("diagnostic loading LG02 response is missing")
    diagnostic_responses["LG02"]["perturbed_quantity"] = "bridge_output_voltage"
    write_json(DIAGNOSTIC_LOADING_PATH, diagnostic_loading)


def update_assessment_document() -> None:
    text = ASSESSMENT_DOC_PATH.read_text(encoding="utf-8")
    marker = "## Correcciones de auditoría científica y editorial interna"
    if marker not in text:
        text = text.rstrip() + "\n\n" + """## Correcciones de auditoría científica y editorial interna

La auditoría interna conjunta de prácticas, evaluaciones y feedback quedó en `passed_with_corrections_applied`.

1. **Carga eléctrica:** `LG01` ahora identifica como cantidad perturbada la **tensión de salida del puente**. La transferencia de deformación pertenece al caso mecánico y no se combina con la carga por impedancia de entrada.
2. **Alcance del rechazo dinámico:** `reject_declared_simple_first_order` significa que el modelo simple declarado no explica la evidencia. No afirma que ningún modelo compuesto pueda contener un subsistema de primer orden.
3. **Alineación diagnóstica:** `SC01` remedia linealidad global indebida; la ruta «mayor sensibilidad es mejor» permanece en los casos donde existe una decisión de sensibilidad o selección.
4. **Trazabilidad:** cada evaluación `U2-A1` a `U2-A5` posee un `evidence_crosswalk` con resultados, prácticas, afirmaciones fuente y artefactos localizados.
5. **Protección de claves:** los campos esperados se conservan solo para evaluación interna. El payload del estudiante y cualquier futuro cliente público deben excluirlos.

Los identificadores de máquina permanecen en inglés para mantener compatibilidad y reproducibilidad; las instrucciones y explicaciones dirigidas al estudiante usan terminología española. Esta auditoría no sustituye revisión profesional externa, prueba cognitiva ni revisión de usabilidad del feedback.
"""
    ASSESSMENT_DOC_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_readiness_document() -> None:
    text = READINESS_PATH.read_text(encoding="utf-8")
    if "scientific_editorial_audit: passed_with_corrections_applied" not in text:
        anchor = "feedback_usability_review: pending\n"
        replacement = (
            anchor
            + "scientific_editorial_audit: passed_with_corrections_applied\n"
            + "unresolved_critical_findings: 0\n"
            + "unresolved_major_findings: 0\n"
        )
        if anchor not in text:
            raise ValueError("readiness status anchor is missing")
        text = text.replace(anchor, replacement, 1)

    old_gate = "- realizar auditoría científica y editorial de prácticas, evaluaciones y feedback;"
    new_gate = "- mantener vigentes las correcciones y el gate de auditoría científica y editorial;"
    text = text.replace(old_gate, new_gate)

    old_next = (
        "Auditar científicamente y editorialmente la implementación conjunta de U2-P1 a U2-P3 y U2-A1 a U2-A5. "
        "La auditoría debe verificar exactitud, trazabilidad, alineación, ausencia de filtración de respuestas y suficiencia "
        "de los límites antes de considerar una autorización de autoría. La teoría completa y la publicación continúan bloqueadas."
    )
    new_next = (
        "Preparar una autorización provisional separada para autoría controlada de la Unidad 2, limitada por el contrato técnico "
        "y por las correcciones de auditoría. La teoría completa no queda autorizada por esta auditoría; la publicación, la promoción "
        "del curso y la revisión profesional continúan bloqueadas."
    )
    if old_next in text:
        text = text.replace(old_next, new_next, 1)

    audit_section = "## Auditoría científica y editorial interna"
    if audit_section not in text:
        insertion = """

## Auditoría científica y editorial interna

La auditoría conjunta de U2-P1 a U2-P3, U2-A1 a U2-A5 y las doce rutas de feedback fue aprobada con correcciones aplicadas. El registro estructurado es:

```text
data/course_audits/bioinstrumentacion/UNIT_02_PRACTICES_ASSESSMENT_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json
```

El gate permanente es:

```text
scripts/validate_bioinstrumentation_u2_scientific_editorial_audit.py
```

La auditoría resolvió la separación entre carga eléctrica y transferencia mecánica, precisó el alcance del rechazo del modelo simple de primer orden, corrigió una ruta diagnóstica no sustentada, añadió trazabilidad evaluación–evidencia y bloqueó la distribución pública de claves. No aporta evidencia humana ni autorización de teoría o publicación.
"""
        next_heading = "\n## Handoff disciplinar"
        if next_heading not in text:
            raise ValueError("readiness handoff heading is missing")
        text = text.replace(next_heading, insertion + next_heading, 1)

    READINESS_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")


def build_audit_record() -> dict[str, Any]:
    findings = [
        {
            "id": "U2-SE-01",
            "severity": "major",
            "category": "electrical_loading_boundary",
            "issue": "LG01 combinaba tensión del puente y transferencia de deformación, mezclando una perturbación eléctrica por impedancia con el mecanismo mecánico de transferencia hacia la galga.",
            "evidence": [
                "docs/pilots/bioinstrumentacion/unit-02/LOADING_CASES_RESOLUTION.md",
                "data/assessment_implementations/bioinstrumentacion-unit-02.json#/machine_scored_assessments/U2-A4/LG01",
            ],
            "resolution": "La cantidad perturbada de LG01 se restringió a bridge_output_voltage; la transferencia de deformación permanece únicamente en el caso mecánico.",
            "corrected_paths": [
                "data/assessment_implementations/bioinstrumentacion-unit-02.json",
                "data/assessment_fixtures/bioinstrumentacion/unit-02/mastery-loading.json",
                "data/assessment_fixtures/bioinstrumentacion/unit-02/diagnostic-loading.json",
                "docs/pilots/bioinstrumentacion/unit-02/ASSESSMENT_IMPLEMENTATION.md",
            ],
            "status": "resolved",
        },
        {
            "id": "U2-SE-02",
            "severity": "major",
            "category": "dynamic_model_scope",
            "issue": "El identificador reject_first_order podía interpretarse como rechazo de cualquier dinámica de primer orden, aunque los controles solo invalidan el modelo simple declarado sin retardo ni polos adicionales.",
            "evidence": [
                "docs/pilots/bioinstrumentacion/unit-02/DYNAMIC_FIRST_ORDER_RESOLUTION.md",
                "scripts/generate_bioinstrumentation_u2_dynamic_dataset.py",
            ],
            "resolution": "Se sustituyó por reject_declared_simple_first_order y se añadió una nota de alcance que permite considerar modelos compuestos sin aceptar el modelo simple evaluado.",
            "corrected_paths": [
                "data/assessment_implementations/bioinstrumentacion-unit-02.json",
                "data/assessment_fixtures/bioinstrumentacion/unit-02/mastery-dynamic.json",
                "docs/pilots/bioinstrumentacion/unit-02/ASSESSMENT_IMPLEMENTATION.md",
            ],
            "status": "resolved",
        },
        {
            "id": "U2-SE-03",
            "severity": "major",
            "category": "diagnostic_alignment",
            "issue": "SC01 activaba la ruta higher-sensitivity-is-better sin que el prompt contuviera una comparación de sensibilidad o una decisión de selección.",
            "evidence": [
                "data/unit_preparation/bioinstrumentacion-unit-02.json#/misconception_bank",
                "data/assessment_implementations/bioinstrumentacion-unit-02.json#/machine_scored_assessments/U2-A2/SC01",
            ],
            "resolution": "SC01 quedó asociado únicamente con linearity-is-intrinsic-global; la ruta de sensibilidad permanece en SC02 y U2-A5, donde sí existe evidencia diagnóstica.",
            "corrected_paths": ["data/assessment_implementations/bioinstrumentacion-unit-02.json"],
            "status": "resolved",
        },
        {
            "id": "U2-SE-04",
            "severity": "major",
            "category": "source_and_evidence_traceability",
            "issue": "Las evaluaciones ejecutables estaban alineadas conceptualmente, pero carecían de un cruce machine-readable que relacionara cada evaluación con resultados, prácticas, afirmaciones fuente y artefactos localizados.",
            "evidence": [
                "data/unit_preparation/bioinstrumentacion-unit-02.json#/source_assertions",
                "data/practice_implementations/bioinstrumentacion-unit-02.json",
            ],
            "resolution": "Se añadió evidence_crosswalk para U2-A1 a U2-A5 y un gate que verifica IDs, archivos existentes, resultados y claims U2-C1 a U2-C6.",
            "corrected_paths": [
                "data/assessment_implementations/bioinstrumentacion-unit-02.json",
                "scripts/validate_bioinstrumentation_u2_scientific_editorial_audit.py",
            ],
            "status": "resolved",
        },
        {
            "id": "U2-SE-05",
            "severity": "major",
            "category": "answer_key_governance",
            "issue": "El contrato interno contiene campos esperados necesarios para regresión; sin una política de distribución explícita podrían incorporarse accidentalmente a un cliente público del estudiante.",
            "evidence": [
                "data/assessment_implementations/bioinstrumentacion-unit-02.json#/feedback_contract/prohibited_output_fields",
                "scripts/bioinstrumentation_u2_assessment_core.py",
            ],
            "resolution": "Se añadió answer_key_distribution_policy: almacenamiento interno, exclusión del payload del estudiante, cliente público no autorizado y revisión separada obligatoria antes del despliegue.",
            "corrected_paths": [
                "data/assessment_implementations/bioinstrumentacion-unit-02.json",
                "docs/pilots/bioinstrumentacion/unit-02/ASSESSMENT_IMPLEMENTATION.md",
                "scripts/validate_bioinstrumentation_u2_scientific_editorial_audit.py",
            ],
            "status": "resolved",
        },
        {
            "id": "U2-SE-06",
            "severity": "minor",
            "category": "editorial_accessibility",
            "issue": "Los identificadores estables de máquina en inglés podían confundirse con la terminología que debe mostrarse al estudiante.",
            "evidence": ["revisión editorial interna de ASSESSMENT_IMPLEMENTATION.md"],
            "resolution": "Se documentó que los identificadores se conservan por reproducibilidad, mientras las instrucciones y explicaciones dirigidas al estudiante usan equivalentes españoles.",
            "corrected_paths": ["docs/pilots/bioinstrumentacion/unit-02/ASSESSMENT_IMPLEMENTATION.md"],
            "status": "resolved",
        },
    ]
    return {
        "schema_version": "1.0",
        "audit_id": "bioinstrumentacion-u2-practices-assessment-scientific-editorial-2026-07-29",
        "subject_id": "bioinstrumentacion",
        "unit": 2,
        "title": "Sensores, transductores y modelos estáticos y dinámicos",
        "audit_type": "internal_scientific_editorial_joint_practices_assessment_feedback",
        "actor_type": "internal_ai_review_accepted_by_project_owner",
        "date": "2026-07-29",
        "status": "passed_with_corrections_applied",
        "reviewed_artifacts": [
            "data/practice_implementations/bioinstrumentacion-unit-02.json",
            "data/assessment_implementations/bioinstrumentacion-unit-02.json",
            "data/assessment_implementations/bioinstrumentacion-unit-02-feedback.json",
            "scripts/generate_bioinstrumentation_u2_static_dataset.py",
            "scripts/generate_bioinstrumentation_u2_dynamic_dataset.py",
            "scripts/audit_bioinstrumentation_u2_datasheets.py",
            "scripts/bioinstrumentation_u2_assessment_core.py",
            "scripts/validate_bioinstrumentation_u2_practices.py",
            "scripts/validate_bioinstrumentation_u2_assessment.py",
            "docs/pilots/bioinstrumentacion/unit-02/PRACTICE_IMPLEMENTATION.md",
            "docs/pilots/bioinstrumentacion/unit-02/ASSESSMENT_IMPLEMENTATION.md",
        ],
        "scope": [
            "validez y límites de los modelos estáticos y dinámicos sintéticos",
            "separación causal de carga eléctrica, térmica, mecánica y óptica",
            "alineación entre resultados, prácticas, evaluaciones y feedback",
            "trazabilidad de fuentes y evidencia ejecutable",
            "ausencia de filtración de claves y puntuación semántica automática",
            "accesibilidad editorial y límites biomédicos, clínicos y regulatorios",
        ],
        "authorities": [
            {"source_id": "VIM3", "locators": ["3.7", "3.8", "4.12", "4.13", "4.23"]},
            {"source_id": "GUM-6:2020", "locators": ["5.3", "5.6–5.8", "6.1–6.6", "9.1"]},
            {
                "source_id": "U2 technical resolutions",
                "locators": [
                    "STATIC_SYNTHETIC_MODEL_RESOLUTION.md",
                    "DYNAMIC_FIRST_ORDER_RESOLUTION.md",
                    "LOADING_CASES_RESOLUTION.md",
                    "COMPONENT_SELECTION_SPEC.md",
                ],
            },
        ],
        "findings": findings,
        "unresolved_critical_findings": 0,
        "unresolved_major_findings": 0,
        "external_professional_review": "pending_human_review",
        "student_cognitive_test": "pending_human_execution",
        "feedback_usability_review": "pending_human_execution",
        "inter_rater_round": "pending_human_execution",
        "full_theory_drafting_authorized": False,
        "public_release_authorized": False,
        "unit_developed": False,
        "course_state": "pending",
        "editorial_effect": "corrections_to_internal_practices_assessment_feedback_only",
        "limitations": [
            "Esta auditoría no constituye revisión profesional externa, aprobación institucional ni evidencia humana.",
            "No reemplaza pruebas cognitivas con estudiantes, revisión de usabilidad del feedback o concordancia real entre revisores.",
            "No valida sensores, personas, tejidos, equipos clínicos, seguridad, conformidad regulatoria o utilidad clínica.",
            "No autoriza la teoría completa, la creación de unit-02.json, publicación ni promoción del curso.",
        ],
    }


def build_report() -> str:
    return """# Auditoría científica y editorial interna — Bioinstrumentación, Unidad 2

Fecha: 2026-07-29

Estado: **aprobada con correcciones aplicadas**.

## Alcance

La auditoría revisó conjuntamente U2-P1 a U2-P3, U2-A1 a U2-A5 y las doce rutas de feedback. Se evaluaron exactitud de modelos, separación de mecanismos de carga, alineación pedagógica, trazabilidad de evidencia, ausencia de filtración de claves, accesibilidad editorial y límites de inferencia biomédica.

Las bases principales fueron VIM3, JCGM GUM-6:2020, las resoluciones técnicas de la Unidad 2 y la documentación fijada de los tres componentes. La revisión es interna y no sustituye revisión profesional externa, prueba cognitiva ni acuerdo real entre revisores.

## Correcciones principales

### 1. Carga eléctrica y transferencia mecánica

`LG01` combinaba la tensión del puente con la transferencia de deformación. Se corrigió a `bridge_output_voltage`: la impedancia de entrada perturba la salida eléctrica de la red; la transferencia de deformación se analiza en el caso mecánico de galga, adhesivo y estructura.

### 2. Alcance del rechazo del primer orden

`reject_first_order` podía interpretarse como rechazo universal. Se sustituyó por `reject_declared_simple_first_order`: el control invalida el modelo simple declarado, pero no excluye un modelo compuesto con retardo, segundo orden u otros subsistemas.

### 3. Feedback diagnóstico de SC01

SC01 activaba una ruta sobre superioridad de sensibilidad sin que el caso presentara una decisión de sensibilidad. Se eliminó esa asociación. La ruta permanece en SC02 y U2-A5, donde sí se examinan saturación, compromisos y selección.

### 4. Cruce de evidencia

Se añadió un `evidence_crosswalk` para U2-A1 a U2-A5. Cada evaluación queda vinculada a resultados, prácticas, claims U2-C1 a U2-C6 y artefactos localizados. El gate rechaza referencias inexistentes o cobertura incompleta.

### 5. Gobierno de claves

Los campos esperados son necesarios para regresión interna, pero no deben llegar al payload del estudiante. Se añadió una política que exige almacenamiento interno, exclusión del cliente, bloqueo de bundles públicos y revisión de despliegue separada.

### 6. Accesibilidad editorial

Los identificadores de máquina permanecen estables en inglés para reproducibilidad. Las explicaciones e instrucciones dirigidas al estudiante usan terminología española y explican el significado de cada decisión técnica.

## Resultado

- Hallazgos críticos sin resolver: **0**
- Hallazgos mayores sin resolver: **0**
- Prácticas internas: **implemented_internal_review**
- Evaluaciones internas: **implemented_internal_review**
- Curso: **pending**
- Unidad autoral 02: **ausente**
- Teoría completa: **no autorizada**
- Publicación: **bloqueada**
- Revisión profesional externa: **pending_human_review**
- Prueba cognitiva: **pending_human_execution**
- Usabilidad del feedback: **pending_human_execution**
- Acuerdo entre revisores: **pending_human_execution**

La versión estructurada y auditable se encuentra en:

`data/course_audits/bioinstrumentacion/UNIT_02_PRACTICES_ASSESSMENT_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json`
"""


def main() -> int:
    apply_assessment_corrections()
    apply_fixture_corrections()
    update_assessment_document()
    update_readiness_document()
    write_json(AUDIT_PATH, build_audit_record())
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report().rstrip() + "\n", encoding="utf-8")
    print("Built Bioinstrumentation U2 internal scientific/editorial audit")
    print("6 resolved findings · 0 critical open · 0 major open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
