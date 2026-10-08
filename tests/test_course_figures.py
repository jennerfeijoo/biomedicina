"""Completed figures must exist, remain accessible and reach the public lessons."""
import json
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from advanced_unit_renderer import load_advanced_unit, render_theory_sections, render_figure

COURSE = ROOT / 'data/courses/desarrollo-dispositivos-medicos'

class CourseFigureTests(unittest.TestCase):
    def test_six_complete_figures_are_rendered_with_sources_and_alt_text(self):
        registry = json.loads((COURSE / 'media.json').read_text())
        self.assertEqual(len(registry['items']), 6)
        for number, item in enumerate(registry['items'], 1):
            with self.subTest(unit=number):
                self.assertEqual(item['status'], 'complete')
                svg = ET.parse(ROOT / item['asset_path']).getroot()
                self.assertTrue(svg.find('{http://www.w3.org/2000/svg}title').text)
                self.assertTrue(svg.find('{http://www.w3.org/2000/svg}desc').text)
                self.assertEqual(svg.attrib['viewBox'], '0 0 900 900')
                rendered = render_theory_sections(load_advanced_unit(ROOT, 'desarrollo-dispositivos-medicos', number))
                self.assertEqual(rendered.count('<figure class="lesson-figure"'), 1)
                self.assertIn(item['asset_path'], rendered)
                self.assertIn('alt="', rendered)
                self.assertIn('CC BY-NC 4.0', rendered)
                self.assertIn('Fuentes de apoyo:', rendered)
                public = ROOT / f'ingenieria-biomedica/desarrollo-dispositivos-medicos/unidades/unidad-{number:02d}.html'
                self.assertIn(item['asset_path'], public.read_text())
                self.assertIn('Ampliar figura', public.read_text())

    def test_unproduced_media_does_not_render_as_an_image(self):
        unit = load_advanced_unit(ROOT, 'biomateriales', 1)
        self.assertNotIn('lesson-figure', render_theory_sections(unit))

    def test_figure_asset_cannot_escape_local_asset_directory(self):
        for path in ('https://example.org/figure.svg', 'assets/figures/../../private.svg'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                render_figure({'asset_path': path})
