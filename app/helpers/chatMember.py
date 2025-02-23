from aiogram import types
from aiogram.enums import ChatMemberStatus

allowed_users = {
    # "-1002116123455": [6373759004],
    "all": [1398600688, 6840837015, 1087968824, 777000],
}


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

    if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return "admin"

    return "unknown"


async def is_admin(chat: types.Chat, user: types.User):
    user_id = user.id
    chat_id = str(chat.id)

    return (
        (await user_status(chat, user) == "admin")
        or (user_id in allowed_users["all"])
        or (user_id in allowed_users.get(chat_id, []))
    )


async def is_muted(chat: types.Chat, user: types.User):
    return await user_status(chat, user) == "muted"


async def is_banned(chat: types.Chat, user: types.User):
    return await user_status(chat, user) == "banned"
