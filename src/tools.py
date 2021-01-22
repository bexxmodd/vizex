""" Utility function for vizex """

import json
import pandas as pd

from math import ceil
from colored import fg, attr, stylize

def bytes_to_human_readable(bytes: int, suffix='B') -> str:
    """
    Converts bytes into the appropriate human
    readable unit with a relevant suffix.
    """
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(bytes) < 1024.0:
            return f'{bytes:3.1f} {unit}{suffix}'
        bytes /= 1024.0
    return f'{bytes:.1f} {"Y"}{suffix}'

def ints_to_human_readable(disk: dict) -> dict:
    """
    Converts the dictionary of integers
    into the human readable strings.
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
    df = pd.DataFrame.from_dict(data, orient=orient)
    df.to_csv(filename, mode='a')

def save_to_json(data: dict,
                filename: str,
                indent: int=4) -> None:
    """Saves disk/partitions data as a JSON file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=indent)