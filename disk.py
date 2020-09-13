#!/usr/bin/python3
"""
- [ ] Option to display TeraBytes (TB)
"""

import psutil
from enum import Enum
from math import ceil
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


class DiskUsage:
    """
    Personalize and visualize the disk usage in the terminal

    options:
        barh: visualize values as a horizontal bar
        barv: visualiz disk space as a vertical bar
        pie: visualize as a pie charts
    """

    def __init__(self,
                chart: Chart,
                header: Color,
                style: Attr,
                exclude: list,
                text: Color = None,
                graph: Color = None) -> None:
        self.chart = chart
        self.header = fg(header.value)
        self.style = attr(style.value)
        self.exclude = exclude
        if text:
            self.text = fg(text.value)
        else:
            self.text = text
        if graph:
            self.graph = fg(graph.value)
        else:
            self.graph = graph

    def main(self) -> None:
        """Prints the charts based on user selection type"""
        if self.chart == Chart.BARH:
            self.print_horizontal_barchart()
        elif self.chart == Chart.BARV:
            self.print_vertical_barchart()
        elif self.chart == Chart.PIE:
            pass

    def disk_space(self) -> dict:
        """Creates a dictionary of the media
        and disk partitions on the given computer. 

        returns:
            keys as partition names and disk size as values
        """
        disks = {}
        # First append the root partition
        disks["root"] = {"total": psutil.disk_usage("/").total,
                        "used": psutil.disk_usage("/").used,
                        "free": psutil.disk_usage("/").free,
                        "fstype": psutil.disk_partitions(all=False)[0][2]}
        # Add media partitions
        disk_parts = psutil.disk_partitions(all=True)
        for disk in disk_parts[:-1]:
            # disk[1] is the path to the disk partition
            # if it starts with media we'll get it
            if 'media' in disk[1]:
                try:
                    disks[disk[1].split('/')[-1]] = {
                        "total": psutil.disk_usage(disk[1]).total,
                        "used": psutil.disk_usage(disk[1]).used,
                        "free": psutil.disk_usage(disk[1]).free,
                        "fstype": disk.fstype
                    }
                except:
                    continue
        return disks

    # Function to convert bytes into Gb or Mb based on its size
    def bytes_to_human_readable(self, bytes: int) -> str:
        """Convert bytes into human readable form

        args:
            bytes
        returns:
            Digits with accompanied value (GB|MB|KB)
        """
        gb = bytes / 1024 / 1024 / 1024
        if gb < 1:
            return f'{round(gb * 1024, 2)} MB'
        return f'{round(gb, 2)} GB'

    def create_horizontal_bar(self, disk: dict) -> str:
        """
        Add args for user option to choose symbols
        for bar and for empty space.

        args:
            media disk from the host computer
        returns:
            horizontal bar representing the space usage
        """
        used = 0
        bar = ' '
        try:
            used = int((disk['used'] / disk['total']) * 36)
        except:
            raise ValueError("Expected total, used, & free as keys")
        for i in range(1, used + 1):
            bar += '█'
        bar += '▒'
        for i in range(1, 37 - used):
            bar += '░'
        return bar

    def usage_percent(self, disk: dict) -> float:
        """calculates the disk space usage percentage

        args:
            disk partition space values
        raises:
            ValueError: if any of the dict keys are missing
        returns:
            percent of the disk space used
        """
        try:
            return disk['used'] / disk['total']
        except:
            raise ValueError("Expected total, used, & free as keys")

    def integers_to_readable(self, disk: dict) -> dict:
        """Returns the dictionary of integers
        converted into human readable strings

        args:
            disk partition
        raises:
            TypeError: if the dict has no requiered keys
        returns:
            alphanumeric text as values and the total,
            used and free space as keys
        """
        try:
            total = self.bytes_to_human_readable(disk['total'])
            used = self.bytes_to_human_readable(disk['used'])
            free = self.bytes_to_human_readable(disk['free'])
        except:
            raise TypeError("Non-media type dict given")
        return {'total': total, 'used': used, 'free': free}

    def print_horizontal_barchart(self) -> None:
        """Prints the disk usage in the Terminal
        """
        disks = self.disk_space()
        for disk in disks:
            if disk not in self.exclude:
                # Print partition name
                print(f"{stylize(disk, self.header + self.style)} ({disks[disk]['fstype']})")
                if self.text == None:
                    res = self.integers_to_readable(disks[disk])
                    print(f"Total: {res['total']}   Used: {res['used']}   Free: {res['free']}")
                else:
                    res = self.integers_to_readable(disks[disk])
                    print(stylize(f"Total: {res['total']}   Used: {res['used']}   Free: {res['free']}", self.text))
                # Print usage and usage percent
                usage = round(self.usage_percent(disks[disk]) * 100, 2)
                if usage >= 80:
                    usage = str(usage) + '% full'
                    if self.graph == None:
                        print(f"{self.create_horizontal_bar(disks[disk])}  "\
                            + f"{stylize(usage, attr(Attr.BLINK.value) + fg(Color.LIGHT_RED.value))}\n")
                    else:
                        print(f"{stylize(self.create_horizontal_bar(disks[disk]), self.graph)}  "\
                            + f"{stylize(usage, fg(Color.LIGHT_RED.value), attr(Attr.BLINK.value))}\n")                    
                elif usage >= 60:
                    usage = str(usage) + '% full'
                    if self.graph == None:
                        print(f"{self.create_horizontal_bar(disks[disk])}  "\
                            + f"{stylize(usage, fg(Color.ORANGE.value))}\n")
                    else:
                        print(f"{stylize(self.create_horizontal_bar(disks[disk]), self.graph)}  "\
                            + f"{stylize(usage, fg(Color.ORANGE.value))}\n")
                else:
                    usage = str(usage) + '% full'
                    if self.graph == None:
                        print(f"{self.create_horizontal_bar(disks[disk])}  "\
                            + f"{stylize(usage, fg(Color.NEON.value))}\n")
                    else:
                        print(f"{stylize(self.create_horizontal_bar(disks[disk]), self.graph)}  "\
                            + f"{stylize(usage, fg(Color.NEON.value))}\n")

    def print_vertical_barchart(self) -> str:
        """prints vertical bar chart in the Terminal
        """
        charts = []
        disks = self.disk_space()
        for disk in disks:
            if disk not in self.exclude:
                usage_percent = self.usage_percent(disks[disk]) * 100
                text = self.integers_to_readable(disks[disk])
                n = 8 * (usage_percent / 100)
                # If the usage % is below 1 print empty chart
                if n < 0.1:
                    n = 0
                else:
                    # Round up to the closest integer
                    n = ceil(n)
                # Print disk usage percent
                if usage_percent >= 80:
                    used = stylize(str(round(usage_percent, 2)) + '% full',
                            attr(Attr.BLINK.value) + fg(Color.LIGHT_RED.value))
                elif usage_percent >= 60:
                    used = stylize(str(round(usage_percent, 2)) + '% full',
                            fg(Color.ORANGE.value))
                else:
                    used = stylize(str(round(usage_percent, 2)) + '% full',
                            fg(Color.NEON.value))

                def draw_chart(n):
                    """
                    creates a multiline string with horizontal bar chart,
                    name of the partition and its detailed usage information.
                    """
                    res = []
                    full, empty = '▓▓▓▓▓▓▓▓▓▓', '░░░░░░░░░░'
                    total, use, free = text['total'], text['used'], text['free']
                    # Check if user has elected graph color
                    if self.graph:
                        full = stylize('▓▓▓▓▓▓▓▓▓▓', self.graph)
                        empty = stylize('░░░░░░░░░░', self.graph)
                    # Check if user selected the text color
                    if self.text:
                        total = stylize(text['total'], self.text)
                        use = stylize(text['used'], self.text)
                        free = stylize(text['free'], self.text)
                    for i in range(n):
                        res.append(full)
                    for i in range(8 - n):
                        res.append(empty)
                    return f'''
    {res[7]}
    {res[6]}  {stylize(disk, self.header + self.style)} ({disks[disk]['fstype']})
    {res[5]}
    {res[4]}  Total: {total}
    {res[3]}  Used: {use}
    {res[2]}  Free: {free}
    {res[1]}   {used}
    {res[0]}
    '''
            charts.append(draw_chart(n))
        # Print out all the partitions
        for ch in charts:
            print(ch)


if __name__ == '__main__':
    du = DiskUsage()
    du.main()