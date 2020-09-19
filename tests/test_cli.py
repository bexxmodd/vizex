import io
import random
import psutil
import unittest
import unittest.mock

from cli import cli, _check_color, _check_attr, _check_chart
from disks import DiskUsage
from tools import Color, Attr, Chart
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

    @patch("module_where_toCreate_is.toCreate")
    def test_created(self, mock_toCreate):
        creator = toTest()
        toTest.createObject()
        mock_toCreate.assert_called_with()
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_keyerror_stdout(self,
                            checking: str,
                            option: str,
                            expected_output: str,
                            mock_stdout: None) -> None:
        """Mocks the stdout in the terminal when
        unavailable option is given as an argument.
        """
        if checking == 'color':
            _check_color(option)
        elif checking == 'attr':
            _check_attr(option)
        self.assertEqual(mock_stdout.getvalue(),
                                    expected_output)

    def test_check_color(self):
        user_inputs = [
                'red', 'green', 'BLUE', 'Yellow',
                'beige', 'pink', 'purple', 'oraNge'
            ]
        for color in user_inputs:
            self.assertTrue(_check_color(color) in Color)
        # Test unavailable color argument
        _check_color('burgundy')
        self.assert_keyerror_stdout('color', 'burgundy',
                        '----- color burgundy is not available\n')

    def test_check_attr(self):
        user_inputs = [
                'bold', 'dim', 'underlined',
                'blink', 'reverse', 'hidden'
            ]
        for attr in user_inputs:
            self.assertTrue(_check_attr(attr) in Attr)
        # Test unavailable attr argument
        _check_attr('italic')
        self.assert_keyerror_stdout('attr', 'italic',
                        '----- attribute italic is not available\n')

    def test_check_chart(self):
        user_inputs = [
                'barv', 'barh', 'pie'
            ]
        for chart in user_inputs:
            self.assertTrue(_check_chart(chart) in Chart)
        # Test if unavailalbe chart option raises error
        with self.assertRaises(NameError):
            _check_chart('scatter')


if __name__ == '__main__':
    unittest.main()