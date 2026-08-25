from __future__ import annotations

# Final human trigger for U3 validation; academic content is unchanged.

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

    def test_exact_mirror_and_review_status(self):
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["title"], "Operaciones y procesos")
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_old_mcda_are_removed(self):
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        self.assertNotIn("v(a)=", text)
        for concept in ("cuello de botella", "ley de little", "punto de pedido", "medida de balance", "pdsa"):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_operations_specific(self):
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for section in sections for p in section["paragraphs"]).casefold()
        for concept in ("capacidad efectiva", "throughput", "turnaround", "stock de seguridad", "resultado, proceso y balance"):
            self.assertIn(concept, theory)
        self.assertIn("no evalúa conformidad completa", theory)

    def test_core_equations_are_present_with_limits(self):
        equations = {e["latex"] for section in self.unit["theory_sections"] for e in section.get("equations", [])}
        for equation in (r"C_i=\frac{T_{avail,i}}{t_{proc,i}}", r"C_{process}=\min_i(C_i)", r"u=\frac{X}{C_{effective}}", r"L=\lambda W", "ROP=dL+SS"):
            self.assertIn(equation, equations)

    def test_examples_and_guided_activity_are_scaffolded_and_synthetic(self):
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 6)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 16)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 10)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("ficticio", text)
        self.assertIn("no uses", text)
        self.assertIn("medida de balance", text)

    def test_glossary_errors_and_assessment_are_specific(self):
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in ("capacidad efectiva", "cuello de botella", "ley de little", "punto de pedido", "medida de balance", "pdsa"):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_include_current_quality_standard(self):
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(source["verification_status"] == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        self.assertIn("https://www.iso.org/standard/76677.html", urls)
        self.assertIn("https://pubsonline.informs.org/doi/abs/10.1287/opre.9.3.383", urls)
        self.assertIn("https://www.ihi.org/library/model-for-improvement", urls)
        self.assertIn("https://extranet.who.int/hslp/content/LQMS-training-toolkit", urls)

    def test_scope_boundaries_are_explicit(self):
        notice = self.unit["editorial_notice"].casefold()
        purpose = self.unit["purpose"].casefold()
        for phrase in ("no constituye revisión disciplinar externa", "acreditación iso 15189", "validación clínica", "conformidad regulatoria"):
            self.assertIn(phrase, notice)
        self.assertIn("estrategia de mercado", purpose)
        self.assertIn("evaluación económica sanitaria", purpose)


if __name__ == "__main__":
    unittest.main()
