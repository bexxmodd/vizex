"""cli.py - Command line interface for vizex"""

import click

from disks import DiskUsage
from battery import Battery
from charts import Options
from cpu import CPUFreq
from colored import fg, attr, stylize


# Command line arguments and options for cli
@click.command()
@click.argument('arg', default='disk')
@click.option(
    "--save",
    help="Save your disk usage data into a csv file:" \
        + "Takes a full path with a file name as an argument"
)
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
@click.option(
    "--every",
    is_flag=True,
    help="Display information for all the disks"
)
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
    "-m",
    "--mark",
    default=None,
    help="Choose the symbols used for the graph"
)
def cli(arg, save, path, every,
        details, exclude, header, style,
        text, graph, mark) -> None:
    """
    ** Displays Disk Usage in the terminal, graphically. **

    Customize visuals by setting colors and attributes.

    COLORS: light_red, red, dark_red, dark_blue, blue,
        cyan, yellow, green, pink, white, black, purple,
        neon, grey, beige, orange, magenta, peach.

    ATTRIBUTES: bold, dim, underlined, blink, reverse.
    """


    options: Options = Options()
    if mark:
        options.symbol = mark
    if header:
        options.header_color = header
    if text:
        options.text_color = text
    if graph:
        options.graph_color = graph
    if style:
        options.header_style = style

    exclude_list = list(exclude)

    if arg == 'battery':
        try:
            battery = Battery()
            battery.print_charts()
        except:
            print('Battery not found!')
    elif arg == 'cpu':
        cpus = CPUFreq()
        cpus.display_separately()
    else:
        # renderer = None
        renderer = DiskUsage(
            path=path, exclude=exclude_list, details=details, every=every
        )
        if save:
            renderer.save_data(save)
        renderer.print_charts(options)


if __name__ == "__main__":
    cli()
