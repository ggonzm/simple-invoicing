from __future__ import annotations

from src.simple_invoicing.services.units_of_work import UnitOfWork
from src.simple_invoicing.domain.model import Family
from src.simple_invoicing.services import services

class FakeFamilyRepository():
    def __init__(self) -> None:
        self._items: set[Family] = set()

    def add(self, item: Family) -> None:
        self._items.add(item)
    
    def get(self, identity: str) -> Family: # type: ignore ... ignore the case in which the item is not found
        for item in self._items:
            if item.name == identity:
                return item
            
    def update(self) -> None:
        pass

    def delete(self, identity: str) -> None:
        for item in self._items:
            if item.name == identity:
                self._items.remove(item)
                return

    def list(self) -> list[Family]:
        return list(self._items)
            
class FakeFamilyUnitOfWork(UnitOfWork[Family]):
    def __init__(self) -> None:
        self.repo = FakeFamilyRepository()
        self.commited = False
        self.rollbacked = False
    
    def __enter__(self) -> FakeFamilyUnitOfWork:
        return self

    def commit(self) -> None:
        self.commited = True
    
    def rollback(self) -> None:
        self.rollbacked = True

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.rollback()

def test_add_family():
    uow = FakeFamilyUnitOfWork()
    services.add_family("manzanos", "Malus domestica", uow)
    assert uow.repo.get("manzanos") is not None

def test_add_rootstock():
    uow = FakeFamilyUnitOfWork()
    services.add_family("manzanos", "Malus domestica", uow)
    services.add_rootstock("MM-109", "manzanos", uow)
    assert len(uow.repo.get("manzanos").rootstocks) == 2    # FRANCO + MM-109

def test_add_fruit_tree():
    uow = FakeFamilyUnitOfWork()
    services.add_family("manzanos", "Malus domestica", uow)
    services.add_fruit_tree("FRANCO", "Golden", "manzanos", uow)
    assert len(uow.repo.get("manzanos").fruit_trees) == 1
    assert uow.commited and uow.rollbacked

def test_remove_rootsetock_will_remove_all_fruit_trees_related():
    uow = FakeFamilyUnitOfWork()
    services.add_family("manzanos", "Malus domestica", uow)
    services.add_fruit_tree("FRANCO", "Golden", "manzanos", uow)
    services.remove_rootstock("FRANCO", "manzanos", uow)
    family = uow.repo.get("manzanos")
    assert family.fruit_trees == set()
    assert family.rootstocks == set()

def test_remove_fruit_tree():
    uow = FakeFamilyUnitOfWork()
    services.add_family("manzanos", "Malus domestica", uow)
    services.add_fruit_tree("FRANCO", "Golden", "manzanos", uow)
    family = uow.repo.get("manzanos")
    assert len(family.fruit_trees) == 1
    assert len(family.rootstocks) == 1
    services.remove_fruit_tree("Golden", "manzanos", uow)
    assert family.fruit_trees == set()
    assert len(family.rootstocks) == 1

def test_remove_family():
    uow =  FakeFamilyUnitOfWork()
    services.add_family("manzanos", "Malus domestica", uow)
    services.add_fruit_tree("FRANCO", "Golden", "manzanos", uow)
    services.add_rootstock("MM-109", "manzanos", uow)
    services.remove_family("manzanos", uow)
    assert uow.repo.list() == []

def test_get_families_returns_all_families_represented_as_dict():
    uow = FakeFamilyUnitOfWork()
    services.add_family("manzanos", "Malus domestica", uow)
    services.add_fruit_tree("FRANCO", "Golden", "manzanos", uow)
    services.add_rootstock("MM-109", "manzanos", uow)
    assert services.get_families(uow) == [
        {"name": "manzanos",
         "sci_name": "Malus domestica",
         "fruit_trees": [{"tag": "Golden", "rootstock": {"tag": "FRANCO"}}],
         "rootstocks": [{"tag": "FRANCO"}, {"tag": "MM-109"}]
        }
        ]