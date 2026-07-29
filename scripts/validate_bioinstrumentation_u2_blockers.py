#!/usr/bin/env python3
"""Validate technical-blocker resolution for Bioinstrumentation unit 2."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOLUTION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-02-blocker-resolution.json"
PREPARATION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-02.json"
SOURCE_PATH = ROOT / "data" / "source_registry" / "bioinstrumentacion-unit-02-blockers.json"
CATALOG_PATH = ROOT / "data" / "catalog_statuses.json"
AUTHORAL_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-02.json"
PRACTICE_PATH = ROOT / "data" / "practice_implementations" / "bioinstrumentacion-unit-02.json"
DOC_DIR = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-02"

EXPECTED_SOURCES = {
    "vim3-step-response-4-23-u2-blocker",
    "jcgm-gum-6-u2-blocker",
    "vishay-ntclg100e2103jb-datasheet",
    "micro-measurements-cea-06-125una-350",
    "ni-strain-gage-loading-u2",
    "hamamatsu-s5821-03-product",
}
EXPECTED_STATIC_MODELS = {"linear-local", "saturation", "dead-zone", "hysteresis"}
EXPECTED_NEGATIVE_CONTROLS = {"pure-delay", "underdamped-second-order", "static-only"}
EXPECTED_COMPONENTS = {
    "thermistor": "NTCLG100E2103JB",
    "strain-gage": "CEA-06-125UNA-350",
    "photodiode": "S5821-03",
}
EXPECTED_LOADING_CASES = {
    "thermal-loading",
    "mechanical-loading",
    "electrical-loading",
    "optical-loading",
}
EXPECTED_DOCS = {
    "STATIC_SYNTHETIC_MODEL_RESOLUTION.md": [
        "resolved_for_practice_implementation",
        "sensibilidad local",
        "Zona muerta",
        "Histéresis",
        "Control negativo",
        "no representan tejido",
    ],
    "DYNAMIC_FIRST_ORDER_RESOLUTION.md": [
        "resolved_for_practice_implementation",
        "τ·dy/dt + y",
        "63,212 %",
        "f_c = 1/(2πτ)",
        "Retardo puro",
        "Segundo orden subamortiguado",
    ],
    "LOADING_CASES_RESOLUTION.md": [
        "resolved_for_safe_cases",
        "Carga térmica",
        "Carga mecánica",
        "Carga eléctrica",
        "Interacción óptica",
        "no incluyen personas",
    ],
    "COMPONENT_SELECTION_SPEC.md": [
        "resolved_and_pinned",
        "NTCLG100E2103JB",
        "CEA-06-125UNA-350",
        "S5821-03",
        "Transferencias prohibidas",
    ],
    "DISCIPLINARY_REVIEW_REQUEST.md": [
        "pending_human_review",
        "approve_for_practice_implementation",
        "approve_with_changes",
        "do_not_approve",
        "Este documento **no es una revisión**",
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


def validate_sources() -> set[str]:
    registry = load_json(SOURCE_PATH)
    if registry.get("registry_id") != "bioinstrumentacion-unit-02-blockers":
        raise ValueError("registry_id incorrecto")
    if registry.get("subject_id") != "bioinstrumentacion" or registry.get("unit_number") != 2:
        raise ValueError("registro suplementario asociado a otra unidad")
    require_text(registry.get("source_policy"), "source_policy", 180)
    sources = require_list(registry.get("sources"), "sources", 6)
    if len(sources) != 6:
        raise ValueError("el registro debe conservar exactamente seis fuentes")
    ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("cada fuente debe ser un objeto")
        source_id = require_text(source.get("id"), "source.id", 8)
        if source_id in ids:
            raise ValueError(f"fuente duplicada: {source_id}")
        ids.add(source_id)
        if source.get("verification_status") != "verified_directly":
            raise ValueError(f"{source_id} no está verificada directamente")
        if not str(source.get("url") or "").startswith("https://"):
            raise ValueError(f"URL no segura o ausente en {source_id}")
        require_text(source.get("locator"), f"{source_id}.locator", 25)
        require_list(source.get("authorized_claims"), f"{source_id}.authorized_claims", 2)
        require_text(source.get("limitations"), f"{source_id}.limitations", 60)
    if ids != EXPECTED_SOURCES:
        raise ValueError(f"fuentes inesperadas o ausentes: {sorted(ids ^ EXPECTED_SOURCES)}")

    derived = require_list(registry.get("derived_relations"), "derived_relations", 2)
    if {item.get("id") for item in derived if isinstance(item, dict)} != {
        "first-order-step",
        "first-order-corner",
    }:
        raise ValueError("relaciones derivadas incompletas")
    for item in derived:
        require_text(item.get("basis"), "derived.basis", 10)
        require_text(item.get("derivation"), "derived.derivation", 45)
        require_text(item.get("allowed_use"), "derived.allowed_use", 35)
    return ids


def validate_identity(resolution: dict[str, Any]) -> None:
    expected = {
        "subject_id": "bioinstrumentacion",
        "unit_number": 2,
        "title": "Resolución de bloqueos técnicos para autoría de la Unidad 2",
        "status": "technical_blockers_resolved_review_pending",
        "course_editorial_state": "pending",
    }
    for key, wanted in expected.items():
        if resolution.get(key) != wanted:
            raise ValueError(f"{key} incorrecto: {resolution.get(key)!r}")
    if resolution.get("preparation_contract") != "data/unit_preparation/bioinstrumentacion-unit-02.json":
        raise ValueError("preparation_contract incorrecto")
    if resolution.get("source_registry") != "data/source_registry/bioinstrumentacion-unit-02-blockers.json":
        raise ValueError("source_registry incorrecto")

    preparation = load_json(PREPARATION_PATH)
    if preparation.get("status") != "authoring_preparation_review":
        raise ValueError("la preparación U2 no conserva su estado")
    if preparation.get("course_editorial_state") != "pending":
        raise ValueError("la preparación U2 no conserva pending")
    blockers = require_list(preparation.get("open_blockers"), "preparation.open_blockers", 5)
    joined = " ".join(map(str, blockers)).lower()
    for marker in ("modelo dinámico", "constante de tiempo", "componentes exactos", "carga", "revisión humana"):
        if marker not in joined:
            raise ValueError(f"el contrato original no registra el bloqueo: {marker}")


def validate_static(resolution: dict[str, Any]) -> None:
    static = resolution.get("static_synthetic_model")
    if not isinstance(static, dict) or static.get("status") != "resolved_for_practice_implementation":
        raise ValueError("modelo estático no resuelto")
    require_text(static.get("decision"), "static.decision", 180)
    independent = static.get("independent_variable")
    if not isinstance(independent, dict):
        raise ValueError("independent_variable ausente")
    if independent.get("domain") != [-10.0, 10.0] or independent.get("grid_step") != 0.1:
        raise ValueError("dominio o paso estático incorrecto")
    if static.get("seed") != 20260729:
        raise ValueError("semilla estática incorrecta")
    models = require_list(static.get("models"), "static.models", 4)
    if len(models) != 4:
        raise ValueError("se requieren exactamente cuatro modelos estáticos")
    ids = {item.get("id") for item in models if isinstance(item, dict)}
    if ids != EXPECTED_STATIC_MODELS:
        raise ValueError(f"modelos estáticos inesperados: {sorted(ids)}")
    for model in models:
        require_text(model.get("equation"), f"{model.get('id')}.equation", 18)
        if not isinstance(model.get("parameters"), dict):
            raise ValueError(f"{model.get('id')}.parameters ausente")
        require_text(model.get("purpose"), f"{model.get('id')}.purpose", 45)
    hysteresis = next(item for item in models if item.get("id") == "hysteresis")
    require_text(hysteresis.get("trajectory"), "hysteresis.trajectory", 80)

    tests = require_list(static.get("acceptance_tests"), "static.acceptance_tests", 7)
    joined = " ".join(map(str, tests)).lower()
    for marker in ("hash", "1 %", "20 %", "zona muerta", "2*h", "dirección"):
        if marker.lower() not in joined:
            raise ValueError(f"falta control estático: {marker}")
    prohibited = " ".join(map(str, require_list(static.get("prohibited_inferences"), "static.prohibited", 4))).lower()
    for marker in ("mecanismo", "r²", "unidades", "persona"):
        if marker not in prohibited:
            raise ValueError(f"falta límite estático: {marker}")


def validate_dynamic(resolution: dict[str, Any]) -> None:
    dynamic = resolution.get("first_order_dynamic_model")
    if not isinstance(dynamic, dict) or dynamic.get("status") != "resolved_for_practice_implementation":
        raise ValueError("modelo dinámico no resuelto")
    require_text(dynamic.get("decision"), "dynamic.decision", 180)
    if dynamic.get("continuous_model") != "tau*dy/dt + y = K*x(t) + b":
        raise ValueError("modelo continuo incorrecto")
    require_text(dynamic.get("exact_discrete_update"), "exact_discrete_update", 80)
    params = dynamic.get("parameters")
    expected_params = {
        "K": 1.5,
        "b": 0.2,
        "tau_s": 2.0,
        "dt_s": 0.02,
        "duration_s": 16.0,
        "step_time_s": 2.0,
        "step_amplitude": 1.0,
    }
    if params != expected_params:
        raise ValueError(f"parámetros dinámicos incorrectos: {params!r}")

    relations = require_list(dynamic.get("derived_relations"), "dynamic.derived_relations", 4)
    by_name = {item.get("name"): item for item in relations if isinstance(item, dict)}
    expected_names = {
        "fraction_at_tau",
        "settling_time_5_percent",
        "settling_time_2_percent",
        "corner_frequency",
    }
    if set(by_name) != expected_names:
        raise ValueError("relaciones dinámicas incompletas")
    if not math.isclose(float(by_name["fraction_at_tau"].get("expected")), 1 - math.exp(-1), rel_tol=1e-9):
        raise ValueError("fracción a tau incorrecta")
    if not math.isclose(float(by_name["settling_time_5_percent"].get("multiple_of_tau")), -math.log(0.05), rel_tol=1e-9):
        raise ValueError("asentamiento al 5 % incorrecto")
    if not math.isclose(float(by_name["settling_time_2_percent"].get("multiple_of_tau")), -math.log(0.02), rel_tol=1e-9):
        raise ValueError("asentamiento al 2 % incorrecto")
    if "1/(2*pi*tau)" not in str(by_name["corner_frequency"].get("relation")):
        raise ValueError("relación de frecuencia de corte incorrecta")

    controls = " ".join(map(str, require_list(dynamic.get("positive_controls"), "dynamic.positive_controls", 5))).lower()
    for marker in ("monótona", "63.212", "99.3", "5 %", "1/sqrt(2)"):
        if marker.lower() not in controls:
            raise ValueError(f"falta control dinámico positivo: {marker}")
    negatives = require_list(dynamic.get("negative_controls"), "dynamic.negative_controls", 3)
    negative_ids = {item.get("id") for item in negatives if isinstance(item, dict)}
    if negative_ids != EXPECTED_NEGATIVE_CONTROLS:
        raise ValueError("controles negativos dinámicos incompletos")
    for item in negatives:
        require_text(item.get("generator"), f"{item.get('id')}.generator", 35)
        require_text(item.get("rejection_rule"), f"{item.get('id')}.rejection_rule", 55)
    limitations = " ".join(map(str, require_list(dynamic.get("limitations"), "dynamic.limitations", 4))).lower()
    for marker in ("retardos", "no se generaliza", "no es sinónimo", "didácticos"):
        if marker not in limitations:
            raise ValueError(f"falta límite dinámico: {marker}")


def validate_components(resolution: dict[str, Any], source_ids: set[str]) -> None:
    selection = resolution.get("component_selection")
    if not isinstance(selection, dict) or selection.get("status") != "resolved_and_pinned":
        raise ValueError("selección de componentes no fijada")
    components = require_list(selection.get("components"), "component_selection.components", 3)
    if len(components) != 3:
        raise ValueError("se requieren exactamente tres componentes")
    found: dict[str, str] = {}
    linked_sources: set[str] = set()
    for component in components:
        if not isinstance(component, dict):
            raise ValueError("cada componente debe ser un objeto")
        component_id = require_text(component.get("id"), "component.id", 5)
        found[component_id] = require_text(component.get("model"), f"{component_id}.model", 5)
        require_text(component.get("manufacturer"), f"{component_id}.manufacturer", 5)
        require_text(component.get("document"), f"{component_id}.document", 25)
        require_list(component.get("pinned_fields"), f"{component_id}.pinned_fields", 5)
        require_text(component.get("measurement_conditions_boundary"), f"{component_id}.boundary", 100)
        linked_sources.add(require_text(component.get("source_id"), f"{component_id}.source_id", 8))
    if found != EXPECTED_COMPONENTS:
        raise ValueError(f"componentes exactos incorrectos: {found!r}")
    if not linked_sources <= source_ids:
        raise ValueError("la selección referencia fuentes desconocidas")
    if "ni-strain-gage-loading-u2" not in source_ids:
        raise ValueError("falta fuente de configuración y carga de galgas")
    require_list(selection.get("comparison_fields"), "comparison_fields", 11)
    forbidden = " ".join(map(str, require_list(selection.get("forbidden_transfer"), "forbidden_transfer", 5))).lower()
    for marker in ("sistema", "garantía", "biomédica", "cadena", "clínica"):
        if marker not in forbidden:
            raise ValueError(f"falta transferencia prohibida: {marker}")


def validate_loading(resolution: dict[str, Any]) -> None:
    loading = resolution.get("loading_cases")
    if not isinstance(loading, dict) or loading.get("status") != "resolved_for_safe_cases":
        raise ValueError("casos de carga no resueltos")
    cases = require_list(loading.get("cases"), "loading_cases.cases", 4)
    if len(cases) != 4:
        raise ValueError("se requieren exactamente cuatro casos de carga")
    ids = {item.get("id") for item in cases if isinstance(item, dict)}
    if ids != EXPECTED_LOADING_CASES:
        raise ValueError(f"casos de carga inesperados: {sorted(ids)}")
    boundaries: list[str] = []
    for item in cases:
        require_text(item.get("chain"), f"{item.get('id')}.chain", 70)
        require_text(item.get("observable"), f"{item.get('id')}.observable", 55)
        require_list(item.get("required_variables"), f"{item.get('id')}.required_variables", 6)
        boundaries.append(require_text(item.get("boundary"), f"{item.get('id')}.boundary", 50))
    joined = " ".join(boundaries).lower()
    for marker in ("personas", "fuerza", "cadena", "oximetría"):
        if marker not in joined:
            raise ValueError(f"falta límite de carga: {marker}")
    require_text(loading.get("acceptance_rule"), "loading.acceptance_rule", 100)


def validate_review_editorial_and_docs(resolution: dict[str, Any]) -> None:
    review = resolution.get("disciplinary_review")
    if not isinstance(review, dict) or review.get("status") != "pending_human_review":
        raise ValueError("la revisión disciplinar debe permanecer pendiente")
    if review.get("review_packet") != "docs/pilots/bioinstrumentacion/unit-02/DISCIPLINARY_REVIEW_REQUEST.md":
        raise ValueError("review_packet incorrecto")
    require_list(review.get("required_competence"), "review.required_competence", 3)
    require_list(review.get("review_questions"), "review.review_questions", 5)
    decisions = set(require_list(review.get("decision_options"), "review.decision_options", 3))
    if decisions != {"approve_for_practice_implementation", "approve_with_changes", "do_not_approve"}:
        raise ValueError("opciones de decisión incorrectas")
    require_text(review.get("prohibition"), "review.prohibition", 100)

    editorial = resolution.get("editorial_decision")
    if not isinstance(editorial, dict):
        raise ValueError("editorial_decision ausente")
    expected_flags = {
        "technical_blockers_resolved": True,
        "human_review_completed": False,
        "practice_implementation_authorized": False,
        "full_theory_drafting_authorized": False,
        "unit_developed": False,
        "public_release_authorized": False,
        "course_state_after_block": "pending",
    }
    for key, wanted in expected_flags.items():
        if editorial.get(key) != wanted:
            raise ValueError(f"editorial_decision.{key} incorrecto")
    require_text(editorial.get("next_gate"), "editorial.next_gate", 100)

    for filename, markers in EXPECTED_DOCS.items():
        path = DOC_DIR / filename
        if not path.exists():
            raise ValueError(f"falta {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                raise ValueError(f"{filename} no contiene: {marker}")

    statuses = load_json(CATALOG_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentación no está en pending")
    if "bioinstrumentacion" in set(statuses.get("developed", [])):
        raise ValueError("Bioinstrumentación fue promovida prematuramente")
    if AUTHORAL_PATH.exists():
        raise ValueError("se creó unit-02.json antes de autorización")
    if PRACTICE_PATH.exists():
        raise ValueError("se implementaron prácticas U2 antes de revisión disciplinar")


def main() -> int:
    try:
        source_ids = validate_sources()
        resolution = load_json(RESOLUTION_PATH)
        validate_identity(resolution)
        validate_static(resolution)
        validate_dynamic(resolution)
        validate_components(resolution, source_ids)
        validate_loading(resolution)
        validate_review_editorial_and_docs(resolution)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(
        "OK: Bioinstrumentación U2 resuelve bloqueos técnicos con "
        "4 modelos estáticos, 3 controles negativos dinámicos, "
        "3 componentes fijados y 4 casos de carga; "
        "revisión humana, prácticas, teoría y publicación permanecen bloqueadas."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
