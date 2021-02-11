import os
import getpass
import shutil
    """Use Dict to store .file type and explanation of what kind of file it is
    """

def disk_usage(path: str="/home/bexx/Projects") -> None:
    """Returns the size of the folders and files in a given path"""
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                print(f'{entry.name} which is a {entry.name.split(".")[-1]}')
            if total == 50: return
            total += 1
        
            

if __name__ == '__main__':
    print(disk_usage())