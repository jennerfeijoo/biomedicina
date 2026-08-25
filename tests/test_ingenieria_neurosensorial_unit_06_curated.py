from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/ingenieria-neurosensorial/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/ingenieria-neurosensorial/unit-06.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/ingenieria-neurosensorial.json"
PUBLIC = ROOT / "ingenieria-biomedica/ingenieria-neurosensorial/unidades/unidad-06.html"
CATALOG = ROOT / "data/catalog_statuses.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_mirror_are_identical():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_u6_identity_and_template_are_correct():
    unit = load(SOURCE)
    text = SOURCE.read_text(encoding="utf-8").casefold()
    assert unit["unit"] == 6
    assert unit["slug"] == "validacion-y-neuroetica"
    assert GENERIC not in text
    assert r"\mathrm{snr}_{db}=10\log_{10}" not in text


def test_u6_has_person_centered_neuroethics_structure():
    unit = load(SOURCE)
    sections = unit["theory_sections"]
    assert len(sections) == 5
    for section in sections:
        assert len(section["paragraphs"]) >= 6
        assert len(section["key_points"]) >= 6
        assert all(len(point.split()) >= 5 for point in section["key_points"])
    headings = " ".join(section["heading"] for section in sections).casefold()
    for concept in ("validación centrada", "plasticidad", "autonomía", "privacidad", "gobernanza"):
        assert concept in headings


def test_u6_separates_technical_performance_from_person_centered_value():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "desempeño técnico",
        "desempeño funcional",
        "usabilidad",
        "workload",
        "contexto de uso",
        "criterios principales",
        "baseline",
    ):
        assert phrase in text
    assert "accuracy, latencia o itr no sustituyen" in text


def test_u6_does_not_equate_longitudinal_improvement_with_plasticity():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "mejora longitudinal no demuestra plasticidad neural",
        "co-adaptación",
        "baseline congelado",
        "retención",
        "no-identificabilidad",
    ):
        assert phrase in text
    assert "adaptar y evaluar sobre las mismas observaciones vuelve circular" in text


def test_u6_operationalizes_autonomy_and_user_control():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "shared control",
        "override",
        "undo",
        "consentimiento continuo",
        "matriz de autoridad",
        "un comando emitido por el sistema no prueba",
    ):
        assert phrase in text


def test_u6_maps_neural_data_privacy_without_overclaiming_anonymity():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "minimización",
        "uso secundario",
        "seudonimización",
        "reidentificación",
        "linkage",
        "threat model",
    ):
        assert phrase in text
    assert "no equivale a anonimización" in text


def test_u6_requires_subgroup_accessibility_and_lifecycle_governance():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "subgrupos sintéticos",
        "accesibilidad",
        "matriz raci",
        "monitoreo posterior",
        "change control",
        "criterios de retirada",
    ):
        assert phrase in text
    assert "no prueba por sí sola discriminación" in text


def test_u6_pedagogical_depth_and_safe_project():
    unit = load(SOURCE)
    assert len(unit["learning_objectives"]) >= 6
    assert len(unit["glossary"]) >= 50
    assert len(unit["worked_examples"]) >= 5
    activity = unit["guided_activities"][0]
    assert activity["estimated_time_minutes"] >= 480
    assert len(activity["instructions"]) >= 10
    assert len(activity["problems"]) >= 24
    assert len(activity["deliverables"]) >= 12
    assert len(activity["checking_criteria"]) >= 25
    assert len(unit["common_errors"]) >= 18
    assert len(unit["self_assessment"]) >= 12
    assert len(unit["biomedical_connections"]) >= 6
    assert len(unit["sources"]) >= 17
    joined = " ".join(activity["instructions"] + activity["checking_criteria"]).casefold()
    assert "no reclutar personas" in joined
    assert "no se realizan pruebas con personas" in joined
    assert "aprobación ética" in joined


def test_u6_sources_cover_current_governance_user_centered_and_privacy_frameworks():
    unit = load(SOURCE)
    assert all(source.get("verification_status") == "verified_directly" for source in unit["sources"])
    urls = {source["url"] for source in unit["sources"]}
    required = {
        "https://www.unesco.org/en/legal-affairs/recommendation-ethics-neurotechnology",
        "https://www.oecd.org/en/topics/sub-issues/neurotechnology.html",
        "https://www.braininitiative.nih.gov/vision/nih-brain-initiative-reports/brain-20-neuroethics-enabling-and-enhancing-neuroscience",
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/implanted-brain-computer-interface-bci-devices-patients-paralysis-or-amputation-non-clinical-testing",
        "https://pubmed.ncbi.nlm.nih.gov/38903409/",
        "https://pubmed.ncbi.nlm.nih.gov/39006157/",
        "https://pubmed.ncbi.nlm.nih.gov/42509357/",
    }
    assert required.issubset(urls)


def test_u6_professional_boundary_is_explicit():
    unit = load(SOURCE)
    text = (unit["professional_scope"] + " " + unit["editorial_notice"]).casefold()
    for phrase in (
        "no acredita competencia",
        "no sustituyen aprobación ética",
        "no equivalen a beneficio centrado en la persona",
        "no prueba intención",
        "seudonimización no garantiza anonimato",
        "no como certificación",
    ):
        assert phrase in text


def test_u6_publication_matches_after_promotion():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(unit for unit in descriptor["detailed_units"] if unit["unit"] == 6)
    assert detail["description"] == source["purpose"]
    assert PUBLIC.exists()
    public = PUBLIC.read_text(encoding="utf-8").casefold()
    for marker in ("validación centrada", "co-adaptación", "shared control", "seudonimización", "monitoreo posterior"):
        assert marker in public
    assert GENERIC not in public


def test_u6_course_is_closed_in_editorial_catalog():
    catalog = load(CATALOG)
    template = set(catalog["dimensions"]["specificity"]["template_detected"])
    screened = set(catalog["dimensions"]["specificity"]["screened_no_known_template_marker"])
    assert "ingenieria-neurosensorial" not in template
    assert "ingenieria-neurosensorial" in screened


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
