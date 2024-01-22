from src.simple_invoicing.domain.model import FruitTree, Family, Rootstock
from src.simple_invoicing.services.units_of_work import UnitOfWork

def add_family(name: str, sci_name: str, uow: UnitOfWork[Family]) -> None:
    with uow:
        uow.repo.add(Family(name, sci_name))
        uow.commit()

def add_fruit_tree(rootstock_tag: str, tag: str, family_name: str, uow: UnitOfWork[Family]) -> None:
    with uow:
        family = uow.repo.get(family_name)
        family.add(FruitTree(tag, rootstock=Rootstock(rootstock_tag)))
        uow.commit()

def add_rootstock(tag: str, family_name: str, uow: UnitOfWork[Family]) -> None:
    with uow:
        family = uow.repo.get(family_name)
        family.add(Rootstock(tag))
        uow.commit()

def remove_fruit_tree(tag: str, family_name: str, uow: UnitOfWork[Family]) -> None:
    with uow:
        family = uow.repo.get(family_name)
        family.remove(FruitTree(tag))
        uow.commit()

def remove_rootstock(tag: str, family_name: str, uow: UnitOfWork[Family]) -> None:
    with uow:
        family = uow.repo.get(family_name)
        family.remove(Rootstock(tag))
        uow.commit()

def remove_family(name: str, uow: UnitOfWork[Family]) -> None:
    with uow:
        uow.repo.delete(name)
        uow.commit()