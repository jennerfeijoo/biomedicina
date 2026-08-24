from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "data" / "courses" / "machine-learning-biomedico-validacion-clinica"

# Final user-authored trigger after strict source-gap closure and deterministic regeneration.


class MachineLearningSourceGapClosureTests(unittest.TestCase):
    def test_traceable_course_has_no_unverified_core_sources(self) -> None:
        course = json.loads((COURSE / "course.json").read_text(encoding="utf-8"))
        sources = {
            item["id"]: item
            for item in json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))["sources"]
        }
        self.assertEqual(course["status"]["sources"], "traceable")
        for source_id in course["core_source_ids"]:
            self.assertIn(source_id, sources)
            self.assertNotEqual(sources[source_id]["verification_status"], "unverified")

    def test_consor_spirit_and_who_sources_are_directly_verified(self) -> None:
        sources = {
            item["id"]: item
            for item in json.loads((COURSE / "sources.json").read_text(encoding="utf-8"))["sources"]
        }
        for source_id in (
            "consort-ai",
            "spirit-ai",
            "who-ethics-and-governance-of-artificial-intelligence-for-health",
        ):
            self.assertEqual(sources[source_id]["verification_status"], "verified_directly")
            self.assertTrue(sources[source_id].get("locator"))
            self.assertTrue(sources[source_id].get("limitations"))
        who = sources["who-ethics-and-governance-of-artificial-intelligence-for-health"]
        self.assertEqual(who["organization"], "World Health Organization")
        self.assertEqual(who["year"], 2021)
        self.assertIn("9789240029200", who["locator"])


if __name__ == "__main__":
    unittest.main()
