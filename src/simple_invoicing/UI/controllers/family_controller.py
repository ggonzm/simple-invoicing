from src.simple_invoicing.UI.views.family_view import FamilyView
from src.simple_invoicing.UI.models.family_model import SupportsFamilyAPI
from src.simple_invoicing.UI.models.events import FamilyAdded, FamilyRemoved

class FamilyController():
    view: FamilyView
    model: SupportsFamilyAPI

    def __init__(self, view: FamilyView, model: SupportsFamilyAPI):
        self.view = view
        self.model = model
        self._bind_events()
        self._preload_view()
    
    def _preload_view(self):
        if families := self.model.get_families():
            self.view.preload_families(families)

    def _bind_events(self):
        self.view.creation_area.save.configure(command=self.add_family)
        self.view.deletion_area.delete.configure(command=self.remove_family)
        self._subscribe_view()
    
    def _subscribe_view(self):
        self.model.subscribe(FamilyAdded, self.view.on_family_added)
        self.model.subscribe(FamilyRemoved, self.view.on_family_removed)

    def add_family(self):
        name = self.view.creation_area.name.get()
        sci_name = self.view.creation_area.sci_name.get()
        self.model.add_family(name, sci_name)
    
    def remove_family(self):
        name = self.view.deletion_area.name.get()
        self.model.remove_family(name)