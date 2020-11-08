"""
-[ ] Option to record the all the cpu freqs
-[ ] Do some analysis on them based on time and maybe what was running from processes
"""

import os
import time
import psutil
import tools
import getpass

from charts import HorizontalBarChart, Chart, Options


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

    def display_separately(self, save=True) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        ch = HorizontalBarChart()
        ch.options.graph_color = 'white'

        while True:
            cpu = psutil.cpu_freq(percpu=True)
            
            for n, i in enumerate(cpu, start=1):
                percent = round((i.current-self._min) / (self._max-self._min) * 100, 2)
                ch.chart(
                    title=f'CPU #{n}',
                    pre_graph_text=f'Current: {round(i.current, 1)}hz || Min: {self._min}hz || Max: {self._max}hz',
                    post_graph_text=tools.create_usage_warning(percent, 30, 15),
                    footer=None,
                    maximum=self._max - self._min,
                    current=i.current - self._min
                )

                if save:
                    cpu = {
                        'user': [getpass.getuser()],
                        'cpu': [n],
                        'time': [time.time()],
                        'current': [i.current],
                        'usage': [percent]
                        }

                    tools.save_to_csv(cpu, '~/cpus.csv')

                print()

            time.sleep(0.8)
            os.system('cls' if os.name == 'nt' else 'clear')
        tools.save_to_csv(cpu, '~/cpu.csv')
    
    def display_combined(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        ch = HorizontalBarChart()
        ch.options.graph_color = 'white'
        while True:
            cpu = psutil.cpu_freq(percpu=False)
            ch.chart(
                title='CPU (ALL)',
                pre_graph_text=f'Current: {round(cpu.current, 1)}hz || Min: {self._min}hz || Max: {self._max}hz',
                post_graph_text=tools.create_usage_warning(
                                round((cpu.current-self._min) / (self._max-self._min) * 100, 2),
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
    cpu_freq.display_separately()