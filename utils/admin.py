from aiogram import types


async def is_admin(chat: types.Chat, user: types.User) -> bool:
    member = await chat.get_member(user.id)
    return member.status in (
        types.ChatMemberStatus.ADMINISTRATOR,
        types.ChatMemberStatus.OWNER,
    )
