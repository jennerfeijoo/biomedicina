#!/usr/bin/env python3
"""Validate technical-blocker resolution for Bioinstrumentation unit 1."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOLUTION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-01-blocker-resolution.json"
SOURCE_PATH = ROOT / "data" / "source_registry" / "bioinstrumentacion-unit-01-blockers.json"
PACKAGE_PATH = ROOT / "data" / "course_plan_packages" / "package-04-bioinstrumentation-excellence-pilot.json"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
READINESS_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-01" / "AUTHORING_READINESS.md"
AUTHORING_UNIT_PATH = ROOT / "data" / "course_redevelopment" / "bioinstrumentacion" / "units" / "unit-01.json"
DOC_DIR = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "unit-01"

EXPECTED_DOCS = {
    "PRESSURE_CASE_RESOLUTION.md": [
        "Presión intraarterial",
        "Estimación auscultatoria",
        "Estimación oscilométrica",
        "Errores que la evaluación debe discriminar",
        "interpretación clínica",
    ],
    "THERMAL_MODEL_RESOLUTION.md": [
        "T_u(t)",
        "T_d(t)",
        "T_s(t)",
        "y(t)",
        "63,2 %",
        "simulación conceptual",
    ],
    "PHYSIONET_RECORD_100_SPEC.md": [
        "MIT-BIH Arrhythmia Database",
        "registro seleccionado: `100`",
        "360 Hz",
        "650000",
        "MLII",
        "V5",
        "no interpretación clínica",
    ],
    "DISCIPLINARY_REVIEW_REQUEST.md": [
        "pending_human_review",
        "approve_for_controlled_drafting",
        "approve_with_changes",
        "do_not_approve",
        "Este documento **no es una revisión**",
    ],
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


def validate_sources() -> set[str]:
    registry = load_json(SOURCE_PATH)
    if registry.get("subject_id") != "bioinstrumentacion" or registry.get("unit_number") != 1:
        raise ValueError("registro suplementario asociado a otra unidad")
    sources = require_list(registry.get("sources"), "sources", 6)
    if len(sources) != 6:
        raise ValueError("el registro de bloqueos debe conservar exactamente seis fuentes")
    ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("cada fuente debe ser un objeto")
        source_id = require_text(source.get("id"), "source.id", 5)
        if source_id in ids:
            raise ValueError(f"fuente duplicada: {source_id}")
        ids.add(source_id)
        if source.get("verification_status") != "verified_directly":
            raise ValueError(f"{source_id} no está verificada directamente")
        url = str(source.get("url") or "")
        if not url.startswith("https://"):
            raise ValueError(f"URL no segura o ausente en {source_id}")
        require_text(source.get("locator"), f"{source_id}.locator", 25)
        require_list(source.get("authorized_claims"), f"{source_id}.authorized_claims", 2)
        require_text(source.get("limitations"), f"{source_id}.limitations", 45)
    expected = {
        "aha-bp-measurement-2019",
        "aha-acc-high-bp-guideline-2025",
        "aha-cuffless-bp-2026",
        "macrae-thermal-skin-model-2021",
        "rudtsch-contact-thermometer-dynamics-2019",
        "physionet-mitdb-record-100",
    }
    if ids != expected:
        raise ValueError(f"fuentes inesperadas o ausentes: {sorted(expected ^ ids)}")
    return ids


def validate_pressure(resolution: dict[str, Any], source_ids: set[str]) -> None:
    pressure = resolution.get("pressure_case")
    if not isinstance(pressure, dict) or pressure.get("status") != "resolved_for_authoring":
        raise ValueError("caso de presión no resuelto para autoría")
    require_text(pressure.get("decision"), "pressure.decision", 100)
    variants = require_list(pressure.get("measurand_variants"), "pressure.measurand_variants", 3)
    if len(variants) != 3:
        raise ValueError("el caso de presión debe contener exactamente tres variantes")
    expected_ids = {
        "intraarterial-waveform",
        "brachial-auscultatory-estimate",
        "brachial-oscillometric-estimate",
    }
    variant_ids: set[str] = set()
    for variant in variants:
        if not isinstance(variant, dict):
            raise ValueError("cada variante de presión debe ser un objeto")
        variant_id = require_text(variant.get("id"), "pressure.variant.id", 5)
        variant_ids.add(variant_id)
        require_text(variant.get("measurand"), f"{variant_id}.measurand", 90)
        require_text(variant.get("method_relation"), f"{variant_id}.method_relation", 90)
        require_text(variant.get("reporting_boundary"), f"{variant_id}.reporting_boundary", 45)
    if variant_ids != expected_ids:
        raise ValueError("variantes de presión incompletas")
    require_list(pressure.get("required_metadata"), "pressure.required_metadata", 8)
    require_list(pressure.get("influence_quantities"), "pressure.influence_quantities", 7)
    forbidden = require_list(pressure.get("forbidden_equivalences"), "pressure.forbidden_equivalences", 5)
    if not any("intraarterial" in str(item) and "manguito" in str(item) for item in forbidden):
        raise ValueError("no se bloquea la equivalencia entre presión directa y manguito")
    linked = set(require_list(pressure.get("source_ids"), "pressure.source_ids", 3))
    if not linked <= source_ids:
        raise ValueError("caso de presión referencia fuentes desconocidas")


def validate_thermal(resolution: dict[str, Any], source_ids: set[str]) -> None:
    thermal = resolution.get("thermal_model")
    if not isinstance(thermal, dict) or thermal.get("status") != "resolved_for_synthetic_dataset_design":
        raise ValueError("modelo térmico no resuelto")
    require_text(thermal.get("decision"), "thermal.decision", 100)
    states = require_list(thermal.get("states"), "thermal.states", 4)
    symbols = {str(state.get("symbol")) for state in states if isinstance(state, dict)}
    if symbols != {"T_u(t)", "T_d(t)", "T_s(t)", "y(t)"}:
        raise ValueError(f"estados térmicos incorrectos: {sorted(symbols)}")
    for state in states:
        require_text(state.get("name"), "thermal.state.name", 8)
        require_text(state.get("role"), "thermal.state.role", 40)
    model = thermal.get("model")
    if not isinstance(model, dict):
        raise ValueError("thermal.model ausente")
    for field in ("disturbance_relation", "dynamic_relation", "indication_relation"):
        require_text(model.get(field), f"thermal.model.{field}", 15)
    constraints = require_list(model.get("constraints"), "thermal.model.constraints", 4)
    if not any("no se atribuyen" in str(item) for item in constraints):
        raise ValueError("los parámetros térmicos no están limitados como sintéticos")
    require_list(thermal.get("didactic_scenarios"), "thermal.didactic_scenarios", 5)
    tests = require_list(thermal.get("acceptance_tests"), "thermal.acceptance_tests", 7)
    if not any("63.2" in str(item) for item in tests):
        raise ValueError("falta prueba de constante de tiempo al 63.2 %")
    if not any("sobreimpulso" in str(item) for item in tests):
        raise ValueError("falta prueba de ausencia de sobreimpulso ideal")
    linked = set(require_list(thermal.get("source_ids"), "thermal.source_ids", 2))
    if not linked <= source_ids:
        raise ValueError("modelo térmico referencia fuentes desconocidas")


def validate_physionet(resolution: dict[str, Any], source_ids: set[str]) -> None:
    record = resolution.get("physionet_record")
    if not isinstance(record, dict) or record.get("status") != "resolved_and_pinned":
        raise ValueError("registro PhysioNet no fijado")
    expected = {
        "database": "MIT-BIH Arrhythmia Database",
        "version": "1.0.0",
        "doi": "10.13026/C2F305",
        "record": "100",
    }
    for field, value in expected.items():
        if record.get(field) != value:
            raise ValueError(f"PhysioNet {field} incorrecto")
    if record.get("required_files") != ["100.hea", "100.dat"]:
        raise ValueError("archivos obligatorios de PhysioNet incorrectos")
    header = require_text(record.get("header_snapshot"), "physionet.header_snapshot", 100)
    for marker in ("100 2 360 650000", "MLII", "V5"):
        if marker not in header:
            raise ValueError(f"header de PhysioNet incompleto: {marker}")
    metadata = record.get("expected_metadata")
    if not isinstance(metadata, dict):
        raise ValueError("expected_metadata ausente")
    if metadata.get("signal_count") != 2:
        raise ValueError("signal_count debe ser 2")
    if metadata.get("sampling_frequency_hz") != 360:
        raise ValueError("sampling_frequency_hz debe ser 360")
    if metadata.get("sample_count") != 650000:
        raise ValueError("sample_count debe ser 650000")
    if metadata.get("channel_labels") != ["MLII", "V5"]:
        raise ValueError("channel_labels incorrectos")
    if metadata.get("license") != "Open Data Commons Attribution License v1.0":
        raise ValueError("licencia de PhysioNet incorrecta")
    require_list(record.get("practice_scope"), "physionet.practice_scope", 5)
    forbidden = require_list(record.get("forbidden_uses"), "physionet.forbidden_uses", 5)
    if not any("diagnóstico" in str(item) for item in forbidden):
        raise ValueError("PhysioNet no excluye diagnóstico")
    linked = set(require_list(record.get("source_ids"), "physionet.source_ids", 1))
    if not linked <= source_ids:
        raise ValueError("PhysioNet referencia fuente desconocida")


def validate_review_and_editorial(resolution: dict[str, Any]) -> None:
    review = resolution.get("disciplinary_review")
    if not isinstance(review, dict) or review.get("status") != "pending_human_review":
        raise ValueError("la revisión humana debe permanecer pendiente")
    review_path = ROOT / str(review.get("review_packet") or "")
    if review_path != DOC_DIR / "DISCIPLINARY_REVIEW_REQUEST.md" or not review_path.exists():
        raise ValueError("review_packet incorrecto o ausente")
    require_list(review.get("required_competence"), "review.required_competence", 3)
    decisions = require_list(review.get("decision_options"), "review.decision_options", 3)
    if set(decisions) != {"approve_for_controlled_drafting", "approve_with_changes", "do_not_approve"}:
        raise ValueError("opciones de decisión de revisión incorrectas")
    require_text(review.get("prohibition"), "review.prohibition", 70)

    editorial = resolution.get("editorial_decision")
    if not isinstance(editorial, dict):
        raise ValueError("editorial_decision ausente")
    if editorial.get("technical_blockers_resolved") is not True:
        raise ValueError("los bloqueos técnicos deben quedar resueltos")
    if editorial.get("human_review_completed") is not False:
        raise ValueError("no puede simularse revisión humana")
    if editorial.get("full_theory_drafting_authorized") is not False:
        raise ValueError("la teoría completa fue autorizada prematuramente")
    if editorial.get("unit_developed") is not False:
        raise ValueError("la unidad fue declarada desarrollada prematuramente")
    if editorial.get("course_state_after_block") != "pending":
        raise ValueError("el curso debe permanecer pending")

    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentación no está en pending")
    if "bioinstrumentacion" in set(statuses.get("developed", [])):
        raise ValueError("Bioinstrumentación fue promovida prematuramente")
    if AUTHORING_UNIT_PATH.exists():
        raise ValueError("se creó unit-01.json antes de la revisión humana")


def validate_package() -> None:
    package = load_json(PACKAGE_PATH)
    resolution = package.get("blocker_resolution")
    if not isinstance(resolution, dict):
        raise ValueError("blocker_resolution ausente en paquete")
    if resolution.get("status") != "technical_blockers_resolved_review_pending":
        raise ValueError("estado incorrecto de blocker_resolution")
    if resolution.get("structured_resolution") != str(RESOLUTION_PATH.relative_to(ROOT)):
        raise ValueError("structured_resolution incorrecto")
    if resolution.get("source_extension") != str(SOURCE_PATH.relative_to(ROOT)):
        raise ValueError("source_extension incorrecto")
    docs = set(require_list(resolution.get("documents"), "blocker_resolution.documents", 4))
    expected = {str((DOC_DIR / name).relative_to(ROOT)) for name in EXPECTED_DOCS}
    if docs != expected:
        raise ValueError("documentos de resolución no coinciden con el paquete")
    require_list(resolution.get("resolved_technical_items"), "resolved_technical_items", 3)
    if resolution.get("human_review_status") != "pending_human_review":
        raise ValueError("human_review_status debe permanecer pendiente")
    if resolution.get("editorial_effect") != "none":
        raise ValueError("la resolución técnica no debe promover contenido")
    if resolution.get("full_theory_drafting_authorized") is not False:
        raise ValueError("paquete autorizó teoría prematuramente")


def validate_documents_and_readiness() -> None:
    for name, markers in EXPECTED_DOCS.items():
        path = DOC_DIR / name
        if not path.exists():
            raise ValueError(f"falta {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            raise ValueError(f"{path.relative_to(ROOT)} incompleto: {', '.join(missing)}")

    readiness = READINESS_PATH.read_text(encoding="utf-8") if READINESS_PATH.exists() else ""
    required = [
        "bloqueos técnicos resueltos",
        "Revisión interna del caso de presión arterial.",
        "Revisión interna del modelo térmico.",
        "Registro de PhysioNet fijado",
        "Revisión disciplinar humana inicial.",
        "teoría completa todavía **no está autorizada**",
        "Estado editorial del curso",
        "Unidad desarrollada",
        "Riesgos abiertos",
        "Gate antes de considerar la unidad desarrollada",
    ]
    missing = [marker for marker in required if marker not in readiness]
    if missing:
        raise ValueError("AUTHORING_READINESS incompleto: " + ", ".join(missing))
    for checked in (
        "- [x] Revisión interna del caso de presión arterial.",
        "- [x] Revisión interna del modelo térmico.",
        "- [x] Registro de PhysioNet fijado y comprobado documentalmente.",
    ):
        if checked not in readiness:
            raise ValueError(f"readiness no cierra bloqueo técnico: {checked}")
    if "- [ ] Revisión disciplinar humana inicial." not in readiness:
        raise ValueError("readiness debe conservar abierta la revisión humana")


def main() -> int:
    try:
        resolution = load_json(RESOLUTION_PATH)
        if resolution.get("subject_id") != "bioinstrumentacion" or resolution.get("unit_number") != 1:
            raise ValueError("resolución asociada a otra unidad")
        if resolution.get("status") != "technical_blockers_resolved_review_pending":
            raise ValueError("estado principal de resolución incorrecto")
        if resolution.get("course_editorial_state") != "pending":
            raise ValueError("course_editorial_state debe permanecer pending")
        if resolution.get("source_registry") != str(SOURCE_PATH.relative_to(ROOT)):
            raise ValueError("source_registry incorrecto")
        source_ids = validate_sources()
        validate_pressure(resolution, source_ids)
        validate_thermal(resolution, source_ids)
        validate_physionet(resolution, source_ids)
        validate_review_and_editorial(resolution)
        validate_package()
        validate_documents_and_readiness()
    except (OSError, ValueError, TypeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    print("OK technical blockers: Bioinstrumentación U1")
    print("pressure resolved · thermal model resolved · PhysioNet 100 pinned · human review pending · course remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
