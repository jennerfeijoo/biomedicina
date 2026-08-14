from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_generic_content.py"
SPEC = importlib.util.spec_from_file_location("audit_generic_content", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GenericContentAuditTests(unittest.TestCase):
    def test_marker_classifies_course_without_claiming_other_course_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            marked = root / "marked"
            screened = root / "screened"
            marked.mkdir()
            screened.mkdir()
            (marked / "unit-01.json").write_text(
                json.dumps({"text": MODULE.KNOWN_MARKERS[0]}), encoding="utf-8"
            )
            (screened / "unit-01.json").write_text(
                json.dumps({"text": "Contenido disciplinar de prueba"}), encoding="utf-8"
            )
            report = MODULE.audit(root)
        self.assertEqual(report["template_detected"], ["marked"])
        self.assertEqual(report["screened_no_known_template_marker"], ["screened"])
        self.assertIn("no equivale", report["interpretation"])


if __name__ == "__main__":
    unittest.main()
