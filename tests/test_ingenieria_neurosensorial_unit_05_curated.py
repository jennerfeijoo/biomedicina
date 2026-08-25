from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/ingenieria-neurosensorial/units/unit-05.json"
MIRROR = ROOT / "data/generated_units/ingenieria-neurosensorial/unit-05.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/ingenieria-neurosensorial.json"
PUBLIC = ROOT / "ingenieria-biomedica/ingenieria-neurosensorial/unidades/unidad-05.html"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_mirror_are_identical():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_u5_identity_and_template_are_correct():
    unit = load(SOURCE)
    text = SOURCE.read_text(encoding="utf-8").casefold()
    assert unit["unit"] == 5
    assert unit["slug"] == "interfaces-y-decodificacion"
    assert GENERIC not in text
    assert r"\mathrm{snr}_{db}=10\log_{10}" not in text


def test_u5_has_disciplinary_decoding_structure():
    unit = load(SOURCE)
    sections = unit["theory_sections"]
    assert len(sections) == 5
    for section in sections:
        assert len(section["paragraphs"]) >= 6
        assert len(section["key_points"]) >= 6
        assert all(len(point.split()) >= 5 for point in section["key_points"])
    headings = " ".join(section["heading"] for section in sections).casefold()
    for concept in ("representación", "partición", "métricas", "control online", "no estacionariedad"):
        assert concept in headings


def test_u5_protects_generalization_and_leakage_distinctions():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "within-session",
        "cross-session",
        "cross-subject",
        "data leakage",
        "normalizar con media/desviación calculadas sobre todos los datos",
        "validación cruzada anidada",
        "ventanas solapadas",
        "ajustarse únicamente con el conjunto de entrenamiento",
    ):
        assert phrase in text
    assert "responden preguntas distintas" in text


def test_u5_separates_offline_score_from_control_utility():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "estado idle",
        "rechazo",
        "falsos comandos por minuto",
        "latencia end-to-end",
        "pseudo-online",
        "desempeño funcional",
    ):
        assert phrase in text
    assert "accuracy offline no equivale a control online útil" in text
    assert "una mejora de balanced accuracy que empeora latencia" in text


def test_u5_bounds_itr_and_probability_interpretation():
    unit = load(SOURCE)
    text = SOURCE.read_text(encoding="utf-8").casefold()
    assert "information transfer rate" in text
    assert "canal estable y sin memoria" in text
    assert "no debe usarse como única medida de utilidad bci" in text
    assert "probabilidades de un clasificador no siempre están calibradas" in text
    equations = [eq for section in unit["theory_sections"] for eq in section.get("equations", [])]
    latex = " ".join(eq["latex"] for eq in equations)
    assert "BAcc" in latex
    assert "\\log_2N" in latex


def test_u5_adaptation_requires_independent_future_evaluation():
    text = SOURCE.read_text(encoding="utf-8").casefold()
    for phrase in (
        "baseline congelado",
        "transferencia negativa",
        "co-adaptación",
        "rollback",
        "datos posteriores no usados para actualizar",
    ):
        assert phrase in text
    assert "adaptar y evaluar sobre las mismas observaciones produce una estimación circular" in text


def test_u5_pedagogical_depth_and_safe_lab():
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
    assert "no adquirir señales de personas" in joined
    assert "no se controla hardware médico" in joined
    assert "u6 queda reservada" in joined


def test_u5_sources_cover_benchmark_leakage_metrics_and_adaptation():
    unit = load(SOURCE)
    assert all(source.get("verification_status") == "verified_directly" for source in unit["sources"])
    urls = {source["url"] for source in unit["sources"]}
    required = {
        "https://moabb.neurotechx.com/docs/index.html",
        "https://pubmed.ncbi.nlm.nih.gov/38765672/",
        "https://pubmed.ncbi.nlm.nih.gov/27845666/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC4185283/",
        "https://pubmed.ncbi.nlm.nih.gov/40425023/",
    }
    assert required.issubset(urls)


def test_u5_professional_boundary_is_explicit():
    unit = load(SOURCE)
    text = (unit["professional_scope"] + " " + unit["editorial_notice"]).casefold()
    for phrase in (
        "no acredita competencia",
        "controlar dispositivos médicos o prótesis reales",
        "no equivale a control online útil",
        "adaptación evaluada sobre los mismos datos",
        "u5 reutiliza u2 y u4",
        "u6",
    ):
        assert phrase in text


def test_u5_publication_matches_after_promotion():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(unit for unit in descriptor["detailed_units"] if unit["unit"] == 5)
    assert detail["description"] == source["purpose"]
    assert PUBLIC.exists()
    public = PUBLIC.read_text(encoding="utf-8").casefold()
    for marker in ("data leakage", "cross-subject", "estado idle", "baseline congelado", "information transfer rate"):
        assert marker in public
    assert GENERIC not in public


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
