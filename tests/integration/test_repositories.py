from src.simple_invoicing.adapters.repositories import FamilyRepository

def test_family_repository(in_memory_db, fruit_trees, rootstock, families):
    product1, product2, product3 = fruit_trees
    family1, family2 = families

    family1.add(rootstock)
    family1.add(product1)
    family1.add(product2)

    repo = FamilyRepository(in_memory_db)
    repo.add(family1)
    repo.add(family2)
    in_memory_db.commit()
    
    assert set(in_memory_db.execute("SELECT name, sci_name FROM families").fetchall()) == set([("manzanos", "Malus domestica",), ("ciruelos", "Prunus domestica",)])
    assert set(in_memory_db.execute("SELECT tag FROM rootstocks").fetchall()) == set([("FRANCO",), ("MM-109",),])
    assert set(in_memory_db.execute("SELECT tag FROM fruit_trees").fetchall()) == set([("GOLDEN D.",), ("MANZANO GENERICO",), ])
    assert repo.get("manzanos") == family1
    assert repo.get("manzanos").fruit_trees == frozenset([product1, product2])
    assert rootstock in repo.get("manzanos").rootstocks
    assert product3 not in repo.get("ciruelos").fruit_trees
    assert set(repo.list()) == set([family1, family2])

