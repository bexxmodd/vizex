import click
import ast
from disk import Color, Attr, DiskUsage, Chart


@click.command()
@click.argument('chart', nargs=1, default=Chart.BARH,
                metavar='[CHART_TYPE]')
@click.option('-I', '--exclude', default=None, multiple=True,
                help='Select partition you want to exclude')
@click.option('-d', '--header', default=None, type=str, metavar='[COLOR]',
                help='Set the partition name color')
@click.option('-s', '--style', default=None, type=str, metavar='[ATTR]',
                help='Change the style of the header\'s display')
@click.option('-t', '--text', default=None, type=str, metavar='[COLOR]',
                help='Set the color of the regular text')
@click.option('-g', '--graph', default=None, type=str, metavar='[COLOR]',
                help='Change the color of the bar graph')
def cli(chart, exclude, header, style, text, graph):
    """** Displayes Disk Usage in the terminal, graphically **

    Customize visual representation by setting colors and attributes

    Select one of the available graph types:

        barv : Vertical Bars
        barh : Horizontal Bars
        pie : Pie Chart


    COLORS: light_red, red, dark_red, dark_blue, blue, cyan, yellow,
    green, neon, white, black, purple, pink, grey, beige, orage.
    
    ATTRIBUTES: bold, dim, underlined, blink, reverse, hidden.
    """
    ch = None
    if chart == Chart.BARH or chart == 'barh':
        ch = Chart.BARH
    elif chart.lower() == 'barv':
        ch = Chart.BARV
    elif chart.lower() == 'pie':
        ch = Chart.PIE
    ex = exclude
    d = Color.RED
    s = Attr.BOLD
    t = None
    g = None
    if check_color(header):
        d = check_color(header)
    if check_attr(style):
        s = check_attr(style)
    if check_color(text):
        t = check_color(text)
    if check_color(graph):
        g = check_color(graph)
    du = DiskUsage(chart=ch, header=d, style=s, exclude=ex)
    if t and g:
        du = DiskUsage(
            chart=ch, header=d, style=s, exclude=ex, text=t, graph=g)
    elif t:
        du = DiskUsage(
            chart=ch, header=d, style=s, exclude=ex, text=t)
    elif g:
        du = DiskUsage(
            chart=ch, header=d, style=s, exclude=ex, graph=g)
    du.main()

def check_color(option: str) -> Color:
    """Checks if the string argument for color is in
    Color(Enum) list and returns enum for that selection
    
    args:
        option (str): user input for selected color
    rtype:
        Color: enum with a selected color
    """
    if option == None:
        return
    for name in Color.__members__.items():
        if option.upper() == name[0]:
            return name[1]

def check_attr(option: str) -> Attr:
    """Checks if the string argument for attribute is in
    Attr(Enum) list and returns enum for that selection
    
    args:
        option (str): user input for selected attribute
    rtype:
        Attr: enum with a selected attribute
    """
    if option == None:
        return
    for name in Attr.__members__.items():
        if option.upper() == name[0]:
            return name[1]


if __name__ == '__main__':
    cli()