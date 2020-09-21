"""cli.py - Command line interface for vizex"""

import click

from disks import DiskUsage
from charts import Options
from colored import fg, attr, stylize

# Command line arguments for cli
@click.command()
@click.argument("chart", nargs=1, default="barh", metavar="[CHART_TYPE]")
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
    default=False,
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
    """ Displays charts in the terminal, graphically """
    chart = "barh"

    options: Options = Options()
    if mark:
        options.symbol = mark
    if header:
        options.header_color = header
    if text:
        options.text_color = text
    if graph:
        options.graph_color = graph

    chart = chart
    style = style
    exclude_list = list(exclude)

    renderer = None
    if chart == "barh":
        renderer = DiskUsage(
            path=path, exclude=exclude_list, details=details, every=every
        )

    renderer.print_charts(options)


if __name__ == "__main__":
    cli()
