from dataclasses import dataclass
from typing import TypeVar, Generic

E = TypeVar('E')

@dataclass
class Node:

    value: E = None
    left: 'Node' = None
    right: 'Node' = None

    def __eq__(self, other: 'Node') -> bool:
        if isinstance(other, Node):
            return self.value == other.value \
                and self.left == other.left \
                and self.right == right

@dataclass
class BinarySearchTree:

    root: E = None

    def contains(self, val: E) -> bool:
        """Check if this BTS contains given node"""
        return self.__contains(root, val)
    
    def __contains(self, p: Node, val: E) -> bool:
        if p.value == val:
            return True
        elif p.value > val:
            return self.__contains(p.left, val)
        else:
            return self.__contains(p.right, val)

    def add(self, val: E) -> bool:
        """Add given node to the BTS"""
        if not self.root:
            self.root = BinarySearchTree(val)
            return True
        return self.__add(self.root, val)

    def __add(self, p: Node, val: E) -> bool:
        if not p or not val:
            return False

        if p.value == val:
            return False # ensure that the same value doesn't appear more than once
        elif p.value > val:
            if not n.left:
                p.left = BinarySearchTree(val)
                return True
            else:
                return self.__add(p.left, val)
        else:
            if not p.right:
                p.right = BinarySearchTree(val)
                return True
            else:
                return self.__add(n.right, val)

    def remove(self, val: E) -> bool:
        """Removes node from a tree"""
        return self.__remove(self.root, None, val)

    def __remove(self, p: Node, parent: Node, val: E) -> bool:
        if not p:
            return False

        if p.value > val:
            return self.__remove(p.left, p, val)
        elif p.value < val:
            return self.__remove(p.right, p, val)
        else:
            if p.left and p.right:
                p.value = self.max_value(p.left)
                self.__remove(p.left, p, p.value)

    def _max_value(self, p: Node) -> E:
        """returns the max value of a node"""
        if not p.right:
            return p.value
        return self._max_value(p.right)

    def is_leaf(self, p: Node) -> bool:
        """Checks if a node is a leaf e.i. has no children"""
        return not p.left and not p.right
    
    def get_children(self, p: Node) -> list:
        """returns the list of children node"""
        children = []
        if p.left:
            children.append(p.left)
        if p.right:
            children.append(p.right)
        return children


if __name__ == '__main__':
    n = Node("First")
    bts = BinarySearchTree(n)
    bts.add('Second')
    children = bts.get_children(n)
    print(children)    
    print(bts)