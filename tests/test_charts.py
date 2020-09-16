import unittest
from tools import Color
from colored import fg, stylize
from charts import ChartPrint

class TestChartPrint(unittest.TestCase):
    """Test Printing of Charts in the terminal"""

    @classmethod
    def setUpClass(cls):
        cls.chart01 = ChartPrint(graph=Color.RED)
        cls.chart02 = ChartPrint(symbol='@')

    def test_grap_color(self):
        self.assertIsInstance(self.chart01,
                                ChartPrint)
        self.assertIsInstance(self.chart02,
                                ChartPrint)
        self.assertEqual(self.chart01.graph,
                                fg('red'))
        self.assertEqual(self.chart01.msymbol,
                            stylize('▒', fg('red')))
        self.assertEqual(self.chart02.fsymbol, '@')
        self.assertEqual(self.chart02.esymbol, '-')
        
    def test_draw_horizontal_bar(self):
        compare = '[@@@@@@@@@@@@@@@@@@>------------------]'
        self.assertEqual(
            self.chart02.draw_horizontal_bar(10, 5),
            compare
        )

    def test_draw_vertical_bar(self):
        self.assertEqual(
            self.chart02.draw_vertical_bar(10, 5)[:22],
            '\n---------  \n---------'
        )


if __name__ == '__main__':
    unittest.main()
