from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/informatica-biomedica/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/informatica-biomedica/unit-06.json"


def test_informatica_biomedica_u6_publication_checkpoint() -> None:
    """Final user-authored checkpoint after publication synchronization of U6."""
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    mirror = json.loads(MIRROR.read_text(encoding="utf-8"))

    assert source == mirror
    assert source["slug"] == "gobernanza-e-implementacion"
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
