import sqlite3
from collections.abc import Set
from typing import Protocol
from src.simple_invoicing.domain.model import Category, FruitTree, Rootstock, Family, Client
from src.simple_invoicing.persistence.snapshot import Snapshot

class Repository[T](Protocol):

    def add(self, item: T) -> None:
        ...

    def get(self, identity: str) -> T:
        ...

    def update(self) -> None:
        ...

    def delete(self, identity: str) -> None:
        ...

    def list(self) -> list[T]:
        ...

class FamilyRepository():
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self._indentity_id: dict[str, int] = {}
        self._snapshots: dict[Family, Snapshot[Family]] = {}

    def add(self, item: Family) -> None:
        self.conn.execute(
            "INSERT INTO families (sci_name, name) VALUES (?, ?)",
            (item.sci_name, item.name),
        )
        if item.rootstocks:
            self._persist_rootstocks(self._get_id(item), item.rootstocks)
        if item.fruit_trees:
            self._persist_fruit_trees(self._get_id(item), item.fruit_trees)

    def get(self, identity: str) -> Family:
        if self._is_already_instantiated(identity):
            for family in self._snapshots.keys():
                if family.name == identity:
                    return family
        return self._load_family_instance(identity)
    
    def _load_family_instance(self, identity: str) -> Family:
        data = self.conn.execute(
                "SELECT id, name, sci_name FROM families WHERE name = ?",
                (identity,),
                ).fetchone()
        self._indentity_id[identity] = data[0]
        family = Family(name=data[1], sci_name=data[2])
        self._load_rootstocks(family)
        self._load_fruit_trees(family)
        self._snapshots[family] = Snapshot(family)
        return family
    
    def _load_fruit_trees(self, family: Family) -> None:
        fruit_trees_data = self.conn.execute(
                """SELECT ft.tag, rs.tag 
                   FROM fruit_trees AS ft 
                   INNER JOIN rootstocks AS rs
                   ON ft.rootstock_id == rs.id
                   WHERE ft.family_id = ?""",
                (self._get_id(family),),
                ).fetchall()
        for row in fruit_trees_data:
            family.add(FruitTree(tag=row[0], rootstock=Rootstock(row[1])))
        
    def _load_rootstocks(self, family: Family) -> None:
        rootstocks_data = self.conn.execute(
                "SELECT tag FROM rootstocks WHERE family_id = ?",
                (self._get_id(family),),
                ).fetchall()
        for row in rootstocks_data:
            family.add(Rootstock(tag=row[0]))

    def update(self) -> None:
        for family, snapshot in self._snapshots.items():
            if not snapshot.is_sync_with(family):
                if snapshot._fruit_trees != family.fruit_trees:
                    self._update_fruit_trees(family, snapshot)
                if snapshot._rootstocks != family.rootstocks:
                    self._update_rootstocks(family, snapshot)
                if snapshot.sci_name != family.sci_name:
                    self._update_family(family)

    def _update_fruit_trees(self, family: Family, snapshot: Snapshot[Family]) -> None:
        to_remove = snapshot._fruit_trees - family.fruit_trees
        to_add = family.fruit_trees - snapshot._fruit_trees
        if to_add:
            self._persist_fruit_trees(self._get_id(family), to_add)
        if to_remove:
            self._delete_fruit_trees(self._get_id(family), to_remove)

    def _update_rootstocks(self, family: Family, snapshot: Snapshot[Family]) -> None:
        to_remove = snapshot._rootstocks - family.rootstocks
        to_add = family.rootstocks - snapshot._rootstocks
        if to_add:
            self._persist_rootstocks(self._get_id(family), to_add)
        if to_remove:
            self._delete_rootstocks(self._get_id(family), to_remove)

    def _update_family(self, family: Family) -> None:
        self.conn.execute(
                "UPDATE families SET sci_name = ? WHERE name = ?",
                (family.sci_name, family.name),
                )

    def _is_already_instantiated(self, identity: str) -> bool:
        return self._indentity_id.get(identity) is not None

    def _get_id(self, family: Family) -> int:
        if not self._is_already_instantiated(family.name):
            id =  self.conn.execute(
                    "SELECT id FROM families WHERE name = ?",
                    (family.name,),
                    ).fetchone()[0]
            self._indentity_id[family.name] = id
        return self._indentity_id[family.name]
    
    def _persist_rootstocks(self, family_id: int, rootstocks: Set[Rootstock]) -> None:
        values = ''
        for rootstock in rootstocks:
            values += f"('{rootstock.tag}', {family_id}), "
        self.conn.execute(f"INSERT INTO rootstocks (tag, family_id) VALUES {values[:-2]}")
    
    def _delete_rootstocks(self, family_id: int, rootstocks: Set[Rootstock]) -> None:
        values = ''
        for rootstock in rootstocks:
            values += f"('{rootstock.tag}', {family_id}), "
        self.conn.execute(f"DELETE FROM rootstocks WHERE (tag, family_id) IN ({values[:-2]})")
    
    def _persist_fruit_trees(self, family_id: int, fruit_trees: Set[FruitTree]) -> None:
        values = ''
        rootstock_ids = self._get_rootstock_ids(family_id)
        for fruit_tree in fruit_trees:
            values += f"('{fruit_tree.tag}', {rootstock_ids[fruit_tree.rootstock.tag]}, {family_id}), "
        self.conn.execute(f"INSERT INTO fruit_trees (tag, rootstock_id, family_id) VALUES {values[:-2]}")

    def _delete_fruit_trees(self, family_id: int, fruit_trees: Set[FruitTree]) -> None:
        values = ''
        rootstock_ids = self._get_rootstock_ids(family_id)
        for fruit_tree in fruit_trees:
            values += f"('{fruit_tree.tag}', {rootstock_ids[fruit_tree.rootstock.tag]}, {family_id}), "
        self.conn.execute(f"DELETE FROM fruit_trees WHERE (tag, rootstock_id, family_id) IN ({values[:-2]})")
    
    def _get_rootstock_ids(self, family_id: int) -> dict[str, int]:
        rootstocks_data = self.conn.execute(
                "SELECT tag, id FROM rootstocks WHERE family_id = ?",
                (family_id,),
                ).fetchall()
        return dict(rootstocks_data)
    
    def delete(self, identity: str) -> None:
        self.conn.execute(
                "DELETE FROM families WHERE name = ?",
                (identity,),
        )

    def list(self) -> list[Family]:
        data = self.conn.execute(
                "SELECT name, sci_name FROM families",
                ).fetchall()
        families = [Family(name=row[0], sci_name=row[1]) for row in data]
        for family in families:
            self._load_rootstocks(family)
            self._load_fruit_trees(family)
        return families