from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "biomateriales" / "units" / "unit-03.json"
MIRROR = ROOT / "data" / "generated_units" / "biomateriales" / "unit-03.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class BiomaterialesUnit03CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "biomateriales")
        self.assertEqual(self.unit["unit"], 3)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_is_removed_and_interface_scope_is_specific(self) -> None:
        text = SOURCE.read_text(encoding="utf-8").casefold()
        self.assertNotIn(GENERIC, text)
        for concept in (
            "capa de acondicionamiento",
            "efecto vroman",
            "integrinas",
            "adhesiones focales",
            "complemento",
            "reacción a cuerpo extraño",
            "citotoxicidad",
        ):
            self.assertIn(concept, text)

    def test_theory_is_substantive_and_respects_course_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 4)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 4 for section in sections))
        theory = " ".join(p for s in sections for p in s["paragraphs"]).casefold()
        self.assertIn("u4 estudiará degradación", theory)
        self.assertIn("iso 10993-1:2025", theory)
        self.assertIn("no debe memorizarse como una regla universal", theory)
        self.assertIn("la clasificación m1/m2", theory)

    def test_core_equations_are_present_and_limited(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"\theta=\frac{KC}{1+KC}", equations)
        self.assertIn(r"A_{rel}=\frac{N_{adheridas}}{N_{sembradas}}", equations)
        self.assertIn(r"V_{rel}(\%)=100\frac{S_{muestra}-S_{blanco}}{S_{control}-S_{blanco}}", equations)

    def test_guided_activities_are_progressive_synthetic_and_scaffolded(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertGreaterEqual(len(activities), 3)
        titles = {a["title"] for a in activities}
        self.assertIn("Actividad guiada: reconstrucción de una interfaz proteica sintética", titles)
        self.assertIn("Actividad guiada: de adhesión celular a respuesta inmune", titles)
        self.assertIn("Actividad integradora: expediente sintético de seguridad biológica preliminar", titles)
        primary = activities[0]
        self.assertGreaterEqual(len(primary["instructions"]), 8)
        self.assertGreaterEqual(len(primary["problems"]), 12)
        self.assertGreaterEqual(len(primary["deliverables"]), 7)
        self.assertGreaterEqual(len(primary["checking_criteria"]), 10)
        text = json.dumps(activities, ensure_ascii=False).casefold()
        self.assertIn("no uses muestras humanas", text)
        self.assertIn("no se declara seguridad biológica integral", text)

    def test_glossary_examples_errors_and_assessment_are_substantive(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 20)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 10)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 10)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "capa de acondicionamiento",
            "integrina",
            "mecanotransducción",
            "célula gigante de cuerpo extraño",
            "biocompatibilidad",
        ):
            self.assertIn(term, terms)

    def test_sources_are_traceable_and_current_standards_are_included(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 9)
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in sources))
        urls = {s["url"] for s in sources}
        self.assertIn("https://www.iso.org/standard/10993-1", urls)
        self.assertIn("https://www.iso.org/standard/36406.html", urls)
        self.assertIn("https://www.iso.org/standard/75769.html", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/40609300/", urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/33775905/", urls)

    def test_clinical_regulatory_and_wet_lab_boundaries_are_explicit(self) -> None:
        text = json.dumps(self.unit, ensure_ascii=False).casefold()
        self.assertIn("no constituye revisión disciplinar externa", text)
        self.assertIn("no autorizan ensayos en personas", text)
        self.assertIn("cultivo celular", text)
        self.assertIn("degradación/corrosión se reserva para u4", text)
        self.assertIn("requisitos regulatorios para u6", text)
        self.assertIn("no debe tratarse como etiqueta absoluta", text)


# Final user-authored trigger after publication metadata synchronization.
if __name__ == "__main__":
    unittest.main()
