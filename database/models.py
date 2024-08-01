from .db import cursor, conn


def get_warning_count(chat_id: int, user_id: int) -> int:
    cursor.execute(
        "SELECT warnings FROM user_info WHERE chat_id = ? AND user_id = ?",
        (chat_id, user_id),
    )
    result = cursor.fetchone()
    return result[0] if result else 0


def set_warning_count(chat_id: int, user_id: int, warnings: int):
    muted = get_muted_count(chat_id, user_id)
    banned = get_banned_count(chat_id, user_id)

    cursor.execute(
        "INSERT OR REPLACE INTO user_info (chat_id, user_id, warnings, muted, banned) VALUES (?, ?, ?, ?, ?)",
        (chat_id, user_id, warnings, muted, banned),
    )
    conn.commit()


def get_muted_count(chat_id: int, user_id: int) -> int:
    cursor.execute(
        "SELECT muted FROM user_info WHERE chat_id = ? AND user_id = ?",
        (chat_id, user_id),
    )
    result = cursor.fetchone()
    return result[0] if result else 0


def set_muted_count(chat_id: int, user_id: int, muted: int):
    warnings = get_warning_count(chat_id, user_id)
    banned = get_banned_count(chat_id, user_id)

    cursor.execute(
        "INSERT OR REPLACE INTO user_info (chat_id, user_id, warnings, muted, banned) VALUES (?, ?, ?, ?, ?)",
        (chat_id, user_id, warnings, muted, banned),
    )
    conn.commit()


def get_banned_count(chat_id: int, user_id: int) -> int:
    cursor.execute(
        "SELECT banned FROM user_info WHERE chat_id = ? AND user_id = ?",
        (chat_id, user_id),
    )
    result = cursor.fetchone()
    return result[0] if result else 0


def set_banned_count(chat_id: int, user_id: int, banned: int):
    warnings = get_warning_count(chat_id, user_id)
    muted = get_muted_count(chat_id, user_id)

    cursor.execute(
        "INSERT OR REPLACE INTO user_info (chat_id, user_id, warnings, muted, banned) VALUES (?, ?, ?, ?, ?)",
        (chat_id, user_id, warnings, muted, banned),
    )
    conn.commit()
