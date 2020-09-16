from math import ceil
from enum import Enum
from colored import fg, attr, stylize

class Color(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    CYAN = 6
    WHITE = 7
    GRAY = 8
    LIGHT_RED = 9
    DARK_BLUE = 18
    DARK_GREEN = 22
    DARK_RED = 52
    NEON = 82
    PURPLE = 93
    ORANGE = 214
    PINK = 218
    BEIGE = 230


class Attr(Enum):
    BOLD = 1
    DIM = 2
    UNDERLINED = 4
    BLINK = 5
    REVERSE = 7
    HIDDEN = 8


class Chart(Enum):
    BARH = 1
    BARV = 2
    PIE = 3


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