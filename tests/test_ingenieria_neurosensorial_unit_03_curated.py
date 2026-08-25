import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/ingenieria-neurosensorial/units/unit-03.json"
MIRROR = ROOT / "data/generated_units/ingenieria-neurosensorial/unit-03.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/ingenieria-neurosensorial.json"
PUBLIC = ROOT / "ingenieria-biomedica/ingenieria-neurosensorial/unidades/unidad-03.html"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Estimulación",
    "\\mathrm{SNR}_{dB}=10\\log_{10}",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_03_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 3
    assert data["slug"] == "estimulacion"
    assert data["title"] == "Estimulación"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "ley de faraday", "campo eléctrico", "tes", "tms", "fem",
        "duty cycle", "sham", "hotspot", "artefacto de estimulación",
        "riesgo residual", "guía de consenso"
    ]:
        assert concept in text


def test_unit_03_protects_core_stimulation_distinctions():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "parámetro programado del estímulo físico realmente entregado" in text
    assert "no predicen por sí solos excitación, inhibición o plasticidad" in text
    assert "un campo escalar máximo no determina qué población neuronal se activa" in text
    assert "una guía de consenso es evidencia de referencia, no autorización automática" in text
    assert "el efecto fisiológico, la eficacia funcional y la utilidad clínica son niveles diferentes" in text
    assert "no se proporcionan dosis humanas" in text


def test_unit_03_keeps_human_stimulation_out_of_scope():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "no acredita competencia para operar estimuladores" in text
    assert "no se proporcionan dosis humanas, límites operativos" in text
    assert "no se procesan imágenes clínicas ni se optimizan dosis individuales" in text
    assert "reserva prótesis sensoriales para u4" in text
    assert "validación centrada en la persona" in text
    assert "u6" in text


def test_unit_03_has_sufficient_academic_and_pedagogical_depth():
    data = load(SOURCE)
    assert len(data["learning_objectives"]) >= 6
    assert len(data["theory_sections"]) >= 5
    for section in data["theory_sections"]:
        assert len(section["paragraphs"]) >= 5
        assert len(section["key_points"]) >= 5
        assert all(len(point.split()) >= 4 for point in section["key_points"])
    assert len(data["glossary"]) >= 40
    assert len(data["worked_examples"]) >= 5
    activity = data["guided_activities"][0]
    assert activity["estimated_time_minutes"] >= 360
    assert len(activity["instructions"]) >= 8
    assert len(activity["problems"]) >= 20
    assert len(activity["deliverables"]) >= 8
    assert len(activity["checking_criteria"]) >= 20
    assert len(data["common_errors"]) >= 15
    assert len(data["self_assessment"]) >= 12
    assert len(data["biomedical_connections"]) >= 6
    assert len(data["sources"]) >= 14


def test_unit_03_quantitative_models_are_physical_and_bounded():
    data = load(SOURCE)
    equations = [eq for section in data["theory_sections"] for eq in section.get("equations", [])]
    latex = " ".join(eq["latex"] for eq in equations)
    meanings = " ".join(eq["meaning"] for eq in equations).lower()
    assert "\\mathcal{E}" in latex
    assert "\\mathbf{J}" in latex
    assert "Q=" in latex
    assert "D=" in latex
    assert "\\nabla\\cdot" in latex
    assert "\\mathbf{E}=-\\nabla V" in latex
    assert "SNR" not in latex
    assert "no calcula parámetros seguros ni eficaces" in meanings
    assert "no proporciona umbrales de carga ni valores de aplicación humana" in meanings
    assert "no predice por sí solo respuesta neural ni seguridad" in meanings


def test_unit_03_uses_verified_stimulation_sources():
    data = load(SOURCE)
    urls = {s["url"] for s in data["sources"]}
    required = {
        "https://pubmed.ncbi.nlm.nih.gov/33243615/",
        "https://pubmed.ncbi.nlm.nih.gov/41622107/",
        "https://pubmed.ncbi.nlm.nih.gov/31487695/",
        "https://pubmed.ncbi.nlm.nih.gov/35421514/",
        "https://pubmed.ncbi.nlm.nih.gov/25767458/",
        "https://simnibs.github.io/simnibs/build/html/index.html",
    }
    assert required.issubset(urls)


def test_unit_03_publication_matches_canonical_source():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 3)
    assert detail["description"] == source["purpose"]
    assert PUBLIC.exists()
    public_text = PUBLIC.read_text(encoding="utf-8").lower()
    for marker in ["ley de faraday", "duty cycle", "riesgo residual", "hotspot", "sham"]:
        assert marker in public_text
    for forbidden in [
        "concepto de la unidad que debe definirse mediante entidades observables",
        "modelo conceptual de estimulación",
    ]:
        assert forbidden not in public_text


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
