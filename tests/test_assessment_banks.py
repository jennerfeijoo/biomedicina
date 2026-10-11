"""Selection invariants over the actual corpus, including quarantines and hashes."""
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

class AssessmentBankTests(unittest.TestCase):
    def test_corpus_sampling_and_bank_integrity(self):
        result = subprocess.run(['node', 'tests/test_assessment_banks.cjs'], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_course_and_unit_entry_points(self):
        import json
        index = json.loads((ROOT/'data/learning-audit/banks.json').read_text())
        for c in index['courses']:
            with self.subTest(course=c['id']):
                self.assertIn('assets/js/course.js', (ROOT/c['path']).read_text())
                for u in c['units']:
                    p = ROOT / Path(c['path']).parent / 'unidades' / f"unidad-{u['unit']:02d}.html"
                    html = p.read_text()
                    self.assertTrue('assets/js/generated-units.js' in html or 'question-bank-entry' in html, str(p))
