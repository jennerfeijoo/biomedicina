#!/usr/bin/env python3
"""Validate the authoring-preparation package for Bioinstrumentation unit 2."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREPARATION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-02.json"
SOURCES_PATH = ROOT / "data" / "source_registry" / "bioinstrumentacion-unit-02.json"
PLANNING_PATH = ROOT / "data" / "course_planning" / "bioinstrumentacion-excellence.json"
CATALOG_PATH = ROOT / "data" / "catalog_statuses.json"
AUTHORAL_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-02.json"
DOC_DIR = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02"

EXPECTED_TITLE = "Sensores, transductores y modelos estáticos y dinámicos"
EXPECTED_OUTCOMES = {f"U2-LO{i}" for i in range(1, 6)}
EXPECTED_ASSESSMENTS = {f"U2-A{i}" for i in range(1, 6)}
EXPECTED_MISCONCEPTIONS = {
    "sensor-equals-system",
    "sensor-equals-transducer-always",
    "higher-sensitivity-is-better",
    "sensitivity-equals-resolution",
    "static-calibration-covers-dynamics",
    "response-time-equals-time-constant",
    "fast-means-accurate",
    "linearity-is-intrinsic-global",
    "hysteresis-is-random-noise",
    "loading-is-negligible",
    "datasheet-is-system-proof",
    "component-performance-is-clinical-utility",
}
REQUIRED_NODES = {
    "sensor",
    "transducer",
    "interface",
    "static_function",
    "sensitivity",
    "selectivity",
    "saturation",
    "hysteresis",
    "loading",
    "dynamic_model",
    "time_constant",
    "step_response_time",
    "bandwidth",
}
REQUIRED_SOURCE_IDS = {
    "vim3-transducer-3-7",
    "vim3-sensor-3-8",
    "vim3-sensitivity-4-12",
    "vim3-selectivity-4-13",
    "vim3-step-response-4-23",
    "jcgm-gum-6-2020-u2",
    "mit-20-309-sensors",
    "nibib-sensors-u2",
    "vishay-ntc-thermistor-u2",
    "ni-strain-gage-u2",
    "hamamatsu-photodiode-u2",
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
EXPECTED_DOCS = {
    "SOURCE_DOSSIER.md": [
        "Fuentes terminológicas primarias",
        "Afirmaciones autorizadas",
        "Afirmaciones prohibidas",
        "Brechas que permanecen abiertas",
    ],
    "CONCEPT_AND_VISUAL_MODEL.md": [
        "Plano 1 — Función en la cadena",
        "Plano 2 — Caracterización estática",
        "Plano 3 — Caracterización dinámica",
        "Errores visuales prohibidos",
        "Criterio de aceptación",
    ],
    "ASSESSMENT_AND_FEEDBACK_BLUEPRINT.md": [
        "Secuencia de evaluación",
        "Banco de errores conceptuales",
        "problema de recuperación diferente",
        "Gate de autoría",
    ],
    "PRACTICE_AND_DATA_PLAN.md": [
        "Banco sintético de características estáticas",
        "Respuesta dinámica de primer orden",
        "Auditoría comparativa de hojas de datos",
        "no se versionan datos humanos",
    ],
    "AUTHORING_READINESS.md": [
        "authoring_preparation_review",
        "course_editorial_state: pending",
        "unit_authoral_file: absent",
        "Qué no está autorizado",
        "Gate antes de autoría completa",
    ],
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"falta {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido en {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} debe contener un objeto JSON")
    return value


def require_text(value: Any, label: str, minimum: int = 20) -> str:
    text = str(value or "").strip()
    if len(text) < minimum:
        raise ValueError(f"{label} es insuficiente")
    return text


def require_list(value: Any, label: str, minimum: int) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"{label} requiere al menos {minimum} elementos")
    return value


def validate_identity(preparation: dict[str, Any]) -> None:
    expected = {
        "subject_id": "bioinstrumentacion",
        "unit_number": 2,
        "title": EXPECTED_TITLE,
        "status": "authoring_preparation_review",
        "course_editorial_state": "pending",
    }
    for key, wanted in expected.items():
        if preparation.get(key) != wanted:
            raise ValueError(f"{key} incorrecto: {preparation.get(key)!r}")
    require_text(preparation.get("central_question"), "central_question", 100)
    require_text(preparation.get("authoring_purpose"), "authoring_purpose", 160)

    prerequisite = preparation.get("prerequisite_contract")
    if not isinstance(prerequisite, dict):
        raise ValueError("prerequisite_contract ausente")
    require_list(prerequisite.get("required_evidence"), "required_evidence", 4)
    require_list(prerequisite.get("recovery_routes"), "recovery_routes", 3)

    scope = preparation.get("scope")
    if not isinstance(scope, dict):
        raise ValueError("scope ausente")
    require_list(scope.get("included"), "scope.included", 10)
    excluded = require_list(scope.get("excluded"), "scope.excluded", 8)
    excluded_text = " ".join(map(str, excluded)).lower()
    for marker in ("interpretación diagnóstica", "personas", "fabricante"):
        if marker not in excluded_text:
            raise ValueError(f"scope.excluded no contiene el límite requerido: {marker}")


def validate_outcomes(preparation: dict[str, Any]) -> None:
    outcomes = require_list(preparation.get("learning_outcomes"), "learning_outcomes", 5)
    if len(outcomes) != 5:
        raise ValueError("la Unidad 2 debe tener exactamente cinco resultados")
    ids: set[str] = set()
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            raise ValueError("cada resultado debe ser un objeto")
        outcome_id = require_text(outcome.get("id"), "learning_outcome.id", 5)
        ids.add(outcome_id)
        require_text(outcome.get("statement"), f"{outcome_id}.statement", 90)
        require_text(outcome.get("mastery_evidence"), f"{outcome_id}.mastery_evidence", 90)
        require_text(outcome.get("criterion"), f"{outcome_id}.criterion", 80)
    if ids != EXPECTED_OUTCOMES:
        raise ValueError(f"resultados inesperados: {sorted(ids)}")


def validate_knowledge_model(preparation: dict[str, Any]) -> None:
    model = preparation.get("knowledge_model")
    if not isinstance(model, dict):
        raise ValueError("knowledge_model ausente")
    nodes = require_list(model.get("nodes"), "knowledge_model.nodes", 17)
    node_ids = {require_text(node.get("id"), "node.id", 3) for node in nodes if isinstance(node, dict)}
    missing = sorted(REQUIRED_NODES - node_ids)
    if missing:
        raise ValueError("faltan nodos críticos: " + ", ".join(missing))
    for node in nodes:
        if not isinstance(node, dict):
            raise ValueError("cada nodo debe ser un objeto")
        require_text(node.get("label"), f"{node.get('id')}.label", 3)
        require_text(node.get("role"), f"{node.get('id')}.role", 45)
    relations = require_list(model.get("required_relations"), "required_relations", 12)
    joined = " ".join(map(str, relations)).lower()
    for marker in ("sensibilidad", "carga", "constante de tiempo", "calibración estática"):
        if marker not in joined:
            raise ValueError(f"required_relations no cubre: {marker}")


def validate_cases(preparation: dict[str, Any]) -> None:
    cases = require_list(preparation.get("biomedical_case_models"), "biomedical_case_models", 3)
    if len(cases) != 3:
        raise ValueError("se requieren exactamente tres casos")
    expected_ids = {"thermistor-case", "strain-gage-case", "photodiode-case"}
    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("cada caso debe ser un objeto")
        case_id = require_text(case.get("id"), "case.id", 5)
        case_ids.add(case_id)
        require_text(case.get("input_quantity"), f"{case_id}.input_quantity", 50)
        require_text(case.get("transduction"), f"{case_id}.transduction", 70)
        require_list(case.get("static_focus"), f"{case_id}.static_focus", 4)
        require_list(case.get("dynamic_focus"), f"{case_id}.dynamic_focus", 4)
        require_list(case.get("loading_or_influence"), f"{case_id}.loading_or_influence", 4)
        require_text(case.get("forbidden_inference"), f"{case_id}.forbidden_inference", 80)
    if case_ids != expected_ids:
        raise ValueError(f"casos inesperados: {sorted(case_ids)}")


def validate_assessment(preparation: dict[str, Any]) -> None:
    misconceptions = require_list(preparation.get("misconception_bank"), "misconception_bank", 12)
    if len(misconceptions) != 12:
        raise ValueError("el banco debe contener exactamente doce errores conceptuales")
    misconception_ids: set[str] = set()
    for item in misconceptions:
        if not isinstance(item, dict):
            raise ValueError("cada error conceptual debe ser un objeto")
        item_id = require_text(item.get("id"), "misconception.id", 5)
        misconception_ids.add(item_id)
        require_text(item.get("claim"), f"{item_id}.claim", 25)
        require_text(item.get("diagnostic_probe"), f"{item_id}.diagnostic_probe", 45)
        require_text(item.get("feedback_focus"), f"{item_id}.feedback_focus", 35)
    if misconception_ids != EXPECTED_MISCONCEPTIONS:
        raise ValueError("el banco de errores conceptuales no coincide con el contrato")

    assessments = require_list(preparation.get("assessment_blueprint"), "assessment_blueprint", 5)
    assessment_ids: set[str] = set()
    covered: set[str] = set()
    for assessment in assessments:
        if not isinstance(assessment, dict):
            raise ValueError("cada evaluación debe ser un objeto")
        assessment_id = require_text(assessment.get("id"), "assessment.id", 5)
        assessment_ids.add(assessment_id)
        linked_outcomes = set(require_list(assessment.get("outcomes"), f"{assessment_id}.outcomes", 1))
        if not linked_outcomes <= EXPECTED_OUTCOMES:
            raise ValueError(f"{assessment_id} referencia resultados desconocidos")
        linked = set(require_list(assessment.get("misconceptions_discriminated"), f"{assessment_id}.misconceptions", 1))
        if not linked <= EXPECTED_MISCONCEPTIONS:
            raise ValueError(f"{assessment_id} referencia errores conceptuales desconocidos")
        covered.update(linked)
        require_text(assessment.get("evidence"), f"{assessment_id}.evidence", 75)
        require_text(assessment.get("mastery_rule"), f"{assessment_id}.mastery_rule", 75)
    if assessment_ids != EXPECTED_ASSESSMENTS:
        raise ValueError(f"evaluaciones inesperadas: {sorted(assessment_ids)}")
    if covered != EXPECTED_MISCONCEPTIONS:
        raise ValueError("las evaluaciones no cubren los doce errores conceptuales")

    feedback = preparation.get("feedback_contract")
    if not isinstance(feedback, dict):
        raise ValueError("feedback_contract ausente")
    fields = set(require_list(feedback.get("required_fields"), "feedback.required_fields", 7))
    if not REQUIRED_FEEDBACK_FIELDS <= fields:
        raise ValueError("faltan campos obligatorios de retroalimentación")
    require_list(feedback.get("prohibited_patterns"), "feedback.prohibited_patterns", 5)


def validate_practices_and_visual(preparation: dict[str, Any]) -> None:
    practice = preparation.get("practice_plan")
    if not isinstance(practice, dict):
        raise ValueError("practice_plan ausente")
    activities = require_list(practice.get("activities"), "practice.activities", 3)
    if {item.get("id") for item in activities if isinstance(item, dict)} != {"U2-P1", "U2-P2", "U2-P3"}:
        raise ValueError("las prácticas U2-P1 a U2-P3 deben estar presentes")
    for activity in activities:
        if not isinstance(activity, dict):
            raise ValueError("cada práctica debe ser un objeto")
        activity_id = require_text(activity.get("id"), "practice.id", 5)
        require_text(activity.get("data"), f"{activity_id}.data", 70)
        require_text(activity.get("task"), f"{activity_id}.task", 80)
        require_text(activity.get("reproducibility"), f"{activity_id}.reproducibility", 60)
    safety = require_text(practice.get("safety_boundary"), "safety_boundary", 100).lower()
    for marker in ("no conectan", "personas", "no emplean muestras", "no solicitan interpretación diagnóstica"):
        if marker not in safety:
            raise ValueError(f"falta límite de seguridad: {marker}")

    visual = preparation.get("visual_specification")
    if not isinstance(visual, dict):
        raise ValueError("visual_specification ausente")
    require_text(visual.get("primary_scene"), "visual.primary_scene", 220)
    require_list(visual.get("required_distinctions"), "visual.required_distinctions", 6)
    require_list(visual.get("prohibited"), "visual.prohibited", 5)


def validate_sources(preparation: dict[str, Any], registry: dict[str, Any]) -> None:
    if registry.get("unit_number") != 2 or registry.get("title") != EXPECTED_TITLE:
        raise ValueError("identidad incorrecta en el registro de fuentes")
    sources = require_list(registry.get("sources"), "sources", 11)
    source_ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("cada fuente debe ser un objeto")
        source_id = require_text(source.get("id"), "source.id", 6)
        source_ids.add(source_id)
        if source.get("verification_status") != "verified_directly":
            raise ValueError(f"{source_id} no fue consultada directamente")
        require_text(source.get("locator"), f"{source_id}.locator", 12)
        require_list(source.get("authorized_claims"), f"{source_id}.authorized_claims", 1)
        require_text(source.get("limitations"), f"{source_id}.limitations", 60)
    missing = sorted(REQUIRED_SOURCE_IDS - source_ids)
    if missing:
        raise ValueError("faltan fuentes obligatorias: " + ", ".join(missing))
    require_list(registry.get("open_source_gaps"), "open_source_gaps", 3)

    assertions = require_list(preparation.get("source_assertions"), "source_assertions", 6)
    assertion_ids: set[str] = set()
    for assertion in assertions:
        if not isinstance(assertion, dict):
            raise ValueError("cada afirmación debe ser un objeto")
        assertion_id = require_text(assertion.get("claim_id"), "claim_id", 5)
        assertion_ids.add(assertion_id)
        linked = set(require_list(assertion.get("source_ids"), f"{assertion_id}.source_ids", 1))
        if not linked <= source_ids:
            raise ValueError(f"{assertion_id} referencia fuentes desconocidas")
        require_list(assertion.get("locators"), f"{assertion_id}.locators", 1)
        require_text(assertion.get("authoring_use"), f"{assertion_id}.authoring_use", 30)
    if assertion_ids != {f"U2-C{i}" for i in range(1, 7)}:
        raise ValueError("source_assertions debe contener U2-C1 a U2-C6")


def validate_planning_and_state(preparation: dict[str, Any]) -> None:
    planning = load_json(PLANNING_PATH)
    units = planning.get("units")
    if not isinstance(units, list):
        raise ValueError("planning.units ausente")
    unit_two = next((item for item in units if isinstance(item, dict) and item.get("unit") == 2), None)
    if not unit_two or unit_two.get("title") != EXPECTED_TITLE:
        raise ValueError("la preparación no coincide con la arquitectura curricular")

    catalog = load_json(CATALOG_PATH)
    serialized = json.dumps(catalog, ensure_ascii=False)
    if "bioinstrumentacion" not in serialized or "pending" not in serialized:
        raise ValueError("el catálogo no conserva Bioinstrumentación en pending")

    if AUTHORAL_PATH.exists():
        raise ValueError("unit-02.json autoral no debe existir durante la preparación")

    readiness = preparation.get("readiness")
    if not isinstance(readiness, dict):
        raise ValueError("readiness ausente")
    expected = {
        "internal_preparation": "implemented_for_review",
        "technical_source_review": "partial_with_documented_gaps",
        "disciplinary_review": "pending_human_review",
        "controlled_authoring_authorized": False,
        "unit_developed": False,
        "public_release_authorized": False,
    }
    for key, wanted in expected.items():
        if readiness.get(key) != wanted:
            raise ValueError(f"readiness.{key} incorrecto")
    require_list(preparation.get("open_blockers"), "open_blockers", 5)
    constraints = require_list(preparation.get("publication_constraints"), "publication_constraints", 5)
    joined = " ".join(map(str, constraints)).lower()
    for marker in ("pending", "unit-02.json", "no se publican", "ci verde"):
        if marker not in joined:
            raise ValueError(f"publication_constraints no contiene: {marker}")


def validate_docs() -> None:
    for name, markers in EXPECTED_DOCS.items():
        path = DOC_DIR / name
        if not path.exists():
            raise ValueError(f"falta {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                raise ValueError(f"{name} no contiene el marcador: {marker}")


def main() -> int:
    preparation = load_json(PREPARATION_PATH)
    registry = load_json(SOURCES_PATH)
    validate_identity(preparation)
    validate_outcomes(preparation)
    validate_knowledge_model(preparation)
    validate_cases(preparation)
    validate_assessment(preparation)
    validate_practices_and_visual(preparation)
    validate_sources(preparation, registry)
    validate_planning_and_state(preparation)
    validate_docs()
    print("Bioinstrumentation U2 preparation gate passed")
    print("outcomes: 5")
    print("concept nodes: 17")
    print("biomedical cases: 3")
    print("misconceptions: 12")
    print("assessments: 5")
    print("practices planned: 3")
    print("verified sources: 11")
    print("course state: pending")
    print("authoral unit: absent")
    print("controlled authoring: not authorized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
