#!/usr/bin/env python3
"""Validate the internal scientific and editorial audit of Bioinstrumentation U1."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from build_bioinstrumentation_u1_authoral_unit import DEFAULT_SOURCE, build_unit

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = (
    ROOT
    / "data"
    / "course_audits"
    / "bioinstrumentacion"
    / "UNIT_01_SCIENTIFIC_EDITORIAL_AUDIT_2026-07-29.json"
)
REPORT_PATH = (
    ROOT
    / "docs"
    / "pilots"
    / "bioinstrumentacion"
    / "unit-01"
    / "INTERNAL_SCIENTIFIC_EDITORIAL_AUDIT.md"
)
PREPARATION_PATH = ROOT / "data" / "unit_preparation" / "bioinstrumentacion-unit-01.json"
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
EXPECTED_FINDINGS = {"SE-01", "SE-02", "SE-03", "SE-04", "SE-05", "SE-06"}
PROHIBITED_ANGLICISMS = re.compile(
    r"\b(submission|misconceptions?|dataset|display|offset)\b",
    re.IGNORECASE,
)


class AuditError(ValueError):
    """Raised when the audit contract or its corrections are incomplete."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuditError(f"missing file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise AuditError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise AuditError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def validate_audit_record() -> dict[str, Any]:
    audit = load_object(AUDIT_PATH)
    expected_identity = {
        "schema_version": "1.0",
        "audit_id": "bioinstrumentacion-u1-scientific-editorial-2026-07-29",
        "subject_id": "bioinstrumentacion",
        "unit": 1,
        "audit_type": "internal_scientific_editorial",
        "actor_type": "internal_ai_review_accepted_by_project_owner",
        "date": "2026-07-29",
        "status": "passed_with_corrections_applied",
    }
    for field, expected in expected_identity.items():
        require(audit.get(field) == expected, f"unexpected audit field {field}: {audit.get(field)!r}")

    findings = audit.get("findings")
    require(isinstance(findings, list), "audit findings must be a list")
    ids = {item.get("id") for item in findings if isinstance(item, dict)}
    require(ids == EXPECTED_FINDINGS, f"unexpected audit findings: {sorted(ids)}")
    for finding in findings:
        require(finding.get("status") == "resolved", f"unresolved finding: {finding.get('id')}")
        require(finding.get("severity") in {"major", "minor"}, f"invalid severity: {finding.get('id')}")
        paths = finding.get("corrected_paths")
        require(isinstance(paths, list) and paths, f"finding lacks corrected paths: {finding.get('id')}")
        for path_text in paths:
            path = ROOT / str(path_text)
            require(path.is_file(), f"corrected path does not exist: {path_text}")

    require(audit.get("unresolved_critical_findings") == 0, "critical findings remain open")
    require(audit.get("unresolved_major_findings") == 0, "major findings remain open")
    require(audit.get("external_professional_review") == "pending_human_review", "external review state changed")
    require(audit.get("cognitive_test") == "pending_human_execution", "cognitive test state changed")
    require(audit.get("inter_rater_round") == "pending_human_execution", "inter-rater state changed")
    require(audit.get("public_release_authorized") is False, "audit authorizes publication")
    require(audit.get("unit_developed") is False, "audit promotes the unit")
    require(audit.get("course_state") == "pending", "audit changes the course state")

    serialized = json.dumps(audit, ensure_ascii=False).casefold()
    for marker in (
        "no constituye revisión profesional externa",
        "no autoriza publicación",
        "no valida utilidad clínica",
    ):
        require(marker in serialized, f"audit limitation missing: {marker}")
    return audit


def resolve_source_links(unit: dict[str, Any]) -> None:
    sources = unit.get("sources")
    require(isinstance(sources, list), "unit sources are missing")
    source_ids = sorted(
        {str(item.get("id")) for item in sources if isinstance(item, dict) and item.get("id")},
        key=len,
        reverse=True,
    )
    require(len(source_ids) == 8, "expected eight directly verified source identifiers")

    preparation = load_object(PREPARATION_PATH)
    assertions = preparation.get("source_assertions")
    require(isinstance(assertions, list), "preparation source assertions are missing")
    claim_ids = {
        str(item.get("claim_id"))
        for item in assertions
        if isinstance(item, dict) and item.get("claim_id")
    }
    require(claim_ids == {"C1", "C2", "C3", "C4", "C5"}, "claim crosswalk is incomplete")

    unresolved: list[str] = []
    sections = unit.get("theory_sections")
    require(isinstance(sections, list) and len(sections) == 6, "six theory sections are required")
    for section_index, section in enumerate(sections, start=1):
        links = section.get("source_links") if isinstance(section, dict) else None
        require(isinstance(links, list) and links, f"section {section_index} lacks source links")
        for link in links:
            reference = str(link)
            if reference in claim_ids:
                continue
            if any(reference == source_id or reference.startswith(source_id + "-") for source_id in source_ids):
                continue
            unresolved.append(f"section {section_index}: {reference}")
    require(not unresolved, "unresolved source links: " + ", ".join(unresolved))


def validate_corrected_content(unit: dict[str, Any]) -> None:
    theory = unit["theory_sections"]
    theory_3 = " ".join(theory[2]["paragraphs"])
    theory_4 = " ".join(theory[3]["paragraphs"])
    theory_6 = " ".join(theory[5]["paragraphs"])

    require(
        "El operador, el procedimiento y las condiciones de ejecución pertenecen al proceso de medición" in theory_3,
        "system/process distinction is missing",
    )
    require(
        "no todo algoritmo que produce una salida biomédica es por ello un modelo de medición" in theory_4,
        "measurement-model correction is missing",
    )
    require(
        "sentido específico del VIM" in theory_4 and "uso más amplio del GUM" in theory_4,
        "VIM/GUM influence-quantity distinction is missing",
    )
    require(
        "necesaria y no suficiente" in theory_6,
        "fitness-for-purpose condition is still presented as sufficient",
    )
    equation_latex = str(theory[5].get("equations", [{}])[0].get("latex", ""))
    require(r"u_{\mathrm{objetivo}}" in equation_latex, "target uncertainty equation is missing")

    glossary = {item.get("term"): item.get("definition") for item in unit.get("glossary", [])}
    require("procedimiento" not in str(glossary.get("Sistema de medición", "")).casefold(), "system glossary still includes procedure")
    require("sentido más amplio" in str(glossary.get("Magnitud de influencia", "")), "influence glossary lacks GUM caveat")
    require("Parámetro no negativo" in str(glossary.get("Incertidumbre de medición", "")), "uncertainty definition is imprecise")

    connections = unit.get("biomedical_connections")
    ai_connection = next((item for item in connections if item.get("topic") == "IA clínica y modelos algorítmicos"), None)
    require(isinstance(ai_connection, dict), "AI biomedical connection is missing")
    require("No toda salida algorítmica es un valor medido" in ai_connection.get("limit", ""), "AI limit is incomplete")

    learner_files = [
        DEFAULT_SOURCE / "theory-03.json",
        DEFAULT_SOURCE / "theory-04.json",
        DEFAULT_SOURCE / "theory-06.json",
        DEFAULT_SOURCE / "examples.json",
        DEFAULT_SOURCE / "activities.json",
    ]
    for path in learner_files:
        text = path.read_text(encoding="utf-8")
        match = PROHIBITED_ANGLICISMS.search(text)
        require(match is None, f"unnecessary anglicism in {path.name}: {match.group(0) if match else ''}")


def validate_repository_state() -> None:
    statuses = load_object(STATUS_PATH)
    require("bioinstrumentacion" in set(statuses.get("pending", [])), "Bioinstrumentation must remain pending")
    require("bioinstrumentacion" not in set(statuses.get("developed", [])), "Bioinstrumentation was promoted")

    report = REPORT_PATH.read_text(encoding="utf-8")
    for marker in (
        "aprobada con correcciones aplicadas",
        "Hallazgos críticos sin resolver: **0**",
        "Revisión profesional externa: **pending_human_review**",
        "Publicación: **bloqueada**",
    ):
        require(marker in report, f"audit report lacks marker: {marker}")


def main() -> int:
    try:
        validate_audit_record()
        unit = build_unit(DEFAULT_SOURCE)
        resolve_source_links(unit)
        validate_corrected_content(unit)
        validate_repository_state()
    except (OSError, TypeError, json.JSONDecodeError, AuditError, ValueError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    print("OK Bioinstrumentation U1 internal scientific and editorial audit")
    print("6 resolved findings · 0 critical open · 0 major open")
    print("course pending · publication blocked · external professional review pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
