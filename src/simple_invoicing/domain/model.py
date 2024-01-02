from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Self

from .TreeStruct import Node


@dataclass(frozen=True, slots=True, kw_only=True)
class FruitTree:
    family: Family
    name: str
    rootstock: Optional[
        Rootstock
    ] = None  # ¿Si family no coincide con la de portainjertos? TODO: mirar libreria attrs y field() en dataclasses

    def __str__(self) -> str:
        return str(self.family) + " " + self.name.upper()


@dataclass(frozen=True, slots=True, kw_only=True)
class Rootstock:
    family: Family
    id: str

    def __str__(self) -> str:
        return (
            self.family.sci_name.capitalize()
            + " Portainjertos "
            + self.family.name.capitalize()
            + " "
            + self.id
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class Family:
    sci_name: str
    name: str

    def __str__(self) -> str:
        return self.sci_name.capitalize() + " " + self.name.capitalize()


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


def add_category_price(client: Client, category: Category, price: float) -> None:
    client._category_prices[category.path] = price
