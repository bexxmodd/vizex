# Utility functions and Classes for vizex/vizexdf

import os
import json
import time
import pandas as pd

from math import ceil
from colored import fg, attr, stylize


def bytes_to_human_readable(bytes: int, suffix='b') -> str:
    """
    Converts bytes into the appropriate human
    readable unit with a relevant suffix.

    Args:
        bytes (int): to convert
        suffix (str, optional): suffix of a size string.
                                Defaults to 'b'.

    Returns:
        str: [description]
    """
    for unit in ['','k','m','g','t','p','e','z']:
        if abs(bytes) < 1024.0:
            return f'{bytes:3.1f} {unit}{suffix}'
        bytes /= 1024.0
    return f'{bytes:.1f} {"Y"}{suffix}'

def ints_to_human_readable(disk: dict) -> dict:
    """Converts the dictionary of integers
    into the human readable size formats.

    Args:
        disk [dict]: of large byte numbers

    Returns:
        dict: same dict but in human readable format
    """
    result = {}
    try:
        for key in disk:
            result[key] = bytes_to_human_readable(disk[key])
    except Exception:
        result[key] = disk[key] # If not able to convert return input back
    return result

def printml(folder: list, cols: int = 1) -> None:
    """Prints multiline strings side by side.

    Args:
        folder (list): list of folders to print
        cols (int, optional): On how many lines should it be printed.
                            Defaults to 1.
    """
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
    """Create disk usage percent with warning color

    Args:
        usage_pct (float): of a given space
        red_flag (int): threshold that decides if print should be red
        yellow_flag (int): threshold that decides if print is yellow

    Returns:
        str: [description]
    """
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
    """Outputs disks/partitions data as a CSV file

    Args:
        data (dict): to be saved to a CSV file
        filename (str): to name a saved file
        orient (str, optional): how lines are saved.
                                Defaults to 'index'.

    Raises:
        NameError: [description]
    """
    if filename.split(".")[-1].lower() == 'csv':
        df = pd.DataFrame.from_dict(data, orient=orient)
        df.to_csv(filename, mode='a')
    else:
        raise NameError('Please include ".csv" in the filename')

def save_to_json(data: dict,
                filename: str,
                indent: int=4) -> None:
    """Saves disk/partitions data as a JSON file

    Args:
        data (dict): to be saved to a JSON file
        filename (str): to name a saved file
        indent (int, optional): of each new line.
                                Defaults to 4.

    Raises:
        NameError: [description]
    """
    if filename.split(".")[-1].lower() == 'json':
        with open(filename, "w") as f:
            json.dump(data, f, indent=indent)
    else:
        raise NameError('Please include ".json" in the filename')

def append_to_bash(alias: str, line: str) -> None:
    """
    Appends terminal command line as an alias in .bashrc for reuse

    Args:
        alias[str]: To set up in the bash
        line[str]: line which will be assigned to an alias
    """
    bash = os.path.expanduser("~") + '/.bash_aliases'
    print(remove_if_exists(alias, bash))
    with open(bash, 'a+') as f:
            # if line.startswith(f'alias {alias}')
        f.write('alias ' + alias + f"='{line}'")

def remove_if_exists(alias: str, path: str) -> None:
    """
    Removes if the given line/alias exists in a given file

    Args:
        alias (str): to check if exists in bash
        path (str): path to the file to read
    """
    if not os.path.exists(path):
        return
    with open(path, "r") as f:
        lines = f.readlines()
    with open(path, "w") as f:
        for line in lines:
            # We only write back lines which is not alias
            if f'alias {alias}' not in line.strip("\n"):
                f.write(line)

def normalize_date(format: str, date: int) -> str:
    """
    Converts date from nanoseconds to the fuman readable form

    Args:
        format (str): example %h-%d-%Y for mm-dd-yyyy
        date_as_nanosecs (int): date in nanoseconds

    Returns:
        str: Human readable format of a date
    """
    return time.strftime(format, time.localtime(date))


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
    file1 = DecoratedData(55456, '54.2 kb')
    file2 = DecoratedData(123233419, '117.5 mb')
    print(f'{file1} is less than {file2} : {file1 < file2}')