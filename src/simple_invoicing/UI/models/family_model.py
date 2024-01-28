import src.simple_invoicing.services.services as api
from src.simple_invoicing.services.units_of_work import FamilyUnitOfWork
from src.simple_invoicing.UI.models.observable import Observable, SupportsObserver
from src.simple_invoicing.UI.models.events import FamilyAdded
from typing import Protocol

class SupportsFamilyAPI(SupportsObserver, Protocol):
    def add_family(self, name: str, sci_name: str) -> None:
        ...

class FamilyModel(Observable):
    def __init__(self):
        super().__init__()
        self.uow = FamilyUnitOfWork()
    
    def add_family(self, name: str, sci_name: str) -> None:
        api.add_family(name, sci_name, self.uow)
        self.trigger_event(FamilyAdded(name, sci_name))