from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Self

from TreeStruct import Node
from exceptions import CategoryError


@dataclass(frozen=True)
class FruitTree:
    id: int
    description: str
    family: str
    rootstock: str


@dataclass(frozen=True)
class Rootstock:
    description: str


class Category[T: (FruitTree, Rootstock)](Node):
    def __init__(self, name: str, parent: Optional[Self] = None):
        self._products: set[T] = set()
        self._price: Optional[float] = None
        super().__init__(name, parent)

    @property
    def products(self) -> set[T]:
        if self.is_internal():
            for leaf in self.leaves:
                self._products.update(leaf.products)
        return self._products

    @property
    def price(self) -> float | None:
        return self._price if not self.is_internal() else None

    @price.setter
    def price(self, value: float) -> None:
        if self.is_internal():
            self._price = None
            raise CategoryError("Price can only be assigned to last level categories")
        self._price = value

    def add_subcategory(
        self, name: str
    ) -> Self:  # Self and self.__class__ could be replaced by Category[T], but I prefer this way
        return self.__class__(name, self)

    def add_products(self, *products: T) -> None:
        '''Adds products to the category. If the category is internal, the products are added to the leaves'''
        if self.is_internal():
            for leaf in self.leaves:
                leaf.add_products(*products)
        for product in products:
            self._products.add(product)

    def get_product_prices(self, product: T) -> dict[str,float|None]:
        '''Returns a dictionary with the prices of the product in category leaves'''
        prices: dict[str,float|None] = {}
        for leaf in self.leaves:
            if product in leaf:
                prices[leaf.name] = leaf.price
        if prices :
            return prices
        raise CategoryError("Product not found in category")

    def __contains__(self, item: T | Self) -> bool:
        if isinstance(item, Category):
            return super().__contains__(item)
        else:
            return item in self._products


class Client:
    pass
