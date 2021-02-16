import unittest

from helpers import DecoratedData


class TestHelpers(unittest.TestCase):

    def test_decorated_data_constructor(self):
        testing = DecoratedData(33, 'Thirteen Three')
        self.assertEqual(33, testing.size,
                        msg='int value was not initialized properly')
        self.assertEqual('Thirteen Three', testing.to_string,
                        msg='to_string of a object was not initialized properly')

    def test_decorated_data_str_printing(self):
        testing = DecoratedData(8, 'E1gh7@')
        self.assertEqual('E1gh7@', str(testing))

    def test_decorated_data_equal(self):
        test_a = DecoratedData(5, 'five')
        test_b = DecoratedData(5, 'five but same')
        self.assertEqual(test_a, test_b)

    def test_decorated_notequal(self):
        test_a = DecoratedData(7, 'five')
        test_b = DecoratedData(5, 'seven')
        self.assertNotEqual(test_a, test_b)

    def test_decorated_greater(self):
        test_a = DecoratedData(7, 'five')
        test_b = DecoratedData(5, 'seven')
        self.assertGreater(test_a, test_b)
    
    def test_decorated_greater_equal(self):
        test_a = DecoratedData(7, 'five')
        test_b = DecoratedData(5, 'seven')
        self.assertGreaterEqual(test_a, test_b)

    def test_decorated_less(self):
        test_a = DecoratedData(3, 'three')
        test_b = DecoratedData(5, 'five and three')
        self.assertLess(test_a, test_b)

    def test_decorated_less_equal(self):
        test_a = DecoratedData(3, 'three')
        test_b = DecoratedData(5, 'five and three')
        self.assertLess(test_a, test_b)


if __name__ == '__main__':
    unittest.main()