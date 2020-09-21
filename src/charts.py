""" Text Chart Printing Functions """

from math import ceil
from colored import fg, attr, stylize


class Options():
    """Options"""
    _graph_color = fg("white")
    _header_color = fg("red")
    _pre_graph_color = fg("white")
    _post_graph_color = fg("white")
    _footer_color = fg("white")
    _fsymbol = '█'
    _msymbol = '▒'
    _esymbol = '░'

    def __init__(self):
        return

    @property
    def graph_color(self):
        """ Graph Color """
        return self._graph_color
    @graph_color.setter
    def graph_color(self, color):
        self._graph_color = fg(color)

    @property
    def header_color(self):
        """ Header Color """
        return self._header_color
    @header_color.setter
    def header_color(self, color):
        self._header_color = fg(color)

    @property
    def pre_graph_color(self):
        """ pre_graph_color """
        return self._pre_graph_color
    @pre_graph_color.setter
    def pre_graph_color(self, color):
        self._pre_graph_color = fg(color)

    @property
    def post_graph_color(self):
        """ post_graph_color """
        return self._post_graph_color
    @post_graph_color.setter
    def post_graph_color(self, color):
        self._post_graph_color=fg(color)

    @property
    def footer_color(self):
        """ footer_color """
        return self._footer_color
    @footer_color.setter
    def footer_color(self, color):
        self._footer_color = fg(color)


    @property
    def symbol(self):
        """ graph symbols to use """
        return [self._fsymbol, self._msymbol, self.esymbol]
    @symbol.setter
    def symbol(self, symbol):
        if symbol:
            self._fsymbol = symbol
            self._msymbol = '>'
            self._esymbol = '-'
        else:
            self._fsymbol = '█'
            self._msymbol = '▒'
            self._esymbol = '░'

    @property
    def fsymbol(self):
        """ The final symbol """
        return self._fsymbol

    @property
    def esymbol(self):
        """ The empty symbol """
        return self._esymbol

    @property
    def msymbol(self):
        """ The used symbol """
        return self._msymbol

class Chart():
    """Abstract base object for charts"""
    options: Options = None

    def __init__(self, options: Options = None):
        if options is None:
            self.options = Options()
        else:
            self.options = options


class BarChart(Chart):
    """Draws chart with user selected color and symbol"""
    def chart(self,
              title: str,
              pre_graph_text: str,
              post_graph_text: str,
              footer: str,
              maximum: float,
              current: float):

        print(stylize(title, self.options.header_color))

        if pre_graph_text:
            print(stylize(pre_graph_text, self.options.pre_graph_color))

        print("["+stylize(self.draw_horizontal_bar(maximum, current),
                      self.options.graph_color) + "]", end=" ")
        if post_graph_text:
            print(stylize(post_graph_text, self.options.post_graph_color))
        else:
            print()

        if footer:
            print(stylize(footer, self.options.footer_color))


    def draw_horizontal_bar(self, maximum: int, current: int) -> str:
        """Draw a horizontal bar chart

        Return:
            drawn horizontal bar chart
        """
        textBar = ''
        usage = int((current / maximum) * 36)
        for i in range(1, usage + 1):
            textBar += self.options.fsymbol
        textBar += self.options.msymbol
        for i in range(1, 37 - usage):
            textBar += self.options.esymbol
        # check if the user set up graph color
        if '█' not in self.options.fsymbol:
            return f'[{textBar}]'
        return textBar

class verticalBarChar(Chart):
    def draw_vertical_bar(self, capacity: int, used: int) -> str:
        """Draw a vertical bar chart

        Returns:
            drawn vertical bar chart
        """
        textBar = '\n'
        n = (used / capacity) * 8
        # If the usage is below 1% print empty chart
        if n < 0.1:
            n = 0
        else:
            n = ceil(n)
        textBar += f'{self.esymbol * 9}  \n' * (8 - n)
        textBar += f'{self.fsymbol * 9}  \n' * n
        return textBar


if __name__ == "__main__":
    ch = BarChart()
    ch.options.post_graph_color = "green"
    ch.options.pre_graph_color = "blue"
    ch.options.footer_color = "yellow"
    ch.chart(title="Test Content",
             maximum=100,
             current=32,
             pre_graph_text="Lorem: Sit ea dolore ad accusantium",
             post_graph_text="Good job!",
             footer="This concludes our test")
