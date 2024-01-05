import sqlite3
from src.simple_invoicing.domain.model import Category, FruitTree, Rootstock, Family, Client


class FamilyRepository():
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def add(self, item: Family) -> None:
        self.conn.execute(
            "INSERT INTO families (hash, sci_name, name) VALUES (?, ?, ?)",
            (hash(item), item.sci_name, item.name),
        )

    def get(self, name: str) -> Family:
        data = self.conn.execute(
                "SELECT name, sci_name FROM families WHERE name = ?",
                (name,),
                ).fetchone()
        return Family(name=data[0], sci_name=data[1])

    def list(self) -> list[Family]:
        data = self.conn.execute(
                "SELECT name, sci_name FROM families",
                ).fetchall()
        families: list[Family] = []
        for row in data:
            families.append(Family(name=row[0], sci_name=row[1]))
        return families

class RootstockRepository():
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def add(self, item: Rootstock) -> None:
        self.conn.execute(
            "INSERT INTO rootstocks (hash, tag, family_hash) VALUES (?, ?, ?)",
            (hash(item), item.tag, hash(item.family)),
        )

    def get(self, tag: str) -> Rootstock:
        data = self.conn.execute(
                "SELECT tag, family_hash FROM rootstocks WHERE tag = ?",
                (tag,),
                ).fetchone()
        family_data = self.conn.execute(
                "SELECT name, sci_name FROM families WHERE hash = ?",
                (data[1],),
                ).fetchone()
        return Rootstock(tag=data[0], family=Family(name=family_data[0], sci_name=family_data[1]))

    def list(self) -> list[Rootstock]:
        data = self.conn.execute(
                "SELECT tag, family_hash FROM rootstocks",
                ).fetchall()
        rootstocks: list[Rootstock] = []
        for row in data:
            family_data = self.conn.execute(
                "SELECT name, sci_name FROM families WHERE hash = ?",
                (row[1],),
                ).fetchone()
            rootstocks.append(Rootstock(tag=row[0], family=Family(name=family_data[0], sci_name=family_data[1])))
        return rootstocks

class FruitTreeRepository():
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def add(self, item: FruitTree) -> None:
        self.conn.execute(
            "INSERT INTO fruit_trees (hash, tag, family_hash, rootstock_hash) VALUES (?, ?, ?, ?)",
            (hash(item), item.tag, hash(item.family), hash(item.rootstock) if item.rootstock else None),
        )

    def get(self, tag: str) -> FruitTree:
        data = self.conn.execute(
                "SELECT tag, family_hash, rootstock_hash FROM fruit_trees WHERE tag = ?",
                (tag,),
                ).fetchone()
        family_data = self.conn.execute(
                "SELECT name, sci_name FROM families WHERE hash = ?",
                (data[1],),
                ).fetchone()
        family = Family(name=family_data[0], sci_name=family_data[1])
        rootstock_data = self.conn.execute(
                "SELECT tag, family_hash FROM rootstocks WHERE hash = ?",
                (data[2],),
                ).fetchone()
        rootstock = Rootstock(tag=rootstock_data[0], family=Family(name=family_data[0], sci_name=family_data[1])) if rootstock_data else None
        return FruitTree(tag=data[0], family=family, rootstock=rootstock)
    
    def list(self) -> list[FruitTree]:
        data = self.conn.execute(
                "SELECT tag, family_hash, rootstock_hash FROM fruit_trees",
                ).fetchall()
        fruit_trees: list[FruitTree] = []
        for row in data:
            family_data = self.conn.execute(
                "SELECT name, sci_name FROM families WHERE hash = ?",
                (row[1],),
                ).fetchone()
            family = Family(name=family_data[0], sci_name=family_data[1])
            rootstock_data = self.conn.execute(
                "SELECT tag, family_hash FROM rootstocks WHERE hash = ?",
                (row[2],),
                ).fetchone()
            rootstock = Rootstock(tag=rootstock_data[0], family=Family(name=family_data[0], sci_name=family_data[1])) if rootstock_data else None
            fruit_trees.append(FruitTree(tag=row[0], family=family, rootstock=rootstock))
        return fruit_trees