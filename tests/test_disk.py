import os
import sys
import inspect
import io
import random
import psutil
import unittest
import unittest.mock

from disk import DiskUsage, Color, Attr, Chart

# Creates path to the main module files
currentdir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(inspect.currentframe())
        )
    )
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class TestDiskUsage(unittest.TestCase):
    """Test DiskUsage class"""

    @classmethod
    def setUpClass(cls):
        # Create mock up class for method testing
        cls.du = DiskUsage(
            chart = Chart.BARH,
            header = Color.LIGHT_RED,
            style = Attr.UNDERLINED,
            exclude = [],
            text = Color.WHITE,
            graph = Color.PINK
        )
        cls.test_disk = {
            'total': 100,
            'used': 50,
            'free': 50,
            'fstype': 'ext4'
        }
        cls.dict_to_test_raise = {'total': 100,
                            'not_used': 50,
                            'not_free': 50}
    
    def test_main(self):
        self.assertIsInstance(self.du, DiskUsage,
                    msg="Class is not created properly")

    def test_disk_space(self):
        disks = self.du.disk_space()
        self.assertIsInstance(disks, dict,
                msg='Function should return dict')
        # Test that proper keys are present
        compare_keys = ['total', 'used', 'free', 'fstype']
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
            self.assertIsInstance(disks[disk]['fstype'], str)

    def test_bytes_to_human_readable(self):
        # Test if method correctly converts to MB
        for i in range(20):
            bt = random.randint(1048576, 943718400)
            h = self.du.bytes_to_human_readable(bt).split(' ')[1]
            self.assertEqual(h, 'MB', msg='Should be MB')
        # Test if method correctly converts to GB
        for i in range(20):
            bt = random.randint(1073741824, 549755813888)
            h = self.du.bytes_to_human_readable(bt).split(' ')[1]
            self.assertEqual(h, 'GB', msg='Should be GB')

    def test_create_horizontal_bar(self):
        compare_bar = ' ██████████████████▒░░░░░░░░░░░░░░░░░░'
        bar = self.du.create_horizontal_bar(self.test_disk)
        self.assertEqual(bar, compare_bar,
                    msg='bar is not printing properly')
        # Test that error is raise
        with self.assertRaises(ValueError):
            self.du.create_horizontal_bar(self.dict_to_test_raise)
    
    def test_usage_percent(self):
        used = self.du.usage_percent(self.test_disk)
        self.assertEqual(used, 0.5, msg='Check your math!')
        # Test raise error
        with self.assertRaises(ValueError):
            self.du.usage_percent(self.dict_to_test_raise)
    
    def test_integers_to_readable(self):
        h = self.du.integers_to_readable(self.test_disk)
        keys = [key for key in h.keys()]
        compare_keys = ['total', 'used', 'free']
        self.assertListEqual(keys, compare_keys)
        # Riase error test
        with self.assertRaises(TypeError):
            self.du.integers_to_readable(self.dict_to_test_raise)
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, expected_output, mock_stdout):
        # I will exclude all the media partitions
        # And only keep the root to test with regex
        disk_parts = psutil.disk_partitions(all=True)
        for disk in disk_parts[:-1]:
            if 'media' in disk[1]:
                try:
                    self.du.exclude.append(disk[1].split('/')[-1])
                except:
                    continue
        self.du.print_horizontal_barchart()
        self.assertRegex(mock_stdout.getvalue(), expected_output)

    def test_print_horizontal_and_vertical_barchart(self):
        self.maxDiff = None
        self.assert_stdout('root')
        self.assert_stdout('▓▓▓▓▓▓▓▓▓▓|░░░░░░░░░░')


if __name__ == '__main__':
    unittest.main()

