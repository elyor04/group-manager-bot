import sqlite3

# Establish database connection
conn = sqlite3.connect("data/bot_data.db")
cursor = conn.cursor()


def initialize_db():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_info (
            chat_id INTEGER,
            user_id INTEGER,
            warnings INTEGER,
            muted INTEGER,
            banned INTEGER
        )
        """
    )
    conn.commit()


def close_db():
    conn.close()
