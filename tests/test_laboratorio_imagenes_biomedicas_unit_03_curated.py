import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/laboratorio-imagenes-biomedicas/units/unit-03.json"
MIRROR = ROOT / "data/generated_units/laboratorio-imagenes-biomedicas/unit-03.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/laboratorio-imagenes-biomedicas.json"
PUBLIC = ROOT / "ingenieria-biomedica/laboratorio-imagenes-biomedicas/unidades/unidad-03.html"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_03_replaces_template_definitions_with_disciplinary_content():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert data["unit"] == 3
    assert data["slug"] == "preprocesamiento"
    assert "concepto de la unidad que debe definirse" not in text
    for concept in [
        "rescale slope",
        "unidades hounsfield",
        "z-score",
        "filtro gaussiano",
        "filtro mediano",
        "difusión anisotrópica",
        "campo de bias",
        "n4itk",
        "fuga de información",
        "mapas de diferencia",
        "espaciado",
        "origen",
        "dirección",
    ]:
        assert concept in text


def test_unit_03_has_explicit_pipeline_boundaries():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "u3 recibe de u1" in text
    assert "de u2 una línea base" in text
    assert "u4 usará esta salida" in text
    assert "imagen original permanece inmutable" in text
    assert "no es una imagen simplemente más agradable" in text


def test_unit_03_blocks_leakage_and_test_set_optimization():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "la partición se realiza por sujeto" in text
    assert "cada pliegue contiene su propio ajuste" in text
    assert "nunca se reparten entre entrenamiento y prueba" in text
    assert "mantener intacto el conjunto de prueba" in text
    assert "no seleccionar el pipeline por su desempeño final en prueba" in text


def test_unit_03_preserves_task_signal_and_geometry():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "reducción de ruido y preservación de señal" in text
    assert "tamaño, espaciado, origen y dirección" in text
    assert "interpolación apropiada" in text
    assert "sobre-corrección" in text or "sobrecorrección" in text
    assert "no demuestra validez clínica" in text


def test_unit_03_uses_traceable_primary_and_official_sources():
    urls = {source["url"] for source in load(SOURCE)["sources"]}
    required = {
        "https://doi.org/10.1109/TMI.2010.2046908",
        "https://dicom.nema.org/medical/dicom/current/output/chtml/part03/PS3.3.html",
        "https://simpleitk.readthedocs.io/en/master/fundamentalConcepts.html",
        "https://scikit-learn.org/stable/common_pitfalls.html",
        "https://doi.org/10.1148/ryai.2020200029",
    }
    assert required.issubset(urls)


def test_published_descriptor_and_html_match_strictly():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(item for item in descriptor["detailed_units"] if item["unit"] == 3)
    assert detail["title"] == source["title"]
    assert detail["description"] == source["purpose"]
    public = PUBLIC.read_text(encoding="utf-8").lower()
    assert source["purpose"].lower() in public
    assert "fuga de información" in public
    assert "n4itk" in public
    assert "concepto de la unidad que debe definirse" not in public

