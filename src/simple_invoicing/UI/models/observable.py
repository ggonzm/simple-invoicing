from __future__ import annotations

from typing import Callable, Protocol
from src.simple_invoicing.UI.models.events import Event

class SupportsObserver(Protocol):
    def subscribe(self, event_type: type[Event], fn: Callable[..., None]) -> None:
        ...

    def trigger_event(self, event: Event) -> None:
        ...

class Observable():
    def __init__(self):
        self.listeners: dict[type[Event], list[Callable]] = {}

    def subscribe(self, event_type: type[Event], fn: Callable[..., None]) -> None:
        if self.listeners.get(event_type) is None:
            self.listeners[event_type] = []
        self.listeners[event_type].append(fn)

    def trigger_event(self, event: Event) -> None:
        for fn in self.listeners.get(type(event), []):
            fn(event)