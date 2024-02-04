import sqlite3
from typing import Self
from functools import wraps
from src.simple_invoicing.persistence.exceptions import TableAlreadyExists, UniqueConstraintError
from src.simple_invoicing.config import get_sqlite_database_uri

class Connection:
    '''Sqlite3 connection wrapper in order to make some generic sqlite3 exceptions more specific'''

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
    
    @classmethod
    def connect(cls, database: str|bytes, *args, uri:bool=False, **kwargs):
        conn = sqlite3.connect(database, uri=uri)
        conn.execute("PRAGMA foreign_keys = ON")
        return cls(conn)

    def execute(self, __sql: str, __parameters: ... = ()) -> sqlite3.Cursor:
        try:
            return self._conn.execute(__sql, __parameters)
        except Exception as e:
            self.rollback()
            if isinstance(e, sqlite3.OperationalError):
                if all(substr in str(e) for substr in ["table", "already exists"]):
                    raise TableAlreadyExists(str(e))
            elif isinstance(e, sqlite3.IntegrityError):
                if "UNIQUE constraint failed" in str(e):
                    raise UniqueConstraintError(str(e))
            raise e
    
    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()

def ignore(exc_type: type[Exception]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except exc_type:
                pass
        return wrapper
    return decorator

@ignore(TableAlreadyExists)
def create_families_table(conn: Connection) -> None:
    conn.execute(
        """
        CREATE TABLE families (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sci_name TEXT NOT NULL,
            name TEXT NOT NULL UNIQUE
        )
        """,
    )

@ignore(TableAlreadyExists)
def create_fruit_trees_table(conn: Connection) -> None:
    conn.execute(
        """
        CREATE TABLE fruit_trees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT NOT NULL,
            rootstock_id INTEGER,
            family_id INTEGER,
            UNIQUE (tag, rootstock_id, family_id),
            FOREIGN KEY (rootstock_id) REFERENCES rootstocks(id) ON DELETE CASCADE,
            FOREIGN KEY (family_id) REFERENCES families(id) ON DELETE CASCADE
        )
        """,
    )

@ignore(TableAlreadyExists)
def create_rootstocks_table(conn: Connection) -> None:
    conn.execute(
        """
        CREATE TABLE rootstocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT NOT NULL,
            family_id INTEGER,
            UNIQUE (tag, family_id),
            FOREIGN KEY (family_id) REFERENCES families(id) ON DELETE CASCADE
        )
        """,
    )

@ignore(TableAlreadyExists)
def create_clients_table(conn: Connection) -> None:
    conn.execute(
        """
        CREATE TABLE clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni_nif TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            tax_name TEXT NOT NULL,
            location TEXT NOT NULL,
            address TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            phone TEXT
        )
        """,
    )

@ignore(TableAlreadyExists)
def create_categories_table(conn: Connection) -> None:
    conn.execute(
        """
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE
        )
        """,
    )

@ignore(TableAlreadyExists)
def create_intermediate_tables(conn: Connection) -> None:
    conn.execute(
        """
        CREATE TABLE fruit_trees2categories (
            product_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            PRIMARY KEY(product_id, category_id),
            FOREIGN KEY (product_id) REFERENCES fruit_trees(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        )
        """,
    )
    conn.execute(
        """
        CREATE TABLE rootstocks2categories (
            product_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            PRIMARY KEY(product_id, category_id),
            FOREIGN KEY (product_id) REFERENCES rootstocks(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        )
        """,
    )


def create_all_tables(conn: Connection) -> None:
    create_families_table(conn)
    create_fruit_trees_table(conn)
    create_rootstocks_table(conn)
    create_clients_table(conn)
    create_categories_table(conn)
    create_intermediate_tables(conn)


def default_conn_factory() -> Connection:
    con = sqlite3.connect(get_sqlite_database_uri(), uri=True)
    con.execute("PRAGMA foreign_keys = ON")
    return Connection(con)