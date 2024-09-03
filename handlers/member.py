from aiogram import Dispatcher, types


async def welcome_new_member(update: types.ChatMemberUpdated):
    new_member = update.new_chat_member
    old_member = update.old_chat_member

    if new_member and (not old_member):
        user = new_member.user

        await update.bot.send_message(
            update.chat.id,
            f'Welcome to the group, <a href="tg://user?id={user.id}">{user.full_name}</a>',
        )


async def delete_join_leave_messages(message: types.Message):
    await message.delete()


def register_member_handlers(dp: Dispatcher):
    dp.register_chat_member_handler(
        welcome_new_member,
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
    dp.register_message_handler(
        delete_join_leave_messages,
        content_types=[
            types.ContentType.NEW_CHAT_MEMBERS,
            types.ContentType.LEFT_CHAT_MEMBER,
        ],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
