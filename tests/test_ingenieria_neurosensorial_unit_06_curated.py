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
    assert "por completar" not in text
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
    for concept in (
        "validación multinivel",
        "plasticidad",
        "autonomía",
        "neurodatos",
        "validación responsable",
    ):
        assert concept in headings


def test_u6_separates_technical_functional_user_and_clinical_layers():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "desempeño técnico",
        "desempeño funcional",
        "experiencia de usuario",
        "beneficio clínico",
        "contexto de uso",
        "métricas primarias/secundarias",
        "datos subjetivos y objetivos",
    ):
        assert phrase in text
    assert "ninguna de estas capas demuestra por sí sola beneficio clínico" in text


def test_u6_does_not_equate_longitudinal_improvement_with_plasticity():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "co-adaptación",
        "plasticidad neural",
        "baseline congelado",
        "retención y transferencia",
        "fatiga o frustración",
        "hipótesis alternativas",
    ):
        assert phrase in text
    assert "mejor desempeño longitudinal no demuestra por sí solo plasticidad neural" in text
    assert "no se deduce automáticamente de una curva de aprendizaje ni de mayor accuracy" in text


def test_u6_operationalizes_autonomy_agency_and_shared_control():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "control compartido",
        "iniciar, modificar, confirmar, rechazar y detener",
        "override",
        "parada accesible",
        "consentimiento",
        "participación significativa",
    ):
        assert phrase in text
    assert "discapacidad no implica incapacidad decisoria" in text
    assert "autonomía y agencia no pueden reducirse a precisión" in text


def test_u6_maps_neural_data_privacy_and_secondary_use_without_overclaiming():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "minimización",
        "uso secundario",
        "seudonimización",
        "reidentificación",
        "modelos, apis y logs",
        "propósito",
        "retención",
        "canal de reclamación",
    ):
        assert phrase in text
    assert "seudonimizar no equivale a anonimizar" in text
    assert "no debe asumirse que el consentimiento original lo cubre" in text


def test_u6_requires_equity_accessibility_change_control_and_traceability():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "análisis por subgrupos",
        "accesibilidad",
        "quién pudo participar",
        "análisis de impacto",
        "matriz afirmación",
        "trazabilidad",
        "riesgos, controles y cambios",
    ):
        assert phrase in text
    assert "cuando no, declara la ausencia como limitación en lugar de afirmar equidad" in text


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
    boundary = (unit["professional_scope"] + " " + unit["editorial_notice"]).casefold()
    for phrase in (
        "exclusivamente sintéticos",
        "no acredita competencia",
        "no incluyen personas",
        "dispositivos reales",
        "neuroestimulación",
        "decisiones clínicas",
    ):
        assert phrase in boundary


def test_u6_sources_cover_current_governance_clinical_and_bci_frameworks():
    unit = load(SOURCE)
    assert all(source.get("verification_status") == "verified_directly" for source in unit["sources"])
    urls = {source["url"] for source in unit["sources"]}
    required = {
        "https://www.unesco.org/en/legal-affairs/recommendation-ethics-neurotechnology?hub=66535",
        "https://www.unesco.org/en/node/86248",
        "https://www.oecd.org/en/topics/sub-issues/neurotechnology.html",
        "https://legalinstruments.oecd.org/api/print?ids=658&Lang=en",
        "https://www.braininitiative.nih.gov/vision/nih-brain-initiative-reports/brain-20-neuroethics-enabling-and-enhancing-neuroscience",
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/implanted-brain-computer-interface-bci-devices-patients-paralysis-or-amputation-non-clinical-testing",
        "https://www.wma.net/what-we-do/medical-ethics/declaration-of-helsinki/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC4185283/",
    }
    assert required.issubset(urls)


def test_u6_professional_boundary_is_explicit():
    unit = load(SOURCE)
    text = (unit["professional_scope"] + " " + unit["editorial_notice"]).casefold()
    for phrase in (
        "no acredita competencia",
        "no convierte resultados educativos en evidencia clínica",
        "mejora longitudinal no demuestra plasticidad",
        "autonomía y agencia no se infieren de accuracy",
        "seudonimización no equivale a anonimización",
        "no sustituye ley, comité de ética ni regulación aplicable",
    ):
        assert phrase in text


def test_u6_publication_matches_when_promotion_is_present():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(unit for unit in descriptor["detailed_units"] if unit["unit"] == 6)
    if detail["description"] == source["purpose"] and PUBLIC.exists():
        public = PUBLIC.read_text(encoding="utf-8").casefold()
        for marker in (
            "validación multinivel",
            "co-adaptación",
            "control compartido",
            "seudonimización",
            "equidad",
        ):
            assert marker in public
        assert GENERIC not in public


def test_u6_catalog_closure_when_editorial_status_is_synchronized():
    catalog = load(CATALOG)
    template = set(catalog["specificity"]["template_detected"])
    if "ingenieria-neurosensorial" not in template:
        screened = set(catalog["specificity"]["screened_no_known_template_marker"])
        assert "ingenieria-neurosensorial" in screened


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
