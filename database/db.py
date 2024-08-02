import sqlite3
from config import DB_PATH

# Establish database connection
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


def initialize_db():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_info (
            chat_id INTEGER,
            user_id INTEGER,
            username VARCHAR(100),
            warnings INTEGER,
            muted INTEGER,
            banned INTEGER,
            PRIMARY KEY (chat_id, user_id)
        )
        """
    )
    conn.commit()


def close_db():
    conn.close()
