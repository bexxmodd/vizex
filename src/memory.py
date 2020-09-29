""" Memory module for vizex """

from math import ceil
import psutil
from colored import fg, attr, stylize
from charts import Chart, HorizontalBarChart, Options
from tools import bytes_to_human_readable


class Memory:
    """ Personalize and visualize the memory usage in the terminal """

    def __init__(self) -> None:
        """ Create a new Battery Object """
        self._memory = psutil.virtual_memory()
        self._swap = psutil.swap_memory()

        return

    def print_charts(self, options: Options = None) -> None:
        """Prints the charts based on user selection type"""
        if options is None:
            options = Options()

        chart = HorizontalBarChart(options)
        memory = self._memory
        self.print_memory_chart(
            chart,
            "Physical Memory",
            memory.total,
            memory.used,
            memory.free,
            memory.available,
        )

        chart = HorizontalBarChart(options)
        memory = self._swap
        self.print_memory_chart(
            chart, "Swap Space", memory.total, memory.used, memory.free, None
        )

    def print_memory_chart(
        self,
        chart: Chart,
        title: str,
        maximum: int,
        current: int,
        free: int,
        available: int,
    ) -> None:
        """ Print information about memory usage """
        post_graph_text = self.create_pct_used(current / maximum)
        footer = self.create_details_text(maximum, current, free, available)

        ch.chart(
            post_graph_text=post_graph_text,
            pre_graph_text=None,
            title=title,
            footer=footer,
            maximum=maximum,
            current=current,
        )
        print()

    def create_pct_used(self, usage_pct: float) -> str:
        """Create memory usage percent with warning color"""
        use = str(ceil(10000 * usage_pct) / 100) + "% full"
        if usage_pct >= 80:
            return f"{stylize(use, attr('blink') + fg(9))}"
        elif usage_pct >= 60:
            return f"{stylize(use, fg(214))}"
        else:
            return f"{stylize(use, fg(82))}"

    def create_details_text(self, maximum, current, free, available) -> str:
        """ Create details about memory usage """
        ret = format(
            "Total: %s Used: %s  Free: %s"
            % (
                bytes_to_human_readable(maximum),
                bytes_to_human_readable(current),
                bytes_to_human_readable(free),
            )
        )
        if available is not None:
            ret += " Avail: %s" % bytes_to_human_readable(available)

        return ret


if __name__ == "__main__":
    self = Memory()
    self.print_charts()
    # Example output:
    
    # Physical Memory
    # █████████████▒░░░░░░░░░░░░░░░░░░░░░░░░░ 35.46% full
    # Total: 15.4 GB Used: 5.5 GB  Free: 988.3 MB Avail: 7.3 GB

    # Swap Space
    # ▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0.03% full
    # Total: 15.7 GB Used: 4.5 MB  Free: 15.7 GB
