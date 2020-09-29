""" Battery module for vizex """
import datetime
import psutil

from math import ceil
from charts import Chart, HorizontalBarChart, Options
from colored import fg, attr, stylize
from tools import bytes_to_human_readable, ints_to_human_readable


class Battery:
    """ Personalize and visualize the Battery usage in the terminal """

    def __init__(self) -> None:
        """ Create a new Battery Object """
        self._battery = psutil.sensors_battery()
        if self._battery is None:
            raise Exception("Battery information currently unavailable")
        return

    def print_charts(self, options: Options = None) -> None:
        """Prints the charts based on user selection type"""
        if options is None:
            options = Options()

        chart = HorizontalBarChart(options)
        self.print_battery_chart(chart)

    def print_battery_chart(self, chart: Chart) -> None:
        ch = chart
        post_graph_text = str(ceil(100 * self._battery.percent) / 100) + "%"
        footer = self.create_details_text()

        ch.chart(
            post_graph_text=post_graph_text,
            pre_graph_text=None,
            title="Battery",
            footer=footer,
            maximum=100,
            current=self._battery.percent,
        )
        print()

    def create_details_text(self) -> str:
        time_left = datetime.timedelta(seconds=self._battery.secsleft)

        plugged = self._battery.power_plugged
        ret: str
        if plugged:
            ret = format("Charging")
        else:
            ret = format("Plugged in: %s\tDischarging: %s\t" % (plugged, time_left))

        return ret


if __name__ == "__main__":
    self = Battery()
    self.print_charts()
    # Example output:

    # Physical Memory
    # █████████████▒░░░░░░░░░░░░░░░░░░░░░░░░░ 35.46% full
    # Total: 15.4 GB Used: 5.5 GB  Free: 988.3 MB Avail: 7.3 GB

    # Swap Space
    # ▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0.03% full
    # Total: 15.7 GB Used: 4.5 MB  Free: 15.7 GB
