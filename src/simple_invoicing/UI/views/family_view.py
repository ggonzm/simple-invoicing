from __future__ import annotations
from tkinter.ttk import Frame, Label, Entry, Button, Style, Treeview, Scrollbar, Combobox, Notebook, Progressbar, Separator, Labelframe
from dataclasses import dataclass
from src.simple_invoicing.UI.models.events import FamilyAdded, FamilyRemoved
from src.simple_invoicing.UI.views.common import Table

class FamilyView(Frame):
    creation_area: CreationArea
    deletion_area: DeletionArea
    display: Table

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_widgets()

    def _create_widgets(self):
        self.creation_area = CreationArea(self, title="Crear familia", padding=(3,3,12,12))
        self.creation_area.grid(row=0, column=0, sticky="nsew")
        self.deletion_area = DeletionArea(self, title="Eliminar familia", padding=(3,3,12,12))
        self.deletion_area.grid(row=1, column=0, sticky="nsew")
        self.display = Table(self, header=["Nombre", "Nombre científico"], padding=(12,9,12,12))
        self.display.grid(row=0, column=1, sticky="nsew")
    
    def preload_families(self, families: list[tuple[str,str]]):
        names = []
        for family in families:
            self.display.add_row(family)
            names.append(family[0])
        self.deletion_area.refresh(names)
    
    def on_family_added(self, event: FamilyAdded):
        self.display.add_row([event.name, event.sci_name])
        self.deletion_area.refresh(self.display[:,0])
    
    def on_family_removed(self, event: FamilyRemoved):
        row_index = self.display.index_of(event.name)
        self.display.delete_row(row_index[0])
        self.deletion_area.refresh(self.display[:,0])

class CreationArea(Labelframe):
    name: Entry
    sci_name: Entry
    save: Button

    def __init__(self, *args, title:str, **kwargs):
        super().__init__(*args, text=title, **kwargs)
        self._create_widgets()
        self._resize_behaviour()

    def _create_widgets(self):
        Label(self, text="Nombre").grid(row=0, column=0, sticky="e")
        self.name = Entry(self)
        self.name.grid(row=0, column=1, padx=3, sticky="ew")

        Label(self, text="Nombre científico").grid(row=1, column=0, sticky="e")
        self.sci_name = Entry(self)
        self.sci_name.grid(row=1, column=1, padx=3, sticky="ew")

        self.save = Button(self, text="Añadir")
        self.save.grid(row=2, column=1, pady=(10,0), sticky="nsew")

    def _resize_behaviour(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

class DeletionArea(Labelframe):
    name: Combobox
    delete: Button

    def __init__(self, *args, title:str, **kwargs):
        super().__init__(*args, text=title, **kwargs)
        self._create_widgets()
        self._resize_behaviour()
    
    def refresh(self, family_names: list[str]):
        self._update_options(family_names)
        self.name.set("")
    
    def _update_options(self, family_names: list[str]):
        self.name["values"] = [""] + family_names

    def _create_widgets(self):
        Label(self, text="Nombre").grid(row=0, column=0, sticky="e")
        self.name = Combobox(self, state="readonly")
        self.name.grid(row=0, column=1, padx=3, sticky="ew")

        self.delete = Button(self, text="Eliminar")
        self.delete.grid(row=1, column=1, pady=(10,0), sticky="nsew")

    def _resize_behaviour(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)