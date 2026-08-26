import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/interfaces-hombre-maquina/units/unit-03.json"
MIRROR = ROOT / "data/generated_units/interfaces-hombre-maquina/unit-03.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/interfaces-hombre-maquina.json"
PUBLIC = ROOT / "ingenieria-biomedica/interfaces-hombre-maquina/unidades/unidad-03.html"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Diseño de interacción",
    "\\mathrm{SNR}_{dB}=10\\log_{10}",
    "señal cruda, función de transferencia, calibración, espectro",
    "entrada patrón, cortocircuito o cero",
    "expediente de cadena de señal",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_03_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 3
    assert data["slug"] == "diseno-de-interaccion"
    assert data["title"] == "Diseño de interacción"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "arquitectura de información", "modelo de interacción", "flujo de tarea",
        "estado del sistema", "transición de estado", "modo", "feedback",
        "visibilidad del estado", "latencia", "restricción", "default",
        "confirmación", "deshacer", "reversibilidad", "error de contexto",
        "prototipo", "walkthrough", "evaluación formativa", "trazabilidad de diseño",
        "iso 9241-110", "iec 62366-1"
    ]:
        assert concept in text


def test_unit_03_protects_interaction_design_distinctions():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "una interfaz puede ser visualmente limpia y, aun así, fracasar" in text
    assert "un flujo de tarea" in text and "no debe confundirse con un flujo de pantallas" in text
    assert "«recibido», «guardado localmente», «enviado», «aceptado por el servidor» y «completado» no son sinónimos" in text
    assert "menos clics" in text and "no es automáticamente mejor" in text
    assert "las confirmaciones son útiles" in text and "¿está seguro?" in text
    assert "un default es más defendible" in text
    assert "«deshacer» no debe prometer revertir consecuencias externas" in text
    assert "walkthrough puede revelar problemas tempranos" in text


def test_unit_03_keeps_course_boundaries_explicit():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "u1 aporta factores humanos" in text
    assert "u2 investigación de usuarios" in text
    assert "u4 desarrollará accesibilidad" in text
    assert "u5 realizará evaluación formal de usabilidad" in text
    assert "u6 abordará interfaces avanzadas" in text


def test_unit_03_is_formative_not_validation_or_conformity():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "no constituye evaluación sumativa" in text
    assert "no declara conformidad" in text
    assert "no se utilizan datos reales" in text
    assert "validación clínica" in text
    assert "no prueban seguridad ni superioridad clínica" in text
    assert "no constituye validación de un dispositivo clínico" in text


def test_unit_03_has_sufficient_academic_and_pedagogical_depth():
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


def test_unit_03_uses_current_authoritative_sources():
    data = load(SOURCE)
    urls = {s["url"] for s in data["sources"]}
    required = {
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
        "https://www.fda.gov/medical-devices/human-factors-and-medical-devices/human-factors-considerations",
        "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-human-factors-information-medical-device-marketing-submissions",
        "https://webstore.iec.ch/en/publication/67220",
        "https://www.iso.org/standard/77520.html",
        "https://www.iso.org/standard/75258.html",
        "https://www.iso.org/standard/63500.html",
        "https://www.nist.gov/publications/technical-basis-user-interface-design-health-it",
        "https://pubmed.ncbi.nlm.nih.gov/39762805/",
        "https://pubmed.ncbi.nlm.nih.gov/28088527/",
    }
    assert required.issubset(urls)


def test_unit_03_has_no_instrumentation_carryover():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False)
    assert "SNR" not in text
    assert "función de transferencia" not in text.lower()
    assert "cortocircuito" not in text.lower()
    assert all(not section.get("equations") for section in data["theory_sections"])


def test_published_descriptor_and_html_match_canonical_unit():
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next(u for u in descriptor["detailed_units"] if u["unit"] == 3)
    assert PUBLIC.exists()
    assert detail["title"] == source["title"]
    assert detail["description"] == source["purpose"]
    public_text = PUBLIC.read_text(encoding="utf-8").lower()
    for marker in [
        "arquitectura de información", "estado del sistema", "feedback",
        "error de contexto", "evaluación formativa"
    ]:
        assert marker in public_text


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
