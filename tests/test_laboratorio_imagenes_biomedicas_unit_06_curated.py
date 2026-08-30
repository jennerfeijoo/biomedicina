import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/laboratorio-imagenes-biomedicas/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/laboratorio-imagenes-biomedicas/unit-06.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def corpus(data):
    return json.dumps(data, ensure_ascii=False).lower()


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_06_is_project_specific_and_template_free():
    data = load(SOURCE)
    text = corpus(data)
    assert data["unit"] == 6
    assert data["slug"] == "proyecto-de-analisis"
    assert data["title"] == "Proyecto de análisis"
    assert "concepto de la unidad que debe definirse mediante entidades observables" not in text
    for concept in [
        "estimando", "unidad independiente", "manifiesto de datos", "geometría física",
        "fuga de información", "conjunto de evaluación final", "baseline", "dice",
        "distancia de superficie", "tre", "análisis de sensibilidad", "validez externa",
        "prueba unitaria", "prueba de integración", "trazabilidad", "claim clínico",
    ]:
        assert concept in text


def test_unit_06_integrates_prior_laboratory_work_without_clinical_overclaim():
    text = corpus(load(SOURCE))
    for concept in ["dicom", "preprocesamiento", "segmentación", "registro", "medición"]:
        assert concept in text
    assert "u1–u5" in text or "u1-u5" in text
    assert "no demuestra" in text
    assert "beneficio clínico" in text
    assert "conformidad regulatoria" in text


def test_unit_06_protects_independent_evaluation():
    text = corpus(load(SOURCE))
    assert "partición por sujeto" in text
    assert "fuga de información" in text
    assert "congelar" in text or "congelación" in text
    assert "evaluación final" in text
    assert "normalizar" in text
    assert "test" in text


def test_unit_06_uses_task_specific_metrics_and_failure_analysis():
    text = corpus(load(SOURCE))
    assert "dice=" in text
    assert "tre_i=" in text
    assert "hausdorff" in text
    assert "métricas por caso" in text
    assert "denominador" in text
    assert "caso fallido" in text


def test_unit_06_has_substantive_practice_and_assessment():
    data = load(SOURCE)
    assert len(data["learning_objectives"]) >= 9
    assert len(data["theory_sections"]) >= 5
    assert len(data["glossary"]) >= 40
    assert len(data["worked_examples"]) >= 5
    assert all(len(example["reasoning_steps"]) >= 5 for example in data["worked_examples"])
    assert len(data["guided_activities"]) >= 3
    lab = data["guided_activities"][0]
    assert lab["duration_minutes"] >= 480
    assert len(lab["instructions"]) >= 15
    assert len(lab["problems"]) >= 18
    assert len(lab["deliverables"]) >= 8
    assert len(lab["checking_criteria"]) >= 12
    assert len(data["assessment"]["components"]) == 5
    assert len(data["common_errors"]) >= 18
    assert len(data["self_assessment"]) >= 12


def test_unit_06_has_reproducibility_and_transfer_requirements():
    text = corpus(load(SOURCE))
    for concept in [
        "readme", "configuración", "entorno", "semilla", "versionado",
        "prueba unitaria", "prueba de integración", "dato sintético",
        "validación interna", "validez externa", "distribution shift",
    ]:
        assert concept in text


def test_unit_06_uses_methodological_and_official_sources():
    data = load(SOURCE)
    urls = {source["url"] for source in data["sources"]}
    required = {
        "https://www.dicomstandard.org/current",
        "https://dicom.nema.org/medical/dicom/current/output/html/part15.html",
        "https://www.rsna.org/research/quantitative-imaging-biomarkers-alliance",
        "https://doi.org/10.1148/radiol.2020191145",
        "https://doi.org/10.1038/sdata.2016.18",
        "https://simpleitk.readthedocs.io/en/master/",
        "https://scikit-image.org/docs/stable/",
        "https://doi.org/10.7717/peerj-cs.86",
    }
    assert required.issubset(urls)
    assert len(data["sources"]) >= 16


def test_unit_06_assessment_weights_sum_to_100():
    data = load(SOURCE)
    weights = [int(item["weight"].split()[0]) for item in data["assessment"]["components"]]
    assert sum(weights) == 100


if __name__ == "__main__":
    tests = [value for name, value in globals().copy().items() if name.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} pruebas U6 superadas")
