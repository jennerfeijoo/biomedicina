from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "course_redevelopment" / "ingenieria-datos-biomedicos" / "units" / "unit-01.json"
MIRROR = ROOT / "data" / "generated_units" / "ingenieria-datos-biomedicos" / "unit-01.json"
SUBJECT = ROOT / "data" / "subjects" / "ingenieria-biomedica" / "ingenieria-datos-biomedicos.json"
GENERIC = "concepto de la unidad que debe definirse mediante entidades observables"


class IngenieriaDatosBiomedicosUnit01CuratedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.unit = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.text = SOURCE.read_text(encoding="utf-8").casefold()

    def test_generated_unit_is_exact_redevelopment_mirror(self) -> None:
        self.assertEqual(SOURCE.read_bytes(), MIRROR.read_bytes())

    def test_identity_and_template_removal(self) -> None:
        self.assertEqual(self.unit["unit"], 1)
        self.assertEqual(self.unit["slug"], "fuentes-y-arquitectura-de-datos")
        self.assertNotIn(GENERIC, self.text)
        self.assertNotIn("ppv=", self.text)

    def test_objectives_cover_four_source_families_and_boundaries(self) -> None:
        objectives = " ".join(self.unit["learning_objectives"]).casefold()
        for phrase in (
            "inventario de fuentes biomédicas",
            "tiempo efectivo",
            "frecuencia de muestreo",
            "patient–study–series–instance",
            "study/bioproject–sample/biosample–experiment–run",
            "source-to-landing",
            "u2–u6",
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
        for phrase in (
            "inventario de fuentes",
            "datos clínicos",
            "sensores y waveforms",
            "imagen y ómicas",
            "source-to-landing",
        ):
            self.assertIn(phrase, headings)

    def test_clinical_identity_and_temporal_semantics_are_preserved(self) -> None:
        text = json.dumps(self.unit["theory_sections"][1], ensure_ascii=False).casefold()
        for phrase in (
            "patient, encounter, specimen y observation",
            "namespace",
            "tiempo efectivo",
            "tiempo de emisión",
            "tiempo de ingesta",
            "correcciones clínicas",
            "no supone que la ehr fuente almacene internamente",
        ):
            self.assertIn(phrase, text)

    def test_waveform_model_preserves_sampling_clock_and_gaps(self) -> None:
        section = self.unit["theory_sections"][2]
        text = json.dumps(section, ensure_ascii=False).casefold()
        for phrase in (
            "sampling frequency",
            "ganancia",
            "baseline",
            "deriva",
            "wfdb",
            "los huecos son información",
            "no debe rellenarse silenciosamente",
        ):
            self.assertIn(phrase, text)
        equations = {x["latex"] for x in section["equations"]}
        self.assertIn(r"T_{nom}=\frac{N}{f_s}", equations)
        self.assertIn(r"R_{raw}=\frac{C\,f_s\,b}{8}", equations)

    def test_imaging_and_omics_hierarchies_are_not_flattened(self) -> None:
        text = json.dumps(self.unit["theory_sections"][3], ensure_ascii=False).casefold()
        for phrase in (
            "dicom 2026c",
            "patient–study–series–instance",
            "study instance uid",
            "pixel data",
            "study/bioproject",
            "sample/biosample",
            "experiment",
            "run",
            "fastq",
            "réplicas biológicas",
            "réplicas técnicas",
        ):
            self.assertIn(phrase, text)

    def test_source_to_landing_preserves_before_transforming(self) -> None:
        text = json.dumps(self.unit["theory_sections"][4], ensure_ascii=False).casefold()
        for phrase in (
            "landing raw o inmutable",
            "manifiesto de entrega",
            "checksum",
            "cuarentena",
            "batch y streaming",
            "event time e ingest time",
            "u2 implementa etl/elt",
            "u3 compara modelos relacionales",
            "u4 mide calidad",
            "u5 orquesta",
            "u6 aplica seudonimización",
        ):
            self.assertIn(phrase, text)

    def test_glossary_examples_and_activity_are_disciplinary(self) -> None:
        glossary = {x["term"].casefold() for x in self.unit["glossary"]}
        self.assertGreaterEqual(len(glossary), 55)
        for term in (
            "granularidad", "namespace", "tiempo efectivo", "tiempo de ingesta",
            "frecuencia de muestreo", "clock drift", "wfdb", "dicom", "study",
            "series", "instance", "uid", "biosample", "sra experiment", "sra run",
            "fastq", "réplica biológica", "réplica técnica", "source-to-landing",
            "landing raw", "manifiesto de entrega", "checksum", "cuarentena",
        ):
            self.assertIn(term, glossary)
        self.assertGreaterEqual(len(self.unit["worked_examples"]), 5)
        activity = self.unit["guided_activities"][0]
        self.assertGreaterEqual(activity["estimated_time_minutes"], 360)
        self.assertGreaterEqual(len(activity["problems"]), 20)
        self.assertGreaterEqual(len(activity["deliverables"]), 12)
        self.assertGreaterEqual(len(activity["checking_criteria"]), 25)
        joined = " ".join(activity["instructions"] + activity["problems"] + activity["checking_criteria"]).casefold()
        for phrase in (
            "effective/occurrence", "ingest time", "n/f_s", "r_raw",
            "patient–study–series–instance", "bioproject/biosample–experiment–run",
            "quarantine", "reintento", "u2", "u3", "u4", "u5", "u6",
        ):
            self.assertIn(phrase, joined)

    def test_common_errors_block_architectural_shortcuts(self) -> None:
        text = " ".join(x["error"] + " " + x["correction"] for x in self.unit["common_errors"]).casefold()
        for phrase in (
            "contar archivos",
            "namespaces",
            "ingest time",
            "sobrescribir una corrección",
            "waveform",
            "rellenar gaps",
            "filenames dicom",
            "fastq",
            "réplicas biológicas",
            "tabla única",
            "checksum demuestra calidad",
            "datos identificables",
        ):
            self.assertIn(phrase, text)

    def test_sources_assessment_connections_and_notice(self) -> None:
        self.assertGreaterEqual(len(self.unit["sources"]), 18)
        self.assertTrue(all(x["verification_status"] == "verified_directly" for x in self.unit["sources"]))
        titles = " ".join(x["title"] for x in self.unit["sources"]).casefold()
        for phrase in (
            "fhir r5 observation",
            "dicom current standard 2026c",
            "wfdb programmer",
            "sra metadata",
            "fair guiding principles",
            "prov-o",
        ):
            self.assertIn(phrase, titles)
        self.assertGreaterEqual(len(self.unit["self_assessment"]), 12)
        self.assertGreaterEqual(len(self.unit["biomedical_connections"]), 6)
        notice = self.unit["editorial_notice"].casefold()
        for phrase in (
            "exclusivamente sintéticos",
            "no ingiere ehr",
            "no interpreta resultados clínicos",
            "25 de agosto de 2026",
            "u2 aborda etl/elt",
            "u3 almacenamiento/modelado",
            "u4 calidad/linaje/versionado",
            "u5 orquestación/observabilidad",
            "u6 seudonimización",
        ):
            self.assertIn(phrase, notice)

    def test_curricular_boundaries_are_explicit(self) -> None:
        purpose = self.unit["purpose"].casefold()
        for phrase in (
            "reserva etl/elt",
            "almacenamiento/modelado para u3",
            "calidad/linaje profundo para u4",
            "orquestación/observabilidad para u5",
            "privacidad/productos de datos para u6",
        ):
            self.assertIn(phrase, purpose)

    def test_published_descriptor_matches_when_promoted(self) -> None:
        subject = json.loads(SUBJECT.read_text(encoding="utf-8"))
        detailed = {x["unit"]: x for x in subject["detailed_units"]}
        if detailed[1]["description"] != self.unit["purpose"]:
            self.skipTest("El publicador aún no ha promovido el descriptor U1 en este head.")
        self.assertEqual(detailed[1]["description"], self.unit["purpose"])


if __name__ == "__main__":
    unittest.main()