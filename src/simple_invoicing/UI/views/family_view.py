from __future__ import annotations
from tkinter.ttk import Frame, Label, Entry, Button, Style, Treeview, Scrollbar, Combobox, Notebook, Progressbar, Separator, Labelframe
from dataclasses import dataclass
from src.simple_invoicing.UI.models.events import FamilyAdded
from src.simple_invoicing.UI.views.common import Table

class FamilyView(Frame):
    creation_area: _CreationArea
    display: Table

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_widgets()

    def _create_widgets(self):
        self.creation_area = _CreationArea(self, title="Crear familia", padding=(3,3,12,12))
        self.creation_area.grid(row=0, column=0, sticky="nsew")
        self.display = Table(self, col_names=["Nombre", "Nombre científico"], padding=(3,3,12,12), style="debug.TFrame")
        self.display.grid(row=0, column=1, sticky="nsew")

    def on_family_added(self, event: FamilyAdded):
        self.display.add_row([event.name, event.sci_name])


class _CreationArea(Labelframe):
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