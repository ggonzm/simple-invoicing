from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Event():
    pass

@dataclass(frozen=True, slots=True)
class FamilyAdded(Event):
    name: str
    sci_name: str