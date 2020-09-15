import click
import ast
from tools import Color, Attr, Chart
from disks import DiskUsage


@click.command()
@click.argument('chart', nargs=1, default=Chart.BARH,
                metavar='[CHART_TYPE]')
@click.option('-P', '--path', default=None, multiple=True,
                help='Print only specific partition/disk')
@click.option('-X', '--exclude', default=None, multiple=True,
                help='Select partition you want to exclude')
@click.option('--every', is_flag=True,
                help='Display information for all the (virtual and physical disks')
@click.option('--details', is_flag=True,
                help='Display additinal details like fstype and mountpoint')
@click.option('-d', '--header', default=None, type=str, metavar='[COLOR]',
                help='Set the partition name color')
@click.option('-s', '--style', default=None, type=str, metavar='[ATTR]',
                help='Change the style of the header\'s display')
@click.option('-t', '--text', default=None, type=str, metavar='[COLOR]',
                help='Set the color of the regular text')
@click.option('-g', '--graph', default=None, type=str, metavar='[COLOR]',
                help='Change the color of the bar graph')
@click.option('-m', '--mark', default=None,
                help='Choose the symbols used for the graph')
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
    ch = check_chart(chart)
    if path:
        p = path
    else:
        p = None
    if every:
        e = True
    else:
        e = False
    if details:
        dets = True
    else:
        dets = False
    x = list(exclude)
    d = Color.RED
    s = Attr.BOLD
    t = None
    g = None
    m = mark
    if _check_color(header):
        d = _check_color(header)
    if check_attr(style):
        s = check_attr(style)
    if _check_color(text):
        t = _check_color(text)
    if _check_color(graph):
        g = _check_color(graph)
    du = DiskUsage(chart=ch, path=p, details=dets, header=d,
            symbol = m, style=s, exclude=x, every=e)
    if t and g:
        du = DiskUsage(
            chart=ch, path=p, header=d, details=dets, symbol=m,
                style=s, exclude=x, text=t, graph=g, every=e)
    elif t:
        du = DiskUsage(
            chart=ch, path=p, header=d, details=dets, style=s,
                symbol=m, exclude=x, text=t, every=e)
    elif g:
        du = DiskUsage(
            chart=ch, path=p, header=d, details=dets, style=s,
                symbol=m, exclude=x, graph=g, every=e)
    du.main()

def _check_color(option: str) -> Color:
def check_color(option: str) -> Color:
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
    if "colors" not in check_color.__dict__:
        check_color.colors = {}
        for name in Color.__members__.items():
            check_color.colors[name[0].upper()] = name
    try:
        # This will fail with a KeyError if color does not exist
        return check_color.colors[option.upper()][1]
    except KeyError:
        return None


def check_attr(option: str) -> Attr:
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
    if "attrs" not in check_attr.__dict__:
        check_attr.attrs = {}
        for name in Attr.__members__.items():
            check_attr.attrs[name.upper()] = name
    try:
        # This will fail with a KeyError if attr does not exist
        return check_attr.attrs[option.upper()][1]
    except KeyError:
        return None


def check_chart(chart: str) -> Chart:
    """Checks what type of bar user wants to be displayed"""
    if chart == Chart.BARH or chart == "barh":
        return Chart.BARH
    elif chart.lower() == "barv":
        return Chart.BARV
    elif chart.lower() == "pie":
        return Chart.PIE
    else:
        raise NameError("Unsupported chart type!")


if __name__ == '__main__':
    cli()