import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/ingenieria-datos-biomedicos/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/ingenieria-datos-biomedicos/unit-06.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/ingenieria-datos-biomedicos.json"
CATALOG = ROOT / "data/catalog_statuses.json"

GENERIC_MARKERS = [
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "v=\\frac{\\Delta y}{\\Delta t}",
    "PPV=\\frac{TP}{TP+FP}",
    "modelo multicriterio transparente",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_and_generated_mirror_match_exactly():
    assert SOURCE.read_bytes() == MIRROR.read_bytes()


def test_unit_06_has_disciplinary_privacy_and_data_product_scope():
    data = load(SOURCE)
    assert data["unit"] == 6
    assert data["slug"] == "privacidad-y-productos-de-datos"
    assert data["title"] == "Privacidad y productos de datos"
    assert data["status"] == "review"
    text = json.dumps(data, ensure_ascii=False).lower()
    for marker in GENERIC_MARKERS:
        assert marker.lower() not in text
    for concept in [
        "minimización", "reidentificación", "cuasi-identificador",
        "seudonimización", "autorización", "mínimo privilegio",
        "rbac", "abac", "data contract", "data use agreement",
        "retención", "deprecación", "riesgo residual"
    ]:
        assert concept in text


def test_unit_06_protects_critical_semantic_boundaries():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "dataset seudonimizado no debe describirse como anónimo" in text
    assert "autenticación responde quién" in text and "autorización responde qué operación" in text
    assert "data contract técnico no es un contrato jurídico ni un data use agreement" in text
    assert "k-anonimato no evita por sí mismo" in text
    assert "hashing" in text and "no constituye anonimización" in text.replace("por sí sola ", "")
    assert "cifrado" in text and "no una técnica de anonimización" in text
    assert "no concede por sí sola permiso" in text
    assert "no prueba por sí sola validez clínica" in text


def test_unit_06_has_sufficient_pedagogical_depth():
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
    assert len(data["sources"]) >= 12


def test_unit_06_uses_privacy_metrics_only_as_limited_diagnostics():
    data = load(SOURCE)
    equations = [eq for s in data["theory_sections"] for eq in s.get("equations", [])]
    latex = " ".join(eq["latex"] for eq in equations)
    meanings = " ".join(eq["meaning"] for eq in equations).lower()
    assert "N_{unique}" in latex
    assert "k_{min}" in latex
    assert "N_{suppressed}" in latex
    assert "no para demostrar anonimato" in meanings
    assert "no prueba anonimato ni cumplimiento" in meanings
    assert "no mide por sí sola privacidad" in meanings


def test_unit_06_uses_only_synthetic_nonclinical_scope():
    data = load(SOURCE)
    text = json.dumps(data, ensure_ascii=False).lower()
    assert "datos sintéticos o no identificables desde origen" in text
    assert "no se conectan ehr, pacs, lis" in text
    assert "no constituyen evaluación jurídica" in text
    assert "no certifican conformidad" in text
    assert "no acredita competencia jurídica" in text


def test_unit_06_references_current_primary_frameworks():
    data = load(SOURCE)
    urls = {s["url"] for s in data["sources"]}
    assert "https://www.nist.gov/privacy-framework" in urls
    assert "https://csrc.nist.gov/pubs/sp/800/188/final" in urls
    assert "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final" in urls
    assert "https://eur-lex.europa.eu/eli/reg/2016/679/oj" in urls
    assert "https://bitol-io.github.io/open-data-contract-standard/v3.1.0/fundamentals/" in urls
    assert "https://pmc.ncbi.nlm.nih.gov/articles/PMC8591903/" in urls


def test_public_descriptor_and_editorial_status_when_published():
    data = load(SOURCE)
    if DESCRIPTOR.exists():
        descriptor = load(DESCRIPTOR)
        detail = next((u for u in descriptor.get("detailed_units", []) if u.get("unit") == 6), None)
        if detail and detail.get("description") != "Integrar privacidad, acceso, contratos para resolver un caso de entrega responsable de productos de datos con evidencia, controles, incertidumbre y comunicación proporcional.":
            assert detail["description"] == data["purpose"]
    if CATALOG.exists():
        catalog = load(CATALOG)
        detected = catalog.get("template_detected", [])
        if "ingenieria-datos-biomedicos" not in detected:
            assert "ingenieria-datos-biomedicos" in catalog.get("screened_no_known_template_marker", [])
