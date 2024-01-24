from src.simple_invoicing.UI.views.family_view import FamilyView
from src.simple_invoicing.UI.models.family_model import SupportsFamilyAPI

class FamilyController():
    view: FamilyView
    model: SupportsFamilyAPI

    def __init__(self, view: FamilyView, model: SupportsFamilyAPI):
        self.view = view
        self.model = model
        self._bind_events()

    def _bind_events(self):
        self.view.creation_area.save.configure(command=self._add_family)

    def _add_family(self):
        name = self.view.creation_area.name.get()
        sci_name = self.view.creation_area.sci_name.get()
        self.model.add_family(name, sci_name)

    