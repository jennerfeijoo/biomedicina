import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/laboratorio-imagenes-biomedicas/units/unit-02.json"
MIRROR = ROOT / "data/generated_units/laboratorio-imagenes-biomedicas/unit-02.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/laboratorio-imagenes-biomedicas.json"
PUBLIC = ROOT / "ingenieria-biomedica/laboratorio-imagenes-biomedicas/unidades/unidad-02.html"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Calidad de imagen",
    "fantoma o imagen sintética, repetición, anotador alternativo",
    "pipeline de imagen reproducible con informe cuantitativo sobre comparación objetiva de protocolos",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_02_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 2
    assert data["slug"] == "calidad-de-imagen"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "dependiente de la tarea",
        "noise power spectrum",
        "nps",
        "frecuencia espacial",
        "edge spread function",
        "line spread function",
        "modulation transfer function",
        "mtf50",
        "mtf10",
        "frecuencia de nyquist",
        "pixel spacing",
        "uniformidad",
        "artefacto",
        "fantoma digital",
    ]:
        assert concept in text


def test_unit_02_purpose_preserves_task_dependency_and_handoff():
    purpose = load(SOURCE)["purpose"].lower()
    assert "dependiente de la tarea" in purpose
    assert "u2 recibe de u1" in purpose
    assert "entrega a u3" in purpose


def test_unit_02_blocks_common_quality_misinterpretations():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "cnr no se presenta como sustituto universal de detectabilidad clínica" in text
    assert "pixel spacing no equivale a resolución efectiva" in text
    assert "nyquist limita muestreo, no garantiza detalle observable" in text
    assert "desviación estándar resume amplitud pero no textura del ruido" in text
    assert "umbrales educativos no son tolerancias clínicas" in text
    assert "no se ponderan métricas con pesos arbitrarios" in text
    assert "no se recomiendan parámetros de exposición ni dosis para pacientes" in text
    assert "no se afirma conformidad, aceptación o certificación de equipos" in text


def test_unit_02_keeps_course_boundaries_explicit():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "u2 parte de datos auditados por u1" in text
    assert "u3 recibirá estas curvas, mapas y métricas como baseline" in text
    assert "u4 tratará segmentación" in text
    assert "u5 registro y mediciones" in text
    assert "u6 el pipeline completo" in text
    assert "no usa pacientes" in text
    assert "no valida eficacia clínica" in text


def test_unit_02_has_sufficient_depth():
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


def test_unit_02_uses_authoritative_quality_sources():
    urls = {s["url"] for s in load(SOURCE)["sources"]}
    required = {
        "https://www.aapm.org/pubs/reports/detail.asp?docid=186",
        "https://www.aapm.org/pubs/reports/detail.asp?docid=169",
        "https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1564webNew-74666420.pdf",
        "https://www-pub.iaea.org/MTCD/publications/PDF/PUB2021_web.pdf",
        "https://dicom.nema.org/medical/dicom/current/output/chtml/part14/ps3.14.html",
    }
    assert required.issubset(urls)


def test_unit_02_uses_quality_equations_with_explicit_limits():
    data = load(SOURCE)
    equations = [
        eq["latex"]
        for section in data["theory_sections"]
        for eq in section.get("equations", [])
    ]
    assert any("CNR" in eq for eq in equations)
    assert any("SNR" in eq for eq in equations)
    assert any("NPS" in eq for eq in equations)
    assert any("LSF" in eq and "ESF" in eq for eq in equations)
    assert any("MTF" in eq for eq in equations)
    assert any("f_N" in eq for eq in equations)


def test_published_descriptor_and_html_match_when_promoted():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 2)
    if detail["description"] != source["purpose"]:
        pytest.skip("U2 todavía no ha sido promovida por el workflow de publicación")
    assert detail["title"] == source["title"]
    assert PUBLIC.exists()
    public_text = PUBLIC.read_text(encoding="utf-8").lower()
    assert source["purpose"].lower() in public_text
    for marker in [
        "noise power spectrum",
        "modulation transfer function",
        "frecuencia de nyquist",
        "mtf50",
        "uniformidad",
    ]:
        assert marker in public_text
    for carryover in [
        "concepto de la unidad que debe definirse",
        "modelo conceptual de calidad de imagen",
    ]:
        assert carryover not in public_text


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
