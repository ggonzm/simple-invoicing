import pytest
from model import Category


@pytest.fixture
def make_category():
    def _category(name: str):
        category = Category(name)
        return category

    yield _category
    # Teardown Categories
    Category._instances.clear()


def test_subcategory_assignation_to_category(make_category):
    category = make_category("Raíz desnuda")
    subcategory1 = make_category("Hueso")
    subcategory2 = make_category("Pepita")
    category.add_subcategories(subcategory1, subcategory2)

    assert category._subcategories["Hueso"] == subcategory1
    assert category._subcategories["Pepita"] == subcategory2


def test_category_equality(make_category):
    category1 = make_category("Raíz desnuda")
    subcategory1 = make_category("Hueso")
    category1.add_subcategories(subcategory1)

    category2 = make_category("Raíz desnuda")
    subcategory2 = make_category("Pepita")
    category2.add_subcategories(subcategory2)

    assert category1 == category2


def test_categories_are_idempotent(make_category):
    category1 = make_category("Raíz desnuda")
    subcategory1 = make_category("Hueso")
    category1.add_subcategories(subcategory1)
    category1.add_subcategories(subcategory1)
    category1.add_subcategories(subcategory1)

    assert category1._subcategories == {"Hueso": subcategory1}
