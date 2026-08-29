import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/laboratorio-imagenes-biomedicas/units/unit-04.json"
MIRROR = ROOT / "data/generated_units/laboratorio-imagenes-biomedicas/unit-04.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/laboratorio-imagenes-biomedicas.json"
PUBLIC = ROOT / "ingenieria-biomedica/laboratorio-imagenes-biomedicas/unidades/unidad-04.html"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_04_is_disciplinary_and_template_free():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert data["unit"] == 4
    assert data["slug"] == "segmentacion"
    assert "concepto de la unidad que debe definirse" not in text
    for concept in [
        "definición operacional",
        "máscara binaria",
        "volumen parcial",
        "crecimiento de regiones",
        "elemento estructurante",
        "dice",
        "jaccard",
        "valor predictivo positivo",
        "distancia de superficie",
        "hd95",
        "variabilidad intraobservador",
        "variabilidad interobservador",
        "adjudicación",
    ]:
        assert concept in text


def test_unit_04_preserves_course_handoffs_and_geometry():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "u4 recibe de u3" in text
    assert "u5 recibirá máscaras" in text
    assert "u6 integrará el pipeline" in text
    assert "tamaño, espaciado, origen y dirección" in text
    assert "coordenadas físicas" in text
    assert "milímetros" in text


def test_unit_04_uses_complementary_metrics_with_limits():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    equations = [
        equation["latex"]
        for section in data["theory_sections"]
        for equation in section.get("equations", [])
    ]
    assert any("Dice" in equation for equation in equations)
    assert any("N_{vox}" in equation for equation in equations)
    assert "depende del tamaño de la región" in text
    assert "no localiza el error" in text
    assert "sin declarar un umbral universal" in text
    assert "no demuestra que la región represente enfermedad" in text


def test_unit_04_has_substantive_practice_and_assessment():
    data = load(SOURCE)
    assert len(data["learning_objectives"]) >= 7
    assert len(data["theory_sections"]) >= 4
    assert len(data["glossary"]) >= 30
    assert len(data["worked_examples"]) >= 4
    assert all("reasoning_steps" in example for example in data["worked_examples"])
    assert len(data["guided_activities"]) >= 3
    benchmark = data["guided_activities"][1]
    assert len(benchmark["instructions"]) >= 7
    assert len(benchmark["problems"]) >= 12
    assert len(benchmark["deliverables"]) >= 6
    assert len(benchmark["checking_criteria"]) >= 9
    assert len(data["common_errors"]) >= 12
    assert len(data["self_assessment"]) >= 12
    for item in data["self_assessment"]:
        assert all(item.get(key) for key in ("question", "answer", "reasoning", "common_error"))


def test_unit_04_preserves_reference_uncertainty_and_split_integrity():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "no una verdad absoluta" in text
    assert "no equivale automáticamente a verdad biológica" in text
    assert "nunca optimizando sobre prueba" in text
    assert "la prueba permanece intacta durante el ajuste" in text
    assert "conservar cada anotación" in text
    assert "sin sobrescribir originales" in text


def test_unit_04_uses_primary_official_and_methodological_sources():
    data = load(SOURCE)
    urls = {source["url"] for source in data["sources"]}
    required = {
        "https://doi.org/10.1186/s12880-015-0068-x",
        "https://doi.org/10.1038/s41592-023-02151-z",
        "https://doi.org/10.1109/TMI.2004.828354",
        "https://doi.org/10.1038/s41467-022-30695-9",
        "https://simpleitk.readthedocs.io/en/master/fundamentalConcepts.html",
        "https://slicer.readthedocs.io/en/latest/user_guide/modules/segmentations.html",
        "https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.51.html",
    }
    assert required.issubset(urls)
    assert len(data["sources"]) >= 16


def test_published_descriptor_and_html_match_strictly():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(item for item in descriptor["detailed_units"] if item["unit"] == 4)
    assert detail["title"] == source["title"]
    assert detail["description"] == source["purpose"]
    public = PUBLIC.read_text(encoding="utf-8").lower()
    assert source["purpose"].lower() in public
    for marker in ("hd95", "variabilidad interobservador", "benchmark sintético"):
        assert marker in public
    assert "concepto de la unidad que debe definirse" not in public


if __name__ == "__main__":
    tests = [value for name, value in globals().copy().items() if name.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} pruebas U4 superadas")
