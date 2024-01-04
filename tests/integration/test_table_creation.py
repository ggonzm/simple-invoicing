from src.simple_invoicing.adapters.db_tables import create_categories_table, create_clients_table, create_families_table, create_fruit_trees_table, create_rootstocks_table

def test_create_families_table(in_memory_db):
    create_families_table(in_memory_db)
    assert in_memory_db.execute("SELECT name FROM sqlite_schema").fetchone() == ('families',)

def test_create_fruit_trees_table(in_memory_db):
    create_fruit_trees_table(in_memory_db)
    assert in_memory_db.execute("SELECT name FROM sqlite_schema").fetchone() == ('fruit_trees',)

def test_create_rootstocks_table(in_memory_db):
    create_rootstocks_table(in_memory_db)
    assert in_memory_db.execute("SELECT name FROM sqlite_schema").fetchone() == ('rootstocks',)

def test_create_clients_table(in_memory_db):
    create_clients_table(in_memory_db)
    assert in_memory_db.execute("SELECT name FROM sqlite_schema").fetchone() == ('clients',)

def test_create_categories_table(in_memory_db):
    create_categories_table(in_memory_db)
    assert in_memory_db.execute("SELECT name FROM sqlite_schema").fetchone() == ('categories',)

def test_table_already_exists_error_is_skipped(in_memory_db):
    create_families_table(in_memory_db)
    create_families_table(in_memory_db)
    