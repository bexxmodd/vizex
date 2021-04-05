# add path to the main package and test cli.py
if __name__ == '__main__':
    from __access import ADD_PATH
    ADD_PATH()


import io
import random
import psutil
import unittest
import unittest.mock

from click.testing import CliRunner
from cli import dirs_files, disk_usage


class TestCli(unittest.TestCase):
    
    def test_dirs_files(self):
        try:
            runner = CliRunner()
            result = runner.invoke(dirs_files, ['-ds', 'name'])
            self.assertTrue(result.exit_code == 0)
            self.assertTrue('name' in result.output)
            self.assertTrue('last modified' in result.output)
            self.assertTrue('size' in result.output)
            self.assertTrue('type' in result.output)
        except Exception as e:
            self.fail(f'Exception occured when calling vizexdf with desc and sort name options {e}')

    def test_dirs_files_help(self):
        try:
            runner = CliRunner()
            result = runner.invoke(dirs_files, ['--help'])
            self.assertTrue(result.exit_code == 0)
            self.assertTrue('Made by: Beka Modebadze' in result.output)
        except Exception as e:
            self.fail(f'Exception occured when calling vizexdf\'s --help {e}')

    def test_disk_usage(self):
        try:
            runner = CliRunner()
            result = runner.invoke(disk_usage, ['--mark', '@'])
            self.assertTrue(result.exit_code == 0)
            self.assertTrue('root' in result.output)
            self.assertTrue('Total' in result.output)
            self.assertTrue('Used' in result.output)
            self.assertTrue('Free' in result.output)
            self.assertTrue('@' in result.output)
        except Exception as e:
            self.fail(f'Exception occured when calling vizex {e}')

    def test_disk_usage_help(self):
        try:
            runner = CliRunner()
            result = runner.invoke(disk_usage, ['--help'])
            self.assertTrue(result.exit_code == 0)
            self.assertTrue('Made by: Beka Modebadze' in result.output)
        except Exception as e:
            self.fail(f'Exception occured when calling vizex --help {e}')


if __name__ == '__main__':
    unittest.main()