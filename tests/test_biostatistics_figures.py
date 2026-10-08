import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from advanced_unit_renderer import load_advanced_unit,render_theory_sections

class BiostatisticsFigureTests(unittest.TestCase):
    def test_eight_figures_reach_their_topics_and_public_pages(self):
        registry=json.loads((ROOT/'data/courses/bioestadistica/media.json').read_text())
        self.assertEqual(len(registry['items']),8)
        for n,item in enumerate(registry['items'],1):
            with self.subTest(unit=n):
                self.assertTrue((ROOT/item['asset_path']).is_file())
                self.assertEqual(item['status'],'complete')
                rendered=render_theory_sections(load_advanced_unit(ROOT,'bioestadistica',n))
                self.assertIn(item['asset_path'],rendered)
                self.assertIn('sintéticos',rendered)
                public=ROOT/f'ciencias-basicas/bioestadistica/unidades/unidad-{n:02d}.html'
                self.assertIn(item['asset_path'],public.read_text())

    def test_interval_coverage_and_multiple_testing_calculations(self):
        data=json.loads((ROOT/'assets/figures/bioestadistica/calculation-record.json').read_text())
        self.assertEqual(len(data['ci_means']),30)
        self.assertAlmostEqual(data['ci_half_width'],1.959963984540054/5)
        self.assertEqual(data['ci_covered'],sum(m-data['ci_half_width']<=0<=m+data['ci_half_width'] for m in data['ci_means']))
        self.assertAlmostEqual(data['family_error_20'],0.6415140775914581)
        self.assertEqual([a-b for a,b in zip(data['after'],data['before'])],[3,1,4,-1,2,3])
