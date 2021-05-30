# Class to collect and organize data about files and directories
import os
import sys
import magic
import concurrent.futures

from tabulate import tabulate
from colored import fg, stylize
from tools import bytes_to_human_readable, normalize_date, DecoratedData
from dataclasses import dataclass


@dataclass
class DirectoryFiles:
    """
    Creates the tabular listing of all the folders and files in a given path.
    This module can be seen as a substitute for du/df Linux terminal commands.
    """

    path: str = os.getcwd()
    show_hidden: bool = False
    sort_by: str = None
    desc: bool = False

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
                try:
                    total_size += os.path.getsize(fp)
                except FileNotFoundError:
                    # Could be a broken symlink or some other weirdness.
                    # Trap the error here so that the directory can continue
                    # to be successfully processed.
                    continue
        return total_size

    @classmethod
    def sort_data(cls, data: list, by: str, desc: bool) -> None:
        """
        Sorts data in place, which is inputted as a list, 
        based on a given index(key) and reverses if 
        user has selected descending order.

        Args:
            data: data with several columns
            by: key as a string to sort by
            desc: to sort in descending order
        """
        if by == 'name':
            column = 0
        elif by == 'dt':
            column = 1
        elif by == 'size':
            column = 2
        else:
            column = -1

        # Sort data inplace based on user's choice
        data.sort(key=lambda x: x[column], reverse=desc)

    @classmethod
    def _decorate_dir_entry(cls, entry) -> tuple:
        """
        Decorates given entry for a directory. Decorate means that creates 
        a colored representation of a name of the entry, grabs 
        the date it was last modified and size in bytes and decorates.
        collects everything and returns as a list.
        """

        # Gives orange color to the string & truncate to 32 chars
        name = entry.split('/')[-1]
        current = [stylize("■ " + name[:33] + "/", fg(202))]

        # Get date and convert in to a human readable format
        date = os.stat(entry).st_mtime
        current.append(
            DecoratedData(date, normalize_date('%h %d %Y %H:%M', date))
        )

        # recursively calculates the total size of a folder
        b = DirectoryFiles().get_dir_size(entry)
        current.append(
            DecoratedData(b, bytes_to_human_readable(b))
        )

        current.append('-')  # add directory type identifier
        return tuple(current)

    @classmethod
    def _decorate_file_entry(cls, entry) -> tuple:
        """
        Decorates given entry for a file. By decorate it means that creates
        a colored representation of a name of the entry, grabs 
        the date it was last modified and size in bytes and decorates,
        determines file type. collects everything and returns as a list.
        """

        # Gives yellow color to the string & truncate to 32 chars
        name = entry.split('/')[-1]
        current = [stylize("» " + name[:33], fg(226))]

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
            magic.from_file(entry, mime=True)
        )
        return tuple(current)

    def get_usage(self) -> list:
        """
        Collects the data for a given path like the name of a file/folder 
        and calculates its size if it's a directory, otherwise 
        just grabs a file size. If the current entry in a given 
        path is a file method evaluates its type. Finally, gives 
        us the date when the given file/folder was last modified.

        Program runs asynchronously using multiple threads or seperate processes

        Returns:
            list: which is a collection of each entry
                (files and folders) in a given path.
        """
        data = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            with os.scandir(self.path) as it:
                for entry in it:
                    try:
                        current = []

                        # Deal with hidden files and folders
                        if entry.name.startswith('.') and not self.show_hidden:
                            continue
                        elif entry.is_file():
                            current = executor.submit(
                                self._decorate_file_entry, entry.path)
                        elif entry.is_dir():
                            current = executor.submit(
                                self._decorate_dir_entry, entry.path)

                        # Add current list to the main list
                        data.append(current.result())
                    except Exception as e:
                        print(f"Bad Entry ::> {e}", file=sys.stderr)
                    except FileNotFoundError:
                        continue

        return data

    def print_tabulated_data(self) -> tabulate:
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
        if self.sort_by:
            self.sort_data(result, self.sort_by, self.desc)
        print(tabulate(result, headers, tablefmt="rst"))


if __name__ == '__main__':
    files = DirectoryFiles(sort_by='type', desc=True)
    files.print_tabulated_data()
