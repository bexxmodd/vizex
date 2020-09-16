import io
import random
import unittest
import unittest.mock

from tools import bytes_to_human_readable
from tools import ints_to_human_readable, printml

class TestTools(unittest.TestCase):
    
    def test_bytes_to_human_readable(self):
        # Test if method correctly converts to MB
        for i in range(20):
            bt = random.randint(1048576, 943718400)
            human = bytes_to_human_readable(bt).split(' ')[1]
            self.assertEqual(human, 'MB', msg='Should be MB')
        # Test if method correctly converts to GB
        for i in range(20):
            bt = random.randint(1073741824, 549755813888)
            human = bytes_to_human_readable(bt).split(' ')[1]
            self.assertEqual(human, 'GB', msg='Should be GB')

    def test_ints_to_human_readable(self):
        for i in range(20):
            test_dict = {
                'mb': random.randint(1048576, 943718400),
                'gb': random.randint(1073741824, 549755813888),
                'bs': random.randint(1, 1024),
                'String': 'This is text'
            }
            result = ints_to_human_readable(test_dict)
            self.assertEqual(result['mb'].split(' ')[1], 'MB')
            self.assertEqual(result['gb'].split(' ')[1], 'GB')
            self.assertEqual(result['bs'].split(' ')[1], 'B')
            self.assertEqual(result['String'], 'This is text')

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


if __name__ == '__main__':
    unittest.main()