from model import Category, FruitTree
from exceptions import CategoryError
import pytest


def test_products_creation(fruit_trees, rootstock, families):
    product1, product2, product3 = fruit_trees
    family1, family2 = families

    assert str(product1) == "Malus domestica Manzanos GOLDEN D." 
    assert product1.family == family1

    assert str(product2) == "Malus domestica Manzanos MANZANO GENERICO"
    assert str(product3) == "Prunus domestica Ciruelos GOLDEN JAPAN"
    assert product3.family == family2

    assert product1.rootstock == rootstock
    assert str(rootstock) == "Malus domestica Portainjertos Manzanos MM-109"
    assert rootstock.family == family1

    assert product2.rootstock == rootstock
    assert product3.rootstock is None
    

def test_subcategory_creation():
    n1 = Category[FruitTree]("Raíz desnuda")
    n2 = n1.add_subcategory("Pepita")
    n3 = n2.add_subcategory("1 año")

    assert n3 in n2
    assert n2 in n1


def test_product_allocation_to_a_final_category(fruit_category_tree, fruit_trees):
    n1, n2, _, n4,*_ = fruit_category_tree
    product1, product2, _ = fruit_trees

    n4.add_products(product1, product2)
    
    assert product1 in n4
    assert n4.products == set([product1, product2])

def test_product_allocation_to_an_internal_category(fruit_category_tree, fruit_trees):
    n1, n2, _, n4, *_ = fruit_category_tree
    product1, product2, _ = fruit_trees

    n2.add_products(product1, product2)
    
    assert product1 in n4
    assert product2 in n4
    assert n4.products == set([product1, product2])

def test_products_mixed_in_the_same_category(fruit_category_tree, fruit_trees, rootstock):  # NOT DESIRED, but possible using python
    n1, _, _, n4,*_ = fruit_category_tree
    fruit_tree,*_ = fruit_trees

    n4.add_products(fruit_tree, rootstock)  # it's a type error
    
    assert not all(isinstance(product, FruitTree) for product in n4.products)

def test_product_deletion():
    pass