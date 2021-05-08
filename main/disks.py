# Class to retrieve, organize, and print disk usage/disk space data

import psutil
import platform

from charts import Chart, HorizontalBarChart, Options
from tools import ints_to_human_readable
from tools import save_to_csv, save_to_json, create_usage_warning


class DiskUsage:
    """
    Personalize and visualize the disk space usage in the terminal
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
        self._platform = platform.system()  # Check on which platform vizex operates

    def print_charts(self, options: Options = None) -> None:
        """
        Prints the charts based on user selection type

        Args:
            options (Options): colors and symbols for printing
        """
        if not options:
            options = Options()

        if self.path:
            parts = self.grab_specific(self.path[0])
        else:
            parts = self.grab_partitions(exclude=self.exclude,
                                         every=self.every)

        chart = HorizontalBarChart(options)
        for partname in parts:
            self.print_disk_chart(chart, partname, parts[partname])

    def print_disk_chart(
            self, ch: Chart, partname: str, part: dict
    ) -> None:
        """Prints the disk data as a chart

        Args:
            ch (Chart): to print
            partname (str): partition title
            part (dict): partition data to be visualized
        """
        pre_graph_text = self.create_stats(part)

        footer = None
        if self.details:
            footer = self.create_details_text(part)

        maximum = part["total"]
        current = part["used"]
        post_graph_text = create_usage_warning(
            part['percent'], 80, 60)

        ch.chart(
            post_graph_text=post_graph_text,
            title=partname,
            pre_graph_text=pre_graph_text,
            footer=footer,
            maximum=maximum,
            current=current,
        )
        print()

    def grab_root(self) -> dict:
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
            if self.exclude and disk[1].split("/")[-1] in exclude:
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
            except Exception as e:
                print(e)
                continue
        return disks

    def grab_specific(self, disk_path: str) -> dict:
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

    def create_details_text(self, disk: dict) -> str:
        """
        Creates a string representation of a disk

        Args:
            disk (dict): text to print
        """
        return f"fstype={disk['fstype']}\tmountpoint={disk['mountpoint']}"

    def create_stats(self, disk: dict) -> str:
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
    self = DiskUsage()
    parts = self.grab_partitions(exclude=[], every=False)

    for partname, part in parts.items():
        ch = HorizontalBarChart()
        title = (partname,)
        pre_graph_text = self.create_stats(part)
        footer = self.create_details_text(part)
        maximum = part["total"]
        current = part["used"]
        post_graph_text = create_usage_warning(
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


if __name__ == "__main__":
    main()
