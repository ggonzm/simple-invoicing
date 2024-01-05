from src.simple_invoicing.adapters.repositories import FamilyRepository, RootstockRepository, FruitTreeRepository

def test_products_repositories(in_memory_db, fruit_trees, rootstock, families):
    product1, product2, product3 = fruit_trees
    family1, family2 = families

    repo1 = FamilyRepository(in_memory_db)
    repo1.add(family1)
    repo1.add(family2)
    repo2 = RootstockRepository(in_memory_db)
    repo2.add(rootstock)
    repo3 = FruitTreeRepository(in_memory_db)
    repo3.add(product1)
    repo3.add(product2)
    repo3.add(product3)
    in_memory_db.commit()
    
    assert set(in_memory_db.execute("SELECT name, sci_name FROM families").fetchall()) == set([("manzanos", "Malus domestica",), ("ciruelos", "Prunus domestica",)])
    assert set(in_memory_db.execute("SELECT tag, family_hash FROM rootstocks").fetchall()) == set([("MM-109", hash(family1),)])
    assert set(in_memory_db.execute("SELECT tag, rootstock_hash, family_hash FROM fruit_trees").fetchall()) == set([("GOLDEN D.", hash(rootstock), hash(family1),), ("MANZANO GENERICO", hash(rootstock), hash(family1),), ("GOLDEN JAPAN", None, hash(family2),)])
    assert repo1.get("manzanos") == family1
    assert repo2.get("MM-109") == rootstock
    assert repo3.get("GOLDEN D.") == product1
    assert set(repo1.list()) == set([family1, family2])
    assert repo2.list() == [rootstock]
    assert set(repo3.list()) == set([product1, product2, product3])

