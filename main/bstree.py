from dataclasses import dataclass
from typing import TypeVar

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

    root: Node = None

    def contains(self, val: E) -> bool:
        """Check if this BTS contains given node"""
        return self.__contains(self.root, val)
    
    def __contains(self, p: Node, val: E) -> bool:
        if not p or not val:
            return False

        if p.value == val:
            return True
        elif p.value > val:
            return self.__contains(p.left, val)
        else:
            return self.__contains(p.right, val)

    def add(self, val: E) -> bool:
        """Add given node to the BTS"""
        if not self.root:
            self.root = Node(val)
            return True
        return self.__add(self.root, val)

    def __add(self, p: Node, val: E) -> bool:
        if not p or not val:
            return False

        if p.value == val:
            return False # ensure that the same value doesn't appear more than once
        elif p.value > val:
            if not p.left:
                p.left = Node(val)
                return True
            else:
                return self.__add(p.left, val)
        else:
            if not p.right:
                p.right = Node(val)
                return True
            else:
                return self.__add(p.right, val)

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
    
    def children(self, p: Node) -> list:
        """returns the list of children node"""
        children = []
        if p.left:
            children.append(p.left)
        if p.right:
            children.append(p.right)
        return children

    def find_node(self, val: E) -> Node:
        """Searchs for a node in a given tree"""
        return self.__find_node(self.root, val)

    def __find_node(self, p: Node, val: E) -> Node:
        if not p or not val:
            return None
    
        if p.value == val:
            return p

        if self.is_leaf(p):
            return None
        elif p.value < val:
            return self.__find_node(p.right, val) # continue checking right children
        else:
            return self.__find_node(p.left, val) # continue checking left children

    def depth(self, val: E) -> int:
        """Calcualtes the depth of a tree from a given node"""
        if not val or not self.contains(val):
            return -1
        return self.__depth(self.root, val)

    def __depth(self, p: Node, val: E) -> int:
        if not p or not val: return 0
        if p.value == val: return 0

        if p.value > val:
            return 1 + self.__depth(p.left, val)
        else:
            return 1 + self.__depth(p.right, val)

    def height(self, val: E) -> int:
        """Returns the height of a tree from a given node"""
        if not val or not self.root:
            return -1
        p = self.find_node(val)
        if not p: return -1
        return self.__height(p)

    def __height(self, p: Node) -> int:
        if not p: return -1
        hght = 0
        for c in self.children(p):
            hght = max(hght, 1 + self.__height(c))
        return hght



if __name__ == '__main__':
    righty = BinarySearchTree()
    righty.add(5)
    righty.add(3)
    righty.add(11)
    righty.add(7)
    righty.add(2)
    righty.add(1)
    var1 = self.tree.depth(2)