from pathlib import Path
from itertools import islice
from tools import find_word

from colored import fg, attr, stylize


SPACE = '    '
BRANCH = '│   '
TEE = '├── '
LEAF = '└── '

FILES_COUNT = 0
DIRS_COUNT = 0


def construct_tree(dir_path: str, level: int, only_dirs: bool = False,
                   max_length: int = 1000) -> None:
    dir_path = Path(dir_path)
    print_colored(str(dir_path), 'red', 'bold')
    iterator = generate_iterable(
        dir_path, level=level, only_dirs=only_dirs)
    for line in islice(iterator, max_length):
        filter_project_dirs(line)
    if next(iterator, None):
        print(f'... length limit of {max_length} is reached! counted:')
    print(f'\n{stylize(DIRS_COUNT, fg(172))} directories'
          + (f', {stylize(FILES_COUNT, fg(12))} files' if FILES_COUNT else ''))


def generate_iterable(dir_path: Path, prefix: str = '',
                      level=-1, only_dirs: bool = False) -> str:
    global FILES_COUNT, DIRS_COUNT
    if not level:
        return  # stop iterating

    if only_dirs:
        contents = [d for d in dir_path.iterdir() if d.is_dir()]
    else:
        contents = list(dir_path.iterdir())

    pointers = [TEE] * (len(contents) - 1) + [LEAF]
    for pointer, path in zip(pointers, contents):
        if path.is_dir():
            yield prefix + pointer + path.name
            DIRS_COUNT += 1
            extension = BRANCH if pointer == TEE else SPACE
            yield from generate_iterable(
                path, prefix=prefix + extension, level=level - 1)
        elif not only_dirs:
            yield prefix + pointer + path.name
            FILES_COUNT += 1


def filter_project_dirs(line: str) -> None:
    if find_word('test', line) or find_word('tests', line):
        print_colored(line, 'sky_blue_2', 'bold')
    elif find_word('src', line) or find_word('main', line):
        print_colored(line, 'chartreuse_2b', 'bold')
    elif find_word('venv', line):
        print_colored(line, 'purple_1a', 'dim')
    elif is_hidden(line):
        print_colored(line, 'dark_gray', 'dim')
    else:
        print(line)


def print_colored(line: str, color: str = None,
                  style: str = None) -> None:
    for c in line:
        if c not in ('├', '─', '│', '└'):
            print(stylize(c, attr(style) + fg(color)), end='')
        else:
            print(c, end='')
    print()


def is_hidden(line: str) -> bool:
    for c in line:
        if c in ('├', '─', '│', '└', ' '):
            continue
        return c == '.'


if __name__ == '__main__':
    construct_tree("../", level=2)
