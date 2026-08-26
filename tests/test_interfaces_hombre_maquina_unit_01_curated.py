import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/interfaces-hombre-maquina/units/unit-01.json"
MIRROR = ROOT / "data/generated_units/interfaces-hombre-maquina/unit-01.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/interfaces-hombre-maquina.json"
PUBLIC = ROOT / "ingenieria-biomedica/interfaces-hombre-maquina/unidades/unidad-01.html"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Factores humanos",
    "\\mathrm{SNR}_{dB}=10\\log_{10}",
    "señal cruda, función de transferencia, calibración, espectro",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_01_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 1
    assert data["slug"] == "factores-humanos"
    assert data["title"] == "Factores humanos"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "sistema sociotécnico", "análisis de tareas", "percepción",
        "atención selectiva", "memoria de trabajo", "memoria prospectiva",
        "modelo mental", "nasa-tlx", "interrupción", "error de modo",
        "forcing function", "evaluación formativa", "iec 62366-1"
    ]:
        assert concept in text


def test_unit_01_protects_human_factors_distinctions():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "un error observado no demuestra por sí mismo incompetencia" in text
    assert "«estaba en pantalla» no es evidencia suficiente" in text
    assert "memoria de trabajo tiene capacidad limitada" in text
    assert "nasa-tlx es una herramienta subjetiva multidimensional" in text
    assert "reducir el tiempo no siempre mejora la interacción" in text
    assert "las categorías de error describen mecanismos" in text
    assert "una confirmación adicional no es automáticamente una barrera eficaz" in text


def test_unit_01_keeps_course_boundaries_explicit():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "u2 profundizará en investigación de usuarios" in text
    assert "u3 profundizará en arquitectura de información" in text
    assert "u4 profundizará en accesibilidad" in text
    assert "se reserva para u5" in text
    assert "las interfaces avanzadas se abordan en u6" in text


def test_unit_01_is_not_regulatory_or_clinical_validation():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "no declara conformidad con normas" in text
    assert "no se asignan probabilidades clínicas reales" in text
    assert "no es un dispositivo validado" in text
    assert "no demuestra seguridad clínica" in text
    assert "no constituye validación de factores humanos" in text
    assert "no involucrar pacientes" in text


def test_unit_01_has_sufficient_academic_and_pedagogical_depth():
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


def test_unit_01_quantitative_models_are_bounded_and_non_generic():
    data = load(SOURCE)
    equations = [eq for section in data["theory_sections"] for eq in section.get("equations", [])]
    latex = " ".join(eq["latex"] for eq in equations)
    meanings = " ".join(eq["meaning"] for eq in equations).lower()
    assert "d'=Z(H)-Z(F)" in latex
    assert "N_{error}" in latex
    assert "SNR" not in latex
    assert "no establece umbrales clínicos" in meanings
    assert "no es una probabilidad universal de daño" in meanings


def test_unit_01_uses_current_authoritative_sources():
    data = load(SOURCE)
    urls = {s["url"] for s in data["sources"]}
    required = {
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
        "https://www.fda.gov/medical-devices/human-factors-and-medical-devices/human-factors-considerations",
        "https://webstore.iec.ch/en/publication/67220",
        "https://www.iso.org/standard/77520.html",
        "https://www.nasa.gov/human-systems-integration-division/nasa-task-load-index-tlx/",
        "https://psnet.ahrq.gov/primer/human-factors-engineering",
    }
    assert required.issubset(urls)


def test_published_descriptor_and_html_match_canonical_unit():
    assert DESCRIPTOR.exists()
    assert PUBLIC.exists()
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 1)
    assert detail["title"] == source["title"]
    assert detail["description"] == source["purpose"]
    public_text = PUBLIC.read_text(encoding="utf-8").lower()
    for marker in [
        "sistema sociotécnico", "memoria prospectiva", "nasa-tlx",
        "error de modo", "iec 62366-1"
    ]:
        assert marker in public_text


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
