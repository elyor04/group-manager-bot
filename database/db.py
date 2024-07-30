import sqlite3
from config import DB_PATH

# Establish database connection
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


def initialize_db():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_warnings (
            chat_id INTEGER,
            user_id INTEGER,
            warnings INTEGER,
            PRIMARY KEY (chat_id, user_id)
        )
        """
    )
    conn.commit()


def close_db():
    conn.close()
