import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from course_figure_assets import figure_source
from advanced_unit_renderer import render_figure
class ExternalLearningImagesTests(unittest.TestCase):
    def test_remote_images_have_provenance_and_guided_reading(self):
        media=json.loads((ROOT/'data/courses/biomateriales/media.json').read_text())
        images=[x for x in media['items'] if x.get('image_url')]
        self.assertEqual(len(images),2)
        for item in images:
            with self.subTest(image=item['id']):
                self.assertEqual(figure_source(item),item['image_url'])
                html=render_figure(item)
                self.assertIn('referrerpolicy="no-referrer"',html)
                self.assertIn(item['license_url'],html)
                self.assertEqual(html.count('<details'),2)
                page=ROOT/f"ingenieria-biomedica/biomateriales/unidades/unidad-{item['unit_id'][-2:]}.html"
                self.assertIn(item['image_url'],page.read_text())
    def test_remote_policy_rejects_unsafe_or_ambiguous_sources(self):
        base={'source_page_url':'https://commons.wikimedia.org/wiki/File:Image.jpg','license_url':'https://creativecommons.org/licenses/by/4.0/'}
        for url in ['http://upload.wikimedia.org/wikipedia/commons/a.jpg','https://upload.wikimedia.org.evil.test/wikipedia/commons/a.jpg','https://upload.wikimedia.org@evil.test/wikipedia/commons/a.jpg','https://upload.wikimedia.org/wikipedia/commons/a.svg','https://upload.wikimedia.org/wikipedia/commons/%2e%2e/a.jpg']:
            with self.subTest(url=url),self.assertRaises(ValueError):figure_source(dict(base,image_url=url))
        with self.assertRaises(ValueError):figure_source(dict(base,image_url='https://upload.wikimedia.org/wikipedia/commons/a.jpg',asset_path='assets/figures/a.svg'))
