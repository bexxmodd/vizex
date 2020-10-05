""" Text Chart Printing Functions """

from math import ceil
from colored import fg, attr, stylize

class Options:
    """Options"""

    _graph_color = fg("white")
    _header_color = fg("red")
    _header_style = attr('bold')
    _text_color = fg("white")
    _fsymbol = "█"
    _msymbol = "▒"
    _esymbol = "░"

    def __init__(self):
        return

    @property
    def graph_color(self):
        """ Graph Color """
        return self._graph_color

    @graph_color.setter
    def graph_color(self, color: str):
        self._graph_color = self._check_color(color, self._graph_color)

    @property
    def header_color(self):
        """ Header Color """
        return self._header_color

    @header_color.setter
    def header_color(self, color: str):
        self._header_color = self._check_color(color, self._header_color)

    @property
    def header_style(self):
        """ header style """
        return self._header_style
    
    @header_style.setter
    def header_style(self, style: str):
        self._header_style = self._check_attr(style, self._header_style)

    @property
    def text_color(self):
        """ text color """
        return self._text_color

    @text_color.setter
    def text_color(self, color: str):
        self._text_color = self._check_color(color, self._text_color)

    @property
    def symbol(self):
        """ graph symbols to use """
        return (self._fsymbol, self._msymbol, self.esymbol)

    @symbol.setter
    def symbol(self, symbol: str):
        if symbol:
            self._fsymbol = symbol
            self._msymbol = ">"
            self._esymbol = "-"
        else:
            self._fsymbol = "█"
            self._msymbol = "▒"
            self._esymbol = "░"

    @property
    def fsymbol(self):
        """ The full symbol """
        return self._fsymbol

    @property
    def esymbol(self):
        """ The empty symbol """
        return self._esymbol

    @property
    def msymbol(self):
        """ The middle symbol """
        return self._msymbol

    def _check_color(self, color: str, default_color: str="white"):
        """Checks if set color is valid"""
        try:
            return fg(color)
        except KeyError:
            return default_color

    def _check_attr(self, style: str, default_attr: str="bold"):
        """Checks if set attribute is valid"""
        try:
            return attr(style)
        except KeyError:
            return default_attr


class Chart:
    """Abstract base object for charts"""

    def __init__(self, options: Options = None):
        if options is None:
            self.options = Options()
        else:
            self.options = options


class HorizontalBarChart(Chart):
    """
    Create horizontal chart with user selected color and symbol
    """

    def chart(self,
            title: str,
            pre_graph_text: str,
            post_graph_text: str,
            footer: str,
            maximum: float,
            current: float) -> None:
        print(
            stylize(title, self.options.header_color + self.options.header_style)
        )

        if pre_graph_text:
            print(stylize(pre_graph_text, self.options.text_color))

        print(
            "%s"
            % stylize(
                self.draw_horizontal_bar(maximum, current),
                self.options.graph_color
            ),
            end=" ",
        )
        if post_graph_text:
            print(stylize(post_graph_text, self.options.text_color))
        else:
            print()

        if footer:
            print(stylize(footer, self.options.text_color))

    def draw_horizontal_bar(self, maximum: int, current: int) -> str:
        """Draw a horizontal bar chart"""

        # Sanity check that numbers add up
        if current > maximum:
            current = maximum

        if current < 0:
            current = 0

        if maximum < 0:
            maximum = 0

        textBar = ""
        usage = int((current / maximum) * 38)
        for i in range(1, usage + 1):
            textBar += self.options.fsymbol
        textBar += self.options.msymbol
        for i in range(1, 39 - usage):
            textBar += self.options.esymbol

        # Check if the user set up graph color
        if "█" not in self.options.fsymbol:
            return f"[{textBar}]"
        return textBar


class VerticalBarChart(Chart):
    """
    Create vertical chart with user selected color and symbol
    """

    def draw_vertical_bar(self, capacity: int, used: int) -> str:
        """Draw a vertical bar chart"""
        textBar = "\n"
        n = (used / capacity) * 8
        # If the usage is below 1% print empty chart
        if n < 0.1:
            n = 0
        else:
            n = ceil(n)
        textBar += f"{self.options.esymbol * 9}  \n" * (8 - n)
        textBar += f"{self.options.fsymbol * 9}  \n" * n
        return textBar


if __name__ == "__main__":
    ch = HorizontalBarChart()
    ch.options.graph_color = 'cyan'
    ch.options.text_color = 'yellow'
    ch.options.header_color = 'red'
    ch.options.header_style = 'underlined'
    ch.chart(
        title="Test Content",
        maximum=100,
        current=32,
        pre_graph_text="Lorem: Sit ea dolore ad accusantium",
        post_graph_text="Good job!",
        footer="This concludes our test",
    )
