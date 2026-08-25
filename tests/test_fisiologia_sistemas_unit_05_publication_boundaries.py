from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_UNIT = ROOT / "biologicas-medicas" / "fisiologia-sistemas" / "unidades" / "unidad-05.html"


class FisiologiaSistemasUnit05PublicationBoundaryTests(unittest.TestCase):
    def test_public_u5_preserves_non_diagnostic_boundaries(self) -> None:
        text = PUBLIC_UNIT.read_text(encoding="utf-8").casefold()
        for phrase in (
            "distinguir infección de inflamación estéril",
            "fiebre de hipertermia",
            "evitando usar una citocina o crp como marcador etiológico específico",
            "sin convertir la temperatura corporal en prueba de infección",
            "resolución activa",
            "perfiles exclusivamente sintéticos",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
