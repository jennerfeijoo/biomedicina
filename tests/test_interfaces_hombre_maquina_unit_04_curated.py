import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/interfaces-hombre-maquina/units/unit-04.json"
MIRROR = ROOT / "data/generated_units/interfaces-hombre-maquina/unit-04.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/interfaces-hombre-maquina.json"
PUBLIC = ROOT / "ingenieria-biomedica/interfaces-hombre-maquina/unidades/unidad-04.html"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Accesibilidad y diseño inclusivo",
    "\\mathrm{SNR}_{dB}=10\\log_{10}",
    "señal cruda, función de transferencia, calibración, espectro",
    "entrada patrón, cortocircuito o cero",
    "expediente de cadena de señal",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_04_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 4
    assert data["slug"] == "accesibilidad-y-diseno-inclusivo"
    assert data["title"] == "Accesibilidad y diseño inclusivo"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "wcag 2.2", "iso 9241-171:2025", "tecnología de apoyo", "lector de pantalla",
        "foco de teclado", "orden de foco", "nombre accesible", "wai-aria", "html semántico",
        "reflow", "uso de color", "alternativa a arrastrar", "accesibilidad cognitiva",
        "autenticación accesible", "prueba automatizada", "revisión manual", "trazabilidad de accesibilidad"
    ]:
        assert concept in text


def test_unit_04_protects_accessibility_distinctions():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "usabilidad y accesibilidad se relacionan pero no son equivalentes" in text
    assert "wcag sea por sí sola una norma completa para hardware médico" in text
    assert "ninguna herramienta automática por sí sola determina" in text
    assert "foco y selección no son sinónimos" in text
    assert "no debe ser la única codificación" in text
    assert "alternativa accesible debe permitir completar la misma función" in text
    assert "accesibilidad y seguridad deben resolverse conjuntamente" in text
    assert "no puede afirmar accesibilidad universal" in text


def test_unit_04_keeps_course_boundaries_explicit():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "u1 aporta factores humanos" in text
    assert "u2 necesidades de usuarios" in text
    assert "u3 diseño de interacción" in text
    assert "u5 realizará evaluación formal de usabilidad" in text
    assert "u6 abordará interfaces avanzadas" in text


def test_unit_04_is_formative_not_certification_or_user_research():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "no reclutes personas" in text
    assert "no constituye investigación con seres humanos" in text
    assert "auditoría certificadora de accesibilidad" in text
    assert "no constituye" in text and "evaluación sumativa de usabilidad" in text
    assert "no constituye" in text and "validación clínica" in text
    assert "demostración de conformidad con wcag, fda, iec o iso" in text


def test_unit_04_has_sufficient_academic_and_pedagogical_depth():
    data = load(SOURCE)
    assert len(data["learning_objectives"]) >= 6
    assert len(data["theory_sections"]) >= 5
    for section in data["theory_sections"]:
        assert len(section["paragraphs"]) >= 5
        assert len(section["key_points"]) >= 5
        assert all(len(point.split()) >= 4 for point in section["key_points"])
    assert len(data["glossary"]) >= 45
    assert len(data["worked_examples"]) >= 5
    activity = data["guided_activities"][0]
    assert activity["estimated_time_minutes"] >= 360
    assert len(activity["instructions"]) >= 8
    assert len(activity["problems"]) >= 20
    assert len(activity["deliverables"]) >= 8
    assert len(activity["checking_criteria"]) >= 20
    assert len(data["common_errors"]) >= 18
    assert len(data["self_assessment"]) >= 12
    assert len(data["biomedical_connections"]) >= 6
    assert len(data["sources"]) >= 16


def test_unit_04_uses_current_authoritative_sources():
    urls = {s["url"] for s in load(SOURCE)["sources"]}
    required = {
        "https://www.w3.org/TR/WCAG22/",
        "https://www.w3.org/WAI/test-evaluate/",
        "https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/",
        "https://www.w3.org/TR/coga-usable/",
        "https://www.iso.org/standard/86308.html",
        "https://www.iso.org/standard/77520.html",
        "https://webstore.iec.ch/en/publication/67220",
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
        "https://www.who.int/news-room/fact-sheets/detail/assistive-technology",
        "https://pubmed.ncbi.nlm.nih.gov/42450979/",
        "https://pubmed.ncbi.nlm.nih.gov/37590050/",
    }
    assert required.issubset(urls)


def test_unit_04_has_no_instrumentation_carryover():
    text = json.dumps(load(SOURCE), ensure_ascii=False)
    assert "SNR" not in text
    assert "función de transferencia" not in text.lower()
    assert "cortocircuito" not in text.lower()
    assert all(not section.get("equations") for section in load(SOURCE)["theory_sections"])


def test_publication_matches_canonical_when_materialized():
    source = load(SOURCE)
    if not PUBLIC.exists():
        return
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 4)
    assert detail["title"] == source["title"]
    public_text = PUBLIC.read_text(encoding="utf-8").lower()
    for marker in ["wcag 2.2", "lector de pantalla", "foco de teclado", "accesibilidad cognitiva", "prueba automatizada"]:
        assert marker in public_text
    for carryover in ["snr", "función de transferencia", "cortocircuito"]:
        assert carryover not in public_text


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
