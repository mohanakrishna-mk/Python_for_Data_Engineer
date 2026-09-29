import sqlite3
from contextlib import contextmanager


DATABASE = "expenses.db"


@contextmanager
def get_connection():

    connection = sqlite3.connect(DATABASE)

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def create_tables():

    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        """)