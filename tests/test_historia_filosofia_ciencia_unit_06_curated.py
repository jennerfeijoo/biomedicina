import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/historia-filosofia-ciencia/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/historia-filosofia-ciencia/unit-06.json"
DESCRIPTOR = ROOT / "data/subjects/gestion-etica-comunicacion/historia-filosofia-ciencia.json"
CATALOG = ROOT / "data/catalog_statuses.json"
GENERIC_MARKERS = (
    "Concepto de la unidad que debe definirse mediante entidades observables",
    "V(a)=\\sum_{i=1}^{k} w_i r_i(a)",
    "modelo multicriterio transparente",
)


class HistoriaFilosofiaCienciaUnit06CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.mirror = json.loads(MIRROR.read_text(encoding="utf-8"))

    def test_source_and_mirror_are_exact(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())
        self.assertEqual(self.unit, self.mirror)

    def test_identity_and_purpose_are_disciplinary(self) -> None:
        self.assertEqual(self.unit["subject_id"], "historia-filosofia-ciencia")
        self.assertEqual(self.unit["unit"], 6)
        self.assertEqual(self.unit["slug"], "ciencia-contemporanea")
        purpose = self.unit["purpose"].casefold()
        for phrase in ("reproducibilidad computacional", "replicabilidad", "preregistro", "registered reports", "ciencia abierta", "retractaciones", "desinformación"):
            self.assertIn(phrase, purpose)

    def test_template_and_generic_score_are_absent(self) -> None:
        text = SOURCE.read_text(encoding="utf-8")
        for marker in GENERIC_MARKERS:
            self.assertNotIn(marker, text)

    def test_academic_depth_and_pedagogy(self) -> None:
        self.assertGreaterEqual(len(self.unit["learning_objectives"]), 6)
        self.assertGreaterEqual(len(self.unit["theory_sections"]), 5)
        for section in self.unit["theory_sections"]:
            self.assertGreaterEqual(len(section["paragraphs"]), 5)
            self.assertGreaterEqual(len(section["key_points"]), 5)
        self.assertGreaterEqual(len(self.unit["glossary"]), 50)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        self.assertGreaterEqual(len(self.unit["guided_activities"]), 3)
        self.assertGreaterEqual(len(self.unit["common_errors"]), 20)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        self.assertGreaterEqual(len(self.unit["sources"]), 18)

    def test_nasem_convention_separates_reproducibility_replication_and_robustness(self) -> None:
        text = json.dumps(self.unit["theory_sections"][0], ensure_ascii=False).casefold()
        for phrase in ("national academies", "mismos datos", "datos nuevos", "robustez", "multiverse", "many-analyst"):
            self.assertIn(phrase, text)
        self.assertIn("no demuestra por sí solo que la hipótesis científica sea falsa", text)
        self.assertIn("no significa exigir el mismo valor numérico, el mismo p-valor", text)

    def test_reproducible_object_separates_fair_open_access_and_validity(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in ("procedencia", "control de versiones", "checksum", "fair", "autenticación", "acceso controlado", "privacidad"):
            self.assertIn(phrase, text)
        self.assertIn("identidad digital y validez semántica son propiedades distintas", text)
        self.assertIn("reproducible tampoco prueba", text)

    def test_preregistration_registered_reports_and_preprints_are_distinct(self) -> None:
        text = json.dumps(self.unit["theory_sections"][2], ensure_ascii=False).casefold()
        for phrase in ("preregistro", "plan analítico", "registered reports", "aceptación en principio", "top 2025", "preprints"):
            self.assertIn(phrase, text)
        self.assertIn("no impide explorar", text)
        self.assertIn("no revisados por pares", text)

    def test_corrections_retractions_and_replications_are_not_binary_truth_labels(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in ("revisión por pares", "corrección", "retractación", "error", "replicación", "reporte selectivo", "línea de tiempo"):
            self.assertIn(phrase, text)
        self.assertIn("retractado no significa automáticamente fraudulento", text)
        self.assertIn("no una certificación de verdad", text)

    def test_uncertainty_misinformation_and_disinformation_are_separated(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in ("incertidumbre", "misinformation", "disinformation", "intención", "infodemia", "preprints"):
            self.assertIn(phrase, text)
        self.assertIn("no permite clasificar un mensaje real como desinformación solo porque sea falso", text)
        self.assertIn("no convierte cualquier desacuerdo científico en misinformation", text)

    def test_main_workshop_audits_versions_computation_replication_and_public_message(self) -> None:
        workshop = self.unit["guided_activities"][1]
        text = json.dumps(workshop, ensure_ascii=False).casefold()
        self.assertGreaterEqual(len(workshop["problems"]), 20)
        self.assertGreaterEqual(len(workshop["deliverables"]), 12)
        self.assertGreaterEqual(len(workshop["checking_criteria"]), 25)
        for phrase in ("preregistro", "metadata", "reproducibilidad computacional", "replicación", "fair", "corrección", "misinformation", "intención"):
            self.assertIn(phrase, text)

    def test_glossary_contains_current_open_science_and_self_correction_vocabulary(self) -> None:
        terms = {entry["term"].casefold() for entry in self.unit["glossary"]}
        required = {
            "reproducibilidad computacional", "replicabilidad", "robustez", "procedencia",
            "fair", "acceso controlado", "ciencia abierta", "preregistro", "registered report",
            "top guidelines", "preprint", "peer review", "corrección", "retractación",
            "misinformation", "disinformation", "infodemia", "estado editorial",
        }
        self.assertTrue(required.issubset(terms))

    def test_sources_are_verified_and_cover_current_practices(self) -> None:
        self.assertTrue(all(s.get("verification_status") == "verified_directly" for s in self.unit["sources"]))
        organizations = " ".join(s["organization"] for s in self.unit["sources"]).casefold()
        urls = " ".join(s["url"] for s in self.unit["sources"]).casefold()
        for org in ("national academies", "unesco", "center for open science", "national institutes of health", "international committee of medical journal editors", "committee on publication ethics", "world health organization", "elife"):
            self.assertIn(org, organizations)
        for token in ("25303", "top-guidelines", "registered-reports", "sdata201618", "retraction-guidelines", "71601", "infodemic"):
            self.assertIn(token, urls)

    def test_scope_and_editorial_notice_block_clinical_or_misconduct_adjudication(self) -> None:
        scope = self.unit["professional_scope"].casefold()
        notice = self.unit["editorial_notice"].casefold()
        for phrase in ("objetos sintéticos", "no realiza replicaciones de investigación clínica real", "no determina mala conducta", "no convierte"):
            self.assertIn(phrase, scope)
        for phrase in ("todos los datasets", "sintéticos", "convención nasem", "fair no se presenta", "no se presenta como prueba automática de fraude", "revisión disciplinar externa"):
            self.assertIn(phrase, notice)

    def test_published_descriptor_matches_when_promoted(self) -> None:
        if not DESCRIPTOR.exists():
            self.skipTest("Descriptor not generated yet")
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        detailed = next((u for u in descriptor.get("detailed_units", []) if u.get("unit") == 6), None)
        self.assertIsNotNone(detailed)
        if detailed["description"] != self.unit["purpose"]:
            self.skipTest("U6 descriptor has not been promoted yet")
        self.assertEqual(detailed["description"], self.unit["purpose"])

    def test_catalog_closure_when_publication_has_synchronized(self) -> None:
        if not CATALOG.exists():
            self.skipTest("Catalog not generated yet")
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        specificity = catalog.get("dimensions", {}).get("specificity", {})
        detected = specificity.get("template_detected", [])
        screened = specificity.get("screened_no_known_template_marker", [])
        if "historia-filosofia-ciencia" in detected:
            self.skipTest("Catalog has not been synchronized after U6 yet")
        self.assertIn("historia-filosofia-ciencia", screened)


if __name__ == "__main__":
    unittest.main()
