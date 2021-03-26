from files import DirectoryFiles
from bstree import Node, BinarySearchTree

import os

if __name__ == '__main__':
    bst_files = DirectoryFiles.get_files(os.getcwd())
    DirectoryFiles.print_tree(bst_files)