from app.database.models import UserInfo


async def get_user_info(chat_id: int, user_id: int):
    user_info = await UserInfo.filter(chat_id=chat_id, user_id=user_id).first()

    if not user_info:
        user_info = await UserInfo.create(chat_id=chat_id, user_id=user_id)

    return user_info


async def get_warning_count(chat_id: int, user_id: int):
    user_info = await get_user_info(chat_id, user_id)
    return user_info.warnings


async def set_warning_count(chat_id: int, user_id: int, warnings: int):
    user_info = await get_user_info(chat_id, user_id)
    user_info.warnings = warnings
    await user_info.save()


async def get_muted_count(chat_id: int, user_id: int):
    user_info = await get_user_info(chat_id, user_id)
    return user_info.muted


async def set_muted_count(chat_id: int, user_id: int, muted: int):
    user_info = await get_user_info(chat_id, user_id)
    user_info.muted = muted
    await user_info.save()


async def get_banned_count(chat_id: int, user_id: int):
    user_info = await get_user_info(chat_id, user_id)
    return user_info.banned


async def set_banned_count(chat_id: int, user_id: int, banned: int):
    user_info = await get_user_info(chat_id, user_id)
    user_info.banned = banned
    await user_info.save()


async def get_message_count(chat_id: int, user_id: int):
    user_info = await get_user_info(chat_id, user_id)
    return user_info.messages


async def set_message_count(chat_id: int, user_id: int, messages: int):
    user_info = await get_user_info(chat_id, user_id)
    user_info.messages = messages
    await user_info.save()
