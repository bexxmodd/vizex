import psutil

from math import ceil
from charts import ChartPrint
from colored import fg, attr, stylize
from tools import Color, Attr, Chart
from tools import bytes_to_human_readable, ints_to_human_readable


class DiskUsage:
    """
    Personalize and visualize the disk space usage in the terminal

    options:
        barh: visualize values as a horizontal bar
        barv: visualiz disk space as a vertical bar
        pie: visualize as a pie charts
    """

    def __init__(self,
                chart: Chart,
                path: str,
                exclude: list,
                header: Color,
                style: Attr,
                details: bool = False,
                every: bool = False,
                symbol: str = None,
                text: Color = None,
                graph: Color = None) -> None:
        self.chart = chart
        self.path = path
        self.details = details
        self.header = fg(header.value)
        self.style = attr(style.value)
        self.exclude = exclude
        self.every = every
        self.symbol = symbol
        self.text = text
        self.graph = graph

    def main(self) -> None:
        """Prints the charts based on user selection type"""
        if self.chart == Chart.BARH:
            self.switch()
        elif self.chart == Chart.BARV:
            pass
        elif self.chart == Chart.PIE:
            pass

    def switch(self) -> None:
        """
        Switch between printing all the
        partitions or only user specified.
        """
        if self.path:
            disks = self.grab_specific_disk(self.path[0])
        else:
            disks = self.grab_partitions(exclude=self.exclude,
                                    every=self.every)
        for disk in disks:
            self.print_horizontal_barchart(disk, disks[disk])

    def print_horizontal_barchart(self,
                                disk_name: str,
                                disk: dict) -> None:
        """
        Prints disk usage in the Terminal with horizontal bars
        """
        print(f"{stylize(disk_name, self.header + self.style)}")
        print(self.create_stats(disk))
        chart = ChartPrint(self.graph, self.symbol)
        print('', chart.draw_horizontal_bar(capacity=disk['total'],
                                used=disk['used']),
                                self.create_warning(disk['percent']))
        if self.details:
            print(self.color_details_text(disk))
        print()

    def grab_partitions(self,
                        exclude: list,
                        every: bool=False) -> dict:
        """Grabs all the partitions from the user's PC."""
        disks = {}
        # First append the root partition
        disks["root"] = {"total": psutil.disk_usage("/").total,
                        "used": psutil.disk_usage("/").used,
                        "free": psutil.disk_usage("/").free,
                        "percent": psutil.disk_usage("/").percent,
                        "fstype": psutil.disk_partitions(all=False)[0][2],
                        "mountpoint": "/"}
        disk_parts = psutil.disk_partitions(all=every)
        for disk in disk_parts[1:]:
            # Exclude mounpoints created by snap
            if disk.device.startswith('/dev/loop'):
                continue
            # Check that part name is not in the excluded list
            if disk[1].split('/')[-1] in self.exclude:
                continue
            try:
                if psutil.disk_usage(disk[1]).total > 0:
                    disks[disk[1].split('/')[-1]] = {
                        "total": psutil.disk_usage(disk[1]).total,
                        "used": psutil.disk_usage(disk[1]).used,
                        "free": psutil.disk_usage(disk[1]).free,
                        "percent": psutil.disk_usage(disk[1]).percent,
                        "fstype": disk.fstype,
                        "mountpoint": disk.mountpoint
                    }
            except:
                continue
        return disks

    def grab_specific_disk(self, path: str) -> dict:
        """
        Grabs data for the partition of the user specified path
        """
        disks = {}
        disks[path] = {
                "total": psutil.disk_usage(path).total,
                "used": psutil.disk_usage(path).used,
                "free": psutil.disk_usage(path).free,
                "percent": psutil.disk_usage(path).percent,
                "fstype": 'N/A',
                "mountpoint": 'N/A'
        }
        return disks

    def color_details_text(self, disk: dict) -> dict:
        """
        Sets the color of fstype and mountpoint
        to the user specified text color.
        """
        if self.text:
            return stylize(f"fstype={disk['fstype']}\tmountpoint={disk['mountpoint']}",
                        fg(self.text.value))
        else:
            return f"fstype={disk['fstype']}\tmountpoint={disk['mountpoint']}"

    def create_stats(self, disk: dict) -> str:
        """Create disk/partition usage stats"""
        if self.text == None:
            res = ints_to_human_readable(disk)
            return f"Total: {res['total']}\t Used: {res['used']}\t Free: {res['free']}"
        else:
            res = ints_to_human_readable(disk)
            return stylize(f"Total: {res['total']}\t Used: {res['used']}\t Free: {res['free']}",
                            fg(self.text.value))

    def create_warning(self, usage: int) -> str:
        """Create disk usage percent with warning color"""
        use = str(usage) + '% full'
        if usage >= 80:
            return f"{stylize(use, attr(Attr.BLINK.value) + fg(Color.LIGHT_RED.value))}"                  
        elif usage >= 60:
            return f"{stylize(use, fg(Color.ORANGE.value))}"
        else:
            return f"{stylize(use, fg(Color.NEON.value))}"

    ####################################################
    ################ UNDER CONSTRUCTION ################
    ####################################################

    def print_vertical_barchart(self) -> str:
        pass
    #     """prints vertical bar chart in the Terminal
    #     """
    #     charts = []
    #     disks = self.disk_space()
    #     for disk in disks:
    #         if disk not in self.exclude:
    #             usage_percent = self.usage_percent(disks[disk]) * 100
    #             text = self.integers_to_readable(disks[disk])
    #             n = 8 * (usage_percent / 100)
    #             # If the usage % is below 1 print empty chart
    #             if n < 0.1:
    #                 n = 0
    #             else:
    #                 # Round up to the closest integer
    #                 n = ceil(n)
    #             # Print disk usage percent
    #             if usage_percent >= 80:
    #                 used = stylize(str(round(usage_percent, 2)) + '% full',
    #                         attr(Attr.BLINK.value) + fg(Color.LIGHT_RED.value))
    #             elif usage_percent >= 60:
    #                 used = stylize(str(round(usage_percent, 2)) + '% full',
    #                         fg(Color.ORANGE.value))
    #             else:
    #                 used = stylize(str(round(usage_percent, 2)) + '% full',
    #                         fg(Color.NEON.value))

    #             def draw_chart(n):
    #                 """
    #                 creates a multiline string with horizontal bar chart,
    #                 name of the partition and its detailed usage information.
    #                 """
    #                 res = []
    #                 full, empty = '▓▓▓▓▓▓▓▓▓▓', '░░░░░░░░░░'
    #                 total, use, free = text['total'], text['used'], text['free']
    #                 # Check if user has elected graph color
    #                 if self.graph:
    #                     full = stylize('▓▓▓▓▓▓▓▓▓▓', self.graph)
    #                     empty = stylize('░░░░░░░░░░', self.graph)
    #                 # Check if user selected the text color
    #                 if self.text:
    #                     total = stylize(text['total'], self.text)
    #                     use = stylize(text['used'], self.text)
    #                     free = stylize(text['free'], self.text)
    #                 for i in range(n):
    #                     res.append(full)
    #                 for i in range(8 - n):
    #                     res.append(empty)
    #                 return f'''
    # {res[7]}
    # {res[6]}  {stylize(disk, self.header + self.style)} ({disks[disk]['fstype']})
    # {res[5]}
    # {res[4]}  Total: {total}
    # {res[3]}  Used: {use}
    # {res[2]}  Free: {free}
    # {res[1]}   {used}
    # {res[0]}
    # '''
    #         charts.append(draw_chart(n))
    #     # Print out all the partitions
    #     for ch in charts:
    #         print(ch)


if __name__ == '__main__':
    du = DiskUsage()
    du.main()