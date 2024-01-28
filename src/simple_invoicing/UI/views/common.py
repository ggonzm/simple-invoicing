from tkinter.ttk import Entry, Frame
from typing import Sequence, Optional, overload
from itertools import chain

def _get_range(s: slice, default_stop: int=0) -> range:
        step = s.step if s.step else 1
        start = s.start if s.start else 0
        stop = s.stop if s.stop else default_stop
        return range(start, stop, step)

class Table(Frame):
    def __init__(self, *args, col_names: Sequence[str], rows:Optional[Sequence[Sequence[str]]]=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._header(col_names)
        if rows:
            for row in rows:
                self.add_row(row)
    
    @property
    def size(self) -> tuple[int, int]:
        '''Returns the size of the table in the form (rows, columns)'''
        cols, rows = self.grid_size()
        return (rows, cols)
    
    @property
    def rows(self) -> list[list[str]]:
        '''Returns a list with the values of the rows'''
        n_row, _ = self.size
        return [[entry.get() for entry in self.grid_slaves(row=r)] for r in range(1,n_row)]
    
    @property
    def cols(self) -> list[list[str]]:
        '''Returns a list with the values of the columns'''
        _, n_cols = self.size
        return [[entry.get() for entry in self.grid_slaves(col=c)][1:] for c in range(n_cols)]
    
    def grid_slaves(self, row: Optional[int]=None, col: Optional[int]=None) -> list[Entry]:
        '''Returns the Entry widgets in the given row and column, from top to bottom'''
        return super().grid_slaves(row, col)[::-1] #type: ignore ... only Entry widgets are allowed to construct the table

    def _header(self, col_values: Sequence[str]):
        '''Adds a header to the table with the given values'''
        for i, item in enumerate(col_values):
            e = Entry(self)
            e.insert(0, item)
            e.grid(row=0, column=i, sticky="e")

    def add_row(self, col_values: Sequence[str]):
        rows, cols = self.size
        for i, item in enumerate(col_values[:cols]):
            e = Entry(self)
            e.insert(0, item)
            e.grid(row=rows, column=i, sticky="e")

    @overload
    def __getitem__(self, keys: int) -> list[str]:...
    @overload
    def __getitem__(self, keys: slice) -> list[list[str]]:...
    @overload
    def __getitem__(self, keys: tuple[int, int]) -> str:...
    @overload
    def __getitem__(self, keys: tuple[int, slice]) -> list[str]:...
    @overload
    def __getitem__(self, keys: tuple[slice, int]) -> list[str]:...
    @overload
    def __getitem__(self, keys: tuple[slice, slice]) -> list[list[str]]:...
    def __getitem__(self, keys):
        # Negative indices are avoided because they do not make sense in this context.
        if len(keys) < 2:
            rows = keys[0] if isinstance(keys[0], slice) else slice(keys[0], keys[0]+1)
            cols = slice(self.size[1])
        else:
            rows = keys[0] if isinstance(keys[0], slice) else slice(keys[0], keys[0]+1)
            cols = keys[1] if isinstance(keys[1], slice) else slice(keys[1], keys[1]+1)
        rows, cols = _get_range(rows, self.size[0]), _get_range(cols, self.size[1])

        values = [[] for _ in rows]
        for r in rows:
            for c in cols:
                values[r-rows.start].extend([entry.get() for entry in self.grid_slaves(row=r, col=c)])
        
        if all([isinstance(k,slice) for k in keys]):
            return values 
        elif any([isinstance(k,slice) for k in keys]):
            return list(chain.from_iterable(values))
        else:
            return values[0][0]