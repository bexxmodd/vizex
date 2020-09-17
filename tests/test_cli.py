import io
import random
import psutil
import unittest
import unittest.mock

from cli import cli, check_color, check_attr, check_chart
from disk import DiskUsage, Color, Attr, Chart
from click.testing import CliRunner

##########################################
########### UNDER CONSTRUCTION ###########
##########################################

class TestCli(unittest.TestCase):

    def test_vizex(self):
        self.test_cli()

    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['barh'])
        assert result.exit_code == 0

    def test_check_color(self):
        user_inputs = [
                'red', 'green', 'BLUE', 'Yellow',
                'beige', 'pink', 'purple', 'oraNge'
            ]
        for color in user_inputs:
            self.assertTrue(check_color(color) in Color)
        with self.assertRaises(KeyError):
            check_color('burgundy')

    def test_check_attr(self):
        user_inputs = [
                'bold', 'dim', 'underlined',
                'blink', 'reverse', 'hidden'
            ]
        for attr in user_inputs:
            self.assertTrue(check_attr(attr) in Attr)
        with self.assertRaises(KeyError):
            check_attr('italic')

    def test_check_chart(self):
        user_inputs = [
                'barv', 'barh', 'pie'
            ]
        for chart in user_inputs:
            self.assertTrue(check_chart(chart) in Chart)
        with self.assertRaises(NameError):
            check_chart('scatter')


if __name__ == '__main__':
    unittest.main()