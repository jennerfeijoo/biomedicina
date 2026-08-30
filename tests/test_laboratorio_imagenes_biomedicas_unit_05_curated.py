import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/laboratorio-imagenes-biomedicas/units/unit-05.json"
MIRROR = ROOT / "data/generated_units/laboratorio-imagenes-biomedicas/unit-05.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def corpus(data):
    return json.dumps(data, ensure_ascii=False).lower()


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_05_is_registration_specific_and_template_free():
    data = load(SOURCE)
    text = corpus(data)
    assert data["unit"] == 5
    assert data["slug"] == "registro-y-mediciones"
    assert data["title"] == "Registro espacial y medición longitudinal reproducible"
    assert "concepto de la unidad que debe definirse" not in text
    assert "cnr=" not in text
    for concept in [
        "espacio físico",
        "imagen fija",
        "imagen móvil",
        "rígidas",
        "afines",
        "deformables",
        "información mutua",
        "multirresolución",
        "interpolación",
        "tre",
        "fre",
        "campo de desplazamiento",
        "jacobiano",
        "bland–altman",
        "repetibilidad",
    ]:
        assert concept in text


def test_unit_05_preserves_longitudinal_handoffs_and_units():
    text = corpus(load(SOURCE))
    assert "u5 recibe de u4" in text
    assert "u6" in text
    assert "milímetros" in text
    assert "volumen físico" in text
    assert "cambio observado" in text
    assert "progresión clínica" in text


def test_unit_05_separates_optimization_from_independent_evaluation():
    text = corpus(load(SOURCE))
    assert "métrica optimizada" in text
    assert "no basta para validar" in text
    assert "landmarks reservados" in text
    assert "fle" in text
    assert "tre" in text
    assert "fre" in text


def test_unit_05_audits_deformable_registration_without_biological_overclaim():
    text = corpus(load(SOURCE))
    assert "determinante jacobiano" in text or "jacobiano" in text
    assert "plegamiento" in text
    assert "no se interpreta automáticamente" in text or "no se interpret" in text
    assert "crecimiento" in text or "atrofia" in text


def test_unit_05_has_substantive_practice_and_assessment():
    data = load(SOURCE)
    assert len(data["learning_objectives"]) >= 8
    assert len(data["theory_sections"]) >= 5
    assert len(data["glossary"]) >= 30
    assert len(data["worked_examples"]) >= 4
    assert all("reasoning_steps" in example for example in data["worked_examples"])
    assert len(data["guided_activities"]) >= 3
    lab = data["guided_activities"][1]
    assert len(lab["instructions"]) >= 8
    assert len(lab["problems"]) >= 12
    assert len(lab["deliverables"]) >= 7
    assert len(lab["checking_criteria"]) >= 8
    assert len(data["common_errors"]) >= 12
    assert len(data["self_assessment"]) >= 12
    for item in data["self_assessment"]:
        assert all(item.get(key) for key in ("question", "answer", "reasoning", "common_error"))


def test_unit_05_uses_methodological_and_official_sources():
    data = load(SOURCE)
    urls = {source["url"] for source in data["sources"]}
    required = {
        "https://doi.org/10.1016/S1361-8415(01)80026-8",
        "https://doi.org/10.1109/42.736021",
        "https://doi.org/10.1016/j.neuroimage.2009.12.037",
        "https://doi.org/10.1016/j.acra.2017.09.023",
        "https://doi.org/10.1148/radiol.2015142202",
        "https://doi.org/10.1016/S0140-6736(86)90837-8",
        "https://doi.org/10.1016/j.jcm.2016.02.012",
        "https://www.dicomstandard.org/current",
    }
    assert required.issubset(urls)
    assert len(data["sources"]) >= 16


def test_unit_05_keeps_measurement_claims_proportional():
    text = corpus(load(SOURCE))
    assert "cambio observado" in text
    assert "repetibilidad" in text
    assert "rc" in text
    assert "progresión clínica" in text
    assert "no demuestra" in text or "no diagnostica" in text


if __name__ == "__main__":
    tests = [value for name, value in globals().copy().items() if name.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} pruebas U5 superadas")
