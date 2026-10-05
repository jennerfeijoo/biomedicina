"""Keep every catalog subject reachable through the public thematic navigation."""
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import unittest
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from home_discovery import update_home


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.targets, self.ids = [], set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.targets.append(attrs.get('href', ''))


class HomePathwayCoverageTests(unittest.TestCase):
    def test_every_subject_has_a_public_pathway_and_every_pathway_has_a_family(self):
        curriculum = json.loads((ROOT / 'data/citonauta_curriculum.json').read_text())
        payload = json.loads((ROOT / 'data/tracks.json').read_text())
        subjects = {s['id'] for a in curriculum['areas'] for s in a['subjects']}
        tracks = {t['id']: t for t in payload['tracks']}
        self.assertEqual({s for t in tracks.values() for s in t['subjects']}, subjects)
        self.assertEqual(Counter(t for g in payload['groups'] for t in g['tracks']),
                         Counter({t: 1 for t in tracks}))
        home = Links((ROOT / 'index.html').read_text())
        public_tracks = {parse_qs(urlparse(href).query)['track'][0]
                         for href in home.targets if 'track=' in href}
        self.assertEqual(public_tracks, set(tracks))
        self.assertTrue(all(href[1:] in home.ids for href in home.targets if href.startswith('#')))
        catalog = Links((ROOT / 'catalogo/index.html').read_text())
        self.assertIn('asignaturas', catalog.ids)

    def test_generation_keeps_no_script_navigation_complete_and_reproducible(self):
        payload = json.loads((ROOT / 'data/tracks.json').read_text())
        source = (ROOT / 'index.html').read_text()
        self.assertEqual(update_home(source, payload), source)
        self.assertEqual(update_home(update_home(source, payload), payload), source)
        # A newly configured route must reach both the family and public filter link.
        payload['tracks'].append(dict(id='example', title='Example', question='Question?', subjects=['x']))
        payload['groups'][0]['tracks'].append('example')
        rendered = update_home(source, payload)
        self.assertIn('track=example#asignaturas', rendered)
