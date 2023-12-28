from model import Category, FruitTree, Rootstock
from exceptions import CategoryError
import pytest


@pytest.fixture
def fruit_category_tree():
    '''
                Raíz desnuda (n1)
                /                \
            Pepita (n2)           Hueso (n3)
            /         \            /        \
        1 año (n4)  2 años (n5)  1 año (n6)  2 años (n7)
    '''
    n1 = Category[FruitTree]("Raíz desnuda")
    n2 = n1.add_subcategory("Pepita")
    n3 = n1.add_subcategory("Hueso")
    n4 = n2.add_subcategory("1 año")
    n5 = n2.add_subcategory("2 años")
    n6 = n3.add_subcategory("1 año")
    n7 = n3.add_subcategory("2 años")

    return (n1, n2, n3, n4, n5, n6, n7)

@pytest.fixture
def fruit_trees():
    product1 = FruitTree(11011, "Malus domestica Manzanos GOLDEN D.", "MANZANO", "MM-109")
    product2 = FruitTree(11012, "Manzano de mesa", "MANZANO", "MM-109")
    product3 = FruitTree(11045, "Prunus domestica Ciruelos GOLDEN JAPAN", "CIRUELO", "Mirabolan")
    return (product1, product2, product3)

@pytest.fixture
def rootstock():
    return Rootstock("MM-109")




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


def test_price_assignment_to_products_in_categories(fruit_category_tree, fruit_trees):
    n1, n2, n3, n4, _, n6, _ = fruit_category_tree
    fruit_tree1, fruit_tree2, fruit_tree3 = fruit_trees

    n4.add_products(fruit_tree1, fruit_tree2)
    n6.add_products(fruit_tree3)

    assert n1.get_product_prices(fruit_tree1) == {n4.name : None}
    
    n4.price = 2.50
    n6.price = 3.50

    assert n1.get_product_prices(fruit_tree1) == {n4.name : 2.50}
    assert n2.get_product_prices(fruit_tree2) == {n4.name : 2.50}
    assert n4.get_product_prices(fruit_tree1) == {n4.name : 2.50}
    assert n1.get_product_prices(fruit_tree3) == {n6.name : 3.50}
    assert n3.get_product_prices(fruit_tree3) == {n6.name : 3.50}
    assert n6.get_product_prices(fruit_tree3) == {n6.name : 3.50}
    with pytest.raises(CategoryError):
        n4.get_product_prices(fruit_tree3)

def test_product_prices_for_duplicated_products_in_different_categories(fruit_category_tree, fruit_trees):
    n1, n2, _, n4, n5, *_ = fruit_category_tree
    fruit_tree1, *_ = fruit_trees

    n4.price = 2.50
    n5.price = 2.00
    n4.add_products(fruit_tree1)
    n5.add_products(fruit_tree1)

    assert n2.get_product_prices(fruit_tree1) == {n4.name: 2.50, n5.name: 2.00}

def test_product_deletion():
    pass