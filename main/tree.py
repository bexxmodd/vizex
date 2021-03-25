from dataclasses import dataclasses
from typing import TypeVar, Generic

E = TypeVar('E')

@dataclasses
class Node:
    value: E
    left: Node = None;
    right: Node = None;

    def __eq__(self, other: Node):
        if isinstance(other, Node):
            return self.value == other.value \
                and self.left == other.left \
                and self.right == right