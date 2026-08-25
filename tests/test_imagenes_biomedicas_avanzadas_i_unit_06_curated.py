from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/imagenes-biomedicas-avanzadas-i/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/imagenes-biomedicas-avanzadas-i/unit-06.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TestImagenesBiomedicasAvanzadasIUnit06Curated(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = load_json(SOURCE)
        cls.mirror = load_json(MIRROR)
        cls.text = json.dumps(cls.unit, ensure_ascii=False).lower()

    def test_source_and_generated_mirror_are_identical(self) -> None:
        self.assertEqual(self.unit, self.mirror)

    def test_unit_identity_and_depth(self) -> None:
        self.assertEqual(self.unit["subject_id"], "imagenes-biomedicas-avanzadas-i")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["slug"], "control-de-calidad-cuantitativo")
        self.assertEqual(self.unit["status"], "review")
        self.assertGreaterEqual(len(self.unit["learning_objectives"]), 6)
        self.assertGreaterEqual(len(self.unit["theory_sections"]), 5)
        for section in self.unit["theory_sections"]:
            self.assertGreaterEqual(len(section["paragraphs"]), 5)
            self.assertGreaterEqual(len(section["key_points"]), 5)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 4)
        self.assertGreaterEqual(len(self.unit["glossary"]), 35)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 16)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        self.assertGreaterEqual(len(self.unit["sources"]), 15)

    def test_guided_activity_is_substantive_and_checkable(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 18)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 18)

    def test_generic_template_and_legacy_cnr_are_removed(self) -> None:
        banned = [
            "concepto de la unidad que debe definirse",
            "modelo conceptual de control de calidad cuantitativo",
            "integrar fantomas, reproducibilidad, incertidumbre para resolver un caso",
            "cnr=",
            "contraste respecto al ruido entre dos regiones",
        ]
        for marker in banned:
            self.assertNotIn(marker, self.text)

    def test_metrology_core_is_explicit(self) -> None:
        required = [
            "mensurando",
            "valor de referencia",
            "sesgo",
            "precisión",
            "linealidad",
            "fantoma físico",
            "objeto digital de referencia",
            "test-retest",
            "repetibilidad",
            "reproducibilidad",
            "wsd",
            "wcv",
            "coeficiente de repetibilidad",
            "2.77",
            "bland-altman",
            "icc",
            "heteroscedasticidad",
            "armonización",
            "presupuesto de incertidumbre",
            "criterio de aceptación",
        ]
        for concept in required:
            self.assertIn(concept, self.text)

    def test_critical_interpretive_boundaries_are_protected(self) -> None:
        self.assertIn("correlación alta no demuestra linealidad ni ausencia de sesgo", self.text)
        self.assertIn("benchmark digital demuestra conformidad computacional con ese caso, no desempeño del escáner ni validez clínica", self.text)
        self.assertIn("icc alto no garantiza error absoluto suficientemente pequeño", self.text)
        self.assertIn("no establece causa biológica, relevancia clínica ni respuesta terapéutica", self.text)
        self.assertIn("desempeño técnico, validez científica y utilidad clínica son capas distintas", self.text)
        self.assertIn("no certifica un dispositivo", self.text)

    def test_qiba_ibsi_and_uncertainty_are_used_with_correct_scope(self) -> None:
        self.assertIn("qiba profiles", self.text)
        self.assertIn("ibsi", self.text)
        self.assertIn("objeto digital", self.text)
        self.assertIn("armonización reduce variabilidad pero no crea utilidad clínica automáticamente", self.text)
        self.assertIn("cambios de versión obligan a revisar qué claims técnicos requieren revalidación", self.text)

    def test_examples_require_interpretation_and_limits(self) -> None:
        for example in self.unit["worked_examples"]:
            self.assertGreaterEqual(len(example["reasoning_steps"]), 5)
            self.assertTrue(example["interpretation"].strip())
            self.assertGreaterEqual(len(example["limitations"]), 3)

    def test_self_assessment_contains_reasoning_and_common_error(self) -> None:
        for item in self.unit["self_assessment"]:
            self.assertTrue(item["question"].strip())
            self.assertTrue(item["answer"].strip())
            self.assertTrue(item["reasoning"].strip())
            self.assertTrue(item["common_error"].strip())

    def test_sources_are_verified_and_relevant(self) -> None:
        for source in self.unit["sources"]:
            self.assertEqual(source["verification_status"], "verified_directly")
            self.assertTrue(source["url"].startswith("https://"))
        urls = " ".join(source["url"].lower() for source in self.unit["sources"])
        for domain in ["pmc.ncbi.nlm.nih.gov", "theibsi.github.io", "rsna.org", "nist.gov", "ncbi.nlm.nih.gov"]:
            self.assertIn(domain, urls)

    def test_editorial_notice_blocks_clinical_or_regulatory_overreach(self) -> None:
        notice = self.unit["editorial_notice"].lower()
        for phrase in [
            "no interpreta imágenes de pacientes",
            "no establece diagnóstico",
            "no acredita sitios ni equipos",
            "no certifica dispositivos o software",
            "no demuestra conformidad regulatoria",
            "no cualifica un biomarcador",
        ]:
            self.assertIn(phrase, notice)


if __name__ == "__main__":
    unittest.main()
