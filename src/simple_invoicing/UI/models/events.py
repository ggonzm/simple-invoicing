from dataclasses import dataclass

class Event():
    pass

@dataclass(frozen=True)
class FamilyAdded(Event):
    name: str
    sci_name: str