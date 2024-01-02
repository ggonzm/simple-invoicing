from __future__ import annotations

from typing import Optional, Self

# why we need Self and not just Node? Because Node is not a final class,
# and it's created with the aim of inheriting from it.
# See PEP673 and https://stackoverflow.com/questions/72174409/type-hinting-the-return-value-of-a-class-method-that-returns-self


class Node:
    def __init__(self, name: str, parent: Optional[Self] = None):
        self._name = name
        self._children: set[Self] = set()
        self._parent = parent
        if self._parent:
            self._parent._children.add(self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def root(self) -> Self:
        if not self._parent:
            return self
        else:
            return self._parent.root

    @property
    def parent(self) -> Optional[Self]:
        return self._parent

    @property
    def path(self) -> str:
        if self._parent:
            return self._parent.path + "." + self._name
        else:
            return self._name

    @property
    def leaves(self) -> set[Self]:
        """Returns a set of all the leaves of the tree rooted at this node"""
        if not self._children:
            return set([self])
        else:
            leaves = set()
            for child in self._children:
                leaves.update(child.leaves)
            return leaves

    def is_internal(self) -> bool:
        """Returns True if the node is not a leaf"""
        return bool(self._children)

    def delete(self) -> None:
        """Deletes the node and all its children"""
        if self._parent:
            self._parent._children.remove(self)
        children = list(self._children)
        for subcategory in children:
            self._children.remove(subcategory)
        del self

    def __iter__(self):
        return iter(self._children)

    def __contains__(self, item: Self) -> bool:
        return item in self._children

    def __eq__(self, other: object) -> bool:
        if not isinstance(
            other, Node
        ):  # tricky point. Self is for type annotation, but we need to check if other iherits from Node
            return False
        return self.path == other.path and self._children == other._children

    def __hash__(self) -> int:
        return hash(self.path)

    def __repr__(self) -> str:
        if self._parent:
            return f"{self.__class__.__name__}(name={self._name}, parent={self._parent.name}, children={len(self._children)})"
        else:
            return f"{self.__class__.__name__}(name={self._name}), children={len(self._children)})"

    def __str__(self, level=0):
        """Returns a string representation of the tree"""
        ret = "  " * level + "|---" * (level > 0) + self._name + "\n"
        for child in self._children:
            ret += child.__str__(level + 1)
        return ret
