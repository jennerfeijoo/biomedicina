import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/laboratorio-imagenes-biomedicas/units/unit-01.json"
MIRROR = ROOT / "data/generated_units/laboratorio-imagenes-biomedicas/unit-01.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/laboratorio-imagenes-biomedicas.json"
PUBLIC = ROOT / "ingenieria-biomedica/laboratorio-imagenes-biomedicas/unidades/unidad-01.html"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Datos DICOM y visualización",
    "CNR=\\frac{|\\mu_1-\\mu_2|}{\\sigma_n}",
    "fantoma o imagen sintética, repetición, anotador alternativo",
    "pipeline de imagen reproducible con informe cuantitativo sobre manejo seguro",
]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()

def test_unit_01_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 1
    assert data["slug"] == "datos-dicom-y-visualizacion"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "study instance uid", "series instance uid", "sop instance uid",
        "sop class", "transfer syntax", "image position (patient)",
        "image orientation (patient)", "pixel spacing", "frame of reference uid",
        "rescale slope", "rescale intercept", "voi lut", "window center",
        "window width", "monochrome1", "monochrome2",
        "basic application level confidentiality profile", "burned-in annotation",
        "referential integrity",
    ]:
        assert concept in text

def test_unit_01_blocks_common_dicom_misinterpretations():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "no se usa como sustituto universal del orden espacial" in text
    assert "slice thickness" in text and "no debe confundirse" in text
    assert "windowing modifica presentación, no adquisición original" in text
    assert "no presupone que todas las modalidades produzcan unidades físicas comparables" in text
    assert "no consiste en borrar patient name" in text
    assert "desidentificación y anonimización absoluta no son sinónimos" in text
    assert "una png vistosa" in text
    assert "no usa cnr, snr" in text

def test_unit_01_keeps_course_boundaries_explicit():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "u2 recibirá esta salida para estudiar contraste, ruido, resolución y fantomas" in text
    assert "u3 tratará preprocesamiento" in text
    assert "u4 segmentación" in text
    assert "u5 registro/mediciones" in text
    assert "u6 la integración del pipeline completo" in text
    assert "no realiza diagnóstico clínico" in text

def test_unit_01_has_sufficient_depth():
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

def test_unit_01_uses_authoritative_dicom_sources():
    urls = {s["url"] for s in load(SOURCE)["sources"]}
    required = {
        "https://www.dicomstandard.org/current",
        "https://dicom.nema.org/medical/dicom/current/output/chtml/part04/sect_C.3.html",
        "https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html",
        "https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.11.2.html",
        "https://dicom.nema.org/medical/dicom/current/output/chtml/part15/chapter_E.html",
        "https://pydicom.github.io/pydicom/stable/reference/pixels.html",
    }
    assert required.issubset(urls)

def test_unit_01_uses_geometry_and_display_equations_not_generic_cnr():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False)
    equations = [eq["latex"] for section in data["theory_sections"] for eq in section.get("equations", [])]
    assert "CNR" not in text
    assert "SNR" not in text
    assert any("\\mathbf{n}" in eq and "\\times" in eq for eq in equations)
    assert any("\\mathbf{IPP}" in eq for eq in equations)
    assert any("v_{mod}" in eq for eq in equations)

def test_published_descriptor_and_html_match_when_promoted():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 1)
    if detail["description"] == source["purpose"]:
        assert detail["title"] == source["title"]
        assert PUBLIC.exists()
        public_text = PUBLIC.read_text(encoding="utf-8").lower()
        assert source["purpose"].lower() in public_text
        for marker in [
            "image position (patient)", "image orientation (patient)",
            "window center", "basic application level confidentiality profile",
            "burned-in annotation"
        ]:
            assert marker in public_text
        for carryover in ["concepto de la unidad que debe definirse", "cnr="]:
            assert carryover not in public_text

if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
