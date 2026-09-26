from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.pilot_publication_state import public_review_migration
from scripts.site_metadata import add_metadata
from scripts import validate_links

ROOT = Path(__file__).resolve().parents[1]


class PublicationStateTests(unittest.TestCase):
    def test_recorded_migration_is_provisional(self):
        self.assertTrue(public_review_migration(ROOT))

    def test_unrecorded_or_claimed_review_does_not_bypass_historical_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertFalse(public_review_migration(root))
            migration = root / 'data/course_migrations/bioinstrumentacion-public-canonical-v1.json'
            migration.parent.mkdir(parents=True)
            payload = json.loads((ROOT / migration.relative_to(root)).read_text())
            payload['publication_state']['human_review_executed'] = True
            migration.write_text(json.dumps(payload))
            self.assertFalse(public_review_migration(root))


class MetadataTests(unittest.TestCase):
    def test_repeat_generation_and_escaping(self):
        source = '<html><head><title>A &amp; B</title><meta name="description" content="A &quot;quote&quot;" /></head></html>'
        rendered = add_metadata(source, 'catalogo/index.html')
        self.assertEqual(rendered, add_metadata(rendered, 'catalogo/index.html'))
        self.assertEqual(rendered.count('rel="canonical"'), 1)
        self.assertIn('content="A &quot;quote&quot;"', rendered)


class LinkTests(unittest.TestCase):
    def test_assets_anchors_and_pages_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / 'index.html'
            page.write_text('<a href="/biomedicina/index.html#ok">ok</a><h1 id="ok">Title</h1><img src="missing.svg"><a href="#bad">bad</a>')
            with patch.object(validate_links, 'ROOT', root):
                broken = validate_links.validate()
                self.assertEqual({row[1] for row in broken}, {'missing.svg', '#bad'})
                self.assertEqual(validate_links.resolve_link(page, 'https://jennerfeijoo.github.io/biomedicina/index.html'), page)
