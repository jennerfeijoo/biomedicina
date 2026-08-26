import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/interfaces-hombre-maquina/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/interfaces-hombre-maquina/unit-06.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/interfaces-hombre-maquina.json"
PUBLIC = ROOT / "ingenieria-biomedica/interfaces-hombre-maquina/unidades/unidad-06.html"
CATALOG = ROOT / "data/catalog_statuses.json"

GENERIC = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Interfaces avanzadas",
    "\\mathrm{SNR}_{dB}=10\\log_{10}",
    "señal cruda, función de transferencia, calibración, espectro",
    "entrada patrón, cortocircuito o cero",
    "expediente de cadena de señal",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def text():
    return json.dumps(load(SOURCE), ensure_ascii=False).lower()


def test_source_and_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_06_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 6
    assert data["slug"] == "interfaces-avanzadas"
    corpus = text()
    for marker in GENERIC:
        assert marker.lower() not in corpus
    for concept in [
        "multimodalidad", "fallback", "iso 9241-920:2024", "iso 9241-960:2017",
        "falsa aceptación", "falso rechazo", "discoverability", "háptica",
        "sincronización", "registro espacial", "error de registro", "tracking",
        "webxr", "xaur", "motion-agnostic", "cybersickness"
    ]:
        assert concept in corpus


def test_unit_06_protects_multimodal_distinctions():
    corpus = text()
    assert "reconocer una entrada no equivale a comprender correctamente la intención" in corpus
    assert "presencia e inmersión no son pruebas de exactitud geométrica" in corpus
    assert "desempeño con háptica no demuestra por sí solo beneficio terapéutico" in corpus
    assert "candidate recommendation draft" in corpus
    assert "xaur" in corpus and "no es un estándar normativo" in corpus
    assert "no existe una modalidad ganadora" in corpus
    assert "no demuestra rehabilitación efectiva" in corpus
    assert "no demuestra competencia clínica real" in corpus


def test_unit_06_integrates_previous_units():
    corpus = text()
    for marker in ["u1", "u2", "u3", "u4", "u5"]:
        assert marker in corpus
    assert "los principios de u1-u5 permanecen vigentes" in corpus


def test_unit_06_has_sufficient_depth():
    data = load(SOURCE)
    assert len(data["learning_objectives"]) >= 6
    assert len(data["theory_sections"]) >= 5
    for section in data["theory_sections"]:
        assert len(section["paragraphs"]) >= 5
        assert len(section["key_points"]) >= 5
        assert all(len(point.split()) >= 4 for point in section["key_points"])
    assert len(data["glossary"]) >= 45
    assert len(data["worked_examples"]) >= 5
    activity = data["guided_activities"][0]
    assert activity["estimated_time_minutes"] >= 420
    assert len(activity["problems"]) >= 20
    assert len(activity["deliverables"]) >= 10
    assert len(activity["checking_criteria"]) >= 20
    assert len(data["common_errors"]) >= 18
    assert len(data["self_assessment"]) >= 12
    assert len(data["biomedical_connections"]) >= 6
    assert len(data["sources"]) >= 16


def test_unit_06_uses_current_authoritative_sources():
    urls = {s["url"] for s in load(SOURCE)["sources"]}
    required = {
        "https://www.iso.org/standard/80751.html",
        "https://www.iso.org/standard/62535.html",
        "https://www.w3.org/TR/webxr/",
        "https://www.w3.org/TR/xaur/",
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
        "https://pubmed.ncbi.nlm.nih.gov/40253724/",
        "https://pubmed.ncbi.nlm.nih.gov/40091919/",
    }
    assert required.issubset(urls)


def test_unit_06_uses_modality_metrics_not_snr():
    data = load(SOURCE)
    corpus = json.dumps(data, ensure_ascii=False)
    assert "SNR" not in corpus
    assert "función de transferencia" not in corpus.lower()
    equations = [eq["latex"] for section in data["theory_sections"] for eq in section.get("equations", [])]
    assert any("FAR" in eq for eq in equations)
    assert any("FRR" in eq for eq in equations)
    assert any("sync" in eq for eq in equations)
    assert any("e_{reg}" in eq for eq in equations)


def test_published_state_when_promoted():
    if not DESCRIPTOR.exists() or not PUBLIC.exists():
        return
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 6)
    if detail["description"] != source["purpose"]:
        return
    public_text = PUBLIC.read_text(encoding="utf-8").lower()
    assert source["purpose"].lower() in public_text
    for marker in ["multimodalidad", "fallback", "webxr", "registro espacial", "háptica"]:
        assert marker in public_text
    for carryover in ["snr", "función de transferencia", "cortocircuito", "concepto de la unidad que debe definirse"]:
        assert carryover not in public_text
    if CATALOG.exists():
        catalog = load(CATALOG)
        templates = catalog["dimensions"]["specificity"]["template_detected"]
        assert "interfaces-hombre-maquina" not in templates


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
