from typing import Any
from copy import deepcopy
from dataclasses import FrozenInstanceError

class Snapshot[T]():
    __slots__ = ['_entity']
    _entity: T
    
    def __init__(self, entity: T) -> None:
        super().__setattr__('_entity', deepcopy(entity))

    def is_sync_with(self, other: object) -> bool:
        if not isinstance(other, self._entity.__class__):
            return False
        return self._entity.__dict__ == other.__dict__
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == '_entity' and self._entity is None:
            super().__setattr__('_entity', __value)
        raise FrozenInstanceError("Cannot modify a snapshot")
    
    def __delattr__(self, __name: str) -> None:
        raise FrozenInstanceError("Cannot modify a snapshot")
    
    def __getattribute__(self, __name: str) -> Any:
        if __name == '_entity':
            return super().__getattribute__('_entity')
        elif __name in self._entity.__dict__ or __name == '__dict__':
            return self._entity.__getattribute__(__name)
        return super().__getattribute__(__name)
    
    def __repr__(self) -> str:
        attrs = ''
        for key, value in self._entity.__dict__.items():
            if not key.startswith('_'):
                attrs += f"{key}='{value}', "
        return f"Snapshot(type='{self._entity.__class__.__name__}', {attrs[:-2]})"

