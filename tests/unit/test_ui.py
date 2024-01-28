from src.simple_invoicing.UI.controllers.family_controller import FamilyController
from src.simple_invoicing.UI.views.family_view import FamilyView
from src.simple_invoicing.UI.models.events import Event, FamilyAdded
from src.simple_invoicing.UI.models.observable import Observable
from src.simple_invoicing.UI.views.common import Table

# https://stackoverflow.com/questions/65468655/vs-code-remote-x11-cant-get-display-while-connecting-to-remote-server
# Needed to run the tests because a GUI is used in a remote server
# VcXsrv is used in Windows as X server

def test_table():
    table = Table(col_names=["col1", "col2"])
    table.add_row(["a", "b"])
    table.add_row(["c", "d"])

    assert table.rows == [["a", "b"], ["c", "d"]]
    assert table.cols == [["a", "c"], ["b", "d"]]
    assert table[1,0] == "a"
    assert table[0,:] == ["col1", "col2"]
    assert table[1,1] == 'b'
    assert table[1,:] == ["a","b"]
    assert table[:,1] == ["col2", "b", "d"]
    assert table[:,:] == [["col1","col2"], ["a", "b"], ["c", "d"]]
    assert table[1:,:] == [["a","b"], ["c", "d"]]
    assert table[1:,1:] == [["b"], ["d"]]
    

class FakeFamilyModel(Observable):
    def __init__(self):
        super().__init__()
        self.commands = []
        self.listeners_called = []

    def add_family(self, name: str, sci_name: str) -> None:
        self.commands.append(f"ADD_FAMILY ({name}, {sci_name})")
        self.trigger_event(FamilyAdded(name, sci_name))
        print(self.commands)
    
    def trigger_event(self, event: Event) -> None:
        for fn in self.listeners.get(type(event), []):
            self.listeners_called.append(f'{fn.__name__}({event})')
            fn(event)
        print(self.listeners_called)

def test_user_can_add_new_families():
    view = FamilyView()
    model = FakeFamilyModel()
    controller = FamilyController(view, model)

    view.creation_area.name.insert(0,"manzanos")
    view.creation_area.sci_name.insert(0,"nombre científico")
    view.creation_area.save.invoke()
    expected_event = FamilyAdded("manzanos", "nombre científico")

    assert len(model.commands) == 1
    assert model.commands == ["ADD_FAMILY (manzanos, nombre científico)"]
    assert len(model.listeners_called) == 1
    assert model.listeners_called == [f"on_family_added({expected_event})"]
    assert view.display[1,:] == ["manzanos", "nombre científico"]