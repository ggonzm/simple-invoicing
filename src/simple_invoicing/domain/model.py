from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Self

from src.simple_invoicing.domain.TreeStruct import Node

class RootstockError(Exception):
    pass

@dataclass(kw_only=True)
class Family:
    sci_name: str
    name: str

    def __post_init__(self) -> None:
        self._fruit_trees: set[FruitTree] = set()
        self._rootstocks: set[Rootstock] = set([Rootstock("FRANCO")])

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
