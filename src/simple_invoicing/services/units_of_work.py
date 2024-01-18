from __future__ import annotations

from src.simple_invoicing.persistence.repositories import Repository, FamilyRepository
from src.simple_invoicing.persistence.db import default_conn_factory
from typing import Protocol, Callable
import sqlite3

class UnitOfWork[T](Protocol):

    def __enter__(self) -> UnitOfWork[T]:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        ...


class FamilyUnitOfWork():
    def __init__(self, conn_factory: Callable[[], sqlite3.Connection] = default_conn_factory) -> None:
        self.conn = conn_factory()
        self.families = FamilyRepository(self.conn)
    
    def __enter__(self) -> FamilyUnitOfWork:
        return self

    def commit(self) -> None:
        self.families.update()
        self.conn.commit()
    
    def rollback(self) -> None:
        self.conn.rollback()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.conn.rollback()
        self.conn.close()