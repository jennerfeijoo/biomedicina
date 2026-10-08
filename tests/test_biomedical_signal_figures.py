import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from advanced_unit_renderer import load_advanced_unit,render_theory_sections

class SignalFigureTests(unittest.TestCase):
    def test_six_figures_are_published_with_synthetic_scope(self):
        items=json.loads((ROOT/'data/courses/senales-biomedicas/media.json').read_text())['items']
        self.assertEqual(len(items),6)
        for n,item in enumerate(items,1):
            with self.subTest(unit=n):
                self.assertTrue((ROOT/item['asset_path']).is_file())
                self.assertIn(item['asset_path'],render_theory_sections(load_advanced_unit(ROOT,'senales-biomedicas',n)))
                text=(ROOT/f'ingenieria-biomedica/senales-biomedicas/unidades/unidad-{n:02d}.html').read_text()
                self.assertIn(item['asset_path'],text)
                self.assertIn('no representa registros clínicos',text)

    def test_aliasing_delay_matching_and_group_partition(self):
        d=json.loads((ROOT/'assets/figures/senales-biomedicas/calculation-record.json').read_text())
        for a,b in zip(d['alias_a'],d['alias_b']):self.assertAlmostEqual(a,b,places=12)
        self.assertAlmostEqual(d['filtered_peak_s']-d['pulse_peak_s'],.02)
        self.assertAlmostEqual(d['dft_10hz_peak_amplitude'],1.)
        self.assertEqual(len({i for i,j in d['matches']}),2)
        self.assertEqual(len({j for i,j in d['matches']}),2)
        for i,j in d['matches']:self.assertLessEqual(abs(d['references'][i]-d['detections'][j]),d['tolerance_s'])
        self.assertEqual(len(d['detections'])-len(d['matches']),2)
        self.assertEqual(len(d['references'])-len(d['matches']),1)
        for row in d['train_test_groups']:self.assertEqual(len(set(row)),1)
