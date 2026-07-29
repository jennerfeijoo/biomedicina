#!/usr/bin/env python3
"""Validate the authoring-preparation package for Bioinstrumentation unit 1."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREPARATION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-01.json"
PLANNING_PATH = ROOT / "data" / "course_planning" / "bioinstrumentacion-excellence.json"
PACKAGE_PATH = ROOT / "data" / "course_plan_packages" / "package-04-bioinstrumentation-excellence-pilot.json"
SOURCES_PATH = ROOT / "data" / "source_registry" / "bioinstrumentacion.json"
CATALOG_STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
DOC_DIR = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-01"

EXPECTED_TITLE = "Mensurando, sistema de medición y cadena de trazabilidad"
EXPECTED_DOCS = {
    "SOURCE_DOSSIER.md": [
        "Afirmaciones autorizadas",
        "Trazabilidad metrológica",
        "Aptitud para el uso",
        "Afirmaciones prohibidas",
        "Brechas que permanecen abiertas",
    ],
    "CONCEPT_AND_VISUAL_MODEL.md": [
        "ruta física y digital de la señal",
        "modelo de cantidades",
        "Capa 8 — Trazabilidad metrológica",
        "Errores visuales prohibidos",
        "Criterio de aceptación",
    ],
    "ASSESSMENT_AND_FEEDBACK_BLUEPRINT.md": [
        "Secuencia de evaluación",
        "Banco de misconceptions y feedback",
        "problema de recuperación diferente",
        "Gate de autoría",
    ],
    "MISCONCEPTION_COMPLETION.md": [
        "La señal registrada es el resultado completo",
        "El nombre habitual especifica el mensurando",
        "El método es el mensurando",
        "Los metadatos son accesorios",
        "Conocer definiciones demuestra transferencia",
        "trece misconceptions",
    ],
    "PRACTICE_AND_DATA_PLAN.md": [
        "Cadena térmica sintética",
        "Auditoría de metadatos ECG abiertos",
        "Auditoría de trazabilidad documental",
        "no se adquieren datos de personas",
        "Pruebas automáticas previstas",
    ],
    "AUTHORING_READINESS.md": [
        "authoring_preparation_review",
        "Estado editorial del curso",
        "Unidad desarrollada",
        "Riesgos abiertos",
        "Gate antes de considerar la unidad desarrollada",
    ],
}

REQUIRED_CONCEPT_NODES = {
    "measurand",
    "measuring_system",
    "measuring_chain",
    "indication",
    "measurement_result",
    "measurement_model",
    "influence_quantity",
    "traceability",
    "fitness_for_purpose",
}
REQUIRED_SOURCE_IDS = {
    "bipm-vim-measurand",
    "bipm-vim-indication",
    "bipm-vim-measurement-result",
    "bipm-vim-measuring-chain",
    "bipm-vim-measurement-model",
    "bipm-vim-traceability",
    "jcgm-gum-1-2023",
    "jcgm-gum-6-2020",
    "nist-tn-2156",
    "physionet-mit-bih-arrhythmia",
}
REQUIRED_FEEDBACK_FIELDS = {
    "diagnosed_misconception",
    "why_the_reasoning_fails",
    "first_hint",
    "second_hint",
    "source_or_section_to_review",
    "different_recovery_problem",
    "objective_continue_criterion",
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"falta {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido en {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} debe contener un objeto JSON")
    return data


def require_text(value: Any, label: str, minimum: int = 20) -> str:
    text = str(value or "").strip()
    if len(text) < minimum:
        raise ValueError(f"{label} es insuficiente")
    return text


def require_list(value: Any, label: str, minimum: int) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"{label} requiere al menos {minimum} elementos")
    return value


def validate_identity_and_scope(preparation: dict[str, Any]) -> None:
    expected = {
        "subject_id": "bioinstrumentacion",
        "unit_number": 1,
        "title": EXPECTED_TITLE,
        "status": "authoring_preparation_review",
        "course_editorial_state": "pending",
    }
    for key, value in expected.items():
        if preparation.get(key) != value:
            raise ValueError(f"{key} incorrecto: {preparation.get(key)!r}")
    require_text(preparation.get("central_question"), "central_question", 80)
    require_text(preparation.get("authoring_purpose"), "authoring_purpose", 120)

    scope = preparation.get("scope")
    if not isinstance(scope, dict):
        raise ValueError("scope debe ser un objeto")
    require_list(scope.get("included"), "scope.included", 8)
    excluded = require_list(scope.get("excluded"), "scope.excluded", 6)
    if not any("interpretación diagnóstica" in str(item) for item in excluded):
        raise ValueError("el alcance debe excluir interpretación diagnóstica")


def validate_outcomes(preparation: dict[str, Any]) -> set[str]:
    outcomes = require_list(preparation.get("learning_outcomes"), "learning_outcomes", 5)
    if len(outcomes) != 5:
        raise ValueError("la Unidad 1 debe conservar exactamente cinco resultados")
    ids: set[str] = set()
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            raise ValueError("cada resultado debe ser un objeto")
        outcome_id = require_text(outcome.get("id"), "learning_outcome.id", 4)
        if outcome_id in ids:
            raise ValueError(f"resultado duplicado: {outcome_id}")
        ids.add(outcome_id)
        require_text(outcome.get("statement"), f"{outcome_id}.statement", 70)
        require_text(outcome.get("mastery_evidence"), f"{outcome_id}.mastery_evidence", 60)
        require_text(outcome.get("criterion"), f"{outcome_id}.criterion", 50)
    return ids


def validate_knowledge_model(preparation: dict[str, Any]) -> None:
    model = preparation.get("knowledge_model")
    if not isinstance(model, dict):
        raise ValueError("knowledge_model ausente")
    nodes = require_list(model.get("nodes"), "knowledge_model.nodes", 15)
    node_ids: set[str] = set()
    for node in nodes:
        if not isinstance(node, dict):
            raise ValueError("cada nodo conceptual debe ser un objeto")
        node_id = require_text(node.get("id"), "knowledge_model.node.id", 3)
        if node_id in node_ids:
            raise ValueError(f"nodo conceptual duplicado: {node_id}")
        node_ids.add(node_id)
        require_text(node.get("label"), f"{node_id}.label", 3)
        require_text(node.get("role"), f"{node_id}.role", 35)
    missing = sorted(REQUIRED_CONCEPT_NODES - node_ids)
    if missing:
        raise ValueError("faltan nodos conceptuales críticos: " + ", ".join(missing))

    relations = require_list(model.get("required_relations"), "knowledge_model.required_relations", 10)
    if not any("trazabilidad" in str(item) and "resultado" in str(item) for item in relations):
        raise ValueError("el modelo no atribuye trazabilidad al resultado")
    if not any("cadena" in str(item) and "modelo" in str(item) for item in relations):
        raise ValueError("el modelo no separa cadena de señal y modelo de medición")


def validate_cases(preparation: dict[str, Any]) -> None:
    cases = require_list(preparation.get("biomedical_case_models"), "biomedical_case_models", 3)
    if len(cases) != 3:
        raise ValueError("se requieren exactamente tres casos biomédicos")
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("cada caso biomédico debe ser un objeto")
        case_id = require_text(case.get("id"), "case.id", 3)
        require_text(case.get("title"), f"{case_id}.title", 8)
        require_text(case.get("measurand_prompt"), f"{case_id}.measurand_prompt", 70)
        require_list(case.get("chain_elements"), f"{case_id}.chain_elements", 6)
        require_list(case.get("influence_quantities"), f"{case_id}.influence_quantities", 4)
        require_text(case.get("forbidden_inference"), f"{case_id}.forbidden_inference", 60)


def validate_feedback_and_assessment(preparation: dict[str, Any], outcome_ids: set[str]) -> None:
    misconceptions = require_list(preparation.get("misconception_bank"), "misconception_bank", 13)
    if len(misconceptions) != 13:
        raise ValueError("el banco debe contener exactamente trece misconceptions")
    misconception_ids: set[str] = set()
    for item in misconceptions:
        if not isinstance(item, dict):
            raise ValueError("cada misconception debe ser un objeto")
        misconception_id = require_text(item.get("id"), "misconception.id", 5)
        if misconception_id in misconception_ids:
            raise ValueError(f"misconception duplicada: {misconception_id}")
        misconception_ids.add(misconception_id)
        require_text(item.get("claim"), f"{misconception_id}.claim", 20)
        require_text(item.get("diagnostic_probe"), f"{misconception_id}.diagnostic_probe", 45)
        require_text(item.get("feedback_focus"), f"{misconception_id}.feedback_focus", 30)

    contract = preparation.get("feedback_contract")
    if not isinstance(contract, dict):
        raise ValueError("feedback_contract ausente")
    fields = set(require_list(contract.get("required_fields"), "feedback_contract.required_fields", 7))
    missing_fields = sorted(REQUIRED_FEEDBACK_FIELDS - fields)
    if missing_fields:
        raise ValueError("faltan campos de feedback: " + ", ".join(missing_fields))
    require_list(contract.get("prohibited_patterns"), "feedback_contract.prohibited_patterns", 5)

    assessments = require_list(preparation.get("assessment_blueprint"), "assessment_blueprint", 5)
    assessment_ids: set[str] = set()
    covered_misconceptions: set[str] = set()
    for assessment in assessments:
        if not isinstance(assessment, dict):
            raise ValueError("cada evaluación debe ser un objeto")
        assessment_id = require_text(assessment.get("id"), "assessment.id", 4)
        if assessment_id in assessment_ids:
            raise ValueError(f"evaluación duplicada: {assessment_id}")
        assessment_ids.add(assessment_id)
        require_text(assessment.get("type"), f"{assessment_id}.type", 5)
        linked_outcomes = set(require_list(assessment.get("outcomes"), f"{assessment_id}.outcomes", 1))
        unknown_outcomes = sorted(linked_outcomes - outcome_ids)
        if unknown_outcomes:
            raise ValueError(f"{assessment_id} referencia resultados desconocidos: {unknown_outcomes}")
        require_text(assessment.get("evidence"), f"{assessment_id}.evidence", 50)
        linked_misconceptions = set(
            require_list(
                assessment.get("misconceptions_discriminated"),
                f"{assessment_id}.misconceptions_discriminated",
                1,
            )
        )
        unknown_misconceptions = sorted(linked_misconceptions - misconception_ids)
        if unknown_misconceptions:
            raise ValueError(
                f"{assessment_id} referencia misconceptions desconocidas: {unknown_misconceptions}"
            )
        covered_misconceptions.update(linked_misconceptions)
        require_text(assessment.get("mastery_rule"), f"{assessment_id}.mastery_rule", 45)
    if not covered_misconceptions:
        raise ValueError("las evaluaciones no discriminan misconceptions")


def validate_practice_and_visual(preparation: dict[str, Any]) -> None:
    practice = preparation.get("practice_plan")
    if not isinstance(practice, dict):
        raise ValueError("practice_plan ausente")
    require_text(practice.get("primary_mode"), "practice_plan.primary_mode", 30)
    for activity in require_list(practice.get("activities"), "practice_plan.activities", 2):
        if not isinstance(activity, dict):
            raise ValueError("cada práctica debe ser un objeto")
        activity_id = require_text(activity.get("id"), "practice.id", 4)
        require_text(activity.get("title"), f"{activity_id}.title", 8)
        require_text(activity.get("data"), f"{activity_id}.data", 45)
        require_text(activity.get("task"), f"{activity_id}.task", 60)
        require_text(activity.get("reproducibility"), f"{activity_id}.reproducibility", 35)
    safety = require_text(practice.get("safety_boundary"), "practice_plan.safety_boundary", 70)
    if "no" not in safety.lower() or "personas" not in safety.lower():
        raise ValueError("la práctica debe excluir adquisición humana")

    visual = preparation.get("visual_specification")
    if not isinstance(visual, dict):
        raise ValueError("visual_specification ausente")
    require_text(visual.get("primary_scene"), "visual_specification.primary_scene", 140)
    require_list(visual.get("required_distinctions"), "visual.required_distinctions", 5)
    require_text(visual.get("accessibility"), "visual.accessibility", 70)
    require_list(visual.get("prohibited"), "visual.prohibited", 4)


def validate_sources(preparation: dict[str, Any]) -> None:
    registry = load_json(SOURCES_PATH)
    sources = require_list(registry.get("sources"), "source_registry.sources", 16)
    source_ids = {
        str(source.get("id"))
        for source in sources
        if isinstance(source, dict) and source.get("id")
    }
    missing_registry = sorted(REQUIRED_SOURCE_IDS - source_ids)
    if missing_registry:
        raise ValueError("faltan fuentes unitarias: " + ", ".join(missing_registry))

    for assertion in require_list(preparation.get("source_assertions"), "source_assertions", 5):
        if not isinstance(assertion, dict):
            raise ValueError("cada source_assertion debe ser un objeto")
        claim_id = require_text(assertion.get("claim_id"), "source_assertion.claim_id", 2)
        require_text(assertion.get("claim"), f"{claim_id}.claim", 80)
        linked_sources = set(require_list(assertion.get("source_ids"), f"{claim_id}.source_ids", 1))
        unknown = sorted(linked_sources - source_ids)
        if unknown:
            raise ValueError(f"{claim_id} referencia fuentes desconocidas: {unknown}")
        locators = require_list(assertion.get("locators"), f"{claim_id}.locators", 1)
        if any(len(str(locator).strip()) < 8 for locator in locators):
            raise ValueError(f"{claim_id} contiene localizadores insuficientes")
        require_text(assertion.get("authoring_use"), f"{claim_id}.authoring_use", 30)


def validate_gates_and_consistency(preparation: dict[str, Any]) -> None:
    gate = preparation.get("authoring_gate")
    if not isinstance(gate, dict):
        raise ValueError("authoring_gate ausente")
    require_list(gate.get("required_before_drafting"), "required_before_drafting", 6)
    require_list(gate.get("required_before_publishing_unit"), "required_before_publishing_unit", 5)
    if gate.get("course_state_after_block") != "pending":
        raise ValueError("el gate debe conservar el curso en pending")

    planning = load_json(PLANNING_PATH)
    units = planning.get("units")
    if not isinstance(units, list) or not units:
        raise ValueError("la planificación no contiene unidades")
    if units[0].get("unit") != 1 or units[0].get("title") != EXPECTED_TITLE:
        raise ValueError("la preparación no coincide con la Unidad 1 de la planificación")

    package = load_json(PACKAGE_PATH)
    if package.get("current_phase") != "unit_01_authoring_preparation_review":
        raise ValueError("el paquete no registra la fase actual")
    unit_preparation = package.get("unit_preparation")
    if not isinstance(unit_preparation, dict):
        raise ValueError("unit_preparation ausente en el paquete")
    if unit_preparation.get("structured_contract") != str(PREPARATION_PATH.relative_to(ROOT)):
        raise ValueError("structured_contract incorrecto en el paquete")
    documents = set(require_list(unit_preparation.get("documents"), "package.unit_preparation.documents", 6))
    expected_paths = {
        str((DOC_DIR / filename).relative_to(ROOT)) for filename in EXPECTED_DOCS
    }
    if documents != expected_paths:
        raise ValueError("los documentos del paquete no coinciden con el readiness de la unidad")
    if unit_preparation.get("editorial_effect") != "none":
        raise ValueError("la preparación no debe producir promoción editorial")

    statuses = load_json(CATALOG_STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentación debe permanecer pending")
    if "bioinstrumentacion" in set(statuses.get("developed", [])):
        raise ValueError("Bioinstrumentación fue promovida prematuramente")


def validate_documents() -> None:
    for filename, markers in EXPECTED_DOCS.items():
        path = DOC_DIR / filename
        if not path.exists():
            raise ValueError(f"falta {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            raise ValueError(f"{path.relative_to(ROOT)} incompleto: {', '.join(missing)}")


def main() -> int:
    try:
        preparation = load_json(PREPARATION_PATH)
        validate_identity_and_scope(preparation)
        outcome_ids = validate_outcomes(preparation)
        validate_knowledge_model(preparation)
        validate_cases(preparation)
        validate_feedback_and_assessment(preparation, outcome_ids)
        validate_practice_and_visual(preparation)
        validate_sources(preparation)
        validate_gates_and_consistency(preparation)
        validate_documents()
    except (OSError, ValueError, TypeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    print("OK pilot unit preparation: Bioinstrumentación U1")
    print("5 outcomes · 15 concept nodes · 13 misconceptions · 3 cases · course remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
