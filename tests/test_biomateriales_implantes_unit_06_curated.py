from __future__ import annotations

import json
import unittest
from pathlib import Path

# Final user-authored gate trigger after publication and mirror synchronization.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales-implantes" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales-implantes" / "unit-06.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesImplantesUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales-implantes")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_old_mechanics_fallback_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("\\sigma=\\frac{f}{a_0}", self.text)
        for concept in (
            "iso 14971:2019",
            "situación peligrosa",
            "riesgo residual",
            "iso 10993-1:2025",
            "pmcf",
            "psur",
            "estudio 522",
            "denominador",
            "causalidad",
        ):
            self.assertIn(concept, self.text)

    def test_theory_closes_the_course_without_collapsing_evidence_layers(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 4 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for phrase in (
            "no son sinónimos",
            "no obliga a una fórmula universal",
            "no equivale a una lista automática",
            "pms es más amplia",
            "no prueba causalidad",
            "un periodo sin eventos no demuestra riesgo cero",
        ):
            self.assertIn(phrase, theory)

    def test_rate_equations_are_present_and_noncausal(self) -> None:
        equations = {
            equation["latex"]: equation["meaning"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn("r=\\frac{E}{N}", equations)
        self.assertIn("r_T=\\frac{E}{T}", equations)
        self.assertIn("RR=\\frac{r_2}{r_1}", equations)
        self.assertIn("no demuestra", equations["RR=\\frac{r_2}{r_1}"].casefold())
        self.assertIn("denominador", equations["r=\\frac{E}{N}"].casefold())

    def test_learning_support_is_substantive(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 5)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "gestión de riesgo",
            "situación peligrosa",
            "riesgo residual",
            "vigilancia poscomercialización",
            "pmcf",
            "psur",
            "señal",
            "denominador",
            "estudio 522",
        ):
            self.assertIn(term, terms)

    def test_guided_activities_are_progressive_synthetic_and_bounded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 3)
        first = activities[0]
        self.assertGreaterEqual(len(first["instructions"]), 10)
        self.assertGreaterEqual(len(first["problems"]), 15)
        self.assertGreaterEqual(len(first["deliverables"]), 8)
        self.assertGreaterEqual(len(first["checking_criteria"]), 10)
        activity_text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("exclusivamente", activity_text)
        self.assertIn("no uses expedientes reales", activity_text)
        self.assertIn("práctica con apoyo reducido", activity_text)
        self.assertIn("reto de transferencia", activity_text)
        self.assertIn("no decide reportabilidad", activity_text)

    def test_sources_are_directly_verified_and_version_aware(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 12)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = {item["url"] for item in sources}
        for url in (
            "https://www.iso.org/standard/72704.html",
            "https://www.iso.org/standard/67942.html",
            "https://www.iso.org/es/norma/10993-1",
            "https://eur-lex.europa.eu/eli/reg/2017/745/2020-04-24",
            "https://health.ec.europa.eu/latest-updates/mdcg-2025-10-guidance-post-market-surveillance-medical-devices-and-vitro-diagnostic-medical-devices-2025-12-19_en",
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/522-postmarket-surveillance-studies-program",
            "https://www.fda.gov/medical-devices/postmarket-requirements-devices/mandatory-reporting-requirements-manufacturers-importers-and-device-user-facilities",
        ):
            self.assertIn(url, urls)
        source_text = json.dumps(sources, ensure_ascii=False).casefold()
        self.assertIn("iso/awi ts 24971-1", source_text)
        self.assertIn("iso/awi tr 20416", source_text)
        self.assertGreaterEqual(source_text.count("trabajo en desarrollo"), 2)

    def test_editorial_boundary_is_explicit(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("asesoría regulatoria o jurídica", notice)
        self.assertIn("todas las actividades y tasas son sintéticas", notice)
        self.assertIn("no contienen datos de pacientes", notice)
        self.assertIn("sin emitir certificaciones", objectives)
        self.assertIn("sin convertir", purpose)


if __name__ == "__main__":
    unittest.main()
