import sqlite3
from src.simple_invoicing.config import get_sqlite_database_uri


def _create(conn: sqlite3.Connection, sql: str):
    try:
        conn.execute(sql)
    except sqlite3.OperationalError as e:
        # Most of the errors raised are OperationalErrors, but I only want to ignore the ones related to the table already existing
        if not all(substr in str(e) for substr in ["table", "already exists"]):
            conn.rollback()
            raise e
    else:
        conn.commit()


def create_families_table(conn: sqlite3.Connection) -> None:
    _create(
        conn,
        """
        CREATE TABLE families (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sci_name TEXT NOT NULL,
            name TEXT NOT NULL UNIQUE
        )
        """,
    )


def create_fruit_trees_table(conn: sqlite3.Connection) -> None:
    _create(
        conn,
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


def create_rootstocks_table(conn: sqlite3.Connection) -> None:
    _create(
        conn,
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


def create_clients_table(conn: sqlite3.Connection) -> None:
    _create(
        conn,
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


def create_categories_table(conn: sqlite3.Connection) -> None:
    _create(
        conn,
        """
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE
        )
        """,
    )


def create_intermediate_tables(conn: sqlite3.Connection) -> None:
    _create(
        conn,
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
    _create(
        conn,
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


def create_all_tables(conn: sqlite3.Connection) -> None:
    create_families_table(conn)
    create_fruit_trees_table(conn)
    create_rootstocks_table(conn)
    create_clients_table(conn)
    create_categories_table(conn)
    create_intermediate_tables(conn)


def default_conn_factory() -> sqlite3.Connection:
    con = sqlite3.connect(get_sqlite_database_uri(), uri=True)
    con.execute("PRAGMA foreign_keys = ON")
    return con