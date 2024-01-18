from src.simple_invoicing.persistence.snapshot import Snapshot
from src.simple_invoicing.domain.model import Family
from dataclasses import FrozenInstanceError
import pytest

def test_snapshot_represents_an_entity_state_but_being_immutable(families):
    family1, _ = families
    snapshot = Snapshot(family1)

    assert snapshot.__dict__ == family1.__dict__
    assert not snapshot == family1 and snapshot is not family1
    assert snapshot.is_sync_with(family1)

    family1.sci_name = "Malus domestica2"
    with pytest.raises(FrozenInstanceError):
        setattr(snapshot, "sci_name", "Malus domestica2")
    assert not snapshot.is_sync_with(family1)