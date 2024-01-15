import sqlite3
from src.simple_invoicing.domain.model import Category, FruitTree, Rootstock, Family, Client


class FamilyRepository():
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self._id_cache: dict[Family, int] = {}

    def add(self, family: Family) -> None:
        self.conn.execute(
            "INSERT INTO families (sci_name, name) VALUES (?, ?)",
            (family.sci_name, family.name),
        )
        if family.rootstocks:
            self._persist_rootstocks(family)
        if family.fruit_trees:
            self._persist_fruit_trees(family)

    def get(self, name: str) -> Family:
        data = self.conn.execute(
                "SELECT name, sci_name FROM families WHERE name = ?",
                (name,),
                ).fetchone()
        family = Family(name=data[0], sci_name=data[1])
        self._load_rootstocks(family)
        self._load_fruit_trees(family)
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

    def _get_id(self, family: Family) -> int:
        if self._id_cache.get(family) is None:
            id =  self.conn.execute(
                    "SELECT id FROM families WHERE name = ?",
                    (family.name,),
                    ).fetchone()[0]
            self._id_cache[family] = id
        return self._id_cache[family]
    
    def _persist_rootstocks(self, family: Family) -> None:
        values = ''
        for rootstock in family.rootstocks:
            values += f"('{rootstock.tag}', {self._get_id(family)}), "
        self.conn.execute(f"INSERT INTO rootstocks (tag, family_id) VALUES {values[:-2]}")
    
    def _persist_fruit_trees(self, family: Family) -> None:
        values = ''
        rootstock_ids = self._get_rootstock_ids(family)
        for fruit_tree in family.fruit_trees:
            values += f"('{fruit_tree.tag}', {rootstock_ids[fruit_tree.rootstock.tag]}, {self._get_id(family)}), "
        self.conn.execute(f"INSERT INTO fruit_trees (tag, rootstock_id, family_id) VALUES {values[:-2]}")
    
    def _get_rootstock_ids(self, family: Family) -> dict[str, int]:
        rootstocks_data = self.conn.execute(
                "SELECT tag, id FROM rootstocks WHERE family_id = ?",
                (self._get_id(family),),
                ).fetchall()
        return dict(rootstocks_data)
        
    def list(self) -> list[Family]:
        data = self.conn.execute(
                "SELECT name, sci_name FROM families",
                ).fetchall()
        families = [Family(name=row[0], sci_name=row[1]) for row in data]
        for family in families:
            self._load_rootstocks(family)
            self._load_fruit_trees(family)
        return families