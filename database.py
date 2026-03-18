# database.py
import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "tarefas.db")

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    from models import CREATE_TABLES
    with get_db_connection() as conn:
        conn.executescript(CREATE_TABLES)
        conn.commit()

        