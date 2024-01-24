from src.simple_invoicing.UI.controllers.family_controller import FamilyController
from src.simple_invoicing.UI.views.family_view import FamilyView

# https://stackoverflow.com/questions/65468655/vs-code-remote-x11-cant-get-display-while-connecting-to-remote-server
# Needed to run the tests because a GUI is used in a remote server
# VcXsrv is used in Windows as X server

class FakeFamilyModel():
    def __init__(self):
        self.commands = []
        self.events = {}

    def add_family(self, name: str, sci_name: str) -> None:
        self.commands.append(f"ADD_FAMILY ({name}, {sci_name})")
        print(self.commands)
    
    def subscribe(self, event, fn):
        if self.events.get(event) is None:
            self.events[event] = []
        self.events[event].append(fn)
        print(self.events)
    
    def trigger_event(self, event):
        pass

    def unsubscribe(self, event, fn):
        pass


def test_user_can_add_new_families():
    view = FamilyView()
    model = FakeFamilyModel()
    controller = FamilyController(view, model)
    view.creation_area.name.insert(0,"manzanos")
    view.creation_area.sci_name.insert(0,"nombre científico")
    view.creation_area.save.invoke()

    assert len(model.commands) == 1
    assert model.commands == ["ADD_FAMILY (manzanos, nombre científico)"]