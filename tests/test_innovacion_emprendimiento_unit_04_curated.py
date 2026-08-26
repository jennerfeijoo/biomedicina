from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-04.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-04.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "innovacion-emprendimiento.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"

def norm(text: str) -> str:
    return text.casefold().replace("–", "-").replace("—", "-")

class InnovacionEmprendimientoUnit04CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = norm(json.dumps(cls.unit, ensure_ascii=False))
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))

    def test_source_mirror_and_identity(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "innovacion-emprendimiento")
        self.assertEqual(self.unit["unit"], 4)
        self.assertEqual(self.unit["title"], "Modelo de negocio y acceso")
        self.assertEqual(self.unit["status"], "review")

    def test_template_and_generic_score_are_absent(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v(a)=\\sum", self.text)
        self.assertNotIn("modelo multicriterio transparente para comparar alternativas", self.text)

    def test_actor_and_payment_roles_are_not_collapsed(self) -> None:
        for concept in (
            "beneficiario", "usuario", "comprador", "pagador", "proveedor",
            "flujo de decisión", "flujo de dinero", "propuesta de valor por actor",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        theory = norm(json.dumps(self.unit["theory_sections"], ensure_ascii=False))
        self.assertIn("«cliente» rara vez es una entidad única", theory)
        self.assertIn("puede no ser quien usa directamente", theory)

    def test_coverage_reimbursement_and_regulation_are_separated(self) -> None:
        for concept in ("cobertura", "reembolso", "compra institucional", "pago de bolsillo", "hta"):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        self.assertIn("autorización de mercado no garantiza cobertura", self.text)
        self.assertIn("separar autorización regulatoria de adopción y financiación", self.text)
        self.assertIn("no se ofrece asesoría de reembolso", self.text)

    def test_unit_economics_are_bounded_and_auditable(self) -> None:
        equations = norm(json.dumps(self.unit["theory_sections"], ensure_ascii=False))
        for concept in ("margen de contribución", "punto de equilibrio", "coste variable", "costes fijos", "costes escalonados"):
            with self.subTest(concept=concept):
                self.assertIn(concept, equations)
        self.assertIn("mc = i_u - c_{v,u}", equations)
        self.assertIn("q_{be}=\\frac{c_f}{mc}", equations)
        self.assertIn("no es una valoración de empresa", equations)
        self.assertIn("precio tampoco equivale a coste para el sistema ni a valor", equations)

    def test_access_and_equity_are_operationalized(self) -> None:
        for concept in (
            "embudo de acceso", "acceso efectivo", "protección financiera",
            "barrera financiera", "barrera geográfica", "barrera organizativa",
            "barrera digital", "equidad de acceso", "salvaguarda de acceso",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, self.text)
        self.assertIn("disponibilidad comercial no garantiza acceso efectivo", self.text)
        self.assertIn("la equidad no se resume en un promedio", self.text)
        self.assertIn("no se fusionan en una única puntuación", self.text)

    def test_theory_and_scaffolds_are_substantial(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        self.assertGreaterEqual(len(self.unit["glossary"]), 45)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertEqual(len(self.unit["guided_activities"]), 1)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 12)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 9)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)

    def test_u3_to_u5_curricular_boundary_is_explicit(self) -> None:
        self.assertIn("dossier de aprendizaje de u3", self.text)
        self.assertIn("transferir propiedad intelectual y regulación a u5", self.text)
        self.assertIn("patentes, libertad de operación, clasificación regulatoria", self.text)
        self.assertIn("u4 no resuelve esas materias", self.text)

    def test_sources_are_verified_and_multisource(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        urls = " ".join(item["url"].casefold() for item in sources)
        for domain in ("who.int", "nice.org.uk", "health.ec.europa.eu", "pubmed.ncbi.nlm.nih.gov", "biodesign.stanford.edu"):
            with self.subTest(domain=domain):
                self.assertIn(domain, urls)

    def test_editorial_boundaries_are_explicit(self) -> None:
        notice = norm(self.unit["editorial_notice"])
        for boundary in (
            "no constituye asesoría de reembolso", "hta formal", "valoración empresarial",
            "recomendación de inversión", "propiedad intelectual", "regulatoria",
            "no demuestra acceso real", "disposición a pagar", "seguridad", "eficacia",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, notice)

    def test_published_descriptor_is_allowed_to_sync_then_must_match_when_promoted(self) -> None:
        published = next(item for item in self.subject["detailed_units"] if item["unit"] == 4)
        self.assertEqual(published["title"], self.unit["title"])
        if published["description"] == self.unit["purpose"]:
            self.assertIn("beneficiario, usuario, comprador, pagador", norm(published["description"]))

if __name__ == "__main__":
    unittest.main()
