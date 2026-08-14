from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_reviewer_validations.py"
SPEC = importlib.util.spec_from_file_location("validate_reviewer_validations", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReviewerValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = ROOT / "data" / "reviewer_validations" / "course-content-reviewer-provisional.json"
        cls.provisional = json.loads(path.read_text(encoding="utf-8"))

    def test_provisional_manifest_is_valid_but_cannot_authorize(self) -> None:
        self.assertEqual(MODULE.validate_manifest(self.provisional), [])
        self.assertFalse(self.provisional["authorization"]["can_authorize_publication"])

    def test_unvalidated_reviewer_cannot_enable_auto_merge(self) -> None:
        payload = copy.deepcopy(self.provisional)
        payload["authorization"]["can_auto_merge"] = True
        errors = MODULE.validate_manifest(payload)
        self.assertTrue(any("auto-merge" in error for error in errors))

    def test_validated_status_requires_comparative_evidence(self) -> None:
        payload = copy.deepcopy(self.provisional)
        payload["status"] = "validated_for_scope"
        payload["authorization"]["can_authorize_publication"] = True
        errors = MODULE.validate_manifest(payload)
        self.assertTrue(any("no inferioridad" in error for error in errors))
        self.assertTrue(any("revisores humanos" in error for error in errors))
        self.assertTrue(any("configuration_sha256" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
