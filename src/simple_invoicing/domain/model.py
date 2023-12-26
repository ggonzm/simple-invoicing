from __future__ import annotations
from typing import Optional


class Category:

    def __init__(self, name: str, parent: Optional[Category] = None):
        self._name = name.upper()
        self._subcategories = dict()
        self._parent = parent
        if self._parent:
            self._parent._subcategories[self._name] = self

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> Optional[Category]:
        return self._parent
    
    def get_root(self) -> Category:
        if not self._parent:
            return self
        else:
            return self._parent.get_root()
        
    
    def get_leaves(self) -> set[Category]:
        if not self._subcategories:
            return set([self])
        else:
            leaves = set()
            for subcategory in self._subcategories.values():
                leaves.update(subcategory.get_leaves())
            return leaves
        
    
    def delete(self) -> None:
        if self._parent:
            del self._parent._subcategories[self._name]
        subcategory_names = list(self._subcategories.keys())
        for name in subcategory_names:
            del self._subcategories[name]
        del self


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Category):
            return False
        return self._name == other._name and self._parent == other._parent and self._subcategories == other._subcategories

    def __hash__(self) -> int:
        if self._parent:
            return hash(self._parent.name+'.'+self._name)
        else:
            return hash(self._name)

    def __repr__(self) -> str:
        if self._parent:
            return f"Category(name={self._name}, parent={self._parent.name})"
        else:
            return f"Category(name={self._name})"

    def __str__(self, level=0):
        """Returns a string representation of the tree"""
        ret = "  " * level + "|---" * (level > 0) + self._name + "\n"
        for _, child in self._subcategories.items():
            ret += child.__str__(level + 1)
        return ret
