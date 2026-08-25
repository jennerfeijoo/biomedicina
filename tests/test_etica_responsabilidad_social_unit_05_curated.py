from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "etica-responsabilidad-social" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "etica-responsabilidad-social" / "unit-05.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class EticaResponsabilidadSocialUnit05CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "etica-responsabilidad-social")
        self.assertEqual(self.unit["unit"], 5)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_generic_mcdm_equation_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn(r"V(a)=\sum", json.dumps(self.unit, ensure_ascii=False))
        for concept in (
            "unidad funcional", "límite del sistema", "residuos sanitarios",
            "segregación en origen", "reprocesamiento", "compra sostenible",
            "debida diligencia", "derechos humanos", "greenwashing",
        ):
            self.assertIn(concept, self.text)

    def test_theory_is_substantive_and_has_curricular_boundaries(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        headings = " ".join(section["heading"] for section in sections).casefold()
        for concept in ("ciclo de vida", "residuos sanitarios", "reutilización", "compra sostenible", "derechos humanos"):
            self.assertIn(concept, headings)
        self.assertIn("u4 abordó quién puede acceder", self.text)
        self.assertIn("u6 integrará deliberación", self.text)

    def test_life_cycle_reasoning_uses_functional_units_and_sensitivity(self) -> None:
        equations = {
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        }
        self.assertIn(r"I_{\mathrm{waste}}=\frac{M_{\mathrm{waste}}}{N_{\mathrm{functional\ units}}}", equations)
        self.assertIn(r"I_{\mathrm{reuse}}(n)=\frac{I_{\mathrm{production}}+I_{\mathrm{end\ of\ life}}}{n}+I_{\mathrm{reprocessing}}", equations)
        self.assertIn("no es una ecuación normativa de acv", self.text)
        self.assertIn("análisis de sensibilidad", self.text)
        self.assertIn("vida útil efectiva", self.text)

    def test_healthcare_waste_is_not_taught_as_one_homogeneous_stream(self) -> None:
        self.assertIn("aproximadamente el 85 %", self.text)
        self.assertIn("alrededor del 15 %", self.text)
        self.assertIn("referencia global, no una regla", self.text)
        for concept in ("punzocortantes", "infecciosos", "químicos o farmacéuticos", "radiactivos", "eléctricos o electrónicos"):
            self.assertIn(concept, self.text)
        self.assertIn("el residuo electrónico puede contener baterías", self.text)
        self.assertIn("minimización", self.text)
        self.assertIn("reciclabilidad teórica y reciclaje real", self.text)

    def test_reusable_vs_single_use_avoids_absolute_claims(self) -> None:
        self.assertIn("no determinan por sí solas el impacto ambiental", self.text)
        self.assertIn("reutilización puede reducir múltiples impactos", self.text)
        self.assertIn("excepto consumo de agua", self.text)
        self.assertIn("el resultado puede cambiar con parámetros locales", self.text)
        self.assertIn("seguridad del paciente", self.text)
        self.assertIn("no es una alternativa funcional válida", self.text)

    def test_supply_chain_due_diligence_is_process_not_certificate(self) -> None:
        for concept in (
            "trabajo forzoso", "trabajo infantil", "libertad de asociación",
            "discriminación", "entorno de trabajo seguro y saludable",
            "mecanismos de queja", "voz de trabajadores",
        ):
            self.assertIn(concept, self.text)
        self.assertIn("debida diligencia no significa", self.text)
        self.assertIn("una auditoría puntual", self.text)
        self.assertIn("proveedor de primer nivel", self.text)

    def test_guided_activity_is_scaffolded_and_synthetic(self) -> None:
        activities = self.unit["guided_activities"]
        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertGreaterEqual(len(activity["instructions"]), 8)
        self.assertGreaterEqual(len(activity["problems"]), 16)
        self.assertGreaterEqual(len(activity["deliverables"]), 7)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 16)
        text = json.dumps(activity, ensure_ascii=False).casefold()
        self.assertIn("no cargues datos de pacientes", text)
        self.assertIn("1 000 unidades funcionales", text)
        self.assertIn("20, 50 y 100 ciclos", text)
        self.assertIn("100 % sostenible", text)
        self.assertIn("no presentes el ejercicio como acv conforme a iso", text)

    def test_learning_scaffolds_are_specific_and_sufficient(self) -> None:
        self.assertGreaterEqual(len(self.unit["glossary"]), 24)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 13)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        for term in (
            "análisis de ciclo de vida (acv)", "unidad funcional", "límite del sistema",
            "segregación en origen", "residuo electrónico", "reprocesamiento",
            "compra sostenible", "coste del ciclo de vida",
            "debida diligencia en derechos humanos", "greenwashing",
        ):
            self.assertIn(term, terms)

    def test_sources_are_directly_verified_and_cover_environment_and_labour(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 10)
        self.assertTrue(all(source.get("verification_status") == "verified_directly" for source in sources))
        urls = {source["url"] for source in sources}
        expected = {
            "https://www.who.int/news-room/fact-sheets/detail/health-care-waste",
            "https://www.who.int/publications/i/item/9789240081888",
            "https://www.iso.org/standard/37456.html",
            "https://www.undp.org/publications/guidelines-sustainable-procurement-healthcare-commodities-and-services",
            "https://www.ilo.org/topics-and-sectors/fundamental-principles-and-rights-work",
            "https://www.ohchr.org/Documents/Publications/GuidingPrinciplesBusinessHR_EN.pdf",
            "https://www.oecd.org/en/publications/2018/02/oecd-due-diligence-guidance-for-responsible-business-conduct_c669bd57.html",
            "https://pubmed.ncbi.nlm.nih.gov/36433787/",
            "https://pubmed.ncbi.nlm.nih.gov/41419285/",
        }
        self.assertTrue(expected.issubset(urls))

    def test_professional_overclaiming_is_blocked(self) -> None:
        notice = self.unit["editorial_notice"].casefold()
        for boundary in (
            "no constituye revisión disciplinar externa",
            "análisis de ciclo de vida conforme o certificado",
            "auditoría ambiental", "certificación de sostenibilidad",
            "verificación de una cadena de suministro",
            "auditoría laboral o de derechos humanos", "asesoría jurídica",
            "evaluación de conformidad", "validación de reprocesamiento",
            "validación clínica", "recomendación de compra", "autorización de despliegue",
        ):
            self.assertIn(boundary, notice)
        self.assertIn("jurisdicción", notice)
        self.assertIn("normativa vigente", notice)


if __name__ == "__main__":
    unittest.main()
