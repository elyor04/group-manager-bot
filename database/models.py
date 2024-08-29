from .db import cursor, conn


def create_if_not_exists(chat_id: int, user_id: int):
    cursor.execute(
        "SELECT * FROM user_info WHERE chat_id = ? AND user_id = ?",
        (chat_id, user_id),
    )

    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO user_info (chat_id, user_id, warnings, muted, banned, messages) VALUES (?, ?, ?, ?, ?, ?)",
            (chat_id, user_id, 0, 0, 0, 0),
        )
        conn.commit()


def get_warning_count(chat_id: int, user_id: int) -> int:
    cursor.execute(
        "SELECT warnings FROM user_info WHERE chat_id = ? AND user_id = ?",
        (chat_id, user_id),
    )
    result = cursor.fetchone()
    return result[0] if result else 0


def set_warning_count(chat_id: int, user_id: int, warnings: int):
    create_if_not_exists(chat_id, user_id)

    cursor.execute(
        "UPDATE user_info SET warnings = ? WHERE chat_id = ? AND user_id = ?",
        (warnings, chat_id, user_id),
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
    create_if_not_exists(chat_id, user_id)

    cursor.execute(
        "UPDATE user_info SET muted = ? WHERE chat_id = ? AND user_id = ?",
        (muted, chat_id, user_id),
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
    create_if_not_exists(chat_id, user_id)

    cursor.execute(
        "UPDATE user_info SET banned = ? WHERE chat_id = ? AND user_id = ?",
        (banned, chat_id, user_id),
    )
    conn.commit()


def get_message_count(chat_id: int, user_id: int) -> int:
    cursor.execute(
        "SELECT messages FROM user_info WHERE chat_id = ? AND user_id = ?",
        (chat_id, user_id),
    )
    result = cursor.fetchone()
    return result[0] if result else 0


def set_message_count(chat_id: int, user_id: int, messages: int):
    create_if_not_exists(chat_id, user_id)

    cursor.execute(
        "UPDATE user_info SET messages = ? WHERE chat_id = ? AND user_id = ?",
        (messages, chat_id, user_id),
    )
    conn.commit()
