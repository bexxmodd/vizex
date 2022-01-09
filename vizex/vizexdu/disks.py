'''
    Personalize and visualize the disk space usage in the terminal
'''

import psutil
import platform

from .charts import Chart, HorizontalBarChart, Options
from tools import ints_to_human_readable
from tools import save_to_csv, save_to_json, create_usage_warning


class DiskUsage:
    """
    Class to retrieve, organize, and print disk usage/disk space data
    """

    def __init__(self,
                 path: str = "",
                 exclude: list = [],
                 details: bool = False,
                 every: bool = False) -> None:
        self.path = path
        self.exclude = exclude
        self.details = details
        self.every = every
        self._platform = platform.system()  # Check for platform

    def print_charts(self, options: Options = None) -> None:
        """
        Prints the charts based on user selection of colors and what to print

        Args:
            options (Options): colors and symbols for printing
        """
        if not options:
            options = Options()

        if self.path:
            parts = DiskUsage.grab_specific_partition(self.path[0])
        else:
            parts = self.grab_partitions(exclude=self.exclude,
                                         every=self.every)

        chart = HorizontalBarChart(options)
        for partname in parts:
            self.print_disk_chart(chart, partname, parts[partname])

    def print_disk_chart(
            self, chart: Chart, partname: str, part: dict
    ) -> None:
        """Prints the disk data int terminal as a chart

        Args:
            ch (Chart): to print
            partname (str): partition title
            part (dict): partition data to be visualized
        """
        pre_graph_text = self.create_stats(part)

        footer = None
        if self.details:
            footer = DiskUsage.create_details_text(part)

        maximum = part["total"]
        current = part["used"]
        post_graph_text = create_usage_warning(
            part['percent'], 80, 60)

        chart.chart(
            post_graph_text=post_graph_text,
            title=partname,
            pre_graph_text=pre_graph_text,
            footer=footer,
            maximum=maximum,
            current=current,
        )
        print()

    @staticmethod
    def grab_root() -> dict:
        """
        Grab the data for the root partition

        return:
            (dict) with column titles as keys
        """
        return {
            "total": psutil.disk_usage("/").total,
            "used": psutil.disk_usage("/").used,
            "free": psutil.disk_usage("/").free,
            "percent": psutil.disk_usage("/").percent,
            "fstype": psutil.disk_partitions(all=False)[0][2],
            "mountpoint": "/",
        }

    def grab_partitions(self,
                        exclude: list,
                        every: bool) -> dict:
        """Grabs data for all the partitions.

        Args:
            exclude (list): of partitions to exclude
            every (bool): if all the partitions should be grabbed
        """
        disks = {}

        # If we don't need every part we grab root separately
        if not every and self._platform != 'Windows':
            disks['root'] = DiskUsage.grab_root()
        disk_parts = psutil.disk_partitions(all=every)

        for disk in disk_parts[1:]:
            if (DiskUsage._valid_mountpoint(disk) and
                    not DiskUsage._needs_excluded(disk, exclude)):
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
                except Exception as e:
                    print(e)
                    continue
        return disks

    @staticmethod
    def _valid_mountpoint(disk) -> bool:
        """Checks if it's an invalid mountpoint"""
        return (not disk.device.startswith("/dev/loop") and
                not disk.mountpoint.startswith("/tmp"))

    @staticmethod
    def _needs_excluded(disk, exclude: list) -> bool:
        """Checks if given disk needs to be excluded from a print"""
        return disk[1].split("/")[-1] in exclude

    @staticmethod
    def grab_specific_partition(disk_path: str) -> dict:
        """
        Grabs data for the partition of the user specified path

        Args:
            disk_path (str): to the partition to grab
        """
        disks = {disk_path: {
            "total": psutil.disk_usage(disk_path).total,
            "used": psutil.disk_usage(disk_path).used,
            "free": psutil.disk_usage(disk_path).free,
            "percent": psutil.disk_usage(disk_path).percent,
            "fstype": "N/A",
            "mountpoint": "N/A",
        }}
        return disks

    @staticmethod
    def create_details_text(disk: dict) -> str:
        """
        Creates a string representation of a disk

        Args:
            disk (dict): text to print
        """
        return f"fstype={disk['fstype']}\tmountpoint={disk['mountpoint']}"

    @staticmethod
    def create_stats(disk: dict) -> str:
        """
        Creates statistics as string for a disk

        Args:
            disk (dict): stats to print
        """
        r = ints_to_human_readable(disk)
        return f"Total: {r['total']}\t Used: {r['used']}\t Free: {r['free']}"

    def save_data(self, filename: str) -> None:
        """
        Outputs disks/partitions data as a CSV file

        Args:
            filename (str): for the saved file
        """
        data = self.grab_partitions(self.exclude, self.every)
        if (file_type := filename.split(".")[-1].lower()) == 'csv':
            save_to_csv(data, filename)
        elif file_type == 'json':
            save_to_json(data, filename)
        else:
            raise NameError("Not supported file type, please indicate "
                            + ".CSV or .JSON at the end of the filename")


def main():
    """Main function running the vizex program"""
    self = DiskUsage()
    parts = self.grab_partitions(exclude=[], every=False)

    for partname, part in parts.items():
        chart = HorizontalBarChart()
        title = (partname,)
        pre_graph_text = DiskUsage.create_stats(part)
        footer = DiskUsage.create_details_text(part)
        maximum = part["total"]
        current = part["used"]
        post_graph_text = create_usage_warning(
            part['percent'], 80, 60)

        chart.chart(
            post_graph_text=post_graph_text,
            title=title[0],
            pre_graph_text=pre_graph_text,
            footer=footer,
            maximum=maximum,
            current=current,
        )
        print()


if __name__ == "__main__":
    main()
