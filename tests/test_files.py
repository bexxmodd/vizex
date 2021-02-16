import unittest
import tempfile
import string
import random
import os

from files import DirectoryFiles

class TestDirectoryFiles(unittest.TestCase):

    # @classmethod
    def test_get_usage_files(self):
        try:
            temp_dir = tempfile.TemporaryDirectory()
            for i in range(5):
                tempfile.NamedTemporaryFile(suffix='.txt', delete=False, dir=temp_dir.name)
            df = DirectoryFiles(dpath=temp_dir.name)
            usage = df.get_usage()
            self.assertTrue(1,1)
            temp_dir.cleanup()
        except Exception as e:
            self.fail(f'Exception occured when trying to get_usage for tmp files {e}')
                    
if __name__ == '__main__':
    unittest.main()