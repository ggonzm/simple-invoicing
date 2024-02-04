from src.simple_invoicing.UI.controllers.family_controller import FamilyController
from src.simple_invoicing.UI.views.family_view import FamilyView
from src.simple_invoicing.UI.models.events import Event, FamilyAdded, FamilyRemoved
from src.simple_invoicing.UI.models.observable import Observable
from src.simple_invoicing.UI.views.common import Table

# https://stackoverflow.com/questions/65468655/vs-code-remote-x11-cant-get-display-while-connecting-to-remote-server
# Needed to run the tests because a GUI is used in a remote server
# VcXsrv is used in Windows as X server

def test_table():
    table = Table(header=["col1", "col2"])
    table.add_row(["a", "b"])
    table.add_row(["c", "d"])
    
    assert table.rows == [["a", "b"], ["c", "d"]]
    assert table.cols == [["a", "c"], ["b", "d"]]
    assert table.header == ["col1", "col2"]
    assert table[0,0] == "a"
    assert table[1,0] == "c"
    assert table[0,:] == ["a", "b"]
    assert table[1,1] == 'd'
    assert table[1,:] == ["c","d"]
    assert table[:,1] == ["b", "d"]
    assert table[:,:] == [["a", "b"], ["c", "d"]]
    assert table[1:,:] == [["c", "d"]]
    assert table[0:,1:] == [["b"], ["d"]]
    assert table[1:,1:] == [["d"]]

class FakeFamilyModel(Observable):
    commands: list[str]
    listeners_called: list[str]
    _families: list[tuple[str,str]]

    def __init__(self):
        super().__init__()
        self.commands = []
        self.listeners_called = []
        self._families = list()

    def add_family(self, name: str, sci_name: str) -> None:
        self.commands.append(f"ADD_FAMILY ({name}, {sci_name})")
        self._families.append((name, sci_name))
        self.trigger_event(FamilyAdded(name, sci_name))
    
    def remove_family(self, name: str) -> None:
        self.commands.append(f"REMOVE_FAMILY ({name})")
        self._families = [f for f in self._families if f[0] != name]
        self.trigger_event(FamilyRemoved(name))
    
    def get_families(self) -> list[tuple[str,str]]:
        return list(self._families)
    
    def trigger_event(self, event: Event) -> None:
        for fn in self.listeners.get(type(event), []):
            self.listeners_called.append((f'{fn.__name__}({event})'))
            fn(event)

def test_existing_families_are_preloaded_when_familyview_is_shown():
    view = FamilyView()
    model = FakeFamilyModel()
    model._families = [("manzanos", "nombre científico"), ("perales", "nombre científico")]
    controller = FamilyController(view, model)

    assert view.display[0,:] == ["manzanos", "nombre científico"]
    assert view.display[1,:] == ["perales", "nombre científico"]
    assert view.deletion_area.name["values"] == ("", "manzanos", "perales")
    assert view.deletion_area.name.get() == ""

def test_user_can_add_new_families():
    view = FamilyView()
    model = FakeFamilyModel()
    controller = FamilyController(view, model)

    view.creation_area.name.insert(0,"manzanos")
    view.creation_area.sci_name.insert(0,"nombre científico")
    view.creation_area.save.invoke()
    expected_event = FamilyAdded("manzanos", "nombre científico")

    assert ("manzanos","nombre científico") in model._families
    assert len(model.commands) == 1
    assert model.commands == ["ADD_FAMILY (manzanos, nombre científico)"]
    assert len(model.listeners_called) == 1
    assert model.listeners_called == [f"on_family_added({expected_event})"]
    assert view.display[0,:] == ["manzanos", "nombre científico"]
    assert view.deletion_area.name["values"] == ("", "manzanos")

def test_user_can_delete_existing_families():
    view = FamilyView()
    model = FakeFamilyModel()
    model._families = [("manzanos", "nombre científico"), ("perales", "nombre científico")]
    controller = FamilyController(view, model)

    view.deletion_area.name.set("manzanos")
    view.deletion_area.delete.invoke()
    expected_event = FamilyRemoved("manzanos")

    assert view.deletion_area.name["values"] == ("", "perales")
    assert view.deletion_area.name.get() == ""
    assert ("manzanos", "nombre científico") not in model._families
    assert len(model.commands) == 1
    assert model.commands == ["REMOVE_FAMILY (manzanos)"]
    assert len(model.listeners_called) == 1
    assert model.listeners_called == [f"on_family_removed({expected_event})"]
    assert view.display[0:,:] == [["perales", "nombre científico"]]