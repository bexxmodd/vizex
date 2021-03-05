# Class to collect and organize data about files and directories

import os
import getpass
import time
import magic

from tabulate import tabulate
from colored import fg, bg, stylize, attr
from tools import DecoratedData, bytes_to_human_readable,  normalize_date

class DirectoryFiles():
    """
    Creates the tabular listing of all the folders and files in a given path.
    This module can be seen as a substitute for du/df Linux terminal commands.

    Args:
        path (str): to the file or directory
        shoiw_hidden (bool): if program'd show hidden files and folders
        sort_by (str): at which column folders and files should be sorted
        desc (bool): if the sorting should be descending or ascending
    """

    def __init__(self, dpath: str=None, show_hidden: bool=False,
                sort_by: str='type', desc: bool=False) -> None:
        # Path is the current working directory if not stated otherwise
        self.path = os.getcwd()
        if dpath: self.path = dpath
        self.show_hidden = show_hidden
        self.sort_by = sort_by
        self.desc = desc

    @staticmethod
    def get_dir_size(start_path: str) -> int:
        """
        Calculates the cumulative size of a given directory.

        Args:
            start_path (str): a path to the folder that's
                    the cumulative file size is calculated.

        Returns:
            int: the size of all files in a given path in bytes
        """
        total_size = 0
        for dirpath, _, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    @classmethod
    def sort_data(cls, data: list, by: str, desc: bool) -> None:
        """
        Sorts data in place, which is inputted as a list, 
        based on a given index(key) and reverses if 
        user has selected descending order.

        Args:
            list: data with several columns
            by: key as a string to sort by
            desc: to sort in descending order
        """
        if by == 'name': column = 0
        elif by == 'dt': column = 1
        elif by == 'size': column = 2
        else: column = -1

        # Sort data inplace based on user's choice
        data.sort(key=lambda x: (x[column], x[-1]), reverse=desc)

    @classmethod
    def _decorate_dir_entry(cls, entry) -> tuple:
        """
        Decorates given entry for a directory. Decorate means that creates 
        a colored representation of a name of the entry, grabs 
        the date it was last modified and size in bytes and decorates.
        collects everything and returns as a list.
        """
        current = []

        # Gives orange color to the string & truncate to 32 chars
        current.append(
            stylize("■ " + entry.name[:33] + "/", fg(202))
        )

        # Get date and convert in to a human readable format
        date = os.stat(entry).st_mtime
        current.append(
            DecoratedData(date, normalize_date('%h %d %Y %H:%M', date))
        ) 

        # recursivly calculates the total size of a folder
        b = DirectoryFiles().get_dir_size(entry)
        current.append(
            DecoratedData(b, bytes_to_human_readable(b))
        )
        
        current.append('-') # Append type 
        return tuple(current)

    @classmethod
    def _decorate_file_entry(cls, entry) -> tuple:
        """
        Decorates given entryfor a file. By decorate it means that creates 
        a colored representation of a name of the entry, grabs 
        the date it was last modified and size in bytes and decorates,
        determins file type. collects everything and returns as a list.
        """
        current = []

        # Gives yellow color to the string & truncate to 32 chars
        current.append(
            stylize("» " + entry.name[:33], fg(226))
        )

        # Convert last modified time (which is in nanoseconds)
        date = os.stat(entry).st_mtime
        current.append(
            DecoratedData(date, normalize_date('%h %d %Y %H:%M', date))
        ) 

        b = os.stat(entry).st_size
        current.append(
            DecoratedData(b, bytes_to_human_readable(b))
        )

        # Evaluate the file type
        current.append(
            magic.from_file(entry.path, mime=True)
        )
        return tuple(current)


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

                    # Deal with hidden files and folders
                    if entry.name.startswith('.') and not self.show_hidden:
                        continue
                    elif entry.is_file():
                        current = self._decorate_file_entry(entry)
                    elif entry.is_dir():
                        current = self._decorate_dir_entry(entry)

                    # Add current list to the main list
                    if len(current) == 4:
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
    files = DirectoryFiles(sort_by='type', desc=True)
    files.print_tables()