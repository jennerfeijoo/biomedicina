from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"


class MachineLearningSourceGapClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        self.sources = json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))
        self.by_id = {item["id"]: item for item in self.sources["sources"]}

    def test_three_core_sources_are_directly_verified(self) -> None:
        expected = {
            "consort-ai",
            "spirit-ai",
            "who-ethics-and-governance-of-artificial-intelligence-for-health",
        }
        self.assertTrue(expected.issubset(set(self.course["core_source_ids"])))
        for source_id in expected:
            source = self.by_id[source_id]
            self.assertEqual(source["verification_status"], "verified_directly")
            self.assertTrue(source["locator"])
            self.assertTrue(source["curricular_function"])
            self.assertTrue(source["limitations"])

    def test_consort_and_spirit_identifiers_are_canonical(self) -> None:
        self.assertEqual(self.by_id["consort-ai"]["doi"], "10.1038/s41591-020-1034-x")
        self.assertEqual(self.by_id["spirit-ai"]["doi"], "10.1038/s41591-020-1037-7")
        ids = [item["id"] for item in self.sources["sources"]]
        self.assertNotIn("consort-ai-2020", ids)
        self.assertNotIn("spirit-ai-2020", ids)

    def test_who_guidance_is_scoped_as_governance_not_validation(self) -> None:
        source = self.by_id["who-ethics-and-governance-of-artificial-intelligence-for-health"]
        self.assertEqual(source["organization"], "World Health Organization")
        self.assertEqual(source["year"], 2021)
        self.assertIn("9789240029200", source["locator"])
        text = (source["role"] + " " + source["curricular_function"] + " " + source["limitations"]).lower()
        self.assertIn("gobernanza", text)
        self.assertIn("no valida un modelo concreto", text)
        self.assertIn("ni sustituye evaluación clínica", text)

    def test_human_review_boundaries_remain_pending(self) -> None:
        status = self.course["status"]
        self.assertEqual(status["content"], "complete")
        self.assertEqual(status["sources"], "traceable")
        self.assertEqual(status["pedagogy"], "complete")
        self.assertEqual(status["internal_review"], "pending")
        self.assertEqual(status["external_review"], "pending")
        self.assertEqual(status["publication"], "published_provisional")


if __name__ == "__main__":
    unittest.main()
