"""cli.py - Command line interface for vizex"""

import click

from disks import DiskUsage
from tools import Color, Attr, Chart


# Command line arguments for vizex
@click.command()
@click.argument("chart", nargs=1, default=Chart.BARH, metavar="[CHART_TYPE]")
@click.option(
    "-P",
    "--path",
    default=None,
    multiple=True,
    help="Print only specific partition/disk",
)
@click.option(
    "-X",
    "--exclude",
    default=None,
    multiple=True,
    help="Select partition you want to exclude",
)
@click.option("--every", is_flag=True, help="Display information for all the disks")
@click.option(
    "--details",
    is_flag=True,
    help="Display additinal details like fstype and mountpoint",
)
@click.option(
    "-d",
    "--header",
    default=None,
    type=str,
    metavar="[COLOR]",
    help="Set the partition name color",
)
@click.option(
    "-s",
    "--style",
    default=None,
    type=str,
    metavar="[ATTR]",
    help="Change the style of the header's display",
)
@click.option(
    "-t",
    "--text",
    default=None,
    type=str,
    metavar="[COLOR]",
    help="Set the color of the regular text",
)
@click.option(
    "-g",
    "--graph",
    default=None,
    type=str,
    metavar="[COLOR]",
    help="Change the color of the bar graph",
)
@click.option(
    "-m", "--mark", default=None, help="Choose the symbols used for the graph"
)
def cli(chart, path, every, details, exclude, header, style, text, graph, mark):
    """** Displays Disk Usage in the terminal, graphically **

    Customize visual representation by setting colors and attributes

    Select one of the available graph types:

        barv : Vertical Bars
        *barh : Horizontal Bars (buggy)
        *pie : Pie Chart (coming soon)


    COLORS: light_red, red, dark_red, dark_blue, blue, cyan, yellow,
    green, neon, white, black, purple, pink, grey, beige, orange.

    ATTRIBUTES: bold, dim, underlined, blink, reverse, hidden.
    """

    chart = _check_chart(chart)
    graph_color = _check_color(graph)
    graph_symbol = mark
    header_color = _check_color(header) or Color.RED
    style = _check_attr(style) or Attr.BOLD
    text_color = _check_color(text)
    exclude_list = list(exclude)

    renderer = DiskUsage(
        chart=chart,
        path=path,
        header=header_color,
        details=details,
        symbol=graph_symbol,
        style=style,
        exclude=exclude_list,
        text=text_color,
        graph=graph_color,
        every=every,
    )

    renderer.main()


def _check_color(option: str) -> Color:
    """Checks if the string argument for color is in
    Color(Enum) list and returns enum for that selection

    args:
        option (str): user input for selected color
    rtype:
        Color: enum with a selected color
    """
    if option is None:
        return None

    # Build a dict of available colors so look ups are O(1) instead of O(n)
    if "colors" not in _check_color.__dict__:
        _check_color.colors = {}
        for name in Color.__members__.items():
            _check_color.colors[name[0].upper()] = name
    try:
        # This will fail with a KeyError if color does not exist
        return _check_color.colors[option.upper()][1]
    except:
        print(f'----- color {option} is not available')
        return None


def _check_attr(option: str) -> Attr:
    """Checks if the string argument for attribute is in
    Attr(Enum) list and returns enum for that selection

    args:
        option (str): user input for selected attribute
    rtype:
        Attr: enum with a selected attribute
    """
    if option is None:
        return None

    # Build a dict of available arrts so look ups are O(1) instead of O(n)
    if "attrs" not in _check_attr.__dict__:
        _check_attr.attrs = {}
        for name in Attr.__members__.items():
            _check_attr.attrs[name[0].upper()] = name
    try:
        # This will fail with a KeyError if attr does not exist
        return _check_attr.attrs[option.upper()][1]
    except:
        print(f'----- attribute {option} is not available')
        return None


def _check_chart(chart: str) -> Chart:
    """Checks what type of bar user wants to be displayed"""
    if isinstance(chart, str):
        chart = chart.lower()
    ret = None
    if chart in [Chart.BARH, "barh"]:
        ret = Chart.BARH
    elif chart in [Chart.BARV, "barv"]:
        ret = Chart.BARV
    elif chart in [Chart.PIE, "pie"]:
        ret = Chart.PIE
    else:
        raise NameError("Unsupported chart type!")
    return ret

if __name__ == "__main__":
    cli()
