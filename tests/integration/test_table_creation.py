from src.simple_invoicing.adapters.db_tables import create_categories_table, create_clients_table, create_families_table, create_fruit_trees_table, create_rootstocks_table, create_intermediate_tables
import pytest
import sqlite3

@pytest.fixture
def empty_in_memory_db():
    return sqlite3.connect(":memory:")

def test_create_families_table(empty_in_memory_db):
    create_families_table(empty_in_memory_db)
    assert empty_in_memory_db.execute("SELECT name FROM sqlite_schema").fetchone() == ('families',)
    try:
        empty_in_memory_db.execute("SELECT id, name, sci_name FROM families").fetchone()
    except sqlite3.OperationalError as e:
        pytest.fail(f'{e}')

def test_create_fruit_trees_table(empty_in_memory_db):
    create_fruit_trees_table(empty_in_memory_db)
    assert empty_in_memory_db.execute("SELECT name FROM sqlite_schema").fetchone() == ('fruit_trees',)
    try:
        empty_in_memory_db.execute("SELECT id, tag, rootstock_id, family_id FROM fruit_trees").fetchone()
    except sqlite3.OperationalError as e:
        pytest.fail(f'{e}')

def test_create_rootstocks_table(empty_in_memory_db):
    create_rootstocks_table(empty_in_memory_db)
    assert empty_in_memory_db.execute("SELECT name FROM sqlite_schema").fetchone() == ('rootstocks',)
    try:
        empty_in_memory_db.execute("SELECT id, tag, family_id FROM rootstocks").fetchone()
    except sqlite3.OperationalError as e:
        pytest.fail(f'{e}')

def test_create_clients_table(empty_in_memory_db):
    create_clients_table(empty_in_memory_db)
    assert empty_in_memory_db.execute("SELECT name FROM sqlite_schema").fetchone() == ('clients',)
    try:
        empty_in_memory_db.execute("SELECT id, dni_nif, name, tax_name, location, address, zip_code, phone FROM clients").fetchone()
    except sqlite3.OperationalError as e:
        pytest.fail(f'{e}')

def test_create_categories_table(empty_in_memory_db):
    create_categories_table(empty_in_memory_db)
    assert empty_in_memory_db.execute("SELECT name FROM sqlite_schema").fetchone() == ('categories',)
    try:
        empty_in_memory_db.execute("SELECT id, path, parent_id FROM categories").fetchone()
    except sqlite3.OperationalError as e:
        pytest.fail(f'{e}')

def test_create_intermediate_tables(empty_in_memory_db):
    create_fruit_trees_table(empty_in_memory_db)
    create_rootstocks_table(empty_in_memory_db)
    create_categories_table(empty_in_memory_db)   #Needed to avoid foreign key errors
    create_intermediate_tables(empty_in_memory_db)
    query = empty_in_memory_db.execute("SELECT name FROM sqlite_schema").fetchall()
    assert ('fruit_trees2categories',) in query
    assert ('rootstocks2categories',) in query
    try:
        empty_in_memory_db.execute("SELECT product_id, category_id FROM fruit_trees2categories").fetchone()
        empty_in_memory_db.execute("SELECT product_id, category_id FROM rootstocks2categories").fetchone()
    except sqlite3.OperationalError as e:
        pytest.fail(f'{e}')


def test_table_already_exists_error_is_skipped(empty_in_memory_db):
    try:
        create_families_table(empty_in_memory_db)
        create_families_table(empty_in_memory_db)
    except sqlite3.OperationalError:
        pytest.fail("create_families_table raised an OperationalError")