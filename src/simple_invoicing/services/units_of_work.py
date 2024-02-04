from __future__ import annotations

from src.simple_invoicing.persistence.repositories import Repository, FamilyRepository
from src.simple_invoicing.persistence.db import default_conn_factory
from src.simple_invoicing.persistence.db import Connection
from src.simple_invoicing.domain.model import Family
from typing import Callable

class UnitOfWork[T]():
    repo: Repository[T]

    def __enter__(self) -> UnitOfWork[T]:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        raise NotImplementedError


class FamilyUnitOfWork(UnitOfWork[Family]):
    def __init__(self, conn_factory: Callable[[], Connection] = default_conn_factory) -> None:
        self.conn = conn_factory()
        self.repo = FamilyRepository(self.conn)
    
    def __enter__(self) -> FamilyUnitOfWork:
        return self

    def commit(self) -> None:
        self.repo.update()
        self.conn.commit()
    
    def rollback(self) -> None:
        self.conn.rollback()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.conn.rollback()
        self.conn.close()