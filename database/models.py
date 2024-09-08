from .db import UserInfo, session


def get_user_info(chat_id: int, user_id: int):
    user_info = (
        session.query(UserInfo).filter_by(chat_id=chat_id, user_id=user_id).first()
    )

    if not user_info:
        user_info = UserInfo(
            chat_id=chat_id, user_id=user_id, warnings=0, muted=0, banned=0, messages=0
        )
        session.add(user_info)
        session.commit()

    return user_info


def get_warning_count(chat_id: int, user_id: int) -> int:
    user_info = get_user_info(chat_id, user_id)
    return user_info.warnings


def set_warning_count(chat_id: int, user_id: int, warnings: int):
    user_info = get_user_info(chat_id, user_id)
    user_info.warnings = warnings
    session.commit()


def get_muted_count(chat_id: int, user_id: int) -> int:
    user_info = get_user_info(chat_id, user_id)
    return user_info.muted


def set_muted_count(chat_id: int, user_id: int, muted: int):
    user_info = get_user_info(chat_id, user_id)
    user_info.muted = muted
    session.commit()


def get_banned_count(chat_id: int, user_id: int) -> int:
    user_info = get_user_info(chat_id, user_id)
    return user_info.banned


def set_banned_count(chat_id: int, user_id: int, banned: int):
    user_info = get_user_info(chat_id, user_id)
    user_info.banned = banned
    session.commit()


def get_message_count(chat_id: int, user_id: int) -> int:
    user_info = get_user_info(chat_id, user_id)
    return user_info.messages


def set_message_count(chat_id: int, user_id: int, messages: int):
    user_info = get_user_info(chat_id, user_id)
    user_info.messages = messages
    session.commit()
