# add path to the main package and test disks.py
if __name__ == '__main__':
    from __access import ADD_PATH
    ADD_PATH()


import io
import random
import psutil
import unittest

from unittest.mock import MagicMock, call
from colored import fg, attr, stylize
from charts import Options

@unittest.skip("Tests need to be updated to suit the changes in the disks.py module")
class TestDiskUsage(unittest.TestCase):
    """Test DiskUsage class"""

    def test_grab_partitions(self):
        disks = self.du.grab_partitions(self.du.exclude)
        self.assertIsInstance(disks, dict,
                msg='Function should return dict')
        # Test that proper keys are present
        compare_keys = ['total',
                        'used',
                        'free',
                        'percent',
                        'fstype',
                        'mountpoint']
        for disk in disks:
            self.assertIsNotNone(disk)
            keys = [key for key in disks[disk].keys()]
            self.assertListEqual(keys, compare_keys,
                        msg=f'{keys} are not present')
        
        # Test that they have positive integer values
        for disk in disks:
            self.assertGreaterEqual(disks[disk]['total'], 1)
            self.assertGreaterEqual(disks[disk]['used'], 1)
            self.assertGreaterEqual(disks[disk]['free'], 0)
            self.assertGreaterEqual(disks[disk]['percent'], 0)
            self.assertIsInstance(disks[disk]['fstype'], str)
            self.assertIsInstance(disks[disk]['mountpoint'], str)

    def test_grab_specific_disk(self):
        disks = self.du.grab_specific_disk('/home/')
        self.assertIsInstance(disks, dict,
                msg='Function should return dict')
        # Test that proper keys are present
        compare_keys = ['total',
                        'used',
                        'free',
                        'percent',
                        'fstype',
                        'mountpoint']
        for disk in disks:
            self.assertIsNotNone(disks)
            keys = [key for key in disks[disk].keys()]
            self.assertListEqual(keys, compare_keys,
                            msg=f'{keys} are not present')
        
        # Test that they have positive integer values
        for disk in disks:
            self.assertGreaterEqual(disks[disk]['total'], 1)
            self.assertGreaterEqual(disks[disk]['used'], 1)
            self.assertGreaterEqual(disks[disk]['free'], 0)
            self.assertGreaterEqual(disks[disk]['percent'], 0)
            self.assertIsInstance(disks[disk]['fstype'], str)
            self.assertIsInstance(disks[disk]['mountpoint'], str)


if __name__ == '__main__':
    unittest.main()

