import json
import math
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from advanced_unit_renderer import load_advanced_unit,render_theory_sections

class ElectronicsFigureTests(unittest.TestCase):
    def test_all_six_figures_are_published_in_their_units(self):
        registry=json.loads((ROOT/'data/courses/electronica/media.json').read_text())
        self.assertEqual(len(registry['items']),6)
        for n,item in enumerate(registry['items'],1):
            with self.subTest(unit=n):
                self.assertTrue((ROOT/item['asset_path']).is_file())
                self.assertIn(item['asset_path'],render_theory_sections(load_advanced_unit(ROOT,'electronica',n)))
                public=ROOT/f'ingenieria-biomedica/electronica/unidades/unidad-{n:02d}.html'
                self.assertIn(item['asset_path'],public.read_text())
                self.assertIn('no mediciones',public.read_text())

    def test_cutoff_bandwidth_margins_and_loading(self):
        d=json.loads((ROOT/'assets/figures/electronica/calculation-record.json').read_text())
        self.assertAlmostEqual(d['fc_hz'],159.15494309189535)
        self.assertAlmostEqual(d['fc_hz'],1/(2*math.pi*d['rc_ohm']*d['c_farad']))
        for gain,bw in zip(d['gains'],d['bandwidth_hz']):self.assertEqual(gain*bw,d['gbw_hz'])
        self.assertAlmostEqual(d['logic_vil']-d['logic_vol'],.4)
        self.assertAlmostEqual(d['logic_voh']-d['logic_vih'],.9)
        self.assertAlmostEqual(d['loaded_voltage_1meg'],100/101)
