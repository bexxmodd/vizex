from math import ceil
from tools import Color, Attr
from colored import fg, attr, stylize


class ChartPrint():
    """Draws chart with user selected color and symbol"""

    def __init__(self,
                graph: Color = None,
                symbol: str = None) -> None:
        if graph:
            self.graph = fg(graph.value)
        else:
            self.graph = graph
        if symbol:
            self.fsymbol = symbol
            self.msymbol = '>'
            self.esymbol = '-'
        else:
            self.fsymbol = '█'
            self.msymbol = '▒'
            self.esymbol = '░'
        self._check_graph_color()

    def _check_graph_color(self):
        if self.graph:
            self.fsymbol = stylize(self.fsymbol, self.graph)
            self.msymbol = stylize(self.msymbol, self.graph)
            self.esymbol = stylize(self.esymbol, self.graph)

    def draw_horizontal_bar(self, capacity: int, used: int) -> str:
        """Draw a horizontal bar chart
        
        Return:
            drawn horizontal bar chart
        """
        bar = ''
        usage = int((used / capacity) * 36)
        for i in range(1, usage + 1):
            bar += self.fsymbol
        bar += self.msymbol
        for i in range(1, 37 - usage):
            bar += self.esymbol
        # check if the user set up graph color
        if '█' not in self.fsymbol:
            return f'[{bar}]'
        return bar

    def draw_vertical_bar(self, capacity: int, used: int) -> str:
        """Draw a vertical bar chart

        Returns:
            drawn vertical bar chart
        """
        bar = '\n'
        n = (used / capacity) * 8
        # If the usage is below 1% print empty chart
        if n < 0.1:
            n = 0
        else:
            n = ceil(n)
        bar += f'{self.esymbol * 9}  \n' * (8 - n)
        bar += f'{self.fsymbol * 9}  \n' * n
        return bar
