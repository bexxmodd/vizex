import io
import unittest
import unittest.mock

from colored import fg, attr, stylize
from charts import Options, Chart, HorizontalBarChart, VerticalBarChart

class TestOptions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.opts = Options()

    def test_symbol_setter(self):
        self.opts.symbol = '@'
        self.assertEqual(self.opts.fsymbol, '@')
        self.assertEqual(self.opts.msymbol, '>')
        self.assertEqual(self.opts.esymbol, '-')

    def test_check_color(self):
        self.opts.graph_color = 'cyan'
        self.assertEqual(
            fg('cyan'), self.opts.graph_color)

        self.assertEqual(
            'white', self.opts._check_color('notcolor'))
        self.assertEqual(
            fg('magenta'), self.opts._check_color('magenta'))

    def test_check_attr(self):
        self.opts.header_style = 'underlined'
        self.assertEqual(
            attr('underlined'), self.opts.header_style)

        self.assertEqual(
            'bold', self.opts._check_attr('notattr'))
        self.assertEqual(
            attr('blink'), self.opts._check_attr('blink'))


class TestChart(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.chart = Chart()

    def test_chart_init(self):
        # Test that if no Options arg given new is created
        self.assertIsInstance(self.chart.options, Options)


class TestHorizontalBarChart(unittest.TestCase):
    """Test Horizontal Bar Chart printing"""

    @classmethod
    def setUpClass(cls):
        cls.horizontal_chart = HorizontalBarChart()

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, expected_output, mock_stdout):
        self.horizontal_chart.chart(
            title='Test Title',
            pre_graph_text='This looks sweet',
            post_graph_text=None,
            footer=None,
            maximum=10,
            current=5
        )

        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_chart(self):
        compare = f"{stylize('Test Title', fg('red') + attr('bold'))}\n" \
            + f"{stylize('This looks sweet', fg('white'))}\n" \
            + f"{stylize('███████████████████▒░░░░░░░░░░░░░░░░░░░', fg('white'))} \n"
        
        self.assert_stdout(compare)

    def test_draw_horizontal_bar(self):
        compare = '███████████████████▒░░░░░░░░░░░░░░░░░░░'
        self.assertEqual(
            compare, self.horizontal_chart.draw_horizontal_bar(10, 5))

        compare_02 = '▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░'
        self.assertEqual(
            compare_02, self.horizontal_chart.draw_horizontal_bar(10, 0))


class TestVerticalBarChart(unittest.TestCase):
    """Test Printing of Vertical bars in the terminal"""

    @classmethod
    def setUpClass(cls):
        cls.chart = VerticalBarChart()

    def test_draw_vertical_bar(self):
        self.assertEqual(
            self.chart.draw_vertical_bar(10, 5)[:22],
            '\n░░░░░░░░░  \n░░░░░░░░░')


if __name__ == '__main__':
    unittest.main()
