from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "economia-gestion-empresas" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "economia-gestion-empresas" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EconomiaGestionEmpresasUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "ley de little",
            "cuello de botella",
            "utilización",
            "punto de reposición",
            "stock de seguridad",
            "pdsa",
            "medida de equilibrio",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_operational(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        self.assertIn("throughput observado", theory)
        self.assertIn("no es sinónimo de capacidad", theory)
        self.assertIn("la prueba pequeña es diferente de la implementación permanente", theory)
        self.assertIn("no autoriza desplegar el cambio", theory)
        self.assertIn("no reproduce cláusulas", theory)
        self.assertIn("no sustituye", theory)

    def test_core_equations_are_present(self):
        equations = {e["latex"] for section in self.unit["theory_sections"] for e in section.get("equations", [])}
        self.assertIn(r"L=\lambda W", equations)
        self.assertIn(r"C_i=\frac{T_{disponible,i}}{t_{ciclo,i}}", equations)
        self.assertIn(r"C_{proceso}=\min_i(C_i)", equations)
        self.assertIn(r"u=\frac{\lambda_d}{C}", equations)
        self.assertIn(r"ROP=dL+SS", equations)

    def test_examples_and_guided_activity_are_synthetic_and_scaffolded(self):
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 10)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 10)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 12)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("sintético", text)
        self.assertIn("no uses datos de pacientes", text)
        self.assertIn("resultado", text)
        self.assertIn("equilibrio", text)

    def test_glossary_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 12)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "throughput",
            "trabajo en proceso (wip)",
            "ley de little",
            "capacidad efectiva",
            "cuello de botella",
            "punto de reposición",
            "medida de equilibrio",
            "gráfico de ejecución",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        self.assertIn("https://pubsonline.informs.org/doi/abs/10.1287/opre.9.3.383", urls)
        self.assertIn("https://www.who.int/publications/i/item/9789241548274", urls)
        self.assertIn("https://www.iso.org/standard/76677.html", urls)
        self.assertIn("https://www.ihi.org/library/model-for-improvement", urls)
        self.assertIn("https://www.ihi.org/library/tools/run-chart-tool", urls)

    def test_real_world_boundary_is_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        self.assertIn("no constituye revisión disciplinar externa", notice)
        self.assertIn("procedimiento operativo estándar", notice)
        self.assertIn("datos personales", notice)
        self.assertIn("no constituye un procedimiento operativo institucional", purpose)
        self.assertIn("acreditación", purpose)


if __name__ == "__main__":
    unittest.main()
