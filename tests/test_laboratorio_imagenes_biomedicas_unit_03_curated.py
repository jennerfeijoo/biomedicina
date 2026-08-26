import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/laboratorio-imagenes-biomedicas/units/unit-03.json"
MIRROR = ROOT / "data/generated_units/laboratorio-imagenes-biomedicas/unit-03.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/laboratorio-imagenes-biomedicas.json"
PUBLIC = ROOT / "ingenieria-biomedica/laboratorio-imagenes-biomedicas/unidades/unidad-03.html"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Preprocesamiento",
    "fantoma o imagen sintética, repetición, anotador alternativo",
    "pipeline de imagen reproducible con informe cuantitativo sobre preparación sin introducir sesgos",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_03_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 3
    assert data["slug"] == "preprocesamiento"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "normalización de intensidad", "fuga de información", "z-score", "clipping",
        "convolución", "filtro gaussiano", "filtro mediana", "voxel anisótropo",
        "nps", "mtf", "bias field", "n4itk", "perturbación sintética",
        "prueba de regresión", "handoff",
    ]:
        assert concept in text


def test_unit_03_preserves_u1_u2_to_u4_handoff():
    purpose = load(SOURCE)["purpose"].lower()
    assert "validada por u1" in purpose
    assert "caracterizada cuantitativamente por u2" in purpose
    assert "entrega a u4" in purpose
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "u4 recibe imagen, diferencias, métricas y límites documentados" in text


def test_unit_03_blocks_preprocessing_misinterpretations():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "normalizar no equivale a calibrar una magnitud física" in text
    assert "los parámetros aprendidos no usan validación o prueba para ajustarse" in text
    assert "suavizar atenúa frecuencias y puede degradar resolución espacial" in text
    assert "pixel spacing no se confunde con resolución efectiva" in text
    assert "n4 no se presenta como corrector universal de artefactos" in text
    assert "no se construye un índice global con pesos arbitrarios" in text
    assert "no se usan pacientes ni estudios asistenciales aportados por el estudiante" in text
    assert "no se infiere utilidad clínica, seguridad, dosis, diagnóstico ni conformidad regulatoria" in text


def test_unit_03_requires_before_after_metrology():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "nps se reevalúa" in text
    assert "mtf o una métrica de borde se reevalúa" in text
    assert "mapa diferencia" in text
    assert "baseline" in text
    assert "trade-off" in text


def test_unit_03_has_sufficient_depth():
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
    assert len(activity["deliverables"]) >= 10
    assert len(activity["checking_criteria"]) >= 20
    assert len(data["common_errors"]) >= 18
    assert len(data["self_assessment"]) >= 12
    assert len(data["biomedical_connections"]) >= 6
    assert len(data["sources"]) >= 16


def test_unit_03_uses_authoritative_preprocessing_sources():
    urls = {s["url"] for s in load(SOURCE)["sources"]}
    required = {
        "https://itk.org/ITKSoftwareGuide/html/Book2/ITKSoftwareGuide-Book2ch2.html",
        "https://pubmed.ncbi.nlm.nih.gov/20378467/",
        "https://pubmed.ncbi.nlm.nih.gov/17354645/",
        "https://pubmed.ncbi.nlm.nih.gov/37283773/",
        "https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html",
    }
    assert required.issubset(urls)


def test_unit_03_uses_equations_with_declared_scope():
    equations = [
        eq["latex"] for section in load(SOURCE)["theory_sections"]
        for eq in section.get("equations", [])
    ]
    assert any("mu_{ref}" in eq and "sigma_{ref}" in eq for eq in equations)
    assert any("p_{low}" in eq and "p_{high}" in eq for eq in equations)
    assert any("(h*x)" in eq for eq in equations)
    assert any("I_{obs}" in eq and "I_{true}" in eq for eq in equations)
    assert any("m_{post}" in eq and "m_{pre}" in eq for eq in equations)


def test_published_descriptor_and_html_match_when_promoted():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 3)
    if detail["description"] != source["purpose"]:
        pytest.skip("U3 todavía no ha sido promovida por el workflow de publicación")
    assert detail["title"] == source["title"]
    assert PUBLIC.exists()
    public_text = PUBLIC.read_text(encoding="utf-8").lower()
    assert source["purpose"].lower() in public_text
    for marker in ["normalización de intensidad", "fuga de información", "filtro gaussiano", "n4itk", "perturbación sintética"]:
        assert marker in public_text
    assert "concepto de la unidad que debe definirse" not in public_text


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
