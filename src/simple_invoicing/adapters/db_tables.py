import sqlite3


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
            hash INTEGER PRIMARY KEY,
            sci_name TEXT NOT NULL,
            name TEXT NOT NULL
        )
        """,
    )


def create_fruit_trees_table(conn: sqlite3.Connection) -> None:
    _create(
        conn,
        """
        CREATE TABLE fruit_trees (
            hash INTEGER PRIMARY KEY,
            tag TEXT NOT NULL,
            family_hash INTEGER NOT NULL,
            rootstock_hash INTEGER,
            FOREIGN KEY (family_hash) REFERENCES families(hash),
            FOREIGN KEY (rootstock_hash) REFERENCES rootstocks(hash)
        )
        """,
    )


def create_rootstocks_table(conn: sqlite3.Connection) -> None:
    _create(
        conn,
        """
        CREATE TABLE rootstocks (
            hash INTEGER PRIMARY KEY,
            tag TEXT NOT NULL,
            family_hash INTEGER NOT NULL,
            FOREIGN KEY (family_hash) REFERENCES families(hash)
        )
        """,
    )


def create_clients_table(conn: sqlite3.Connection) -> None:
    _create(
        conn,
        """
        CREATE TABLE clients (
            hash INTEGER PRIMARY KEY,
            dni_nif TEXT NOT NULL,
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
            hash INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            parent_hash INTEGER,
            FOREIGN KEY (parent_hash) REFERENCES categories(hash)
        )
        """,
    )


def create_intermediate_tables(conn: sqlite3.Connection) -> None:
    _create(
        conn,
        """
        CREATE TABLE fruit_trees2categories (
            product_hash INTEGER NOT NULL,
            category_hash INTEGER NOT NULL,
            FOREIGN KEY (product_hash) REFERENCES fruit_trees(hash),
            FOREIGN KEY (category_hash) REFERENCES category(hash)
        )
        """,
    )
    _create(
        conn,
        """
        CREATE TABLE rootstocks2categories (
            product_hash INTEGER NOT NULL,
            category_hash INTEGER NOT NULL,
            FOREIGN KEY (product_hash) REFERENCES rootstocks(hash),
            FOREIGN KEY (category_hash) REFERENCES category(hash)
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
