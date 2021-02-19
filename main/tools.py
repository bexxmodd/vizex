""" Utility functions and Classes for vizex/vizexdf """

import os
import json
import pandas as pd

from math import ceil
from colored import fg, attr, stylize


def bytes_to_human_readable(bytes: int, suffix='b') -> str:
    """
    Converts bytes into the appropriate human
    readable unit with a relevant suffix.
    """
    for unit in ['','k','m','g','t','p','e','z']:
        if abs(bytes) < 1024.0:
            return f'{bytes:3.1f} {unit}{suffix}'
        bytes /= 1024.0
    return f'{bytes:.1f} {"Y"}{suffix}'

def ints_to_human_readable(disk: dict) -> dict:
    """
    Converts the dictionary of integers
    into the human readable size formats.
    """
    result = {}
    try:
        for key in disk:
            result[key] = bytes_to_human_readable(disk[key])
    except:
        result[key] = disk[key]
    return result

def printml(folder: list, cols: int = 1) -> None:
    """Prints multiline strings side by side."""
    size = len(folder)
    incr = ceil(size / cols)
    end, start = 0, 0
    while True:
        if end >= size:
            break
        end += incr
        # Check if the end index exceeds the last index
        if end > size:
            end = size
        lines = [folder[i].splitlines() for i in range(start, end)]
        for line in zip(*lines):
            print(*line, sep='  ')
        print()
        start = end

def create_usage_warning(usage_pct: float,
                        red_flag: int,
                        yellow_flag: int) -> str:
    """Create disk usage percent with warning color"""
    if usage_pct < 0:
        usage_pct = 0

    if usage_pct > 100:
        usage_pct = 100

    use = str(usage_pct) + '% used'

    if usage_pct >= red_flag:
        return f"{stylize(use, attr('blink') + fg(9))}"
    elif usage_pct >= yellow_flag:
        return f"{stylize(use, fg(214))}"
    else:
        return f"{stylize(use, fg(82))}"

def save_to_csv(data: dict,
                filename: str,
                orient: str='index') -> None:
    """Outputs disks/partitions data as a CSV file"""
    file_type = filename.split(".")[-1]
    if file_type.lower() == 'csv':
        df = pd.DataFrame.from_dict(data, orient=orient)
        df.to_csv(filename, mode='a')
    else:
        raise NameError('Please include ".csv" in the filename')

def save_to_json(data: dict,
                filename: str,
                indent: int=4) -> None:
    """Saves disk/partitions data as a JSON file"""
    file_type = filename.split(".")[-1]
    if file_type.lower() == 'json':
        with open(filename, "w") as f:
            json.dump(data, f, indent=indent)
    else:
        raise NameError('Please include ".json" in the filename')

def set_alias(alias: str, line: str) -> None:
    """
    Saves terminal command line as an alias in .bashrc for reuse
    """
    bash = os.path.expanduser("~") + '/.bash_aliases'
    line_number = check_if_alias_exists(bash, 'pipreqs')
    # if line_number != -1:
    #     with open(bash, 'w')
    # else:
    #     print(-1)
    with open(bash, 'a+') as f:
            # if line.startswith(f'alias {alias}')
        f.write('alias ' + alias + f"='{line}'")

def check_if_alias_exists(path: str, alias: str) -> bool:
    """Checks if the alias already exists in bash file"""
    if not os.path.exists(path):
        return -1
    with open(path, 'r') as f:
        for n, line in enumerate(f, 0):
            print(n, line)
            if line.strip().startswith(f'alias {alias}'):
                print('FOUND!', n)
                return n
    return -1

    
class DecoratedData():
    """
    Custom class to compare numerical data for sorting
    which appears in the stylized representation of a string.
    """

    def __init__(self, size: int, to_string: str) -> None:
        self.size = size
        self.to_string = to_string

    def __eq__(self, other) -> bool:
        """Equals"""
        return self.size == other.size

    def __ne__(self, other) -> bool:
        """Not equals"""
        return self.size != other.size

    def __gt__(self, other) -> bool:
        """Greater than"""
        return self.size > other.size
    
    def __ge__(self, other) -> bool:
        """Greater than or equals to"""
        return self.size >= other.size
    
    def __lt__(self, other) -> bool:
        """Less than"""
        return self.size < other.size

    def __le__(self, other) -> bool:
        """Less than or equals to"""
        return self.size <= other.size

    def __str__(self):
        """String representation of the class"""
        return self.to_string


if __name__ == '__main__':
    # file1 = DecoratedData(55456, '54.2 kb')
    # file2 = DecoratedData(123233419, '117.5 mb')
    # print(f'{file1} is less than {file2} : {file1 < file2}')
    set_alias('test', 'something -set -like -this')