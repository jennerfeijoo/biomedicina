import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/ingenieria-neurosensorial/units/unit-04.json"
MIRROR = ROOT / "data/generated_units/ingenieria-neurosensorial/unit-04.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/ingenieria-neurosensorial.json"
PUBLIC = ROOT / "ingenieria-biomedica/ingenieria-neurosensorial/unidades/unidad-04.html"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_unit_04_source_and_generated_mirror_are_identical():
    assert SOURCE.read_text(encoding="utf-8") == MIRROR.read_text(encoding="utf-8")


def test_unit_04_is_disciplinary_not_generic_template():
    unit = load(SOURCE)
    text = SOURCE.read_text(encoding="utf-8").lower()
    assert unit["unit"] == 4
    assert unit["slug"] == "protesis-sensoriales"
    assert len(unit["learning_objectives"]) >= 6
    assert len(unit["theory_sections"]) >= 5
    for section in unit["theory_sections"]:
        assert len(section.get("paragraphs", [])) >= 6
        assert len(section.get("key_points", [])) >= 6
    for forbidden in [
        "concepto de la unidad que debe definirse mediante entidades observables",
        "modelo conceptual de prótesis sensoriales",
        "\\mathrm{snr}_{db}",
    ]:
        assert forbidden not in text


def test_unit_04_preserves_core_sensory_prosthesis_distinctions():
    text = SOURCE.read_text(encoding="utf-8").lower()
    for marker in [
        "implante coclear",
        "no restaura audición normal",
        "fosfeno",
        "visión protésica simulada",
        "prótesis somatosensorial",
        "lazo cerrado",
        "matriz de confusión",
        "curva de aprendizaje",
        "embodiment",
        "canal físico",
        "canal funcional",
    ]:
        assert marker in text
    assert "contar electrodos no equivale a medir resolución sensorial" in text
    assert "número de electrodos" in text and "agudeza visual" in text
    assert "canales" in text and "independientes" in text
    assert "cuadrícula perfecta" in text and "no una predicción" in text


def test_unit_04_has_substantial_pedagogy_and_assessment():
    unit = load(SOURCE)
    assert len(unit["glossary"]) >= 50
    assert len(unit["worked_examples"]) >= 5
    assert len(unit["guided_activities"]) >= 1
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


def test_unit_04_keeps_curricular_and_clinical_boundaries():
    unit = load(SOURCE)
    text = SOURCE.read_text(encoding="utf-8").lower()
    scope = (unit.get("professional_scope", "") + " " + unit.get("editorial_notice", "")).lower()
    assert "u3" in text and "u5" in text and "u6" in text
    for marker in ["program", "cirug", "parámetros", "clínic"]:
        assert marker in scope
    assert "usuarios virtuales" in text or "sintétic" in text
    assert "no especifica sitios, intensidades, formas de pulso ni procedimientos invasivos" in text
    assert "no programan implantes" in text


def test_unit_04_uses_verified_sources_for_all_three_modalities():
    unit = load(SOURCE)
    assert all(source.get("verification_status") == "verified_directly" for source in unit["sources"])
    urls = " ".join(source["url"].lower() for source in unit["sources"])
    assert "nidcd.nih.gov" in urls
    assert "pubmed.ncbi.nlm.nih.gov" in urls
    text = " ".join((source["title"] + " " + source.get("used_for", "")).lower() for source in unit["sources"])
    assert "coclear" in text
    assert "visual" in text or "retinal" in text
    assert "somatos" in text or "sensory feedback" in text


def test_unit_04_publication_matches_canonical_source():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 4)
    assert detail["description"] == source["purpose"]
    assert PUBLIC.exists()
    public_text = PUBLIC.read_text(encoding="utf-8").lower()
    for marker in ["implante coclear", "fosfeno", "lazo cerrado", "matriz de confusión"]:
        assert marker in public_text
    assert "concepto de la unidad que debe definirse mediante entidades observables" not in public_text
