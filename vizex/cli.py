# Command line interface for VIZEX ,VIZEXdf and VIZEXtree

import click
import sys

from tools import append_to_bash
from vizexdu.disks import DiskUsage
from vizexdu.battery import Battery
from vizexdu.charts import Options
from vizexdu.cpu import CPUFreq
from vizexdf.files import DirectoryFiles
from vizextree.viztree import construct_tree


# ----- vizextree options and arguments -----
@click.version_option('2.1.1', message='%(prog)s version %(version)s')
@click.command(options_metavar='[options]')
@click.argument(
    'path',
    type=click.Path(exists=True),
    default='.',
    metavar='[path]'
)
@click.option(
    'level', '-l',
    type=int,
    default=3,
    help="How many levels of Directory Tree to be printed (By Default it's 3)"
)
def print_tree(path: str, level: int) -> None:
    """
\b

__   _(_)_________  _| |_ _ __ ___  ___
\ \ / / |_  / _ \ \/ / __| '__/ _ \/ _ \
 \ V /| |/ /  __/>  <| |_| | |  __/  __/
  \_/ |_/___\___/_/\_\\__|_|  \___|\___|

    Made by: Beka Modebadze


    If you want to print the directory tree run vizextree -path -level
    the level of how many child directory/files you want to be printed.

    Example:

        vizextree -l 2

    This'll print a directory tree of current working directory for two levels
    """
    construct_tree(path, level)


# ----- vizexdf options and arguments -----
@click.version_option('2.1.1', message='%(prog)s version %(version)s')
@click.command(options_metavar='[options]')
@click.argument(
    'path',
    type=click.Path(exists=True),
    default='.',
    metavar='[path]'
)
@click.option(
    '-s', '--sort',
    type=click.Choice(['type', 'size', 'name', 'dt']),
    default=None,
    help='Sort table with one of four given columns'
)
@click.option(
    '-a', '--all',
    is_flag=True,
    help='Include hidden files and folders'
)
@click.option(
    '-d', '--desc',
    is_flag=True,
    help='Sort columns in descending order')
@click.option(
    '-l', '--alias',
    is_flag=True,
    help='Store customized terminal command for vizexdf as an alias so '
    + 'you don\'t have to repeat the line everytime.'
    + '<-l> should always be the last command in the line'
)
def dirs_files(sort: str, all: str, desc: str, path: str, alias: str) -> None:
    """
\b
██╗   ██╗██╗███████╗███████╗██╗  ██╗     _  __
██║   ██║██║╚══███╔╝██╔════╝╚██╗██╔╝  __| |/ _|
██║   ██║██║  ███╔╝ █████╗   ╚███╔╝  / _` | |_
╚██╗ ██╔╝██║ ███╔╝  ██╔══╝   ██╔██╗ | (_| |  _|
 ╚████╔╝ ██║███████╗███████╗██╔╝ ██╗ \__,_|_|
  ╚═══╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
    Made by: Beka Modebadze

The command-line program `vizexdf` is a branch of the `vizex` that
displays directories and files information in a tabular form.

`vizexdf` Prints data of current working path in a tabular form.
You can pass a path for a specific directory you want to print.

    Example: vizexdf /home/bexx/test

You can also chain options for --all --desc --sort.

    Example: vizexdf -ads name

Here `vizexdf` will print 'all' (-a) files and directories
and 'sort' (-s) them by 'name' in 'descending' (-d) order.


This'll sort in descending order by name and show all the hidden files & folders.
!Just make sure 's' is placed at the end of the options chain!
    """
    if alias:  # Set vizexdf as alias
        line = 'vizexdf ' + ' '.join(sys.argv[1:-1])
        append_to_bash('vizexdf', line)

    show = all
    desc_sort = desc
    sort_by = sort
    dirpath = path

    # Execute vizexdf
    dir_files = DirectoryFiles(path=dirpath, sort_by=sort_by,
                               show_hidden=show, desc=desc_sort)
    dir_files.print_tabulated_data()


# ----- vizex options and arguments -----
@click.version_option('2.1.1', message='%(prog)s version %(version)s')
@click.command(options_metavar='[options]')
@click.argument('arg',
                default='disk',
                metavar='command')
@click.option(
    "--save",
    help="Export your disk/cpu usage data into a CSV or JSON file:"
    + "Takes a full path with a file name as an argument. "
    + "File type will be defined based on a <.type> of the filename"
)
@click.option(
    "-P",
    "--path",
    default=None,
    multiple=True,
    help="Print directory for a provided path."
    + " It can be both, full and relative path",
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
@click.option(
    '-l', '--alias',
    is_flag=True,
    help='Store customized terminal command for vizexdf as an alias so you'
    + ' don\'t have to repeat the line everytime.'
    + '<-l> should always be the last command in the line'
)
def disk_usage(arg, save, path, every,
               details, exclude, header, style,
               text, graph, mark, alias) -> None:
    """
\b
██╗   ██╗██╗███████╗███████╗██╗  ██╗
██║   ██║██║╚══███╔╝██╔════╝╚██╗██╔╝
██║   ██║██║  ███╔╝ █████╗   ╚███╔╝
╚██╗ ██╔╝██║ ███╔╝  ██╔══╝   ██╔██╗
 ╚████╔╝ ██║███████╗███████╗██╔╝ ██╗
  ╚═══╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
    Made by: Beka Modebadze

<< Customize and display Disk Usage in the terminal >>

\b
COLORS: light_red, red, dark_red, dark_blue, blue,
    cyan, yellow, green, pink, white, black, purple,
    neon, grey, beige, orange, magenta, peach.

\b
ATTRIBUTES: bold, dim, underlined, blink, reverse.

\b
You can also give *args like [BATTERY] and [CPU]

\b
battery --> will display the battery information if found.
cpu --> will visualize the usage of each CPU in live time *(beta mode)
    """
    if alias:  # Set vizex as alias
        line = 'vizex ' + ' '.join(sys.argv[1:-1])
        append_to_bash('vizex', line)

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
        except Exception:
            print('Battery not found!')
    elif arg == 'cpu':
        cpus = CPUFreq()
        cpus.display_separately(filename=save)
    else:
        renderer = DiskUsage(
            path=path, exclude=exclude_list, details=details, every=every
        )
        if save:
            renderer.save_data(save)
        renderer.print_charts(options)


if __name__ == "__main__":
    print_tree()
