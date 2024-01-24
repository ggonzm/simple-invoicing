from __future__ import annotations

from typing import Callable, Protocol
from src.simple_invoicing.UI.models.events import Event

class SupportsObserver(Protocol):
    def subscribe(self, event: Event, fn: Callable) -> None:
        ...

    def trigger_event(self, event: Event) -> None:
        ...

    def unsubscribe(self, event: Event, fn: Callable) -> None:
        ...

class Observable():
    def __init__(self):
        self.listeners: dict[type[Event], list[Callable]] = {}

    def subscribe(self, event: Event, fn: Callable) -> None:
        if self.listeners.get(type(event)) is None:
            self.listeners[type(event)] = []
        self.listeners[type(event)].append(fn)

    def trigger_event(self, event: Event) -> None:
        for fn in self.listeners.get(type(event), []):
            fn()
    
    def unsubscribe(self, event: Event, fn: Callable) -> None:
        if self.listeners.get(type(event)) is None:
            return
        self.listeners[type(event)].remove(fn)