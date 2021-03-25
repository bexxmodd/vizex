import io
import os
import json
import random
import tempfile
import unittest
import unittest.mock

from colored import fg, attr, stylize

# --- Tools' methods to be tested ---
from main.tools import save_to_csv, save_to_json
from main.tools import bytes_to_human_readable, create_usage_warning
from main.tools import ints_to_human_readable, printml
from main.tools import append_to_bash, remove_if_exists


class TestTools(unittest.TestCase):

    def test_bytes_to_human_readable_zero_input(self):
        try:
            bt = bytes_to_human_readable(0)
            self.assertEqual('0.0 b', bt)
        except Exception as e:
            self.fail(f"Exception occured when None value was given as an argument {e}")

    def test_bytes_to_humand_readable_exact_conversion(self):
        try:
            bt = bytes_to_human_readable(12288)
            self.assertEqual('12.0 kb', bt, msg='12288 b should have been 12.0 kb')
            bt = bytes_to_human_readable(3300000)
            self.assertEqual('3.1 mb', bt, msg='3300000 b should have been 3.1 mb')
            bt = bytes_to_human_readable(13000000000)
            self.assertEqual('12.1 gb', bt, msg='13000000000 b should have been 12.1 gb')
            bt = bytes_to_human_readable(24500000000000)
            self.assertEqual('22.3 tb', bt, msg='24500000000000 b should have been 22.3 tb')
        except Exception as e:
            self.fail(f"Exception occured when tried to convert bytes to human readable format {e}")
    
    def test_bytes_to_human_readable_convert_to_mb(self):
        try:
            for i in range(20):
                bt = random.randint(1048576, 943718400)
                human = bytes_to_human_readable(bt).split(' ')[1]
                self.assertEqual(human, 'mb', msg='Should be mb')
        except Exception as e:
            self.fail(f"Exception occured when mb range values were given as an argument {e}")

    def test_bytes_to_human_readable_convert_to_gb(self):
        try:
            for i in range(20):
                bt = random.randint(1073741824, 549755813888)
                human = bytes_to_human_readable(bt).split(' ')[1]
                self.assertEqual(human, 'gb', msg='Should be gb')
        except Exception as e:
            self.fail(f"Exception occured when gb range values were given as an argument {e}")

    def test_ints_to_human_readable_for_mb_gb_b_tb(self):
        try:
            for i in range(100):
                test_dict = {
                    'mb': random.randint(1048576, 943718400),
                    'kb': random.randint(4000, 140000),
                    'gb': random.randint(1073741824, 549755813888),
                    'tb': random.randint(1300000000000, 130000000000000),
                    'bs': random.randint(1, 999),
                    'String': 'This is text'
                }
                result = ints_to_human_readable(test_dict)
                self.assertEqual(result['mb'].split(' ')[1], 'mb')
                self.assertEqual(result['kb'].split(' ')[1], 'kb')
                self.assertEqual(result['gb'].split(' ')[1], 'gb')
                self.assertEqual(result['tb'].split(' ')[1], 'tb')
                self.assertEqual(result['bs'].split(' ')[1], 'b')
                self.assertEqual(result['String'], 'This is text')
        except Exception as e:
            self.fail(f"Exception occured when trying to convert dict of bytes into readable sizes {e}")

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, arts, col, expected_output, mock_stdout):
        printml(arts, col)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_printml(self):
        arts = ['''
1''','''
4''']
        expected1 = '''  
1  4

'''
        expected2 = '''
1


4

'''
        self.assert_stdout(arts, 1, expected1)
        self.assert_stdout(arts, 2, expected2)
    
    def test_create_usage_warning_blinking_red(self):
        try:
            compare_red = f"{stylize('39.5% used', attr('blink') + fg(9))}"
            self.assertEqual(
                create_usage_warning(39.5, 39.4, 39), compare_red)
        except Exception as e:
            self.fail(f"Exception occured when trying create a red blinking warning {e}")

    def test_create_usage_warning_orange(self):
        try:
            compare_orange = f"{stylize('0.1% used', fg(214))}"
            self.assertEqual(
                create_usage_warning(0.1, 0.2, 0.1), compare_orange)
        except Exception as e:
            self.fail(f"Exception occured when trying tocreate a orange warning {e}")

    def test_create_usage_warning_green(self):
        try:
            compare_green = f"{stylize('99.5% used', fg(82))}"
            self.assertEqual(
                create_usage_warning(99.5, 99.9, 99.6), compare_green)
        except Exception as e:
            self.fail(f"Exception occured when trying create a green warning {e}")

    def test_create_usage_warning_negative_number(self):
        try:
            compare_negative = f"{stylize('0% used', fg(82))}"
            self.assertEqual(
                create_usage_warning(-15.5, 1.1, 1.0), compare_negative)
        except Exception as e:
            self.fail(f"Exception occured when trying to create a warning with negative number {e}")

    def test_create_usage_warning_over_100_usage(self):
        try:
            compare_over100 = f"{stylize('100% used', attr('blink') + fg(9))}"
            self.assertEqual(
                create_usage_warning(101.1, 99.9, 99.8), compare_over100)
        except Exception as e:
            self.fail(f"Exception occured when trying to create a 100% usage warning {e}")

    def test_save_to_csv_wrong_filename(self):
        data = {'test_01': [11, 33, 55]}
        try:
            self.assertRaises(NameError, save_to_csv, data, 'wrongformat')
        except Exception as e:
            self.fail(f'Exception occured when trying to create a file without full name {e}')

    def test_save_to_csv_create_file(self):
        data = {}
        try:
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as tmpf:
                filename = tmpf.name
                save_to_csv(data=data, filename=filename)
                self.assertTrue(os.path.isfile(filename),
                                msg=f'{filename} was not created')
                self.assertTrue(os.path.getsize(filename),
                                msg=f'{filename} is not empty')
        except Exception as e:
            self.fail(f'Exception occured when trying to save an empty CSV file {e}')
    
    def test_save_to_json_wrong_filename(self):
        data = {'test_01': [11, 33, 55]}
        try:
            self.assertRaises(NameError, save_to_json, data, 'wrongformat')
        except Exception as e:
            self.fail(f'Exception occured when trying to create a file without full name {e}')

    def test_save_to_csv_full_data(self):
        data = {
            'test_01': [11, 33, 55],
            'test_02': [22, 44, 66],
            'test_03': [33, 77, 99]
        }
        try:
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as tmpf:
                save_to_csv(data=data, filename=tmpf.name, orient='index')
                self.assertTrue(os.path.isfile(tmpf.name))

                other_f = [
                    ['', '0', '1', '2\n'],
                    ['test_01', '11', '33', '55\n'],
                    ['test_02', '22', '44', '66\n'],
                    ['test_03', '33', '77', '99\n']
                ]
                
                with open(tmpf.name) as f:
                    for line, other in zip(f, other_f):
                        self.assertListEqual(other, line.split(','),
                                    msg='Given two rows in a CSV files are not the same')
        except Exception as e:
            self.fail(f'Exception occured when trying to save a CSV file {e}')

    def test_save_to_json_create_file(self):
        data = {}
        try:
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.json') as tmpf:
                filename = tmpf.name
                save_to_json(data=data, filename=filename)
                self.assertTrue(os.path.isfile(filename),
                                msg=f'{filename} was not created')
                self.assertTrue(os.path.getsize(filename),
                                msg=f'{filename} is not empty')
        except Exception as e:
            self.fail(f'Exception occured when trying to create an empty JSON file {e}')

    def test_save_to_json_full_data(self):
        data = {
            'test_01': [11, 22, 33],
            'test_02': [44, 55, 66],
            'test_03': [77, 88, 99]
        }
        try:
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.json') as tmpf:
                save_to_json(data=data, filename=tmpf.name)
                self.assertTrue(os.path.isfile(tmpf.name))
                
                with open(tmpf.name) as f:
                    loaded = json.load(tmpf)
                    for key in data.keys():
                        for i, o in zip(loaded[key], data[key]):
                            self.assertEqual(o, i,
                                    msg='Given two rows in a JSON files are not the same')
        except Exception as e:
            self.fail(f'Exception occured when trying to save a JSON file {e}')

    def test_append_to_bash(self):
        bash_aliases = os.path.expanduser("~") + '/.bash_aliases'
        try:
            alias_line= "this will be here temporarily"
            append_to_bash('toolstest', alias_line)
            with open(bash_aliases, 'r') as f:
                for line in f:
                    if 'toolstest' in line:
                        self.assertTrue(1 == 1)
                        return
                remove_if_exists('toolstest', bash_aliases)
                self.fail('Alias was not appended!')
        except Exception as e:
            self.fail(f'Exception occured when tried to set alias {e}')

    def test_remove_if_exists(self):
        bash_aliases = os.path.expanduser("~") + '/.bash_aliases'
        try:
            append_to_bash('toolstest', 'this line is a test for remove_if_exists')
            remove_if_exists('toolstest', bash_aliases)
            with open(bash_aliases, 'r') as f:
                for line in f:
                    if 'tooltest' in line:
                        self.fail('alias was note removed')
            self.assertTrue(1 == 1)
        except Exception as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main()