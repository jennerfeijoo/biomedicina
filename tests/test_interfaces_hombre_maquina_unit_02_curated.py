import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/interfaces-hombre-maquina/units/unit-02.json"
MIRROR = ROOT / "data/generated_units/interfaces-hombre-maquina/unit-02.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/interfaces-hombre-maquina.json"
PUBLIC = ROOT / "ingenieria-biomedica/interfaces-hombre-maquina/unidades/unidad-02.html"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Investigación de usuarios",
    "\\mathrm{SNR}_{dB}=10\\log_{10}",
    "señal cruda, función de transferencia, calibración, espectro",
    "entrada patrón, cortocircuito o cero",
    "expediente de cadena de señal",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_02_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 2
    assert data["slug"] == "investigacion-de-usuarios"
    assert data["title"] == "Investigación de usuarios"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "contexto de uso", "grupo de usuarios", "trabajo prescrito",
        "trabajo realizado", "hta", "cta", "contextual inquiry",
        "entrevista semiestructurada", "caso negativo", "triangulación",
        "requisito de usuario", "criterio de aceptación", "matriz de trazabilidad",
        "coreq", "srqr", "iso 9241-210", "iec 62366-1"
    ]:
        assert concept in text


def test_unit_02_protects_research_distinctions():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "una cita de usuario no es un requisito" in text
    assert "la frecuencia de menciones no equivale automáticamente" in text
    assert "el relato retrospectivo puede simplificar" in text
    assert "saturación no es un número universal" in text
    assert "personas y mapas sintetizan evidencia, pero no sustituyen datos originales" in text
    assert "trabajo prescrito y trabajo realizado deben compararse explícitamente" in text
    assert "no se presenta como «lo que los usuarios necesitan»" in text


def test_unit_02_keeps_course_boundaries_explicit():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "u1 aporta factores humanos" in text
    assert "u3 desarrollará diseño de interacción" in text
    assert "u4 accesibilidad" in text
    assert "u5 evaluación formal de usabilidad" in text
    assert "u6 interfaces avanzadas" in text


def test_unit_02_is_not_human_subjects_or_regulatory_validation():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "u2 no recluta participantes reales" in text
    assert "no constituye investigación con seres humanos" in text
    assert "no constituye validación de usabilidad" in text
    assert "no calcula ni aprueba riesgo residual" in text
    assert "no permite declarar cumplimiento" in text


def test_unit_02_has_sufficient_academic_and_pedagogical_depth():
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


def test_unit_02_uses_current_authoritative_sources():
    data = load(SOURCE)
    urls = {s["url"] for s in data["sources"]}
    required = {
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
        "https://www.fda.gov/medical-devices/human-factors-and-medical-devices/human-factors-considerations",
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-human-factors-information-medical-device-marketing-submissions",
        "https://webstore.iec.ch/en/publication/67220",
        "https://www.iso.org/standard/77520.html",
        "https://digital.ahrq.gov/health-it-tools-and-resources/evaluation-resources/workflow-assessment-health-it-toolkit/all-workflow-tools/hierarchical-task-analysis",
        "https://pubmed.ncbi.nlm.nih.gov/17872937/",
        "https://pubmed.ncbi.nlm.nih.gov/24979285/",
    }
    assert required.issubset(urls)


def test_unit_02_has_no_instrumentation_equation_carryover():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False)
    assert "SNR" not in text
    assert "función de transferencia" not in text.lower()
    assert all(not section.get("equations") for section in data["theory_sections"])


def test_publication_matches_when_promoted():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 2)
    if detail["description"] != source["purpose"]:
        return
    assert PUBLIC.exists()
    public_text = PUBLIC.read_text(encoding="utf-8").lower()
    for marker in [
        "contexto de uso", "contextual inquiry", "trabajo prescrito",
        "matriz de trazabilidad", "caso negativo"
    ]:
        assert marker in public_text


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
