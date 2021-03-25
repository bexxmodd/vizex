from access import ADD_PATH
ADD_PATH()

import unittest

from battery import Battery

class TestBattery(unittest.TestCase):
    """ Test battry module """

    @unittest.skip("Correction needed to properly catch exception")
    def test_Battery_constructor(self):
        self.assertRaises(Exception, Battery())

    def test_print_battery_chart(self):
        pass

    def test_create_details(self):
        pass

if __name__ == '__main__':
    unittest.main()