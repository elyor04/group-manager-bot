from aiogram import Dispatcher, types, enums, F
from aiogram.enums import ChatMemberStatus


async def welcome_new_member(update: types.ChatMemberUpdated):
    new_member = update.new_chat_member
    old_member = update.old_chat_member

    if new_member and (new_member.status == ChatMemberStatus.MEMBER):
        user = new_member.user

        if not old_member:
            await update.bot.send_message(
                update.chat.id,
                f'Welcome to the group, <a href="tg://user?id={user.id}">{user.full_name}</a>',
            )

        elif old_member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
            await update.bot.send_message(
                update.chat.id,
                f'Welcome back to the group, <a href="tg://user?id={user.id}">{user.full_name}</a>',
            )


async def delete_join_leave_messages(message: types.Message):
    await message.delete()


def register_member_handlers(dp: Dispatcher):
    dp.chat_member.register(
        welcome_new_member,
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
    dp.message.register(
        delete_join_leave_messages,
        F.content_types.in_(
            [enums.ContentType.NEW_CHAT_MEMBERS, enums.ContentType.LEFT_CHAT_MEMBER]
        ),
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
