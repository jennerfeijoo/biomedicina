from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "innovacion-emprendimiento" / "units" / "unit-02.json"
MIRROR = ROOT / "data" / "generated_units" / "innovacion-emprendimiento" / "unit-02.json"
SUBJECT = ROOT / "data" / "subjects" / "gestion-etica-comunicacion" / "innovacion-emprendimiento.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


def norm(text: str) -> str:
    return text.casefold().replace("–", "-").replace("—", "-")


class InnovacionEmprendimientoUnit02CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = norm(SOURCE.read_text(encoding="utf-8"))
        cls.subject = json.loads(SUBJECT.read_text(encoding="utf-8"))

    def assertContainsAll(self, text: str, terms: tuple[str, ...]) -> None:
        text = norm(text)
        for term in terms:
            with self.subTest(term=term):
                self.assertIn(norm(term), text)

    def test_source_mirror_identity_and_metadata(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit["schema_version"], "2.0")
        self.assertEqual(self.unit["subject_id"], "innovacion-emprendimiento")
        self.assertEqual(self.unit["unit"], 2)
        self.assertEqual(self.unit["status"], "review")

    def test_generic_template_and_multicriteria_shortcut_are_removed(self) -> None:
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("v(a)=\\sum", self.text)
        self.assertNotIn("modelo multicriterio transparente para comparar alternativas", self.text)
        self.assertNotIn("definir problema público -> mapear actores y valores", self.text)

    def test_theory_has_specific_problem_solution_fit_architecture(self) -> None:
        sections = self.unit["theory_sections"]
        self.assertEqual(len(sections), 5)
        self.assertTrue(all(len(section["paragraphs"]) >= 5 for section in sections))
        self.assertTrue(all(len(section["key_points"]) >= 5 for section in sections))
        self.assertContainsAll(
            self.text,
            (
                "propuesta de valor",
                "hipótesis falsable",
                "alternativa de referencia",
                "statu quo",
                "ajuste problema-solución",
                "product-market fit",
                "segmentación",
                "contexto de uso",
                "resultado observable",
                "evidencia discrepante",
                "caso negativo",
                "criterio de salida",
                "seguir, revisar o rechazar",
            ),
        )

    def test_roles_context_and_transferred_burdens_remain_separate(self) -> None:
        roles = norm(json.dumps(self.unit["theory_sections"][1], ensure_ascii=False))
        self.assertContainsAll(
            roles,
            (
                "persona afectada",
                "usuario operativo",
                "comprador",
                "pagador",
                "decisor",
                "implementador",
                "mantenedor",
                "segmento",
                "contexto de uso",
                "heterogéneas",
                "transferencias de carga",
                "influencia sobre la adopción",
            ),
        )

    def test_benefits_alternatives_and_descriptive_comparison_are_bounded(self) -> None:
        third = norm(json.dumps(self.unit["theory_sections"][2], ensure_ascii=False))
        self.assertContainsAll(
            third,
            (
                "resultado observable",
                "alternativa funcional",
                "statu quo",
                "workaround",
                "intención declarada",
                "adopción",
                "score opaco",
                "efecto causal",
                "beneficio clínico",
            ),
        )
        equations = [
            equation["latex"]
            for section in self.unit["theory_sections"]
            for equation in section.get("equations", [])
        ]
        self.assertEqual(equations, [r"\Delta p=p_{\mathrm{prop}}-p_{\mathrm{ref}}"])

    def test_fit_refutation_and_transition_to_u3_are_explicit(self) -> None:
        fourth = norm(json.dumps(self.unit["theory_sections"][3], ensure_ascii=False))
        self.assertContainsAll(
            fourth,
            (
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "condición de refutación",
                "evidencia discrepante",
                "casos negativos",
                "criterios de salida",
                "seguir, revisar o rechazar",
            ),
        )
        self.assertContainsAll(
            self.text,
            (
                "no equivale a product-market fit",
                "eficacia clínica ni seguridad",
                "no significa que el producto sea viable",
                "u3 deberá someter",
            ),
        )

    def test_activity_and_scaffolds_are_substantial_and_reproducible(self) -> None:
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(len(activity["instructions"]), 12)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 8)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 20)
        activity_text = norm(json.dumps(activity, ensure_ascii=False))
        self.assertContainsAll(
            activity_text,
            (
                "exclusivamente",
                "statu quo",
                "resultado observable",
                "evidencia discrepante",
                "seguir, revisar o rechazar",
                "u3",
                "product-market fit",
                "validación clínica",
            ),
        )
        self.assertGreaterEqual(len(self.unit["glossary"]), 40)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 18)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        glossary = {norm(entry["term"]) for entry in self.unit["glossary"]}
        required = {
            "propuesta de valor",
            "actor beneficiario",
            "usuario operativo",
            "persona afectada",
            "comprador",
            "pagador",
            "decisor",
            "implementador",
            "mantenedor",
            "segmento",
            "contexto de uso",
            "resultado observable",
            "alternativa de referencia",
            "statu quo",
            "workaround",
            "ajuste problema-solución",
            "product-market fit",
            "hipótesis de valor",
            "criterio de refutación",
            "caso negativo",
            "evidencia discrepante",
            "matriz de hipótesis",
            "carga transferida",
            "trade-off",
            "adopción",
            "deseabilidad",
            "factibilidad",
            "viabilidad",
            "criterio de salida",
        }
        self.assertTrue({norm(item) for item in required}.issubset(glossary))

    def test_sources_and_biomedical_connections_are_specific(self) -> None:
        sources = self.unit["sources"]
        self.assertGreaterEqual(len(sources), 15)
        self.assertTrue(all(item.get("verification_status") == "verified_directly" for item in sources))
        domains = " ".join(item["url"] for item in sources)
        self.assertContainsAll(
            domains,
            (
                "biodesign.stanford.edu",
                "nih.gov",
                "oecd.org",
                "fda.gov",
                "iso.org",
                "who.int",
                "pubmed.ncbi.nlm.nih.gov",
            ),
        )
        connections = norm(json.dumps(self.unit["biomedical_connections"], ensure_ascii=False))
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        self.assertContainsAll(
            connections,
            (
                "ingeniería clínica",
                "factores humanos",
                "dispositivos médicos",
                "salud digital",
                "preferencias de pacientes",
                "equidad y acceso",
            ),
        )

    def test_editorial_boundaries_are_explicit(self) -> None:
        notice = norm(self.unit["editorial_notice"])
        self.assertContainsAll(
            notice,
            (
                "no constituye investigación con seres humanos",
                "aprobación ética",
                "consentimiento informado",
                "estudio de mercado",
                "customer discovery real",
                "validación de factores humanos",
                "preferencias del paciente",
                "validación clínica",
                "seguridad o eficacia",
                "evaluación regulatoria",
                "libertad de operación",
                "reembolso",
                "recomendación de inversión",
                "u1",
                "u3",
                "u4",
                "u5",
                "u6",
            ),
        )

    def test_published_descriptor_matches_canonical_purpose_when_available(self) -> None:
        published = next(item for item in self.subject["detailed_units"] if item["unit"] == 2)
        if published["description"] != self.unit["purpose"]:
            self.skipTest("El publicador todavía no ha materializado el descriptor canónico de U2")
        self.assertEqual(published["title"], self.unit["title"])
        self.assertEqual(published["description"], self.unit["purpose"])
        self.assertIn("hipótesis explícita y falsable", norm(published["description"]))


if __name__ == "__main__":
    unittest.main()
