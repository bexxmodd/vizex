# add path to the main package and test battery.py
if __name__ == '__main__':
    from __access import ADD_PATH
    ADD_PATH()

import unittest
import psutil

from vizexdu.battery import Battery


class TestBattery(unittest.TestCase):
    """ Test battry module """

    def test_Battery_constructor(self):
        if not (has_battery := psutil.sensors_battery()):
            with self.assertRaises(Exception):
                Battery()
        else:
            self.assertTrue(has_battery.percent > 0)

    def test_create_details_text(self):
        if not psutil.sensors_battery():
            pass
        else:
            self.assertTrue(isinstance(Batter().create_details_text(), str))


if __name__ == '__main__':
    unittest.main()
