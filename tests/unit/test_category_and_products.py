from src.simple_invoicing.domain.model import Category, FruitTree, Rootstock, RootstockError
import pytest


def test_products_creation_and_addition_to_a_family(fruit_trees, rootstock, families):
    product1, product2, product3 = fruit_trees
    family1, family2 = families
    family1.add(rootstock)
    family1.add(product1)
    family1.add(product2)
    family2.add(product3)

    assert rootstock.tag == "MM-109"
    assert rootstock in family1.rootstocks
    assert family1.rootstocks == frozenset([Rootstock("FRANCO"), rootstock])

    assert product1.tag == "GOLDEN D."
    assert product1.rootstock == rootstock

    assert product2.tag == "MANZANO GENERICO"
    assert product2.rootstock == rootstock
    assert family1.fruit_trees == frozenset([product1, product2])

    assert product3.tag == "GOLDEN JAPAN"
    assert product3.rootstock == Rootstock("FRANCO")
    assert family2.fruit_trees == frozenset([product3])
    assert family2.rootstocks == frozenset([Rootstock("FRANCO")])

    with pytest.raises(RootstockError):
        family2.add(FruitTree("CIRUELO JAPONES", Rootstock("MM-109"))) 

def test_product_deletion_from_a_family(fruit_trees, rootstock, families):
    product1, product2, _ = fruit_trees
    family1, _ = families
    family1.add(rootstock)
    family1.add(product1)
    family1.add(product2)

    assert family1.fruit_trees == frozenset([product1, product2])
    family1.remove(product1)
    assert family1.fruit_trees == frozenset([product2])

    assert rootstock in family1.rootstocks
    family1.remove(rootstock)
    assert rootstock not in family1.rootstocks
    assert family1.rootstocks == frozenset([Rootstock("FRANCO")])
    assert family1.fruit_trees == frozenset()

def test_subcategory_creation():
    n1 = Category("Raíz desnuda")
    n2 = n1.add_subcategory("Pepita")
    n3 = n2.add_subcategory("1 año")

    assert n3 in n2
    assert n2 in n1


def test_product_allocation_to_a_final_category(fruit_category_tree, fruit_trees):
    _, _, _, n4, *_ = fruit_category_tree
    product1, product2, _ = fruit_trees

    n4.add_product(product1)
    n4.add_product(product2)

    assert product1 in n4
    assert n4.products == frozenset([product1, product2])


def test_product_allocation_to_an_internal_category(fruit_category_tree, fruit_trees):
    _, n2, _, n4, *_ = fruit_category_tree
    product1, product2, _ = fruit_trees

    n2.add_product(product1)
    n2.add_product(product2)

    assert product1 in n4
    assert product2 in n4
    assert n4.products == frozenset([product1, product2])

def test_products_mixed_in_the_same_category(
    fruit_category_tree, fruit_trees, rootstock
):  # NOT DESIRED, but possible using python
    n1, _, _, n4, *_ = fruit_category_tree
    fruit_tree, *_ = fruit_trees

    n4.add_product(fruit_tree) # OK
    n4.add_product(rootstock) # should be a type error

    assert not all(isinstance(product, FruitTree) for product in n4.products)