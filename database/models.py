from .db import cursor, conn


def get_warning_count(chat_id: int, user_id: int) -> int:
    cursor.execute(
        "SELECT warnings FROM user_warnings WHERE chat_id = ? AND user_id = ?",
        (chat_id, user_id),
    )
    result = cursor.fetchone()
    return result[0] if result else 0


def set_warning_count(chat_id: int, user_id: int, warnings: int):
    cursor.execute(
        "INSERT OR REPLACE INTO user_warnings (chat_id, user_id, warnings) VALUES (?, ?, ?)",
        (chat_id, user_id, warnings),
    )
    conn.commit()


def reset_warning_count(chat_id: int, user_id: int):
    cursor.execute(
        "DELETE FROM user_warnings WHERE chat_id = ? AND user_id = ?",
        (chat_id, user_id),
    )
    conn.commit()
