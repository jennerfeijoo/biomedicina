from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/informatica-biomedica/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/informatica-biomedica/unit-06.json"
DESCRIPTOR = ROOT / "data/subjects/ingenieria-biomedica/informatica-biomedica.json"
CATALOG = ROOT / "data/catalog_statuses.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_informatica_biomedica_u6_publication_checkpoint() -> None:
    """Validate the exact published state that closes Informática Biomédica U6."""
    source = load_json(SOURCE)
    mirror = load_json(MIRROR)
    descriptor = load_json(DESCRIPTOR)
    catalog = load_json(CATALOG)

    assert source == mirror
    assert source["slug"] == "gobernanza-e-implementacion"

    published = next(item for item in descriptor["detailed_units"] if item["unit"] == 6)
    assert published["description"] == source["purpose"]

    detected = catalog["dimensions"]["specificity"]["template_detected"]
    screened = catalog["dimensions"]["specificity"]["screened_no_known_template_marker"]
    assert "informatica-biomedica" not in detected
    assert "informatica-biomedica" in screened

    text = json.dumps(source, ensure_ascii=False).lower()
    for concept in (
        "derechos de decisión",
        "privacidad y ciberseguridad",
        "gestión del cambio",
        "contingencia",
        "implementación sociotécnica",
        "revalidación",
    ):
        assert concept in text
