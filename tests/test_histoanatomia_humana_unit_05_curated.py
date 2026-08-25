from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "histoanatomia-humana" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "histoanatomia-humana" / "unit-05.json"
SUBJECT = ROOT / "data" / "subjects" / "biologicas-medicas" / "histoanatomia-humana.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class HistoanatomiaHumanaUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["slug"], "sistemas-digestivo-renal-y-endocrino")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"v=\\frac{\\delta y}{\\delta t}", self.text)

    def test_objectives_cover_digestive_renal_endocrine_multiscale_anatomy(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "mucosa → submucosa → muscularis externa",
            "glándulas de brunner",
            "flujo sanguíneo y biliar",
            "corpúsculo renal",
            "aparato yuxtaglomerular",
            "adenohipófisis y neurohipófisis",
            "folículos tiroideos",
            "corteza y médula suprarrenal",
            "tres rasgos positivos",
        ):
            self.assertIn(phrase, objectives)

    def test_five_substantive_theory_sections(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        for section in sections:
            self.assertGreaterEqual(len(section["paragraphs"]), 6)
            self.assertGreaterEqual(len(section["key_points"]), 6)
            for point in section["key_points"]:
                self.assertGreaterEqual(len(point.split()), 5)
        headings = " ".join(x["heading"] for x in sections).casefold()
        for phrase in ("tubo digestivo", "hígado, vesícula y páncreas", "riñón y nefrona", "órganos endocrinos", "identificación integrada"):
            self.assertIn(phrase, headings)

    def test_gastrointestinal_section_uses_wall_architecture_and_regional_transitions(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in (
            "epitelio, lámina propia y muscularis mucosae",
            "epitelio plano estratificado no queratinizado",
            "fositas gástricas",
            "carece de vellosidades",
            "glándulas de brunner",
            "agregados linfoides",
            "colon carece de vellosidades",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no autoriza inferencias sobre inflamación", text)

    def test_hepatobiliary_pancreas_section_preserves_opposite_flows_and_mixed_gland(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "vena central",
            "tractos portales",
            "sinusoides",
            "dirección general opuesta",
            "espacio perisinusoidal o de disse",
            "carece de una submucosa típica",
            "células centroacinares",
            "islotes más pálidos",
            "no posee conductos estriados",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no deben asignarse por posición o color", text)

    def test_kidney_section_builds_nephron_and_juxtaglomerular_relations(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in (
            "corteza externa y médula",
            "corpúsculo renal",
            "polo vascular",
            "polo urinario",
            "endotelio capilar fenestrado",
            "membrana basal glomerular",
            "podocitos",
            "borde en cepillo",
            "aparato yuxtaglomerular",
            "mácula densa",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no usa número de glomérulos", text)

    def test_endocrine_section_distinguishes_organs_and_he_limits(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "adenohipófisis y neurohipófisis",
            "pituicitos",
            "folículos llenos de coloide",
            "células principales",
            "zonas glomerulosa, fasciculata y reticularis",
            "células cromafines",
            "islotes",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no es seguro diferenciar células beta, alfa, delta o pp", text)
        self.assertIn("sin apoyo metodológico", text)

    def test_integrated_identification_requires_low_power_positive_negative_and_alternative(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "empieza a bajo aumento",
            "al menos tres rasgos positivos",
            "rasgos negativos",
            "corte tangencial",
            "clasificación provisional",
            "otro nivel de corte",
            "u6 pasará a sistemas nervioso y reproductor",
        ):
            self.assertIn(phrase, text)
        self.assertIn("no establece si una muestra clínica es normal o patológica", text)

    def test_glossary_and_examples_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 60)
        for term in (
            "mucosa", "glándula de brunner", "lobulillo hepático clásico", "canalículo biliar",
            "acino pancreático", "islote pancreático", "corpúsculo renal", "podocito",
            "túbulo contorneado proximal", "aparato yuxtaglomerular", "adenohipófisis",
            "folículo tiroideo", "célula principal paratiroidea", "zona fasciculata", "médula suprarrenal",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)

    def test_guided_activity_is_multiorgan_and_safe(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 300)
        self.assertGreaterEqual(len(activity["problems"]), 24)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 26)
        joined = " ".join(activity["instructions"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "cuatro rutas paralelas",
            "tres rasgos positivos",
            "dos rasgos negativos",
            "flujo sanguíneo",
            "flujo biliar",
            "aparato yuxtaglomerular",
            "no se formula diagnóstico",
        ):
            self.assertIn(phrase, joined)

    def test_sources_assessment_connections_and_editorial_boundary(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "no constituye entrenamiento diagnóstico",
            "interpretación clínica de biopsias",
            "no establece por sí sola",
            "inmunohistoquímica",
            "tampoco prescribe tratamiento",
        ):
            self.assertIn(phrase, notice)

    def test_u1_to_u6_curricular_boundaries(self) -> None:
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "orientación y preparación de u1",
            "criterios tisulares de u2",
            "razonamiento multiescala de u3",
            "organización vascular de u4",
            "u6 pasará a sistemas nervioso y reproductor",
        ):
            self.assertIn(phrase, purpose)

    def test_published_descriptor_matches_curated_unit(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        self.assertEqual(detailed[5]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()
