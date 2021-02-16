import io
import os
import random
import unittest
import unittest.mock

from colored import fg, attr, stylize
from tools import bytes_to_human_readable, create_usage_warning
from tools import ints_to_human_readable, printml
from tools import save_to_csv, save_to_json

'''
-[ ] Finish testing save_to_csv and save_to_json
'''


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
        data = {
            'test_01': [11, 33, 55],
        }
        filename = 'wrongwrongwrong'
        try:
            save_to_csv(data=data, filename=filename)
            self.assertFalse(os.path.isfile(filename),
                        msg=f'{filename} was still created')
        except Exception as e:
            os.remove(filename)
            self.fail(f'Exception occured when trying to create a file without full name {e}')

    def test_save_to_csv_empty_file(self):
        data = {}
        filename = 'test.csv'

        try:
            save_to_csv(data=data, filename=filename)
            self.assertTrue(os.path.isfile(filename),
                            msg=f'{filename} was not created')
            self.assertTrue(os.path.getsize(filename),
                            msg=f'{filename} is not empty')
            os.remove(filename)
        except Exception as e:
            self.fail(f'Exception occured when trying to save an empty CSV file {e}')


    def test_save_to_csv_full_data(self):
        data = {
            'test_01': [11, 33, 55],
            'test_02': [22, 44, 66],
            'test_03': [33, 77, 99]
        }
        filename = 'test_file.csv'

        try:
            save_to_csv(data=data, filename=filename, orient='index')
            self.assertTrue(os.path.isfile(filename))

            other_f = [
                ['', '0', '1', '2\n'],
                ['test_01', '11', '33', '55\n'],
                ['test_02', '22', '44', '66\n'],
                ['test_03', '33', '77', '99\n']
            ]
            
            with open('test_file.csv') as f:
                for line, other in zip(f, other_f):
                    self.assertListEqual(other, line.split(','),
                                msg='Given two rows in a CSV files are not the same')

            os.remove(filename)
        except Exception as e:
            self.fail(f'Exception occured when trying to save a CSV file {e}')


if __name__ == '__main__':
    unittest.main()