import os
import sys
import inspect

# Creates path to the main module files
def add_path():
    currentdir = os.path.dirname(
        os.path.abspath(
            inspect.getfile(inspect.currentframe())
            )
        )
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

if __name__ == '__main__':
    add_path()