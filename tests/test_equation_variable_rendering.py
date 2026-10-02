"""Prevent MathJax commands being hidden in excluded code elements."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from advanced_unit_renderer import render_equation, render_variable_symbol


class VariableRenderingTests(unittest.TestCase):
    def test_explicit_tex_uses_inline_math_outside_code(self):
        output = render_equation({'latex': r'\mathbf M_P=\mathbf M_O-\mathbf r\times\mathbf F',
                                  'variables': {r'\mathbf M_P': 'momento respecto de P'}})
        self.assertIn(r'<span class="math-inline">\(\mathbf M_P\)</span>', output)
        self.assertNotIn(r'<code>\mathbf', output)
        self.assertIn('momento respecto de P', output)

    def test_existing_delimiters_are_not_nested(self):
        for symbol in (r'\(\mathbf F\)', r'\[\mathbf F\]', r'$\mathbf F$', r'$$\mathbf F$$'):
            with self.subTest(symbol=symbol):
                self.assertEqual(render_variable_symbol(symbol), r'<span class="math-inline">\(\mathbf F\)</span>')

    def test_plain_identifiers_are_preserved_without_guessing_notation(self):
        for symbol in ('mu_a', 'N_casos que cumplen', '%Delta Q_D'):
            self.assertEqual(render_variable_symbol(symbol), f'<code>{symbol}</code>')

    def test_symbols_and_descriptions_remain_html_escaped(self):
        output = render_equation({'latex': 'x<y', 'variables': {r'\alpha<img src=x>': '<script>alert(1)</script>'}})
        self.assertNotIn('<img', output)
        self.assertNotIn('<script>', output)
        self.assertIn('&lt;img', output)
        self.assertIn('&lt;script&gt;', output)
