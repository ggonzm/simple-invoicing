from src.simple_invoicing.services.units_of_work import FamilyUnitOfWork

def test_uow_can_add_a_family_retrieve_it_and_add_or_remove_products_using_different_conn_objects(conn_factory, families, fruit_trees, rootstock):
    family1, _ = families
    product1, product2, _ = fruit_trees

    with FamilyUnitOfWork(conn_factory) as uow:
        assert uow.repo.list() == []
        family1.add(rootstock)
        family1.add(product1)
        uow.repo.add(family1)
        uow.commit()

    with FamilyUnitOfWork(conn_factory) as uow:
        assert uow.repo.get("manzanos") == family1
        assert uow.repo.get("manzanos").fruit_trees == frozenset([product1])
        assert rootstock in uow.repo.get("manzanos").rootstocks

        family = uow.repo.get("manzanos")
        family.add(product2)
        uow.commit()

    with FamilyUnitOfWork(conn_factory) as uow:
        assert uow.repo.get("manzanos").fruit_trees == frozenset([product1, product2])
    
    with FamilyUnitOfWork(conn_factory) as uow:
        family = uow.repo.get("manzanos")
        family.remove(product2)
        uow.commit()
    
    with FamilyUnitOfWork(conn_factory) as uow:
        assert uow.repo.get("manzanos").fruit_trees == frozenset([product1])
    
    with FamilyUnitOfWork(conn_factory) as uow:
        family = uow.repo.get("manzanos")
        family.remove(rootstock)
        uow.commit()
    
    with FamilyUnitOfWork(conn_factory) as uow:
        family = uow.repo.get("manzanos")
        assert rootstock not in family.rootstocks
        assert family.fruit_trees == frozenset([])
    