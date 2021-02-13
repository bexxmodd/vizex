import os
import getpass
import shutil
import time
import magic

from tabulate import tabulate
from tools import bytes_to_human_readable
from colored import fg, bg, stylize, attr

class DirectorySize():
    """
    Creates the tabular listing of all the folders and files in a given path.
    This module can be seen as a substitute for a du/df linux terminal commands.
    """

    def __init__(self, path: str=None, ignore_hidden: bool=True,
                sort_by: str='type', desc: bool=False) -> None:
        path = os.getcwd()
        if path: self.path = path
        self.ignore_hidden = ignore_hidden
        self.sort_by = sort_by
        self.desc = desc

    def get_usage(self) -> list:
        """
        Collects the data for a given path like name of a file/folder 
         and calculates its size if it's a directory, otherwise 
         just grabs a file size. If the current entry in a given 
         path is a file method evaluates its type. Finally, gives 
         us the date when given file/folder was last modified.

        Returns:
            list: which is a collection of each entry
                  (files and folders) in a given path.
        """
        data = []
        with os.scandir(self.path) as it:
            for entry in it:
                try:
                    if self.ignore_hidden and entry.name.startswith('.'):
                        continue
                    current = []
                    entry_name = entry.name[:32] # Truncate the name string to 32 chars
                    size = 0
                    file_type = '-'

                    if entry.is_file():
                        size = os.stat(entry).st_size
                        # Evaluate the file type
                        file_type = magic.from_file(entry_name, mime=True)
                        # Gives yellow color to the string
                        entry_name = stylize("» " + entry_name, fg(226))
                    elif entry.is_dir():
                        # Gives orange color to the string
                        entry_name = stylize("■ " + entry_name + "/", fg(202))
                        # Calculates the total size of a given folder recursivly
                        size = self._get_size(entry)
                    
                    # Convert last modified time (which is in nanoseconds)
                    #  in to a human readable time
                    dt = time.strftime(
                            '%h %d %Y %H:%M',
                            time.localtime(os.stat(entry).st_mtime))

                    # Append all the collected data of a current entry
                    current.append(entry_name)
                    current.append(dt)
                    current.append(bytes_to_human_readable(size))
                    current.append(file_type[:24])
                    # Add current list to the main list
                    data.append(current)
                except FileNotFoundError:
                    continue
        return data     

    def _get_size(self, start_path: str) -> int:
        """
        Calculates the cumulative size of a given directory in bytes

        Args:
            start_path (str): path to the folder who's
            cumulative file size is calulated.

        Returns:
            int: size of all files in a given path
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def sort_data(self) -> list:
        """
        Sorts data, which is inputed as a list, 
        based on given index(key) and reverses if 
        user has selected descending ordering.

        Returns:
            list: sorted based on given arg as key
        """
        key = -1
        if self.sort_by == '-n': key = 0
        elif self.sort_by == '-dt': key = 1
        elif self.sort_by == '-z': key = 2

        # Sort and return data based on user's choice
        return sorted(self.get_usage(), 
                    key=lambda x: (x[key], x[0]),
                    reverse=self.desc)

    def tabulate_disk(self) -> tabulate:
        """
        Creates the tabular representation of the data.
        Adds headers and sorts list's data as rows.

        Returns:
            tabulate: tabulated form of the current 
                      directory's folders and files.
        """
        headers = [
            'name ' + stylize('-n', attr("blink")),
            'last modified ' + stylize('-dt', attr("blink")), 
            'size ' + stylize('-z', attr("blink")),
            'type ' + stylize('-t', attr("blink"))
        ]
        result = self.sort_data()
        return tabulate(result, headers, tablefmt="rst")

    def print_tables(self) -> None:
        """Prints tabular data in the terminal"""
        print(self.tabulate_disk())
        print(" - sort by blinking arguments above or sort in descending order with -desc")


if __name__ == '__main__':
    files = DirectorySize()
    files.print_tables()