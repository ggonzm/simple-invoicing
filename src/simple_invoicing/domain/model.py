from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Self

from src.simple_invoicing.domain.TreeStruct import Node

class RootstockError(Exception):
    pass

class Family:
    def __init__(self, name:str, sci_name:str) -> None:
        self._name = name
        self.sci_name = sci_name
        self._fruit_trees: set[FruitTree] = set()
        self._rootstocks: set[Rootstock] = set([Rootstock("FRANCO")])

    @property
    def name(self) -> str:
        return self._name

    @property
    def fruit_trees(self) -> frozenset[FruitTree]:
        return frozenset(self._fruit_trees)
    
    @property
    def rootstocks(self) -> frozenset[Rootstock]:
        return frozenset(self._rootstocks)
    
    def add(self, item: FruitTree | Rootstock) -> None:
        if isinstance(item, FruitTree):
            if item.rootstock not in self._rootstocks:
                raise RootstockError(f"{item.rootstock} is not defined in the family {self.name}")
            self._fruit_trees.add(item)
        else:
            self._rootstocks.add(item)
    
    def remove(self, item: FruitTree | Rootstock) -> None:
        if isinstance(item, FruitTree):
            self._fruit_trees.remove(item)
        else:
            self._rootstocks.remove(item)
            self._remove_fruit_trees_with_rootstock(item)
    
    def _remove_fruit_trees_with_rootstock(self, rootstock: Rootstock) -> None:
        to_remove = set([item for item in self._fruit_trees if item.rootstock == rootstock])
        self._fruit_trees.difference_update(to_remove)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Family) and self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)
            

@dataclass(frozen=True, slots=True)
class Rootstock:
    tag: str


@dataclass(frozen=True, slots=True)
class FruitTree:
    tag: str
    rootstock: Rootstock = Rootstock("FRANCO")


class Category[T: (FruitTree, Rootstock)](Node):
    def __init__(self, name: str, parent: Optional[Self] = None):
        self._products: set[T] = set()
        super().__init__(name, parent)

    @property
    def products(self) -> frozenset[T]:
        if self.is_internal():
            for leaf in self.leaves:
                self._products.update(leaf.products)
        return frozenset(self._products)

    def add_subcategory(self, name: str) -> Category:
        return Category(name, self)

    def add_product(self, item: T) -> None:
        if self.is_internal():
            for leaf in self.leaves:
                leaf.add_product(item)
        self._products.add(item)

    def __contains__(self, item: T | Self) -> bool:
        if isinstance(item, Category):
            return super().__contains__(item)
        else:
            return item in self.products


@dataclass
class Client:
    dni_nif: str
    name: str
    tax_name: str
    location: str
    address: str
    zip_code: str
    phone: str | None

    def __post_init__(self) -> None:
        self._category_prices: dict[str, float | None] = {}
    
    def __hash__(self) -> int:
        return hash(self.dni_nif)

def add_category_price(client: Client, category: Category, price: float) -> None:
    client._category_prices[category.path] = price
