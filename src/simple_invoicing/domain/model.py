from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Self

from src.simple_invoicing.domain.TreeStruct import Node
from src.simple_invoicing.utils import custom_hash

class IncompatibleFamilyError(Exception):
    pass

class FruitTree:
    def __init__(self, tag:str, family:Family, rootstock:Optional[Rootstock]) -> None:
        if rootstock and family != rootstock.family:
            raise IncompatibleFamilyError("The family of the fruit tree and the rootstock must be the same")
        self.tag = tag
        self.family =  family
        self.rootstock = rootstock

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FruitTree):
            return False
        return self.tag == other.tag
    
    def __hash__(self) -> int:
        return custom_hash(self.tag)


class Rootstock:
    def __init__(self, tag:str, family:Family) -> None:
        self.tag = tag
        self.family = family

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rootstock):
            return False
        return self.tag == other.tag

    def __hash__(self) -> int:
        return custom_hash(self.tag)


class Family:
    def __init__(self, sci_name:str, name:str) -> None:
        self.sci_name = sci_name
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Family):
            return False
        return self.name == other.name
    
    def __hash__(self) -> int:
        return custom_hash(self.name)


class Category[T: (FruitTree, Rootstock)](Node):
    def __init__(self, name: str, parent: Optional[Self] = None):
        self._products: set[T] = set()
        super().__init__(name, parent)

    @property
    def products(self) -> set[T]:
        if self.is_internal():
            for leaf in self.leaves:
                self._products.update(leaf.products)
        return self._products

    def add_subcategory(
        self, name: str
    ) -> Self:  # Self and self.__class__ could be replaced by Category[T], but I prefer this way
        return self.__class__(name, self)

    def add_products(self, *products: T) -> None:
        """Adds products to the category. If the category is internal, the products are added to the leaves"""
        if self.is_internal():
            for leaf in self.leaves:
                leaf.add_products(*products)
        for product in products:
            self._products.add(product)

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
        return custom_hash(self.dni_nif)

def add_category_price(client: Client, category: Category, price: float) -> None:
    client._category_prices[category.path] = price
