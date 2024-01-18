import os

def get_sqlite_database_uri() -> str:
    path = os.environ.get("SQLITE_DATABASE_PATH")
    uri = "file:" + path + "?mode=rw" if path else "file:src/simple_invoicing/persistence/sqlite.db?mode=rw"
    return uri