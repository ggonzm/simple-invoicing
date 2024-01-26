from __future__ import annotations
from tkinter.ttk import Frame, Label, Entry, Button, Style, Treeview, Scrollbar, Combobox, Notebook, Progressbar, Separator, Labelframe
from dataclasses import dataclass
from src.simple_invoicing.UI.models.events import FamilyAdded

class FamilyView(Frame):
    creation_area: _CreationArea
    display: _Display

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_widgets()

    def _create_widgets(self):
        self.creation_area = _CreationArea(self, title="Crear familia", padding=(3,3,12,12))
        self.creation_area.grid(row=0, column=0, sticky="nsew")
        self.display = _Display(self, padding=(3,3,12,12), style="debug.TFrame")
        self.display.grid(row=0, column=1, sticky="nsew")


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

class _Display(Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_widgets()
        self._resize_behaviour()

    def _create_widgets(self):
        Label(self, text="Familia").grid(row=0, column=1, sticky="e", padx=12)
        Label(self, text="Nombre científico").grid(row=0, column=2, sticky="e", padx=12)
        Label(self, text="Portainjertos").grid(row=0, column=3, sticky="e", padx=12)
        Label(self, text="Árboles").grid(row=0, column=4, sticky="e", padx=12)
    
    def show_family(self, name: str, sci_name: str) -> None:
        rows , cols = self.grid_size()
        Button(self, text=name, state='pressed').grid(row=rows + 1, column=0, sticky="ew")
        Button(self, text=sci_name, state='pressed').grid(row=rows + 1, column=cols + 2, sticky="ew")

    def _resize_behaviour(self):
        pass
