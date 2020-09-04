#!/usr/bin/python3
"""
visualize disk usage and disk space in terminal
"""

import psutil
from colored import fg, bg, attr, stylize


def main():
    """
    Add option for user to choose colors
    """
    disks = disk_space()
    for disk in disks:
        final = f"{stylize(disk, fg(197), attr('bold'))}" \
            + f"\n{stylize(print_stats(disks[disk]), attr('res_blink'))}" \
            + f"\n{print_graph(disks[disk])[0]}   " \
            + f"{stylize(print_graph(disks[disk])[1], attr('dim'))}\n"
        print(final)

def disk_space() -> dict:
    disks = {}
    # First append the root partition
    disks["root"] = {"total": psutil.disk_usage("/").total,
                    "used": psutil.disk_usage("/").used,
                    "free": psutil.disk_usage("/").free}
    # Add media partitions
    disk_parts = psutil.disk_partitions(all=True)
    for disk in disk_parts[:-1]:
        # disk[1] is Path to the disk partition,
        # if it starts with media will grab it
        if 'media' in disk[1]:
            disks[disk[1].split('/')[-1]] = {"total": psutil.disk_usage(disk[1]).total,
                            "used": psutil.disk_usage(disk[1]).used,
                            "free": psutil.disk_usage(disk[1]).free}
    return disks


# Function to convert bytes into Gb or Mb based on its size
def bytes_to_readable_format(bytes: int) -> int:
    gb = round(bytes / 1024 / 1024 / 1024, 2)
    if gb < 1.0:
        return f'{gb * 1024} MB'
    return f'{gb} GB'

# Printing free and used space
def print_graph(disk: dict) -> str:
    """
    Add args for user option to choose symbols
    for bar and for empty space.
    """
    used = 0
    bar = ''
    try:
        used = int((disk['used'] / disk['total']) * 36)
    except:
        raise ValueError("Expected total, used, and free as dict keys")
    for i in range(1, used + 1):
        bar += '█'
    for i in range(1, 37 - used):
        bar += '░'
    free_portion = round(disk['used'] / disk['total'] * 100, 2)
    return f'{bar}', f'{free_portion} %'

def print_stats(disk: dict) -> str:
    try:
        total = bytes_to_readable_format(disk['total'])
        used = bytes_to_readable_format(disk['used'])
        free = bytes_to_readable_format(disk['free'])
    except:
        raise TypeError("Non-media type dict given")
    return f'Total: {total}   Used: {used}   Free: {free}'


# "████████████████░░░░░░░░░"
# print('\n', psutil.sensors_temperatures())
# print('\n', psutil.Process(5622).memory_info())

# print(os.path.abspath('../'))
# folder = os.listdir('.')
# for i in folder:
#     if os.path.isfile('./' + i):
#         print(f'file {i} is:', os.path.getsize('./' + i))

if __name__ == '__main__':
    main()