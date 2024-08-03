from aiogram import types
from aiogram.types import ChatMemberStatus

allowed_users = [1398600688, 6840837015]


async def user_status(chat: types.Chat, user: types.User):
    member = await chat.get_member(user.id)

    if member.status == ChatMemberStatus.KICKED:
        return "banned"

    if member.status == ChatMemberStatus.RESTRICTED:
        if not member.can_send_messages:
            return "muted"
        else:
            return "member"

    if member.status == ChatMemberStatus.LEFT:
        return "left"

    if member.status == ChatMemberStatus.MEMBER:
        return "member"

    if member.status in [
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.CREATOR,
    ]:
        return "admin"

    return "unknown"


async def is_admin(chat: types.Chat, user: types.User):
    return (await user_status(chat, user) == "admin") or (user.id in allowed_users)


async def is_muted(chat: types.Chat, user: types.User):
    return await user_status(chat, user) == "muted"


async def is_banned(chat: types.Chat, user: types.User):
    return await user_status(chat, user) == "banned"
