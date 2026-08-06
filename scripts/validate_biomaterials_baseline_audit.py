#!/usr/bin/env python3
"""Validate the Biomaterials baseline evidence and its current lifecycle state."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "editorial_audits" / "biomateriales-baseline.json"
SOURCE = ROOT / "data" / "source_intake" / "biomateriales-yachay-outline.json"
REPORT = ROOT / "docs" / "audits" / "biomateriales" / "BASELINE_CONTENT_AUDIT.md"
CATALOG = ROOT / "data" / "catalog_statuses.json"
PUBLIC_INDEX = ROOT / "ingenieria-biomedica" / "biomateriales" / "index.html"
PUBLIC_UNITS = ROOT / "ingenieria-biomedica" / "biomateriales" / "unidades"
GENERATED_COURSE = ROOT / "data" / "generated_courses" / "biomateriales.json"
GENERATED_UNITS = ROOT / "data" / "generated_units" / "biomateriales"
SUBJECT_OVERLAY = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "biomateriales.json"
REDEVELOPMENT = ROOT / "data" / "course_redevelopment" / "biomateriales"

EXPECTED_CURRENT_TITLES = [
    "Clases y propiedades",
    "Estructura-propiedad",
    "Interfaz material-biología",
    "Degradación y corrosión",
    "Caracterización",
    "Diseño y evaluación preclínica",
]
EXPECTED_RECOMMENDED_TITLES = [
    "Fundamentos, requisitos y selección de biomateriales",
    "Estructura, propiedades mecánicas, térmicas y superficiales",
    "Polímeros, redes e hidrogeles",
    "Metales, cerámicas, vidrios y materiales compuestos",
    "Adsorción de proteínas, adhesión celular e interfaz biológica",
    "Toxicidad, respuesta inmune, inflamación, cuerpo extraño y biofilms",
    "Degradación, corrosión, desgaste y productos de degradación",
    "Caracterización fisicoquímica, mecánica, superficial y microscópica",
    "Procesamiento, esterilización, fibras huecas y microfabricación",
    "Evaluación biológica, evidencia preclínica, riesgo y expediente de selección",
]
EXPECTED_OUTLINE_TITLES = {
    "Introduction",
    "Material properties",
    "Classes of materials used in medicine",
    "Polymer",
    "Hydrogels",
    "Ceramics, glasses, glass-ceramics",
    "Metals",
    "Biomaterials and biological response",
    "Toxicity and immune response",
    "Inflammation, wound healing, and foreign body reactions",
    "In vivo testing of biomaterials",
    "Biofilms and device related infections",
    "Burn Dressings and Skin Substitutes",
    "Skin Tissue Engineering",
    "Hollow fibers",
    "Introduction to microlithography",
    "Overview of Tissue Engineering Concepts and Applications",
    "Bioartificial Liver",
    "Sterilization of Implants and Devices",
    "Microscopes in Biomaterials Science",
    "Bone Tissue Engineering",
    "Blood Vessel Tissue Engineering",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def load_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def require_list(data: dict[str, Any], key: str, minimum: int, label: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or len(value) < minimum:
        fail(f"{label}.{key} requires at least {minimum} items")
    return value


def validate_source() -> None:
    source = load_object(SOURCE)
    if source.get("source_id") != "biomateriales-yachay-classes":
        fail("unexpected source_id")
    if source.get("subject_id") != "biomateriales":
        fail("source subject_id mismatch")
    if source.get("source_type") != "user_supplied_pdf":
        fail("source type must identify a user-supplied PDF")
    if source.get("file_name") != "Clases Biomateriales Yachay.pdf":
        fail("source file name mismatch")
    if source.get("sha256") != "4be2d0e32d29b675ba02d7ca8d7366b18c92afbbae2c743ab558d19f4314b87c":
        fail("source checksum mismatch")
    if source.get("page_count") != 584:
        fail("source page count must be 584")
    outline = require_list(source, "outline", 22, "source")
    if len(outline) != 22:
        fail("source outline must contain exactly 22 entries")
    titles = {str(item.get("title") or "").strip() for item in outline if isinstance(item, dict)}
    if titles != EXPECTED_OUTLINE_TITLES:
        fail("source outline titles do not match the inspected PDF")
    boundary = source.get("content_use_boundary")
    if not isinstance(boundary, dict):
        fail("source content_use_boundary missing")
    if boundary.get("verbatim_slide_text_committed") is not False:
        fail("verbatim slide text must not be committed")
    if boundary.get("images_committed") is not False:
        fail("source images must not be committed")
    if boundary.get("copyrighted_source_file_committed") is not False:
        fail("the copyrighted source PDF must not be committed")
    if boundary.get("publication_requires_independent_rewrite") is not True:
        fail("future publication must require independent rewriting")


def validate_pending_public_state() -> None:
    if not PUBLIC_INDEX.exists():
        fail("public Biomateriales course page is missing")
    index_text = PUBLIC_INDEX.read_text(encoding="utf-8")
    if 'data-status="placeholder"' not in index_text:
        fail("pending public course page must retain the placeholder status")
    for title in EXPECTED_CURRENT_TITLES:
        if title not in index_text:
            fail(f"current public unit missing from index: {title}")

    for number, title in enumerate(EXPECTED_CURRENT_TITLES, start=1):
        path = PUBLIC_UNITS / f"unidad-{number:02d}.html"
        if not path.exists():
            fail(f"missing public fallback unit {number}")
        text = path.read_text(encoding="utf-8")
        if title not in text:
            fail(f"public unit {number} title mismatch")
        if 'data-status="placeholder"' not in text:
            fail(f"public unit {number} must remain placeholder while pending")
        if "Contenido de respaldo" not in text:
            fail(f"public unit {number} no longer identifies fallback content")

    if GENERATED_COURSE.exists():
        fail("advanced generated course must not exist while Biomateriales is pending")
    if GENERATED_UNITS.exists():
        fail("advanced generated units must not exist while Biomateriales is pending")
    if SUBJECT_OVERLAY.exists():
        fail("subject overlay must not exist while Biomateriales is pending")
    if REDEVELOPMENT.exists():
        fail("course redevelopment package must not exist while Biomateriales is pending")


def validate_developed_public_state() -> None:
    required_paths = (PUBLIC_INDEX, GENERATED_COURSE, GENERATED_UNITS, SUBJECT_OVERLAY, REDEVELOPMENT)
    for path in required_paths:
        if not path.exists():
            fail(f"developed Biomateriales is missing {path.relative_to(ROOT)}")

    index_text = PUBLIC_INDEX.read_text(encoding="utf-8")
    if 'data-status="generated"' not in index_text:
        fail("developed public course must use the generated status")
    if "revisión experta pendiente" not in index_text.lower():
        fail("developed public course must disclose pending expert review")
    if "Contenido de respaldo" in index_text:
        fail("developed public course cannot identify itself as fallback content")

    course = load_object(REDEVELOPMENT / "course.json")
    generated_course = load_object(GENERATED_COURSE)
    overlay = load_object(SUBJECT_OVERLAY)
    for label, payload in (
        ("redevelopment course", course),
        ("generated course", generated_course),
        ("subject overlay", overlay),
    ):
        if payload.get("status") != "review":
            fail(f"{label} must remain in review until external validation")
        if payload.get("subject_id") != "biomateriales":
            fail(f"{label} subject_id mismatch")

    detailed_units = course.get("detailed_units")
    if not isinstance(detailed_units, list) or len(detailed_units) != len(EXPECTED_CURRENT_TITLES):
        fail("developed course must declare the six canonical detailed units")

    expected_files = {f"unit-{number:02d}.json" for number in range(1, 7)}
    actual_files = {path.name for path in GENERATED_UNITS.glob("unit-*.json")}
    if actual_files != expected_files:
        fail("developed generated-unit set must contain exactly units 01 through 06")

    for number, title in enumerate(EXPECTED_CURRENT_TITLES, start=1):
        html_path = PUBLIC_UNITS / f"unidad-{number:02d}.html"
        if not html_path.exists():
            fail(f"missing developed public unit {number}")
        html = html_path.read_text(encoding="utf-8")
        if title not in html or 'data-status="generated"' not in html:
            fail(f"developed public unit {number} is not canonical")
        if "Contenido de respaldo" in html:
            fail(f"developed public unit {number} still identifies fallback content")

        unit = load_object(GENERATED_UNITS / f"unit-{number:02d}.json")
        if unit.get("status") != "review":
            fail(f"developed unit {number} must remain in review")
        for key, minimum in (("theory_sections", 4), ("guided_activities", 3), ("self_assessment", 8), ("sources", 5)):
            require_list(unit, key, minimum, f"developed unit {number}")

    completion = load_object(ROOT / "data" / "curriculum_coverage" / "catalog-completion-2026.json")
    courses = completion.get("courses")
    biomaterials = courses.get("biomateriales") if isinstance(courses, dict) else None
    if not isinstance(biomaterials, dict) or biomaterials.get("coverage_state") != "implemented":
        fail("developed Biomateriales must have implemented curriculum coverage")


def validate_repository_baseline(audit: dict[str, Any]) -> None:
    baseline = audit.get("repository_baseline")
    if not isinstance(baseline, dict):
        fail("repository_baseline missing")
    expected = {
        "catalog_state": "pending",
        "public_status_marker": "placeholder",
        "public_unit_count": 6,
        "advanced_course_descriptor_present": False,
        "advanced_unit_directory_present": False,
        "subject_overlay_present": False,
        "course_redevelopment_package_present": False,
    }
    for key, value in expected.items():
        if baseline.get(key) != value:
            fail(f"repository_baseline.{key} must be {value!r}")

    catalog = load_object(CATALOG)
    pending = catalog.get("pending")
    developed = catalog.get("developed")
    complete = catalog.get("complete")
    if isinstance(complete, list) and "biomateriales" in complete:
        fail("Biomateriales cannot be complete before external disciplinary review")

    is_pending = isinstance(pending, list) and "biomateriales" in pending
    is_developed = isinstance(developed, list) and "biomateriales" in developed
    if is_pending == is_developed:
        fail("Biomateriales must belong to exactly one lifecycle state: pending or developed")
    if is_pending:
        validate_pending_public_state()
    else:
        validate_developed_public_state()


def validate_audit() -> None:
    audit = load_object(AUDIT)
    if audit.get("audit_id") != "biomateriales-baseline-2026-08-03":
        fail("unexpected audit_id")
    if audit.get("subject_id") != "biomateriales":
        fail("audit subject_id mismatch")
    if audit.get("status") != "completed_internal":
        fail("audit must be completed_internal")
    validate_repository_baseline(audit)

    current = require_list(audit, "current_public_units", 6, "audit")
    if len(current) != 6:
        fail("current_public_units must contain exactly six units")
    current_titles = [str(item.get("title") or "").strip() for item in current if isinstance(item, dict)]
    if current_titles != EXPECTED_CURRENT_TITLES:
        fail("current public unit titles are not canonical")
    if any(item.get("state") != "generic_fallback" for item in current if isinstance(item, dict)):
        fail("all current public units must be marked generic_fallback")

    findings = require_list(audit, "findings", 5, "audit")
    finding_ids = [item.get("id") for item in findings if isinstance(item, dict)]
    if finding_ids != ["BM-F01", "BM-F02", "BM-F03", "BM-F04", "BM-F05"]:
        fail("audit findings are incomplete or out of order")
    for finding in findings:
        if not isinstance(finding, dict):
            fail("each finding must be an object")
        for key in ("severity", "category", "finding", "resolution"):
            if not str(finding.get(key) or "").strip():
                fail(f"finding {finding.get('id')} missing {key}")
        if not isinstance(finding.get("evidence"), list) or not finding["evidence"]:
            fail(f"finding {finding.get('id')} requires evidence")

    coverage = require_list(audit, "coverage_assessment", 12, "audit")
    actions = {str(item.get("action") or "") for item in coverage if isinstance(item, dict)}
    if not {"expand", "dedicated_unit", "integrate_with_biological_response", "cross_reference_only"}.issubset(actions):
        fail("coverage assessment does not encode all planned actions")

    architecture = require_list(audit, "recommended_architecture", 10, "audit")
    if len(architecture) != 10:
        fail("recommended architecture must contain exactly ten units")
    numbers = [item.get("unit") for item in architecture if isinstance(item, dict)]
    if numbers != list(range(1, 11)):
        fail("recommended architecture must be contiguous from 1 to 10")
    titles = [str(item.get("title") or "").strip() for item in architecture if isinstance(item, dict)]
    if titles != EXPECTED_RECOMMENDED_TITLES:
        fail("recommended architecture titles do not match the approved baseline")
    for item in architecture:
        if not isinstance(item, dict) or not isinstance(item.get("core_domains"), list) or len(item["core_domains"]) < 5:
            fail("each recommended unit requires at least five core domains")

    boundaries = audit.get("scope_boundaries")
    if not isinstance(boundaries, dict):
        fail("scope_boundaries missing")
    for key, minimum in (("included", 4), ("cross_reference", 4), ("excluded", 4)):
        value = boundaries.get(key)
        if not isinstance(value, list) or len(value) < minimum:
            fail(f"scope_boundaries.{key} is incomplete")

    decision = audit.get("editorial_decision")
    if not isinstance(decision, dict):
        fail("editorial_decision missing")
    expected_decision = {
        "baseline_audit_complete": True,
        "restructuring_authorized": True,
        "source_registry_authorized": True,
        "advanced_course_drafting_authorized": True,
        "public_replacement_authorized": False,
        "catalog_promotion_authorized": False,
        "human_review_executed": False,
        "disciplinary_review_complete": False,
    }
    for key, value in expected_decision.items():
        if decision.get(key) is not value:
            fail(f"editorial_decision.{key} must be {value}")

    next_gate = audit.get("next_gate")
    if not isinstance(next_gate, dict) or next_gate.get("name") != "biomateriales-architecture-and-source-registry":
        fail("next gate is not defined correctly")
    requirements = next_gate.get("requirements")
    if not isinstance(requirements, list) or len(requirements) < 5:
        fail("next gate requirements are incomplete")


def validate_report() -> None:
    if not REPORT.exists():
        fail("human-readable audit report is missing")
    text = REPORT.read_text(encoding="utf-8")
    required_markers = [
        "Auditoría base de Biomateriales",
        "Clases Biomateriales Yachay.pdf",
        "Arquitectura recomendada",
        "BM-F01",
        "BM-F05",
        "baseline_audit_complete: true",
        "public_replacement_authorized: false",
        "human_review_executed: false",
        "disciplinary_review_complete: false",
        "Siguiente gate",
    ]
    missing = [marker for marker in required_markers if marker not in text]
    if missing:
        fail("audit report is incomplete: " + ", ".join(missing))


def main() -> int:
    validate_source()
    validate_audit()
    validate_report()
    catalog = load_object(CATALOG)
    developed = isinstance(catalog.get("developed"), list) and "biomateriales" in catalog["developed"]
    print("OK: Biomateriales baseline evidence retained and internally validated")
    if developed:
        print("Current course is developed with six advanced units; expert review remains pending")
    else:
        print("Current course remains pending and placeholder; advanced drafting is authorized")
    print("Human and disciplinary review remain unexecuted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
