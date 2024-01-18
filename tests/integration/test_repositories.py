from src.simple_invoicing.persistence.repositories import FamilyRepository

def insert_items(conn):
    conn.execute("INSERT INTO families (name, sci_name) VALUES ('manzanos', 'Malus domestica'), ('ciruelos', 'Prunus domestica')")
    conn.execute("INSERT INTO rootstocks (tag, family_id) VALUES ('FRANCO', 1), ('MM-109', 1), ('FRANCO', 2)")
    conn.execute("INSERT INTO fruit_trees (tag, rootstock_id, family_id) VALUES ('GOLDEN D.', 2, 1), ('MANZANO GENERICO', 2, 1)")
    conn.commit()

def test_family_repository_can_add_families_and_their_products(conn, fruit_trees, rootstock, families):
    product1, product2, _ = fruit_trees
    family1, family2 = families

    family1.add(rootstock)
    family1.add(product1)
    family1.add(product2)

    repo = FamilyRepository(conn)
    repo.add(family1)
    repo.add(family2)
    conn.commit()
    
    assert set(conn.execute("SELECT name, sci_name FROM families").fetchall()) == set([("manzanos", "Malus domestica",), ("ciruelos", "Prunus domestica",)])
    assert set(conn.execute("SELECT tag FROM rootstocks").fetchall()) == set([("FRANCO",), ("MM-109",),])
    assert set(conn.execute("SELECT tag FROM fruit_trees").fetchall()) == set([("GOLDEN D.",), ("MANZANO GENERICO",), ])

def test_family_repository_can_get_families_and_their_products(conn, fruit_trees, rootstock, families):
    product1, product2, product3 = fruit_trees
    family1, family2 = families
    insert_items(conn)

    repo = FamilyRepository(conn)

    assert repo.get("manzanos") == family1
    assert repo.get("manzanos").fruit_trees == frozenset([product1, product2])
    assert rootstock in repo.get("manzanos").rootstocks
    assert product3 not in repo.get("ciruelos").fruit_trees
    assert set(repo.list()) == set([family1, family2])

def test_family_repository_can_update_sci_name(conn):
    insert_items(conn)
    repo = FamilyRepository(conn)
    family = repo.get("manzanos")
    assert family.sci_name == "Malus domestica"

    family.sci_name = "Malus domestica2"
    repo.update()
    conn.commit()
    assert repo.get("manzanos").sci_name == "Malus domestica2"


def test_family_repository_can_add_new_products_to_an_existing_family(conn, fruit_trees):
    _, _, product3 = fruit_trees
    insert_items(conn)
    repo = FamilyRepository(conn)
    family = repo.get("ciruelos")
    assert family.fruit_trees == frozenset()

    family.add(product3)
    repo.update()
    conn.commit()
    assert repo.get("ciruelos").fruit_trees == frozenset([product3])

def test_family_repository_can_remove_products_from_an_existing_family(conn, fruit_trees):
    product1, product2, _ = fruit_trees
    insert_items(conn)
    repo = FamilyRepository(conn)
    family = repo.get("manzanos")
    assert family.fruit_trees == frozenset([product1, product2])

    family.remove(product1)
    repo.update()
    conn.commit()
    assert repo.get("manzanos").fruit_trees == frozenset([product2])

def test_family_repository_always_returns_the_same_object(conn):
    insert_items(conn)
    repo = FamilyRepository(conn)
    family1 = repo.get("manzanos")
    family2 = repo.get("manzanos")
    assert family1 is family2