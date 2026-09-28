"""The catalog and scientific audit must inspect the same authoritative registry."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import audit_scientific_traceability as audit
import sync_catalog_statuses as catalog


class CatalogCanonicalTraceabilityTests(unittest.TestCase):
    def test_manifest_agrees_with_canonical_audit(self):
        expected = sorted(row['course_id'] for row in audit.audit()['courses']
                          if row['claims'] and not row['errors'])
        self.assertEqual(catalog.traced_subjects(), expected)
        self.assertIn('bioestadistica', expected)

    def test_invalid_canonical_registry_overrides_valid_legacy_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy = root / 'data/claim_registry'
            canonical = root / 'data/courses'
            legacy.mkdir(parents=True)
            (canonical / 'example').mkdir(parents=True)
            (legacy / 'example.json').write_text(json.dumps({
                'subject_id': 'example', 'claims': [{'text': 'legacy'}]}))
            path = canonical / 'example/claims.json'
            path.write_text(json.dumps({'course_id':'example','claims':[{'text':'invalid canonical'}]}))
            with patch.object(catalog, 'ROOT', root), \
                 patch.object(audit, 'DEFAULT_DIRECTORY', legacy), \
                 patch.object(audit, 'CANONICAL_COURSE_DIRECTORY', canonical), \
                 patch.object(catalog.validate_scientific_traceability, 'validate_repository_registry',
                              side_effect=lambda payload, label: [] if payload['claims'][0]['text'] == 'legacy' else ['invalid']):
                self.assertEqual(catalog.traced_subjects(), [])
