import os
import getpass
import time
import magic

from tools import DecoratedData
from tabulate import tabulate
from tools import bytes_to_human_readable
from colored import fg, bg, stylize, attr

class DirectoryFiles():
    """
    Creates the tabular listing of all the folders and files in a given path.
    This module can be seen as a substitute for du/df Linux terminal commands.
    """

    def __init__(self, dpath: str=None, show_hidden: bool=False,
                sort_by: str='type', desc: bool=False) -> None:
        self.path = os.getcwd()
        if dpath: self.path = dpath
        self.show_hidden = show_hidden
        self.sort_by = sort_by
        self.desc = desc

    @staticmethod
    def _get_size(start_path: str) -> int:
        """
        Calculates the cumulative size of a given directory.

        Args:
            start_path (str): a path to the folder that's
                    the cumulative file size is calculated.

        Returns:
            int: the size of all files in a given path in bytes
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    @staticmethod
    def sort_data(data: list, by: str, desc: bool) -> None:
        """
        Sorts data in place, which is inputted as a list, 
        based on a given index(key) and reverses if 
        user has selected descending order.

        Args:
            list: data with several columns
            by: key as a string to sort by
            desc: to sort in descending order
        """
        key = -1
        if by == 'name': key = 0
        elif by == 'dt': key = 1
        elif by == 'dt': key = 2

        # Sort and return data based on user's choice
        data.sort(key=lambda x: (x[key], x[-1]), reverse=desc)

    def get_usage(self) -> list:
        """
        Collects the data for a given path like the name of a file/folder 
         and calculates its size if it's a directory, otherwise 
         just grabs a file size. If the current entry in a given 
         path is a file method evaluates its type. Finally, gives 
         us the date when the given file/folder was last modified.

        Returns:
            list: which is a collection of each entry
                (files and folders) in a given path.
        """
        data = []
        with os.scandir(self.path) as it:
            for entry in it:
                try:
                    current = []
                    entry_name = entry.name[:33] # Truncate the name string to 32 chars
                    size = 0
                    file_type = '-'

                    # Deal with hidden files and folders
                    if entry.name.startswith('.') and not self.show_hidden:
                        continue

                    if entry.is_file():
                        b = os.stat(entry).st_size
                        size = DecoratedData(b, bytes_to_human_readable(b))
                        # Evaluate the file type
                        file_type = magic.from_file(
                            self.path + "/" + entry_name, mime=True)
                        # Gives yellow color to the string
                        entry_name = stylize("» " + entry_name, fg(226))
                    elif entry.is_dir():
                        # Gives orange color to the string
                        entry_name = stylize("■ " + entry_name + "/", fg(202))
                        # recursivly calculates the total size of a folder 
                        b = DirectoryFiles()._get_size(entry)
                        size = DecoratedData(b, bytes_to_human_readable(b))
                    
                    # Convert last modified time (which is in nanoseconds)
                    #  in to a human readable format
                    raw_dt = os.stat(entry).st_mtime
                    dt = DecoratedData(raw_dt, time.strftime(
                            '%h %d %Y %H:%M',
                            time.localtime(raw_dt)))

                    # Append all the collected data of a current entry
                    current.append(entry_name)
                    current.append(dt)
                    current.append(size)
                    current.append(file_type[:26])

                    # Add current list to the main list
                    data.append(current)
                except FileNotFoundError:
                    continue
        return data

    def tabulate_disk(self) -> tabulate:
        """
        Creates the tabular representation of the data.
        Adds headers and sorts the list's data as rows.

        Returns:
            tabulate: a tabulated form of the current 
                    the directory's folders and files.
        """
        headers = [
            'name',
            'last modified (dt)', 
            'size',
            'type'
        ]
        result = self.get_usage()
        self.sort_data(result, self.sort_by, self.desc)
        return tabulate(result, headers, tablefmt="rst")

    def print_tables(self) -> None:
        """Prints tabular data in the terminal"""
        print(self.tabulate_disk())


if __name__ == '__main__':
    files = DirectoryFiles(sort_by='dt')
    files.print_tables()