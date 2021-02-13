import os
import getpass
import shutil
import time
import magic

from tabulate import tabulate
from collections import defaultdict
from tools import bytes_to_human_readable
from colored import fg, bg, stylize, attr

def get_usage(path: str=None, ignore_hidden: bool=True) -> list:
    """Returns the size of the folders and files in a given path"""
    if path is None:
        path = os.getcwd()
    data = []
    with os.scandir(path) as it:
        for entry in it:
            try:
                if ignore_hidden and entry.name.startswith('.'):
                    continue
                current = []
                entry_name = entry.name[:32]
                size = 0
                file_type = '-'
                if entry.is_file():
                    size = os.stat(entry).st_size
                    file_type = magic.from_file(entry_name, mime=True)
                    entry_name = stylize("» " + entry_name, fg(226))
                elif entry.is_dir():
                    entry_name = stylize("■ " + entry_name + "/", fg(202))
                    size = get_size(entry)
                dt = time.strftime(
                        '%h %d %Y %H:%M',
                        time.localtime(os.stat(entry).st_mtime))
                current.append(entry_name)
                current.append(dt)
                current.append(bytes_to_human_readable(size))
                current.append(file_type[:24])
                # add current list to the main list
                data.append(current)
            except FileNotFoundError:
                continue
    return data     

def get_size(start_path: str) -> int:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def sort_data(path: str=None,
            sort_by: str='type',
            desc: bool=False) -> list:
    key = -1
    if sort_by == 'name':
        key = 0
    elif sort_by == 'last modified':
        key = 1
    elif sort_by == 'size':
        key = 2
    # Grab the path data and sort inplace based on users input and name
    return sorted(get_usage(path), 
                key=lambda x: (x[key], x[0]),
                reverse=desc)

def tabulate_disk(path: str=None,
                sort_by: str='type',
                desc: bool=False) -> tabulate:
    headers = [
        'name ' + stylize('-n', attr("blink")),
        'last modified ' + stylize('-dt', attr("blink")), 
        'size ' + stylize('-z', attr("blink")),
        'type ' + stylize('-t', attr("blink"))
    ]
    result = sort_data(path, sort_by, desc)
    return tabulate(result, headers, tablefmt="rst")


if __name__ == '__main__':
    print(tabulate_disk())