#!/usr/bin/env python3
"""Validate the foundation and current editorial state of the Bioinstrumentation pilot."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "docs" / "COURSE_EXCELLENCE_CONTRACT.md"
PLANNING_PATH = ROOT / "data" / "course_planning" / "bioinstrumentacion-excellence.json"
PACKAGE_PATH = ROOT / "data" / "course_plan_packages" / "package-04-bioinstrumentation-excellence-pilot.json"
SOURCES_PATH = ROOT / "data" / "source_registry" / "bioinstrumentacion.json"
ALIGNMENT_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "ALIGNMENT_MATRIX.md"
READINESS_PATH = ROOT / "docs" / "pilots" / "bioinstrumentacion" / "REVIEW_READINESS.md"
CATALOG_STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
GENERATED_COURSE_PATH = ROOT / "data" / "generated_courses" / "bioinstrumentacion.json"
PUBLIC_MIGRATION_PATH = ROOT / "data" / "course_migrations" / "bioinstrumentacion-public-canonical-v1.json"
GENERATOR_PATH = ROOT / "scripts" / "generate_site.py"
UNIT_TEMPLATE_PATH = ROOT / "templates" / "unidad.html"
README_PATH = ROOT / "README.md"

ALLOWED_SOURCE_STATES = {
    "verified_directly",
    "verified_metadata",
    "recommended_future_review",
    "superseded",
    "excluded",
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


def validate_contract() -> None:
    text = CONTRACT_PATH.read_text(encoding="utf-8") if CONTRACT_PATH.exists() else ""
    required = [
        "Verdad editorial",
        "Trazabilidad de evidencia",
        "Contrato de unidad",
        "Alineación educativa",
        "Progresión y autonomía",
        "Modelos mentales y visualización",
        "Reproducibilidad",
        "Accesibilidad y resiliencia",
        "Revisión humana",
        "Gates de publicación",
    ]
    missing = [heading for heading in required if heading not in text]
    if missing:
        raise ValueError("contrato de excelencia incompleto: " + ", ".join(missing))
    if "un workflow verde no permiten promover" not in text:
        raise ValueError("el contrato debe separar integridad técnica y madurez académica")


def validate_planning() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    data = load_json(PLANNING_PATH)
    if data.get("subject_id") != "bioinstrumentacion":
        raise ValueError("subject_id incorrecto en planificación")
    if data.get("area_id") != "ingenieria-biomedica":
        raise ValueError("area_id incorrecto en planificación")
    if data.get("status") != "foundation_review":
        raise ValueError("la planificación histórica debe conservar foundation_review")
    require_text(data.get("purpose"), "purpose", 80)
    require_list(data.get("terminal_competencies"), "terminal_competencies", 8)
    require_list(data.get("entry_knowledge"), "entry_knowledge", 5)
    scope = data.get("scope")
    if not isinstance(scope, dict):
        raise ValueError("scope debe ser un objeto")
    require_list(scope.get("included"), "scope.included", 8)
    require_list(scope.get("excluded"), "scope.excluded", 5)

    decision = data.get("architecture_decision")
    if not isinstance(decision, dict) or decision.get("selected_unit_count") != 10:
        raise ValueError("la decisión curricular debe seleccionar diez unidades")
    require_text(decision.get("rationale"), "architecture_decision.rationale", 100)
    require_list(decision.get("alternatives_considered"), "alternatives_considered", 3)

    units = require_list(data.get("units"), "units", 10)
    if len(units) != 10:
        raise ValueError("Bioinstrumentación debe contener exactamente diez unidades")
    expected_numbers = list(range(1, 11))
    numbers = [unit.get("unit") for unit in units if isinstance(unit, dict)]
    if numbers != expected_numbers:
        raise ValueError(f"numeración de unidades inválida: {numbers}")
    titles = [str(unit.get("title") or "").strip() for unit in units]
    if len(set(titles)) != 10 or any(not title for title in titles):
        raise ValueError("títulos de unidad vacíos o duplicados")

    for unit in units:
        number = unit["unit"]
        prefix = f"unidad {number}"
        require_text(unit.get("central_question"), f"{prefix}.central_question", 30)
        require_list(unit.get("core_domains"), f"{prefix}.core_domains", 4)
        require_list(unit.get("learning_outcomes"), f"{prefix}.learning_outcomes", 3)
        require_list(unit.get("misconception_targets"), f"{prefix}.misconception_targets", 3)
        require_list(unit.get("assessment_evidence"), f"{prefix}.assessment_evidence", 3)
        require_list(unit.get("feedback_and_remediation"), f"{prefix}.feedback_and_remediation", 2)
        require_text(unit.get("visual_model"), f"{prefix}.visual_model", 50)
        require_list(unit.get("biomedical_contexts"), f"{prefix}.biomedical_contexts", 3)

    constraints = require_list(data.get("publication_constraints"), "publication_constraints", 5)
    if not any("permanece pending" in str(item) for item in constraints):
        raise ValueError("la planificación histórica debe conservar su bloqueo de promoción original")
    return data, units


def validate_package(units: list[dict[str, Any]]) -> None:
    package = load_json(PACKAGE_PATH)
    if package.get("status") != "foundation_review":
        raise ValueError("el paquete histórico debe conservar foundation_review")
    if package.get("subject_count") != 1 or package.get("planned_unit_count") != 10:
        raise ValueError("conteos incorrectos en el paquete piloto")
    if package.get("generation_order") != ["bioinstrumentacion"]:
        raise ValueError("generation_order incorrecto")
    subjects = require_list(package.get("subjects"), "package.subjects", 1)
    if len(subjects) != 1:
        raise ValueError("el paquete piloto solo debe contener Bioinstrumentación")
    subject = subjects[0]
    if subject.get("status") != "foundation_review":
        raise ValueError("estado histórico incorrecto del sujeto piloto")
    if subject.get("unit_source") != "data/course_planning/bioinstrumentacion-excellence.json#/units":
        raise ValueError("unit_source incorrecto")
    if subject.get("unit_count") != 10:
        raise ValueError("unit_count incorrecto")
    expected_titles = [unit["title"] for unit in units]
    if subject.get("unit_titles") != expected_titles:
        raise ValueError("los títulos del paquete no coinciden con la planificación")
    require_list(subject.get("external_prerequisite_subjects"), "external_prerequisite_subjects", 7)
    contract = package.get("shared_unit_contract")
    if not isinstance(contract, dict):
        raise ValueError("shared_unit_contract ausente")
    require_list(contract.get("required_sections"), "required_sections", 15)
    require_list(contract.get("forbidden"), "forbidden", 7)
    scores = contract.get("minimum_review_scores")
    if not isinstance(scores, dict) or len(scores) < 7 or any(value < 4 for value in scores.values()):
        raise ValueError("minimum_review_scores insuficientes")


def validate_sources() -> None:
    registry = load_json(SOURCES_PATH)
    if registry.get("subject_id") != "bioinstrumentacion":
        raise ValueError("registro de fuentes asociado a otra asignatura")
    sources = require_list(registry.get("sources"), "sources", 8)
    ids: set[str] = set()
    directly_verified = 0
    metadata_only = 0
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("cada fuente debe ser un objeto")
        source_id = require_text(source.get("id"), "source.id", 3)
        if source_id in ids:
            raise ValueError(f"fuente duplicada: {source_id}")
        ids.add(source_id)
        state = source.get("verification_status")
        if state not in ALLOWED_SOURCE_STATES:
            raise ValueError(f"estado de verificación inválido en {source_id}: {state}")
        require_text(source.get("title"), f"{source_id}.title", 5)
        url = str(source.get("url") or "")
        if not url.startswith("https://"):
            raise ValueError(f"URL no segura o ausente en {source_id}")
        require_text(source.get("locator"), f"{source_id}.locator", 10)
        require_text(source.get("curricular_function"), f"{source_id}.curricular_function", 30)
        require_list(source.get("coverage"), f"{source_id}.coverage", 1)
        require_text(source.get("limitations"), f"{source_id}.limitations", 25)
        if state == "verified_directly":
            directly_verified += 1
        if state == "verified_metadata":
            metadata_only += 1
            if "No se consultó" not in source["limitations"]:
                raise ValueError(f"{source_id} debe declarar explícitamente que no se consultó el texto completo")
    if directly_verified < 6:
        raise ValueError("se requieren al menos seis fuentes consultadas directamente")
    if metadata_only < 1:
        raise ValueError("debe conservarse al menos una fuente metadata-only relevante")
    require_list(registry.get("coverage_gaps"), "coverage_gaps", 4)
    require_list(registry.get("review_notes"), "review_notes", 4)


def validate_documents() -> None:
    for path, required in (
        (
            ALIGNMENT_PATH,
            ["Matriz por unidad", "Contrato de feedback", "Gates de alineación", "Criterio para continuar"],
        ),
        (
            READINESS_PATH,
            ["foundation_review", "Unidades desarrolladas en este bloque", "ninguna", "Gates antes de complete", "Riesgos abiertos"],
        ),
    ):
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        missing = [item for item in required if item not in text]
        if missing:
            raise ValueError(f"{path.relative_to(ROOT)} incompleto: {', '.join(missing)}")


def validate_editorial_truth() -> None:
    statuses = load_json(CATALOG_STATUS_PATH)
    pending = set(statuses.get("pending", []))
    developed = set(statuses.get("developed", []))
    complete = set(statuses.get("complete", []))
    if "bioinstrumentacion" not in developed:
        raise ValueError("Bioinstrumentación debe estar developed tras publicar diez unidades avanzadas")
    if "bioinstrumentacion" in pending:
        raise ValueError("Bioinstrumentación no debe seguir dependiendo de unidades de respaldo")
    if "bioinstrumentacion" in complete:
        raise ValueError("Bioinstrumentación no puede ser complete sin revisión disciplinar documentada")
    if statuses.get("counts", {}).get("developed") != len(developed):
        raise ValueError("conteo developed inconsistente")
    if statuses.get("counts", {}).get("pending") != len(pending):
        raise ValueError("conteo pending inconsistente")

    generated = load_json(GENERATED_COURSE_PATH)
    if generated.get("status") != "review":
        raise ValueError("la capa pública de Bioinstrumentación debe permanecer review")
    sequence = generated.get("curriculum_sequence")
    if not isinstance(sequence, list) or [item.get("unit") for item in sequence] != list(range(1, 11)):
        raise ValueError("la capa pública no expone una secuencia canónica 1–10")
    migration = generated.get("migration")
    if not isinstance(migration, dict) or migration.get("public_layer") != "canonical_ten_unit_sequence":
        raise ValueError("falta el marcador de migración canónica")
    if migration.get("human_review_executed") is not False:
        raise ValueError("se declaró una revisión humana no ejecutada")
    if migration.get("disciplinary_review_complete") is not False:
        raise ValueError("se declaró una revisión disciplinar no ejecutada")

    public_migration = load_json(PUBLIC_MIGRATION_PATH)
    if public_migration.get("status") != "implemented_public_layer":
        raise ValueError("la migración pública canónica no está registrada")
    publication_state = public_migration.get("publication_state")
    if not isinstance(publication_state, dict) or publication_state.get("educational_publication") != "review":
        raise ValueError("estado de publicación educativa incorrecto")
    for key in (
        "human_review_executed",
        "disciplinary_review_complete",
        "professional_approval_claimed",
        "clinical_validity_claimed",
        "safety_conformity_claimed",
        "emc_conformity_claimed",
        "regulatory_conformity_claimed",
        "accreditation_claimed",
    ):
        if publication_state.get(key) is not False:
            raise ValueError(f"afirmación editorial indebida: {key}")

    generator = GENERATOR_PATH.read_text(encoding="utf-8")
    template = UNIT_TEMPLATE_PATH.read_text(encoding="utf-8")
    readme = README_PATH.read_text(encoding="utf-8")
    required_generator_markers = [
        "CATALOG_STATUSES_PATH",
        "def catalog_editorial_status",
        "def unit_status_label",
        '"unit_status":',
        '"unit_status_label":',
    ]
    missing_generator = [item for item in required_generator_markers if item not in generator]
    if missing_generator:
        raise ValueError("el generador no aplica la verdad editorial: " + ", ".join(missing_generator))
    if '{{ unit_status }}' not in template or '{{ unit_status_label }}' not in template:
        raise ValueError("la plantilla de unidad conserva un estado codificado")
    if "84 asignaturas" in readme or "--limit 84" in readme:
        raise ValueError("README conserva el inventario histórico de 84 asignaturas")
    for required in (
        "94 asignaturas",
        f"{len(developed)} desarrolladas",
        f"{len(pending)} pendientes",
        "0 con revisión disciplinar completa",
    ):
        if required not in readme:
            raise ValueError(f"README no declara el estado actual: {required}")


def main() -> int:
    try:
        validate_contract()
        _, units = validate_planning()
        validate_package(units)
        validate_sources()
        validate_documents()
        validate_editorial_truth()
    except (OSError, ValueError, TypeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK excellence pilot foundation and canonical publication: Bioinstrumentación")
    print("10 canonical units · course developed in review · human and disciplinary review pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
