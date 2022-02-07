"""
-[ ] Option to record the all the cpu freqs
-[ ] Do some analysis on them based on time and maybe what was running from processes
"""

import os
import time
import psutil
import getpass
import tools

from .charts import HorizontalBarChart


class CPUFreq:
    _max = psutil.cpu_freq().max
    _min = psutil.cpu_freq().min

    @property
    def max_freq(self) -> int:
        return self._max

    @max_freq.setter
    def max_freq(self, maximum: int) -> None:
        self._max = maximum

    @property
    def min_freq(self) -> int:
        return self._min

    @min_freq.setter
    def min_freq(self, minimum: int) -> None:
        self._min = minimum

    def __init__(self) -> None:
        return

    def display_separately(self, filename="") -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        ch = HorizontalBarChart()
        ch.options.graph_color = 'white'

        while True:
            cpu = psutil.cpu_freq(percpu=True)

            for i, core in enumerate(cpu, start=1):
                min_freq, max_freq, current_freq = core.min, core.max, core.current
                percent = round((current_freq - min_freq) / (max_freq - min_freq) * 100, 2)
                ch.chart(
                    title=f'CPU #{i}',
                    pre_graph_text=f'Current: {round(current_freq, 1)}MHz || Min: {min_freq}MHz || Max: {max_freq}MHz',
                    post_graph_text=tools.create_usage_warning(percent, 30, 15),
                    footer=None,
                    maximum=max_freq - min_freq,
                    current=current_freq - min_freq,
                )

                if filename:
                    cpu = {
                        'user': [getpass.getuser()],
                        'cpu': [i],
                        'time': [time.time()],
                        'current': [current_freq],
                        'usage': [percent],
                    }

                    if (filename.split(".")[-1].lower()) == 'csv':
                        tools.save_to_csv(cpu, filename)
                    else:
                        raise NameError("Not supported file type, please indicate "
                                        + ".CSV at the end of the filename")

                print()

            time.sleep(0.8)
            os.system('cls' if os.name == 'nt' else 'clear')

    def display_combined(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        ch = HorizontalBarChart()
        ch.options.graph_color = 'white'
        while True:
            cpu = psutil.cpu_freq(percpu=False)
            ch.chart(
                title='CPU (ALL)',
                pre_graph_text=f'Current: {round(cpu.current, 1)}MHz || Min: {self._min}MHz || Max: {self._max}MHz',
                post_graph_text=tools.create_usage_warning(
                    round((cpu.current - self._min) / (self._max - self._min) * 100, 2),
                    30, 15),
                footer=None,
                maximum=self._max - self._min,
                current=cpu.current - self._min
            )
            print()

            time.sleep(0.8)
            os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    cpu_freq = CPUFreq()
    cpu_freq.display_separately("~/cpu.csv")
