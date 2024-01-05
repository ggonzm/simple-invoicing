from src.simple_invoicing.domain.model import (
    Category,
    FruitTree,
    Rootstock,
    Family,
    Client,
)

import pytest
from sqlite3 import connect
from src.simple_invoicing.adapters.db_tables import create_all_tables


@pytest.fixture
def fruit_category_tree():
    """
                Raíz desnuda (n1)
                /                \
            Pepita (n2)           Hueso (n3)
            /         \            /        \
        1 año (n4)  2 años (n5)  1 año (n6)  2 años (n7)
    """
    n1 = Category[FruitTree]("Raíz desnuda")
    n2 = n1.add_subcategory("Pepita")
    n3 = n1.add_subcategory("Hueso")
    n4 = n2.add_subcategory("1 año")
    n5 = n2.add_subcategory("2 años")
    n6 = n3.add_subcategory("1 año")
    n7 = n3.add_subcategory("2 años")

    return (n1, n2, n3, n4, n5, n6, n7)


@pytest.fixture
def families():
    return (
        Family(sci_name="Malus domestica", name="manzanos"),
        Family(sci_name="Prunus domestica", name="ciruelos"),
    )


@pytest.fixture
def fruit_trees(rootstock, families):
    family1, family2 = families
    product1 = FruitTree("GOLDEN D.", family1, rootstock)
    product2 = FruitTree("MANZANO GENERICO", family1, rootstock)
    product3 = FruitTree("GOLDEN JAPAN", family2, None)
    return (product1, product2, product3)


@pytest.fixture
def rootstock(families):
    family1, _ = families
    return Rootstock("MM-109", family1)


@pytest.fixture
def clients():
    client1 = Client(
        dni_nif="12345678Z",
        name="Jhon Doe",
        tax_name="Vivero de Jhon",
        location="Madrid",
        address="Calle Falsa 123",
        phone="123456789",
        zip_code="28000",
    )
    client2 = Client(
        dni_nif="87654321A",
        name="Jane Doe",
        tax_name="Vivero de Jane",
        location="Madrid",
        address="Calle Falsa 123",
        phone="123456789",
        zip_code="28000",
    )
    client3 = Client(
        dni_nif="12365432F",
        name="Jhon Doe",
        tax_name="Vivero de Jhon",
        location="Vitoria",
        address="Calle Falsa 123",
        phone="123456789",
        zip_code="28000",
    )
    return (client1, client2, client3)

@pytest.fixture
def in_memory_db():
    con = connect(":memory:")
    create_all_tables(con)
    con.commit()
    return con