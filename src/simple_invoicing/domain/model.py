from __future__ import annotations


class Category:
    _instances = {}

    def __new__(cls, name: str, *args, **kwargs) -> Category:
        if name in cls._instances:
            return cls._instances[name]
        else:
            instance = super().__new__(cls)
            cls._instances[name] = instance
            return instance

    def __init__(self, name: str):
        self._name = name
        if not hasattr(self, "_subcategories"):
            self._subcategories = dict()

    @property
    def name(self) -> str:
        return self._name

    def add_subcategories(self, *subcategories: Category) -> None:
        for subcategory in subcategories:
            self._subcategories[subcategory.name] = subcategory

    def get_leaves(self) -> list[Category]:
        if not self._subcategories:
            return [self]
        else:
            leaves = []
            for subcategory in self._subcategories.values():
                leaves.extend(subcategory.get_leaves())
            return leaves

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Category):
            return False
        return self._name == other._name and self._subcategories == other._subcategories

    def __hash__(self) -> int:
        return hash(self._name)

    def __repr__(self) -> str:
        return f"Category(name={self._name})"

    def __str__(self, level=0):
        """Returns a string representation of the tree"""
        ret = "\t" * level + "|---" * (level > 0) + repr(self) + "\n"
        for _, child in self._subcategories.items():
            ret += child.__str__(level + 1)
        return ret
