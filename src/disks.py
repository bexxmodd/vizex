import psutil
import tools
import platform
import pandas as pd

from math import ceil
from charts import Chart, HorizontalBarChart, Options
from colored import fg, attr, stylize


class DiskUsage:
    """
    Personalize and visualize the disk space usage in the terminal
    """

    def __init__(self,
                path: str = "",
                exclude: list=None,
                details: bool=False,
                every: bool=False) -> None:
        self.path = path
        if exclude is None:
            self.exclude = []
        else:
            self.exclude = exclude
        self.details = details
        self.every = every
        self._platform = platform.system() # Check on which platform vizex operates

    def print_charts(self, options: Options=None) -> None:
        """Prints the charts based on user selection type"""
        if options is None:
            options = Options()

        if self.path:
            parts = self.grab_specific(self.path[0])
        else:
            parts = self.grab_partitions(exclude=self.exclude,
                                        every=self.every)

        chrt = HorizontalBarChart(options)
        for partname in parts:
            self.print_disk_chart(chrt, partname, parts[partname])

    def print_disk_chart(
            self, chart: Chart, partname: str, part: dict
        ) -> None:
        ch = chart
        title = (partname,)
        pre_graph_text = self.create_stats(part)
        if self.details:
            footer = self.create_details_text(part)
        else:
            footer = None

        maximum = part["total"]
        current = part["used"]
        post_graph_text = tools.create_usage_warning(
                                part['percent'], 80, 60)

        ch.chart(
            post_graph_text=post_graph_text,
            title=title[0],
            pre_graph_text=pre_graph_text,
            footer=footer,
            maximum=maximum,
            current=current,
        )
        print()

    def grab_root(self) -> dict:
        """Grab the data about the root partition"""
        root = {
            "total": psutil.disk_usage("/").total,
            "used": psutil.disk_usage("/").used,
            "free": psutil.disk_usage("/").free,
            "percent": psutil.disk_usage("/").percent,
            "fstype": psutil.disk_partitions(all=False)[0][2],
            "mountpoint": "/",
        }
        return root

    def grab_partitions(self,
                        exclude: list,
                        every: bool) -> dict:
        """Grabs all the partitions"""
        if self.exclude is None:
            exclude = []
        disks = {}
        
        # If we don't need every part we grab root seperately
        if not every and self._platform != 'Windows':
            disks['root'] = self.grab_root()
        disk_parts = psutil.disk_partitions(all=every)
        
        for disk in disk_parts[1:]:

            # Exclude mounpoints created by snap
            if disk.device.startswith("/dev/loop"):
                continue

            # Check that tmp is not slipping as partition
            if disk.mountpoint.startswith("/tmp"):
                continue

            # Check that part name is not in the excluded list
            if disk[1].split("/")[-1] in exclude:
                continue

            try:
                if psutil.disk_usage(disk[1]).total > 0:
                    disks[disk[1].split("/")[-1]] = {
                        "total": psutil.disk_usage(disk[1]).total,
                        "used": psutil.disk_usage(disk[1]).used,
                        "free": psutil.disk_usage(disk[1]).free,
                        "percent": psutil.disk_usage(disk[1]).percent,
                        "fstype": disk.fstype,
                        "mountpoint": disk.mountpoint,
                    }
            except:
                continue
        return disks

    def grab_specific(self, disk_path: str) -> dict:
        """
        Grabs data for the partition of the user specified path
        """
        disks = {}
        disks[disk_path] = {
            "total": psutil.disk_usage(disk_path).total,
            "used": psutil.disk_usage(disk_path).used,
            "free": psutil.disk_usage(disk_path).free,
            "percent": psutil.disk_usage(disk_path).percent,
            "fstype": "N/A",
            "mountpoint": "N/A",
        }
        return disks

    def create_details_text(self, disk: dict) -> str:
        return f"fstype={disk['fstype']}\tmountpoint={disk['mountpoint']}"

    def create_stats(self, disk: dict) -> str:
        r = tools.ints_to_human_readable(disk)
        return f"Total: {r['total']}\t Used: {r['used']}\t Free: {r['free']}"

    def save_data(self, filename: str) -> None:
        """Outputs disks/partitions data as a CSV file"""
        data = self.grab_partitions(self.exclude, self.every)
        file_type = filename.split(".")[-1]
        if file_type.lower() == 'csv':
            tools.save_to_csv(data, filename)
        elif file_type.lower() == 'json':
            tools.save_to_json(data, filename)
        else:
            print("Not support file type")


if __name__ == "__main__":
    self = DiskUsage()
    parts = self.grab_partitions(exclude=[], every=False)

    for partname in parts:
        part = parts[partname]
        ch = HorizontalBarChart()
        title = (partname,)
        pre_graph_text = self.create_stats(part)
        footer = self.create_details_text(part)
        maximum = part["total"]
        current = part["used"]
        post_graph_text = tools.create_usage_warning(
                                    part['percent'], 80, 60)

        ch.chart(
            post_graph_text=post_graph_text,
            title=title[0],
            pre_graph_text=pre_graph_text,
            footer=footer,
            maximum=maximum,
            current=current,
        )
        print()
