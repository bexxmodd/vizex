#!/usr/bin/python3
"""
visualize disk usage and disk space in terminal
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
    Personalize and visualize disk space and its usage in the terminal

    options:
        barh: visualizes values as a horizontal bar
        barv: visualize disk space as a vertical bar
        pie: visualizes as a pie charts
    """

    def __init__(self,
                chart: Chart,
                header: Color,
                style: Attr,
                text: Color = None,
                graph: Color = None) -> None:
        self.chart = chart
        self.header = fg(header.value)
        self.style = attr(style.value)
        if text:
            self.text = fg(text.value)
        else:
            self.text = text
        if graph:
            self.graph = fg(graph.value)
        else:
            self.graph = graph

    def main(self) -> None:
        if self.chart == Chart.BARH:
            self.print_barh()
        elif self.chart == Chart.BARV:
            self.print_barv()

    def disk_space(self) -> dict:
        """Gets and creates a dictionary of the media
        and disk partitions on the given computer. 

        rtype:
            dict: partition names as keys and disk paths as values
        """
        disks = {}
        # First append the root partition
        disks["root"] = {"total": psutil.disk_usage("/").total,
                        "used": psutil.disk_usage("/").used,
                        "free": psutil.disk_usage("/").free}
        # Add media partitions
        disk_parts = psutil.disk_partitions(all=True)
        for disk in disk_parts[:-1]:
            # disk[1] is the path to the disk partition
            # if it starts with media we'll get it
            if 'media' in disk[1]:
                try:
                    disks[disk[1].split('/')[-1]] = {"total": psutil.disk_usage(disk[1]).total,
                                                    "used": psutil.disk_usage(disk[1]).used,
                                                    "free": psutil.disk_usage(disk[1]).free}
                except:
                    continue
        return disks

    # Function to convert bytes into Gb or Mb based on its size
    def bytes_to_readable_format(self, bytes: int) -> str:
        """Convert bytes into human readable form

        args:
            bytes (int): bytes
        rtype:
            str: from based on the size of return value(GB|MB|KB)
        """
        gb = bytes / 1024 / 1024 / 1024
        if gb < 1:
            return f'{round(gb * 1024, 2)} MB'
        return f'{round(gb, 2)} GB'

    def print_graph(self, disk: dict) -> str:
        """
        Add args for user option to choose symbols
        for bar and for empty space.

        args:
            disk (dict): media disk from the host computer
        rtype:
            str: horizontal bar representing the space usage
        """
        used = 0
        bar = ' '
        try:
            used = int((disk['used'] / disk['total']) * 36)
        except:
            raise ValueError("Expected total, used, and free as dict keys")
        for i in range(1, used + 1):
            bar += '█'
        bar += '▒'
        for i in range(1, 37 - used):
            bar += '░'
        return bar

    def usage_percent(self, disk: dict) -> float:
        """calculates the disk space usage percentage

        args:
            disk (dict): disk partition space values
        raises:
            ValueError: if any of the dict keys are missing
        rtype:
            int: percent of the disk space used
        """
        try:
            return disk['used'] / disk['total']
        except:
            raise ValueError("Expected total, used, and free as dict keys")

    def print_stats(self, disk: dict) -> str:
        """Returns the disk total, used, and free space

        args:
            disk (dict): disk partition
        raises:
            TypeError: if the dict has no requiered keys
        rtype:
            str: alphanumeric text of the total, used and free space
        """
        try:
            total = self.bytes_to_readable_format(disk['total'])
            used = self.bytes_to_readable_format(disk['used'])
            free = self.bytes_to_readable_format(disk['free'])
        except:
            raise TypeError("Non-media type dict given")
        return f'Total: {total}   Used: {used}   Free: {free}'

    def print_barh(self) -> str:
        """Prints the disk usage based on the selected parameters
        """
        disks = self.disk_space()
        for disk in disks:
            print(f"{stylize(disk, self.header + self.style)}")
            if self.text == None:
                print(f"{self.print_stats(disks[disk])}")
            else:
                print(f"{stylize(self.print_stats(disks[disk]), self.text)}")
            usage = round(self.usage_percent(disks[disk]) * 100, 2)
            if usage >= 80:
                usage = str(usage) + '% full'
                if self.graph == None:
                    print(f"{self.print_graph(disks[disk])}  "\
                        + f"{stylize(usage, attr(Attr.BLINK.value) + fg(Color.LIGHT_RED.value))}\n")
                else:
                    print(f"{stylize(self.print_graph(disks[disk]), self.graph)}  "\
                        + f"{stylize(usage, fg(Color.LIGHT_RED.value), attr(Attr.BLINK.value))}\n")                    
            elif usage >= 60:
                usage = str(usage) + '% full'
                if self.graph == None:
                    print(f"{self.print_graph(disks[disk])}  "\
                        + f"{stylize(usage, fg(Color.ORANGE.value))}\n")
                else:
                    print(f"{stylize(self.print_graph(disks[disk]), self.graph)}  "\
                        + f"{stylize(usage, fg(Color.ORANGE.value))}\n")
            else:
                usage = str(usage) + '% full'
                if self.graph == None:
                    print(f"{self.print_graph(disks[disk])}  "\
                        + f"{stylize(usage, fg(Color.NEON.value))}\n")
                else:
                    print(f"{stylize(self.print_graph(disks[disk]), self.graph)}  "\
                        + f"{stylize(usage, fg(Color.NEON.value))}\n")

    def print_barv(self) -> str:
        disks = self.disk_space()
        for disk in disks:
            usage = self.usage_percent(disks[disk]) * 100
            n = 8 * (usage / 100)
            # If the usage is below 1% set up chart to empty
            if n < 0.1:
                n = 0
            else:
                # Round up to closest integer
                n = ceil(n)
            if usage >= 80:
                used = stylize(round(used, 2), attr(Attr.BLINK.value) + fg(Color.LIGHT_RED.value))
            elif usage >= 60:
                used = stylize(round(usage, 2), fg(Color.ORANGE.value))
            else:
                used = stylize(round(usage, 2), fg(Color.NEON.value))

            def draw_chart(n):
                res = []
                fb = '▓▓▓▓▓▓▓▓▓'
                eb = '░░░░░░░░░'
                for i in range(n):
                    res.append(fb)
                for i in range(8 - n):
                    res.append(eb)
                return f'''
    {res[7]}
    {res[6]}  {disk}
    {res[5]}
    {res[4]}  Total: {disks[disk]['total']}
    {res[3]}  Used: {disks[disk]['used']}
    {res[2]}  Free: {disks[disk]['free']}
    {res[1]}  {used} % full
    {res[0]}
                '''
            print(draw_chart(n))

if __name__ == '__main__':
    du = DiskUsage()
    du.main()