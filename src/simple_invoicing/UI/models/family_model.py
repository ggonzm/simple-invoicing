import src.simple_invoicing.services.services as api
from src.simple_invoicing.services.units_of_work import FamilyUnitOfWork
from src.simple_invoicing.UI.models.observable import Observable, SupportsObserver
from src.simple_invoicing.UI.models.events import FamilyAdded, FamilyRemoved
from typing import Protocol

class SupportsFamilyAPI(SupportsObserver, Protocol):
    def add_family(self, name: str, sci_name: str) -> None:
        ...

    def remove_family(self, name: str) -> None:
        ...
    
    def get_families(self) -> list[tuple[str,str]]:
        ...

class FamilyModel(Observable):
    def __init__(self):
        super().__init__()
        self.uow = FamilyUnitOfWork()
    
    def add_family(self, name: str, sci_name: str) -> None:
        api.add_family(name, sci_name, self.uow)
        self.trigger_event(FamilyAdded(name, sci_name))
    
    def remove_family(self,  name: str) -> None:
        api.remove_family(name, self.uow)
        self.trigger_event(FamilyRemoved(name))
    
    def get_families(self) -> list[tuple[str,str]]:
        families =  api.get_families(self.uow)
        return [(family['name'], family['sci_name']) for family in families]