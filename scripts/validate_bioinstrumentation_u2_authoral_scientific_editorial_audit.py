#!/usr/bin/env python3
"""Validate the internal scientific/editorial audit of Bioinstrumentation Unit 2."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/course_audits/bioinstrumentacion/UNIT_02_AUTHORAL_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-30.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-02.json"
SOURCE_DIR = ROOT / "data/course_redevelopment/bioinstrumentacion/unit-02-source"
REPORT = ROOT / "docs/pilots/bioinstrumentacion/unit-02/AUTHORAL_SCIENTIFIC_EDITORIAL_AUDIT.md"
STATUS = ROOT / "data/catalog_statuses.json"
DECISION = ROOT / "data/review_evidence/bioinstrumentacion-unit-02-disciplinary-review.json"
MANIFEST = ROOT / "data/review_evidence/bioinstrumentacion-unit-02-review-packet.json"
EXPECTED_FINDINGS = {f"U2-AUTH-SE-{number:02d}" for number in range(1, 7)}
EXPECTED_COMPONENTS = {"NTCLG100E2103JB", "CEA-06-125UNA-350", "S5821-03"}
EXPECTED_PRACTICES = {"U2-P1", "U2-P2", "U2-P3"}
EXPECTED_ASSESSMENTS = {"U2-A1", "U2-A2", "U2-A3", "U2-A4", "U2-A5"}
WORD_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_audit() -> None:
    audit = load(AUDIT)
    expected = {
        "schema_version": "1.0",
        "audit_id": "bioinstrumentacion-u2-authoral-scientific-editorial-2026-07-30",
        "subject_id": "bioinstrumentacion",
        "unit": 2,
        "unit_path": str(UNIT.relative_to(ROOT)),
        "source_dir": str(SOURCE_DIR.relative_to(ROOT)),
        "reviewed_commit": "c1e0c304749563223620103548c9ffdd11e89db7",
        "audit_type": "internal_scientific_editorial_authoral",
        "actor_type": "internal_ai_review_accepted_by_project_owner",
        "date": "2026-07-30",
        "status": "passed_internal_review",
        "unresolved_critical_findings": 0,
        "unresolved_major_findings": 0,
        "external_professional_review": "pending_human_review",
        "student_cognitive_test": "pending_human_execution",
        "feedback_usability_review": "pending_human_execution",
        "inter_rater_round": "pending_human_execution",
        "public_release_authorized": False,
        "unit_developed": False,
        "course_state": "pending",
    }
    for key, wanted in expected.items():
        require(audit.get(key) == wanted, f"audit field changed: {key}")
    findings = audit.get("findings")
    require(isinstance(findings, list) and len(findings) == 6, "six audit findings required")
    require({row.get("id") for row in findings if isinstance(row, dict)} == EXPECTED_FINDINGS, "audit finding ids changed")
    for row in findings:
        require(row.get("severity") in {"major", "minor"}, f"invalid severity: {row.get('id')}")
        require(row.get("status") == "resolved", f"unresolved finding: {row.get('id')}")
        paths = row.get("corrected_paths")
        require(isinstance(paths, list) and paths, f"finding lacks paths: {row.get('id')}")
        for path in paths:
            require((ROOT / str(path)).is_file(), f"audit path missing: {path}")
    limits = " ".join(map(str, audit.get("limitations", []))).casefold()
    for marker in ("no constituye revisión profesional", "prueba cognitiva", "seguridad", "no autoriza publicación"):
        require(marker in limits, f"audit limitation missing: {marker}")


def validate_unit() -> None:
    unit = load(UNIT)
    require(unit.get("schema_version") == "2.0" and unit.get("unit") == 2, "canonical Unit 2 identity changed")
    require(unit.get("status") == "review", "Unit 2 is no longer an internal review draft")
    sections = unit.get("theory_sections")
    require(isinstance(sections, list) and len(sections) == 6, "six theory sections required")
    theory = " ".join(" ".join(map(str, row.get("paragraphs", []))) for row in sections if isinstance(row, dict))
    require(len(WORD_RE.findall(theory)) >= 2200, "authoral theory density fell below 2200 words")
    folded = theory.casefold()
    for marker in (
        "sensor", "transductor", "interfaz", "sistema", "sensibilidad", "resolución", "selectividad",
        "saturación", "zona muerta", "histéresis", "carga eléctrica", "térmica", "mecánica", "óptica",
        "primer orden", "constante de tiempo", "tiempo de respuesta", "retardo", "−3 db", "utilidad clínica",
    ):
        require(marker in folded, f"audited scientific marker disappeared: {marker}")
    require("63,2" in theory or "63.2" in theory, "first-order 63.2 percent checkpoint is missing")
    require("modelo simple declarado" in folded, "dynamic rejection scope is no longer limited")
    require("modelo compuesto" in folded, "composite-model caveat is missing")

    examples = unit.get("worked_examples")
    require(isinstance(examples, list) and len(examples) == 3, "three worked examples required")
    serialized = json.dumps(examples, ensure_ascii=False)
    for component in EXPECTED_COMPONENTS:
        require(component in serialized, f"component disappeared from audited examples: {component}")

    practices = unit.get("executable_practices")
    require({row.get("id") for row in practices if isinstance(row, dict)} == EXPECTED_PRACTICES, "practice alignment changed")
    assessments = unit.get("assessment_alignment")
    require({row.get("id") for row in assessments if isinstance(row, dict)} == EXPECTED_ASSESSMENTS, "assessment alignment changed")
    require(len(unit.get("common_errors", [])) == 12, "twelve misconceptions required")
    require(len(unit.get("self_assessment", [])) == 12, "twelve self-assessment questions required")
    require(len(unit.get("glossary", [])) == 20, "twenty glossary terms required")
    require(len(unit.get("sources", [])) == 12, "twelve localized sources required")

    review = unit.get("review_state")
    require(isinstance(review, dict), "review state is missing")
    require(review.get("external_professional_review") == "pending_human_review", "external review was fabricated")
    require(review.get("public_release") is False, "public release was authorized")
    require(review.get("unit_developed") is False, "unit was promoted")


def validate_repository_state() -> None:
    statuses = load(STATUS)
    require("bioinstrumentacion" in set(statuses.get("pending", [])), "Bioinstrumentation must remain pending")
    require("bioinstrumentacion" not in set(statuses.get("developed", [])), "Bioinstrumentation was promoted")
    require(not DECISION.exists() and not MANIFEST.exists(), "audit fabricated external review evidence")
    report = REPORT.read_text(encoding="utf-8")
    for marker in (
        "audit_status: passed_internal_review",
        "resolved_findings: 6",
        "pending_human_review",
        "public_release_authorized: false",
        "unit_developed: false",
        "course_state: pending",
        "no constituye revisión disciplinar profesional",
    ):
        require(marker in report, f"audit report lacks marker: {marker}")


def main() -> int:
    try:
        validate_audit()
        validate_unit()
        validate_repository_state()
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK Bioinstrumentation U2 authoral scientific and editorial audit")
    print("6 resolved findings · 0 critical open · 0 major open")
    print("course pending · publication blocked · external professional review pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
