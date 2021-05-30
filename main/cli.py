# Command line interface for VIZEX and VIZEXdf

import click
import sys

from disks import DiskUsage
from files import DirectoryFiles
from battery import Battery
from charts import Options
from cpu import CPUFreq
from tools import append_to_bash
from viztree import construct_tree


# ----- vizexdf options and arguments -----
@click.version_option('2.0.4', message='%(prog)s version %(version)s')
@click.command(options_metavar='[options]')
@click.argument(
    'path',
    type=click.Path(exists=True),
    default='.',
    metavar='[path]'
)
@click.option(
    '-t', '--tree',
    nargs=1,
    type=int,
    help='Print the directory list tree'
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
    help='Store customized terminal command for vizexdf as an alias so you don\'t have to repeat the line everytime.'
         + '<-l> should always be the last command in the line'
)
def dirs_files(tree: int, sort: str, all: str,
               desc: str, path: str, alias: str) -> None:
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

If you just want to print the directory tree run vizexdf with --tree/-tree and supply
the level of how many child directory/files you want to be printed.

    Example: vizexdf -tree=2

This will sort in descending order by name and show all the hidden files and folders.
!Just make sure 's' is placed at the end of the options chain!
    """
    if alias:  # Set vizexdf as alias
        line = 'vizexdf ' + ' '.join(sys.argv[1:-1])
        append_to_bash('vizexdf', line)

    if tree:
        construct_tree(dir_path=path, level=tree)
        return

    show = all
    desc_sort = desc
    sort_by = sort
    dirpath = path



    # Execute vizexdf
    dir_files = DirectoryFiles(path=dirpath, sort_by=sort_by,
                               show_hidden=show, desc=desc_sort)
    dir_files.print_tabulated_data()


# ----- vizex options and arguments -----
@click.version_option('2.0.4', message='%(prog)s version %(version)s')
@click.command(options_metavar='[options]')
@click.argument('arg',
                default='disk',
                metavar='command')
@click.option(
    "--save",
    help="Export your disk usage data into a CSV or JSON file:"
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
    help='Store customized terminal command for vizexdf as an alias so you don\'t have to repeat the line everytime.'
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
        cpus.display_separately()
    else:
        renderer = DiskUsage(
            path=path, exclude=exclude_list, details=details, every=every
        )
        if save:
            renderer.save_data(save)
        renderer.print_charts(options)


if __name__ == "__main__":
    dirs_files()
