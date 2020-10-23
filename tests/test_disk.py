import io
import random
import psutil
import unittest

from unittest.mock import MagicMock, call
from colored import fg, attr, stylize
from charts import Options


class TestDiskUsage(unittest.TestCase):
    """Test DiskUsage class"""

#     @classmethod
#     def setUpClass(cls):
#         # Create mock up class for method testing
#         cls.du = DiskUsage(
#             chart=Chart.BARH,
#             path=None,
#             exclude=[],
#             header=Color.PINK,
#             style=Attr.UNDERLINED,
#             details=False,
#             every=False,
#             symbol=None,
#             text=Color.BEIGE,
#             graph=None
#         )
#         cls.test_disk = {
#             'total': 100000,
#             'used': 60000,
#             'free': 40000,
#             'percent': 60,
#             'fstype': 'ext4',
#             'mountpoint': '/test'

#         }
#         cls.dict_to_test_raise = {
#                 'total': 100,
#                 'not_used': 50,
#                 'not_free': 50,
#                 'precent': 50,
#                 'fstype': 'ext4',
#                 'mountpoint': '/test'
#         }

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

#     def test_print_horizontal_barchart(self):
#         self.du.create_stats = MagicMock()
#         self.du.print_horizontal_barchart(
#                                 'test_disk', self.test_disk)
#         self.du.create_stats.assert_called()

#     def test_color_details_text(self):
#         expected_output = stylize(f"fstype={self.test_disk['fstype']}\tmountpoint={self.test_disk['mountpoint']}",
#                         fg(self.du.text.value))
#         self.assertEqual(
#             expected_output, self.du.color_details_text(self.test_disk))

#     def test_create_stats(self):
#         # Switch back text color to defualt
#         self.du.text = None
#         compare = "Total: 97.7 KB\t Used: 58.6 KB\t Free: 39.1 KB"
#         self.assertEqual(
#             self.du.create_stats(self.test_disk), compare)


if __name__ == '__main__':
    unittest.main()

