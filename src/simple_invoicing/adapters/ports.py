from typing import Protocol

class Repository[T](Protocol):

    def add(self, item: T) -> None:
        ...

    def get(self, id: str) -> T:
        ...

    def list(self) -> list[T]:
        ...