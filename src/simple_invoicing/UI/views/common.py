from tkinter.ttk import Entry, Frame
from typing import Sequence, Optional, overload, Literal
from itertools import chain

def _get_range(s: slice, default_stop: int=0) -> range:
    step = s.step if s.step else 1
    start = s.start if s.start else 0
    stop = s.stop if s.stop else default_stop
    return range(start, stop, step)

def _slide_slice(s: slice, n: int=1) -> slice:
    start = s.start + n if s.start else n
    stop = s.stop + n if s.stop else None
    return slice(start, stop, s.step)

class Table(Frame):
    def __init__(self, *args, header: Sequence[str], mode: Literal['normal']|Literal['readonly']='normal', rows: Optional[Sequence[Sequence[str]]]=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_header(header)
        self._mode = mode
        self._preload_rows(rows)         
    
    @property
    def size(self) -> tuple[int, int]:
        '''Returns the size of the table in the form (rows, columns), including the header row'''
        cols, rows = self.grid_size()
        return (rows, cols)
    
    @property
    def header(self) -> list[str]:
        '''Returns a list with the values of the headers'''
        return [entry.get() for entry in self.grid_slaves(row=0)]
    
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
    
    @property
    def mode(self) -> str:
        return self._mode
    
    def grid_slaves(self, row: Optional[int]=None, col: Optional[int]=None) -> list[Entry]:
        '''Returns the Entry widgets in the given row and column, from top to bottom'''
        return super().grid_slaves(row, col)[::-1] #type: ignore ... only Entry widgets are allowed to construct the table

    def _add_header(self, col_values: Sequence[str]):
        '''Adds a header to the table with the given values'''
        for i, item in enumerate(col_values):
            e = Entry(self)
            e.insert(0, item)
            e.state(("disabled",))
            e.grid(row=0, column=i, sticky="e")
    
    def _preload_rows(self, rows: Optional[Sequence[Sequence[str]]]):
        if rows:
            for row in rows:
                self.add_row(row)

    def add_row(self, col_values: Sequence[str]):
        '''Adds a row to the table with the given values'''
        rows, cols = self.size
        for i, item in enumerate(col_values[:cols]):
            e = Entry(self, state=self.mode)
            e.insert(0, item)
            e.grid(row=rows, column=i, sticky="e")
    
    def delete_row(self, row: int):
        '''
        Given a row index, copy all the other row values to a temporary list
        and redraw the table only with these values.
        '''
        values = [values for i, values in enumerate(self.rows) if i != row]
        self._redraw(values)
    
    def index_of(self, value: str) -> tuple[int, int]:
        '''Returns the index of the given value in the table. Raises IndexError if not found.'''
        for c in range(self.size[1]):
            for r in range(self.size[0]):
                if self[r,c] == value:
                    return (r,c)
        raise IndexError(f"'{value}' not found in the table")
    
    def _redraw(self, rows: list[list[str]]):
        '''Redraws the table with the given row values, cleaning the rest of the table'''

        row_values = self._fill_with_none(rows)
        for i, row_val in zip(range(1, self.size[0]), row_values):
            if row_val is None:
                if row := self.grid_slaves(row=i):
                    for entry in row:
                        entry.destroy()
            else:
                for text, cell in zip(row_val, self.grid_slaves(row=i)):
                    cell.delete(0, "end")
                    cell.insert(0, text)
    
    def _fill_with_none(self, rows: list[list[str]]) -> list[list[str]|None]:
        '''Fills rows list with None to match the number of rows cached by the grid manager'''
        empty_rows = [None] * (self.size[0] - len(rows) - 1) # -1 is for ignoring the header
        return rows + empty_rows
     
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
        '''
        Returns the values of the table in the given range, ignoring the header.

        If a single index is given, it returns the values of the row.
        If a single slice is given, it returns the values of the rows.
        If a tuple with two indices is given, it returns the value of the cell.
        If a tuple with a slice and an index is given, it returns the values of the column/row.
        If a tuple with two slices is given, it returns the specific frame of the table.
        
        Negative indices are not supported.
        '''
        rows = _slide_slice(keys[0]) if isinstance(keys[0], slice) else slice(keys[0]+1, keys[0]+2)
        if len(keys) < 2:
            cols = slice(self.size[1])
        else:
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