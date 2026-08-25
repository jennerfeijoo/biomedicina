import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/ingenieria-neurosensorial/units/unit-01.json"
MIRROR = ROOT / "data/generated_units/ingenieria-neurosensorial/unit-01.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/ingenieria-neurosensorial.json"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "Modelo conceptual de Sistemas sensoriales",
    "\\mathrm{SNR}_{dB}=10\\log_{10}",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_01_is_disciplinary_and_template_free():
    data = load(SOURCE)
    assert data["unit"] == 1
    assert data["slug"] == "sistemas-sensoriales"
    assert data["title"] == "Sistemas sensoriales"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "estímulo adecuado", "potencial receptor", "potencial de acción",
        "línea etiquetada", "rate coding", "population coding",
        "campo receptivo", "adaptación", "somatotopía", "retinotopía",
        "tonotopía", "jnd", "fracción de weber", "percepción"
    ]:
        assert concept in text


def test_unit_01_protects_core_neurosensory_distinctions():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "potencial receptor y potencial de acción son señales fisiológicas diferentes" in text
    assert "transducción convierte energía del estímulo" in text
    assert "la tasa es una característica del código, no el código completo" in text
    assert "adaptación no equivale simplemente a fatiga" in text
    assert "el tamaño anatómico del receptor y el campo receptivo funcional no son sinónimos" in text
    assert "actividad neural y percepción pertenecen a niveles de observación diferentes" in text
    assert "no una constante universal" in text


def test_unit_01_keeps_recording_and_stimulation_out_of_scope():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "u1 no incluye todavía electrodos, amplificadores ni snr de registro" in text
    assert "esa cadena de adquisición pertenece a u2" in text
    assert "no se registran ni estimulan personas" in text
    assert "no se conectan electrodos, eeg, amplificadores ni hardware clínico" in text
    assert "no acredita competencia clínica" in text


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


def test_unit_01_quantitative_models_are_bounded_and_not_generic_snr():
    data = load(SOURCE)
    equations = [eq for section in data["theory_sections"] for eq in section.get("equations", [])]
    latex = " ".join(eq["latex"] for eq in equations)
    meanings = " ".join(eq["meaning"] for eq in equations).lower()
    assert "I_{50}" in latex
    assert "R_{initial}" in latex
    assert "\\Delta I_{JND}" in latex
    assert "SNR" not in latex
    assert "no se presenta como ley universal" in meanings
    assert "depende de cómo se definan las ventanas" in meanings
    assert "no como constante universal" in meanings


def test_unit_01_uses_verified_neurosensory_sources():
    data = load(SOURCE)
    urls = {s["url"] for s in data["sources"]}
    required = {
        "https://openstax.org/books/biology/pages/36-1-sensory-processes",
        "https://www.ncbi.nlm.nih.gov/sites/books/NBK539861/",
        "https://www.ncbi.nlm.nih.gov/books/NBK10788/",
        "https://www.ncbi.nlm.nih.gov/books/NBK52768/",
        "https://pubmed.ncbi.nlm.nih.gov/35412676/",
        "https://pubmed.ncbi.nlm.nih.gov/35218890/",
    }
    assert required.issubset(urls)


def test_published_descriptor_matches_when_unit_01_is_promoted():
    if not DESCRIPTOR.exists():
        return
    source = load(SOURCE)
    descriptor = load(DESCRIPTOR)
    detail = next((u for u in descriptor.get("detailed_units", []) if u.get("unit") == 1), None)
    if detail and detail.get("description") != "Integrar transducción, codificación, vías y percepción para resolver un caso de definición de señales relevantes para neurotecnología con evidencia, controles, incertidumbre y comunicación proporcional.":
        assert detail["description"] == source["purpose"]
