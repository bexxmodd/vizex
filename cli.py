import click
from disk import Color, Attr, DiskUsage

@click.command()
@click.option('-d', '--header', default=None, type=str, metavar='[COLOR]',
                help='Set the partition name color')
@click.option('-s', '--style', default=None, type=str, metavar='[ATTR]',
                help='Change the style of the header\'s display')
@click.option('-t', '--text', default=None, type=str, metavar='[COLOR]',
                help='Set the color of the regular text')
@click.option('-g', '--graph', default=None, type=str, metavar='[COLOR]',
                help='Change the color of the bar graph')
def cli(header, style, text, graph):
    """** Displayes Disk Space, File & Folder size, User Theme, graphically **

    Customize visual representation by setting colors and attributes

    COLORS: Light_red, Red, Dark_red, Dark_blue, Blue, Cyan, Yellow,
    Green, Neon, White, Black, Purple, Pink, Grey, Beige, Orage.
    
    ATTRIBUTES: Bold, Dim, Underlined, Blink, Reverse, Hidden.
    """
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
    du = DiskUsage(header=d, style=s)
    if t and g:
        du = DiskUsage(header=d, style=s, text=t, graph=g)
    elif t:
        du = DiskUsage(header=d, style=s, text=t)
    elif g:
        du = DiskUsage(header=d, style=s, graph=g)
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