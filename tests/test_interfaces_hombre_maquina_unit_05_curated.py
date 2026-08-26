import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/interfaces-hombre-maquina/units/unit-05.json"
MIRROR = ROOT / "data/generated_units/interfaces-hombre-maquina/unit-05.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/interfaces-hombre-maquina.json"
PUBLIC = ROOT / "ingenieria-biomedica/interfaces-hombre-maquina/unidades/unidad-05.html"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Evaluación de usabilidad",
    "\\mathrm{SNR}_{dB}=10\\log_{10}",
    "señal cruda, función de transferencia, calibración, espectro",
    "entrada patrón, cortocircuito o cero",
    "expediente de cadena de señal",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_05_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 5
    assert data["slug"] == "evaluacion-de-usabilidad"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "evaluación formativa", "evaluación sumativa", "efectividad", "eficiencia",
        "satisfacción", "usuario previsto", "tarea crítica", "error de uso", "close call",
        "éxito de tarea", "tiempo de tarea", "sus", "nasa-tlx", "representatividad",
        "human factors validation", "desviación de protocolo", "trazabilidad"
    ]:
        assert concept in text


def test_unit_05_blocks_common_usability_misinterpretations():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "no existe un tamaño de muestra universal" in text
    assert "un sus alto no demuestra ausencia de errores críticos" in text
    assert "un tiempo menor" in text and "no implica automáticamente" in text
    assert "error del usuario" in text
    assert "no se combinan métricas heterogéneas en un score" in text
    assert "no constituye human factors validation" in text
    assert "no demuestra por sí sola efectividad clínica" in text


def test_unit_05_keeps_course_boundaries_explicit():
    text = json.dumps(load(SOURCE), ensure_ascii=False).lower()
    assert "u1 aporta factores humanos" in text
    assert "u2 contexto y requisitos" in text
    assert "u3 flujos de interacción" in text
    assert "u4 barreras de accesibilidad" in text
    assert "u6 abordará interfaces avanzadas" in text


def test_unit_05_has_sufficient_depth():
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


def test_unit_05_uses_current_authoritative_sources():
    urls = {s["url"] for s in load(SOURCE)["sources"]}
    required = {
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-human-factors-information-medical-device-marketing-submissions",
        "https://webstore.iec.ch/en/publication/67220",
        "https://www.iso.org/standard/63500.html",
        "https://www.iso.org/standard/77520.html",
        "https://www.nist.gov/publications/nistir-7804-technical-evaluation-testing-and-validation-usability-electronic-health",
        "https://pubmed.ncbi.nlm.nih.gov/41483527/",
        "https://pubmed.ncbi.nlm.nih.gov/41272660/",
    }
    assert required.issubset(urls)


def test_unit_05_uses_metrics_with_denominators_not_snr():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False)
    assert "SNR" not in text
    assert "función de transferencia" not in text.lower()
    equations = [eq["latex"] for section in data["theory_sections"] for eq in section.get("equations", [])]
    assert any("CompletionRate" in eq for eq in equations)
    assert any("UseErrorRate" in eq for eq in equations)
    assert "denominador" in text.lower()


def test_published_descriptor_and_html_match_canonical_unit():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 5)
    assert PUBLIC.exists()
    assert detail["title"] == source["title"]
    assert detail["description"] == source["purpose"]
    public_text = PUBLIC.read_text(encoding="utf-8").lower()
    assert source["purpose"].lower() in public_text
    for marker in ["evaluación formativa", "error de uso", "close call", "sus", "representatividad", "human factors validation"]:
        assert marker in public_text
    for carryover in ["snr", "función de transferencia", "cortocircuito", "concepto de la unidad que debe definirse"]:
        assert carryover not in public_text


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
