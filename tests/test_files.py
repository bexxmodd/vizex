# add path to the main package and test files.py
if __name__ == '__main__':
    from __access import ADD_PATH
    ADD_PATH()

import unittest
import tempfile
import os
import warnings

from vizexdf.files import DirectoryFiles


class TestDirectoryFiles(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.tmpd = tempfile.TemporaryDirectory()

    @classmethod
    def tearDown(cls):
        cls.tmpd.cleanup()

    def test_get_usage_files(self):
        try:
            for i in range(5):
                tempfile.NamedTemporaryFile(prefix='TEST_', delete=False, dir=self.tmpd.name)
            df = DirectoryFiles(path=self.tmpd.name)
            usage = df.get_usage()
            self.assertEqual(5, len(usage),
                            msg='There should have been 5 items in the list')
            for i in usage:
                self.assertTrue('TEST' in i[0])
        except Exception as e:
            self.fail(f'Exception occured when trying to get_usage for tmp files {e}')

    def test_get_usage_files_empty_dir(self):
        try:
            df = DirectoryFiles(path=self.tmpd.name)
            usage = df.get_usage()
            self.assertListEqual([], usage,
                                msg='For empty folder method should return an empty list')
        except Exception as e:
            self.fail(f'Exception occured when tried to get_usage of an empty directory {e}')

    def test_get_dir_size(self):
        try:
            warnings.filterwarnings('ignore') # suppress tempfile warnings
            # Nest folders three times
            tmp = tempfile.TemporaryDirectory(dir=self.tmpd.name)
            nested_tmp = tempfile.TemporaryDirectory(dir=tmp.name)
            nested_nested_tmp = tempfile.TemporaryDirectory(dir=nested_tmp.name)
            # Create 10 files zie of 1024 * 1024 bytes each
            for i in range(10):
                f = tempfile.NamedTemporaryFile(mode='wb',
                                                dir=nested_nested_tmp.name,
                                                delete=False)
                f.write(b'0' * 1024 * 1024)
            size = DirectoryFiles().get_dir_size(self.tmpd.name)
            self.assertEqual(10485760, size,
                            msg='Total size of directory should be 10485760')
        except Exception as e:
            self.fail(f'Exception occured when tried to get_size nested files {e}')

    def test_get_dir_size_empty_dir(self):
        try:
            size = DirectoryFiles().get_dir_size(self.tmpd.name)
            self.assertEqual(0, size, msg='Size 0 was expected')
        except Exception as e:
            self.fail(f'Exception occured when tried to get_size for an empty folder {e}')

    def test_get_dir_size_broken_symlink(self):
        os.symlink(
            '/this/path/could/not/possibly/exist/like/evar',
            os.path.join(self.tmpd.name, 'broken-link'),
        )
        size = DirectoryFiles().get_dir_size(self.tmpd.name)
        self.assertEqual(0, size)

    def test_sort_data(self):
        try:
            data = [
                ['folder1', 1927317893, 333, 'dir'],
                ['file1', 3419273173817333, 9081231, 'file'],
                ['folder2', 921231938192, 12313744908, 'dir'],
                ['file2', 1238193123, 22, 'file'],
                ['x-file', 34192773817333, 445522, 'x-files']
            ]

            DirectoryFiles().sort_data(data, 'type', True)
            self.assertEqual('x-file', data[0][0])

            DirectoryFiles().sort_data(data, 'name', True)
            self.assertListEqual(['x-file', 34192773817333, 445522, 'x-files'], data[0])

            DirectoryFiles().sort_data(data, 'size', False)
            self.assertEqual(22, data[0][2])

            DirectoryFiles().sort_data(data, 'dt', True)
            self.assertListEqual(['file1', 3419273173817333, 9081231, 'file'], data[0])
        except Exception as e:
            self.fail(f'Exception occured when trying to sort data {e}')

    @unittest.skip("UNDER CONSTRUCTION!")
    def test_decorate_dir(self):
        # TODO
        self.fail("TODO")

    @unittest.skip("UNDER CONSTRUCTION!")
    def test_decorate_file(self):
        # TODO
        self.fail("TODO")


if __name__ == '__main__':
    unittest.main()
