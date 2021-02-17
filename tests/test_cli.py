import io
import random
import psutil
import unittest
import unittest.mock

from click.testing import CliRunner

from main.cli import dirs_files, disk_usage
from main.disks import DiskUsage

##########################################
########### UNDER CONSTRUCTION ###########
##########################################

@unittest.skip("Tests needs to be updated to suit the changes in a cli.py module")
class TestCli(unittest.TestCase):
    
    def test(self):
        pass


if __name__ == '__main__':
    unittest.main()